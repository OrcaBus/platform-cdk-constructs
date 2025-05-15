import {PythonFunction, PythonFunctionProps, PythonLayerVersion} from "@aws-cdk/aws-lambda-python-alpha";
import {Construct} from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as secretsManager from "aws-cdk-lib/aws-secretsmanager";
import * as ssm from "aws-cdk-lib/aws-ssm";
import * as iam from "aws-cdk-lib/aws-iam";
import * as s3 from "aws-cdk-lib/aws-s3";
import {DockerImage} from 'aws-cdk-lib';

import path from "path";

import {
    ParamsAndSecretsLayerVersion,
    ParamsAndSecretsLogLevel,
    ParamsAndSecretsVersions,
} from 'aws-cdk-lib/aws-lambda';
import {
    DEFAULT_HOSTNAME_SSM_PARAMETER,
    DEFAULT_ORCABUS_TOKEN_SECRET_ID,
    MART_ENV_VARS, MART_LAMBDA_FUNCTION_NAME,
    MART_S3_BUCKET,
    MART_S3_PREFIX
} from "./config";
import {accountIdAlias, region, resolveStageName} from "../utils";


function getPythonUvDockerImage(): DockerImage {
    return DockerImage.fromBuild(path.join(__dirname, 'build_python'));
}

export interface OrcabusResourcesProps {
    /**
     * Provide the orcabusTokenSecretId, otherwise it will default to @DEFAULT_ORCABUS_TOKEN_SECRET_ID
     */
    readonly orcabusTokenSecretId?: string

    /**
     * Provide the hostnameSsmParameterName, otherwise it will default to @DEFAULT_HOSTNAME_SSM_PARAMETER
     */
    readonly hostnameSsmParameterName?: string
}

export interface MartEnvironmentVariables {
    /**
     * Provide the athenaWorkgroupName, otherwise it will default to @MART_ENV_VARS.ATHENA_WORKGROUP_NAME
     */
    readonly ATHENA_WORKGROUP_NAME?: string

    /**
     * Provide the athenaDatasourceName, otherwise it will default to @MART_S3_BUCKET.A
     */
    readonly ATHENA_DATASOURCE_NAME?: string

    /**
     * Provide the athenaDatabaseName, otherwise it will default to @MART_ENV_VARS.ATHENA_DATABASE_NAME
     */
    readonly ATHENA_DATABASE_NAME?: string
}

export interface PythonUvFunctionProps extends PythonFunctionProps {
    /**
     * Whether or not to include the orcabus api tools layer in the lambda function build
     */
    readonly includeOrcabusApiToolsLayer?: boolean

    /**
     * Whether or not to include the mart layer in the lambda function build
     * Note that the mart layer is a little heavier than the orcabus api tools layer
     * Since we require pandas to be installed
     */
    readonly includeMartLayer?: boolean

    /**
     * Provide the orcabusTokenResources, optional, otherwise it will default to
     * @DEFAULT_ORCABUS_TOKEN_SECRET_ID and @DEFAULT_HOSTNAME_SSM_PARAMETER
     * for the secret and SSM parameter respectively
     */
    readonly orcabusTokenResources?: OrcabusResourcesProps

    /**
     * Provide the martEnvironmentVariables, optional, otherwise it will default to
     * @MART_ENV_VARS.ATHENA_WORKGROUP_NAME, @MART_ENV_VARS.ATHENA_DATASOURCE_NAME
     * and @MART_ENV_VARS.ATHENA_DATABASE_NAME for the athena workgroup, datasource and database respectively
     */
    readonly martEnvironmentVariables?: MartEnvironmentVariables
}


export class PythonUvFunction extends PythonFunction {
    // Class constructs, to be used for caching the layers
    // This means that if there are multiple lambdas throughout the stack
    // They will all use the same layer
    private static orcabusApiToolsLayer: lambda.ILayerVersion;
    private static martLayer: lambda.ILayerVersion;

