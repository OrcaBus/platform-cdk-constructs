import { Construct } from "constructs";
import { Environment, Stack, Stage } from "aws-cdk-lib";
import {
  BuildSpec,
  ComputeType,
  LinuxArmBuildImage,
} from "aws-cdk-lib/aws-codebuild";
import { StringParameter } from "aws-cdk-lib/aws-ssm";
import {
  CodeBuildStep,
  CodePipeline,
  CodePipelineSource,
  ManualApprovalStep,
} from "aws-cdk-lib/pipelines";
import {
  Pipeline,
  CfnPipeline,
  PipelineType,
} from "aws-cdk-lib/aws-codepipeline";
import {
  BETA_ENVIRONMENT,
  GAMMA_ENVIRONMENT,
  PROD_ENVIRONMENT,
} from "./config";

/**
 * The default partial build spec for the synth step in the pipeline.
 */
export const DEFAULT_SYNTH_STEP_PARTIAL_BUILD_SPEC = {
  phases: {
    install: {
      "runtime-versions": {
        nodejs: "22.x",
      },
    },
  },
};

export interface StageEnvProps {
  /**
   * The environment for the beta stage
   */
  readonly beta: Environment;
  /**
   * The environment for the gamma stage
   */
  readonly gamma: Environment;
  /**
   * The environment for the prod stage
   */
  readonly prod: Environment;
}

export interface StackConfigProps {
  /**
   * The configuration for the beta (dev) stage
   */
  readonly beta: Record<string, any>;
  /**
   * The configuration for the gamma (stg) stage
   */
  readonly gamma: Record<string, any>;
  /**
   * The configuration for the prod stage
   */
  readonly prod: Record<string, any>;
}

export interface DeploymentStackPipelineProps {
  /**
   * The github branch name it will listen to.
   */
  readonly githubBranch: string;
  /**
   * The repository name that exist in the 'OrcaBus' github organisation. e.g. `a-micro-service-repo`
   */
  readonly githubRepo: string;
  /**
   * The stack to which the pipeline will be deploying to its respective account
   */
  readonly stack: any;
  /**
   * The stack name (in cloudformation) for the stack defined in `stack`. The stack name will prepend with the stage
   * name e.g. `OrcaBusBeta-<stackName>`, `OrcaBusGamma-<stackName>`, `OrcaBusProd-<stackName>`
   */
  readonly stackName: string;
  /**
   * The stack configuration/constants that will be passed to the stack props.
   */
  readonly stackConfig: StackConfigProps;
  /**
   * The pipeline name in the bastion account.
   */
  readonly pipelineName: string;
  /**
   * The file paths to trigger the pipeline. e.g. ["stateless/**"]
   *
   * https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-gitfilepathfiltercriteria.html
   *
   */
  readonly filePaths?: string[];
  /**
   * The command to run to synth the cdk stack which also installing the cdk dependencies. e.g. ["yarn install --immutable", "yarn cdk synth"]
   */
  readonly cdkSynthCmd: string[];
  /**
   * The location where the cdk output will be stored.
   *
   * @default cdk.out
   */
  readonly cdkOut?: string;
  /**
   * Additional configuration for the CodeBuild step during the CDK synth phase. It will passed as the `partialBuildSpec` to the `CodeBuildStep`.
   *
   * @default DEFAULT_SYNTH_STEP_PARTIAL_BUILD_SPEC
   */
  readonly synthBuildSpec?: Record<string, any>;
  /**
   * The stage environment for the deployment stack
   */
  readonly stageEnv?: StageEnvProps;
}

export class DeploymentStackPipeline extends Construct {
  /**
   * The code pipeline construct that is created.
   */
  readonly pipeline: Pipeline;

  constructor(
    scope: Construct,
    id: string,
    props: DeploymentStackPipelineProps,
  ) {
    super(scope, id);

    const codeStarArn = StringParameter.valueForStringParameter(
      this,
      "/orcabus/codestar_github_arn",
    );
    const codeStarSourceActionName = "pipeline-src";
    const sourceFile = CodePipelineSource.connection(
      `OrcaBus/${props.githubRepo}`,
      props.githubBranch,
      {
        connectionArn: codeStarArn,
        actionName: codeStarSourceActionName,
        triggerOnPush: true,
      },
    );

    this.pipeline = new Pipeline(this, "DeploymentCodePipeline", {
      pipelineType: PipelineType.V2,
      pipelineName: props.pipelineName,
      crossAccountKeys: true,
    });

    if (props.filePaths) {
      // Add event filter to only trigger if the push event is from `deploy` directory
      const cfnPipeline = this.pipeline.node.defaultChild as CfnPipeline;
      cfnPipeline.addPropertyOverride("Triggers", [
        {
          GitConfiguration: {
            Push: [
              {
                Branches: {
                  Includes: [props.githubBranch],
                },
                FilePaths: {
                  Includes: props.filePaths,
                },
              },
            ],
            SourceActionName: codeStarSourceActionName,
          },
          ProviderType: "CodeStarSourceConnection",
        },
      ]);
    }

    const { synthBuildSpec = DEFAULT_SYNTH_STEP_PARTIAL_BUILD_SPEC } = props;
    const cdkPipeline = new CodePipeline(this, "CDKCodePipeline", {
      codePipeline: this.pipeline,
      synth: new CodeBuildStep("CdkSynth", {
        installCommands: [
          "node -v",
          "npm install --global corepack@latest",
          "corepack --version",
          "corepack enable",
        ],
        commands: props.cdkSynthCmd,
        input: sourceFile,
        primaryOutputDirectory: props.cdkOut || "cdk.out",
        partialBuildSpec: BuildSpec.fromObject(synthBuildSpec),
      }),
      selfMutation: true,
      codeBuildDefaults: {
        buildEnvironment: {
          computeType: ComputeType.LARGE,
          buildImage: LinuxArmBuildImage.AMAZON_LINUX_2_STANDARD_3_0,
          environmentVariables: {
            NODE_OPTIONS: {
              value: "--max-old-space-size=8192",
            },
          },
        },
      },
    });

    const defaultStageEnv: StageEnvProps = {
      beta: BETA_ENVIRONMENT,
      gamma: GAMMA_ENVIRONMENT,
      prod: PROD_ENVIRONMENT,
    };
    const stageEnv = props.stageEnv || defaultStageEnv;

    cdkPipeline.addStage(
      new DeploymentStage(
        this,
        "OrcaBusBeta",
        stageEnv.beta,
        props.stackName,
        props.stack,
        props.stackConfig.beta,
      ),
    );

    cdkPipeline.addStage(
      new DeploymentStage(
        this,
        "OrcaBusGamma",
        stageEnv.gamma,
        props.stackName,
        props.stack,
        props.stackConfig.gamma,
      ),
      { post: [new ManualApprovalStep("PromoteToProd")] },
    );

    cdkPipeline.addStage(
      new DeploymentStage(
        this,
        "OrcaBusProd",
        stageEnv.prod,
        props.stackName,
        props.stack,
        props.stackConfig.prod,
      ),
    );
  }
}

class DeploymentStage extends Stage {
  constructor(
    scope: Construct,
    environmentName: string,
    env: Environment,
    stackName: string,
    stackClass: new (scope: Construct, id: string, props: any) => Stack,
    appStackProps: any,
  ) {
    super(scope, environmentName, { env: env });
    new stackClass(this, stackName, {
      env: env,
      tags: {
        "umccr-org:Product": "OrcaBus",
        "umccr-org:Creator": "CDK",
        "umccr-org:Service": stackName,
      },
      ...appStackProps,
    });
  }
}
