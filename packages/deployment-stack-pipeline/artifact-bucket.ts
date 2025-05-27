import { Construct } from "constructs";
import { Bucket, BucketEncryption, IBucket } from "aws-cdk-lib/aws-s3";
import { IKey, Key } from "aws-cdk-lib/aws-kms";
import { Duration, RemovalPolicy } from "aws-cdk-lib";
import { ArnPrincipal, PolicyStatement } from "aws-cdk-lib/aws-iam";
import {
  BETA_ENVIRONMENT,
  GAMMA_ENVIRONMENT,
  PROD_ENVIRONMENT,
} from "./config";
import { StringParameter } from "aws-cdk-lib/aws-ssm";

export const CROSS_DEPLOYMENT_ARTIFACT_BUCKET_NAME =
  "orcabus-cross-deployment-codepipeline-artifact";

export const CROSS_DEPLOYMENT_ARTIFACT_KMS_ALIAS =
  "orcabus-cross-deployment-codepipeline-artifact";

export const CROSS_DEPLOYMENT_ARTIFACT_KMS_ARN_SSM_PARAMETER_NAME =
  "orcabus/deployment-stack-pipeline/artifact-bucket/kms-key-arn";

export interface ICrossDeploymentArtifactBucket {
  /**
   * The S3 bucket used to store artifacts for cross-deployment pipelines.
   */
  readonly artifactBucket: IBucket;
  /**
   * The KMS key used to encrypt artifacts for cross-deployment pipelines.
   */
  readonly artifactKms: IKey;
}

export class CrossDeploymentArtifactBucket
  extends Construct
  implements ICrossDeploymentArtifactBucket
{
  /**
   * The S3 bucket used to store artifacts for cross-deployment pipelines.
   */
  public readonly artifactBucket: Bucket;
  /**
   * The KMS key used to encrypt artifacts for cross-deployment pipelines.
   */
  public readonly artifactKms: Key;

  constructor(scope: Construct, id: string) {
    super(scope, id);

    this.artifactKms = new Key(this, "KmsKeyCodepipelineArtifactBucket", {
      pendingWindow: Duration.days(30),
      description: "OrcaBus Cross Deployment Artifact Bucket KMS Key",
      enableKeyRotation: false,
      removalPolicy: RemovalPolicy.RETAIN,
      alias: CROSS_DEPLOYMENT_ARTIFACT_KMS_ALIAS,
    });

    new StringParameter(this, "SSMArtifactBucketKmsArnParameter", {
      parameterName: CROSS_DEPLOYMENT_ARTIFACT_KMS_ARN_SSM_PARAMETER_NAME,
      stringValue: this.artifactKms.keyArn,
      description:
        "KMS Key ARN for the OrcaBus cross-deployment artifact bucket",
    });

    this.artifactBucket = new Bucket(this, "BucketCodepipelineCrossArtifact", {
      bucketName: CROSS_DEPLOYMENT_ARTIFACT_BUCKET_NAME,
      versioned: false,
      removalPolicy: RemovalPolicy.RETAIN,
      encryption: BucketEncryption.KMS,
      encryptionKey: this.artifactKms,
    });

    this.artifactBucket.addToResourcePolicy(
      new PolicyStatement({
        actions: ["s3:GetObject*", "s3:GetBucket*", "s3:List*"],
        resources: [
          this.artifactBucket.bucketArn,
          this.artifactBucket.arnForObjects("*"),
        ],
        principals: [
          new ArnPrincipal(
            `arn:aws:iam::${BETA_ENVIRONMENT.account}:role/cdk-hnb659fds-deploy-role-${BETA_ENVIRONMENT.account}-ap-southeast-2`,
          ),
          new ArnPrincipal(
            `arn:aws:iam::${GAMMA_ENVIRONMENT.account}:role/cdk-hnb659fds-deploy-role-${GAMMA_ENVIRONMENT.account}-ap-southeast-2`,
          ),
          new ArnPrincipal(
            `arn:aws:iam::${PROD_ENVIRONMENT.account}:role/cdk-hnb659fds-deploy-role-${PROD_ENVIRONMENT.account}-ap-southeast-2`,
          ),
        ],
      }),
    );
  }

  /**
   * Imports an existing cross-deployment artifact bucket and its KMS key
   * using SSM and resource lookups.
   * @param scope The scope in which to look up the artifact bucket.
   * @returns ICrossDeploymentArtifactBucket
   */
  public static fromLookup(scope: Construct): ICrossDeploymentArtifactBucket {
    const artifactBucketKmsArn = StringParameter.valueForStringParameter(
      scope,
      CROSS_DEPLOYMENT_ARTIFACT_KMS_ARN_SSM_PARAMETER_NAME,
    );

    const artifactBucketKmsKey = Key.fromKeyArn(
      scope,
      "KmsKeyCodepipelineArtifactBucket",
      artifactBucketKmsArn,
    );
    const artifactBucket = Bucket.fromBucketAttributes(
      scope,
      "BucketCodepipelineCrossArtifact",
      {
        bucketName: CROSS_DEPLOYMENT_ARTIFACT_BUCKET_NAME,
        encryptionKey: artifactBucketKmsKey,
      },
    );

    return {
      artifactBucket: artifactBucket,
      artifactKms: artifactBucketKmsKey,
    };
  }
}