    constructor(scope: Construct, id: string, props: PythonUvFunctionProps) {
        const uvProps = {
            ...props,
            bundling: {
                ...props.bundling,
                buildArgs: {
                    ...props.bundling?.buildArgs,
                    // Add TARGETPLATFORM to build args if it's not already set
                    TARGETPLATFORM:
                        props.bundling?.buildArgs?.TARGETPLATFORM ?? lambda.Architecture.ARM_64.dockerPlatform,
                },
                image: getPythonUvDockerImage(),
                commandHooks: {
                    // @ts-ignore
                    beforeBundling(inputDir: string, outputDir: string): string[] {
                        return [];
                    },
                    // @ts-ignore
                    afterBundling(inputDir: string, outputDir: string): string[] {
                        return [`rm -rf ${outputDir}/pandas/tests`];
                    },
                },
            },
            paramsAndSecrets:
                props.paramsAndSecrets ??
                ParamsAndSecretsLayerVersion.fromVersion(ParamsAndSecretsVersions.V1_0_103, {
                    cacheEnabled: true,
                    cacheSize: 300,
                    logLevel: ParamsAndSecretsLogLevel.DEBUG,
                }),
        };
        super(scope, id, uvProps);

        if (props.includeOrcabusApiToolsLayer) {
            /* Set the environment variables for the Orcabus resources */
            this.setOrcabusResources(props.orcabusTokenResources ?? {})

            /* Build the orcabus Api tools layer */
            this.buildOrcabusApiToolsLayer()
            this.addLayers(PythonUvFunction.orcabusApiToolsLayer)
        }

        if (props.includeMartLayer) {
            /* Set the environment variables for the mart resources */
            this.setAthenaResources(props.martEnvironmentVariables ?? {})

            /* Build the mart layer */
            this.buildMartToolsLayer()
            this.addLayers(PythonUvFunction.martLayer)
        }
    }

    private buildOrcabusApiToolsLayer() {
        // Only build orcabus api layer if it doesn't exist
        if (!PythonUvFunction.orcabusApiToolsLayer) {
            PythonUvFunction.orcabusApiToolsLayer = new PythonLayerVersion(this, 'orcabusApiToolsLayer', {
                layerVersionName: 'orcabusApiToolsLayer',
                entry: path.join(__dirname, 'layers/orcabus_api_tools'),
                compatibleRuntimes: [lambda.Runtime.PYTHON_3_12],
                compatibleArchitectures: [lambda.Architecture.ARM_64],
                license: 'GPL3',
                description: 'orcabusApiToolsLayer',
                bundling: {
                    image: getPythonUvDockerImage(),
                    commandHooks: {
                        // eslint-disable-next-line @typescript-eslint/no-unused-vars
                        beforeBundling(inputDir: string, outputDir: string): string[] {
                            return [];
                        },
                        afterBundling(inputDir: string, outputDir: string): string[] {
                            return [
                                `pip install ${inputDir} --target ${outputDir}`,
                                `find ${outputDir} -name 'pandas' -exec rm -rf {}/tests/ \\;`,
                            ];
                        },
                    },
                },
            });
        }
    }

    private buildMartToolsLayer() {
        // Only build the layer if it doesn't exist
        if (!PythonUvFunction.martLayer) {
            PythonUvFunction.martLayer = new PythonLayerVersion(this, 'martToolsLayer', {
                layerVersionName: 'martToolsLayer',
                entry: path.join(__dirname, 'layers/mart_tools'),
                compatibleRuntimes: [lambda.Runtime.PYTHON_3_12],
                compatibleArchitectures: [lambda.Architecture.ARM_64],
                license: 'GPL3',
                description: 'martToolsLayer',
                bundling: {
                    image: getPythonUvDockerImage(),
                    commandHooks: {
                        // eslint-disable-next-line @typescript-eslint/no-unused-vars
                        beforeBundling(inputDir: string, outputDir: string): string[] {
                            return [];
                        },
                        afterBundling(inputDir: string, outputDir: string): string[] {
                            return [
                                `pip install ${inputDir} --target ${outputDir}`,
                                `find ${outputDir} -name 'pandas' -exec rm -rf {}/tests/ \\;`,
                            ];
                        },
                    },
                },
            });
        }

    }

    private setOrcabusResources(
        props: OrcabusResourcesProps
    ) {
        // Set secret object
        const orcabusTokenSecretId = secretsManager.Secret.fromSecretNameV2(
            this, 'orcabusTokenSecretId',
            props.orcabusTokenSecretId ?? DEFAULT_ORCABUS_TOKEN_SECRET_ID
        );
        const hostnameSsmParameterName = ssm.StringParameter.fromStringParameterName(
            this, 'hostnameSsmParameterName',
            props.hostnameSsmParameterName ?? DEFAULT_HOSTNAME_SSM_PARAMETER,
        )

        // Add permissions for the secret and SSM parameter
        // To the current version
        orcabusTokenSecretId.grantRead(this.currentVersion);
        hostnameSsmParameterName.grantRead(this.currentVersion)

        // Add environment variables
        this.addEnvironment(
            'ORCABUS_TOKEN_SECRET_ID', orcabusTokenSecretId.secretName,
        )
        this.addEnvironment(
            'HOSTNAME_SSM_PARAMETER_NAME', hostnameSsmParameterName.parameterName,
        )
    }


    private setAthenaResources(
        props: MartEnvironmentVariables
    ) {
        // Resolve the stage name by performing a reverse lookup using cdk.Aws.ACCOUNT_ID on accountIdAlias
        const stageName = resolveStageName()

        const athenaS3Bucket = s3.Bucket.fromBucketName(
            this, 'athenaS3Bucket',
            MART_S3_BUCKET[stageName]
        )

        const athenaFunctionName = lambda.Function.fromFunctionName(
            this, 'lambdaFunctionName', MART_LAMBDA_FUNCTION_NAME
        )

        // Add env vars
        // Iterate over kv pairs of MART_ENV_VARS
        for (const [key, value] of Object.entries(MART_ENV_VARS)) {
            if (Object(props).getAttr(key) !== undefined) {
                this.addEnvironment(key, Object(props).getAttr(key));
            }
            this.addEnvironment(key, value);
        }

        // Permissions
        this.currentVersion.addToRolePolicy(
            // From https://docs.aws.amazon.com/athena/latest/ug/example-policies-workgroup.html
            new iam.PolicyStatement({
                actions: [
                    // Workgroup lists
                    'athena:ListEngineVersions',
                    'athena:ListWorkGroups',
                    'athena:ListDataCatalogs',
                    'athena:ListDatabases',
                    'athena:GetDatabase',
                    'athena:ListTableMetadata',
                    'athena:GetTableMetadata',
                    'athena:GetDataCatalog',
                ],
                resources: [`arn:aws:athena:${region}:${accountIdAlias[stageName]}:*`],
            })
        );

        this.currentVersion.addToRolePolicy(
            // From https://docs.aws.amazon.com/athena/latest/ug/example-policies-workgroup.html
            new iam.PolicyStatement({
                actions: [
                    // Workgroup executions
                    'athena:BatchGetQueryExecution',
                    'athena:GetQueryExecution',
                    'athena:ListQueryExecutions',
                    'athena:StartQueryExecution',
                    'athena:StopQueryExecution',
                    'athena:GetQueryResults',
                    'athena:GetQueryResultsStream',
                    'athena:CreateNamedQuery',
                    'athena:GetNamedQuery',
                    'athena:BatchGetNamedQuery',
                    'athena:ListNamedQueries',
                    'athena:DeleteNamedQuery',
                    'athena:CreatePreparedStatement',
                    'athena:GetPreparedStatement',
                    'athena:ListPreparedStatements',
                    'athena:UpdatePreparedStatement',
                    'athena:DeletePreparedStatement',
                ],
                resources: [
                    `arn:aws:athena:${region}:${accountIdAlias[stageName]}:workgroup/${MART_ENV_VARS.ATHENA_WORKGROUP_NAME}`,
                ],
            })
        );

        // Add read access to the S3 bucket
        athenaS3Bucket.grantReadWrite(
            this.currentVersion,
            `${MART_S3_PREFIX}*`
        )

        // Add invoke access to the lambda function
        athenaFunctionName.grantInvoke(
            this.currentVersion
        )
    }
}




