import {PythonFunction, PythonFunctionProps, PythonLayerVersion} from "@aws-cdk/aws-lambda-python-alpha";
import {Construct} from "constructs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as secretsManager from "aws-cdk-lib/aws-secretsmanager";
import * as ssm from "aws-cdk-lib/aws-ssm";
import * as iam from "aws-cdk-lib/aws-iam";
import * as s3 from "aws-cdk-lib/aws-s3";
import {NagSuppressions} from "cdk-nag";
import {DockerImage} from 'aws-cdk-lib';

import path from "path";

import {
    ParamsAndSecretsLayerVersion,
    ParamsAndSecretsLogLevel,
    ParamsAndSecretsVersions,
} from 'aws-cdk-lib/aws-lambda';
import {
    // Orcabus defaults
    DEFAULT_HOSTNAME_SSM_PARAMETER, DEFAULT_ORCABUS_TOKEN_SECRET_ID,
    // Mart defaults
    MART_ENV_VARS, MART_LAMBDA_FUNCTION_NAME,
    MART_S3_BUCKET,
    MART_S3_PREFIX,
} from "./config";
import {resolveStageName} from "../utils";
import {ACCOUNT_ID_ALIAS, REGION} from "../shared-config/accounts";
import {
  ICAV2_ACCESS_TOKEN_SECRET_ID,
  ICAV2_BASE_URL, ICAV2_PROJECT_TO_STORAGE_CONFIGURATIONS_SSM_PARAMETER_PATH_PREFIX,
  ICAV2_STORAGE_CONFIGURATION_SSM_PARAMETER_PATH_PREFIX, ICAV2_STORAGE_CREDENTIALS_SSM_PARAMETER_PATH_PREFIX
} from "../shared-config/icav2";


export function getPythonUvDockerImage(): DockerImage {
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
    readonly athenaWorkgroupName?: string

    /**
     * Provide the athenaDatasourceName, otherwise it will default to @MART_ENV_VARS.athenaDatasourceName
     */
    readonly athenaDatasourceName?: string

    /**
     * Provide the athenaDatabaseName, otherwise it will default to @MART_ENV_VARS.ATHENA_DATABASE_NAME
     */
    readonly athenaDatabaseName?: string
}

export interface Icav2ResourcesProps {
    /**
     * The id of the secret that contains the icav2 access token
     * otherwise it will default to @ICAV2_ACCESS_TOKEN_SECRET_ID
     */
    readonly icav2AccessTokenSecretId?: string
    readonly icav2StorageConfigurationSsmParameterPathPrefix?: string
    readonly icav2ProjectToStorageConfigurationsSsmParameterPathPrefix?: string
    readonly icav2StorageCredentialsSsmParameterPathPrefix?: string
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
     * Whether or not to include the icav2 layer in the lambda function build
     */
    readonly includeIcav2Layer?: boolean

    /**
     * Whether or not to include the fastapi layer in the lambda function build
     */
    readonly includeFastApiLayer?: boolean

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

    /**
     * Provide the icav2Resources, optional, otherwise it will default to
     * @DEFAULT_ICAV2_ACCESS_TOKEN_SECRET_ID for the secret
     */
    readonly icav2Resources?: Icav2ResourcesProps
}


export class PythonUvFunction extends PythonFunction {
    // Class constructs, to be used for caching the layers
    // This means that if there are multiple lambdas throughout the stack
    // They will all use the same layer
    private static orcabusApiToolsLayer: Map<Construct, lambda.ILayerVersion> = new Map();
    private static martLayer: Map<Construct, lambda.ILayerVersion> = new Map();
    private static icav2Layer: Map<Construct, lambda.ILayerVersion> = new Map();
    private static fastApiLayer: Map<Construct, lambda.ILayerVersion> = new Map();

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
                        return props.bundling?.commandHooks?.beforeBundling as unknown as string[] ?? [];
                    },
                    // @ts-ignore
                    afterBundling(inputDir: string, outputDir: string): string[] {
                        return (props.bundling?.commandHooks?.afterBundling as unknown as string[] ?? []).concat(
                          [
                            // Delete the tests directory from pandas
                            `rm -rf ${outputDir}/pandas/tests`,
                            // Delete the *pyc files and __pycache__ directories
                            `find ${outputDir} -type f -name '*.pyc' -delete`,
                            // Delete the __pycache__ directories contents
                            `find ${outputDir} -type d -name '__pycache__' -exec rm -rf {}/* \\;`,
                            // Delete the __pycache__ directories themselves
                            `find ${outputDir} -type d -name '__pycache__' -delete`,
                          ]
                        );
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
            this.buildOrcabusApiToolsLayer(scope)
            this.addLayers(<PythonLayerVersion>PythonUvFunction.orcabusApiToolsLayer.get(scope))
        }

        if (props.includeMartLayer) {
            /* Set the environment variables for the mart resources */
            this.setAthenaResources(props.martEnvironmentVariables ?? {})

            /* Build the mart layer */
            this.buildMartToolsLayer(scope)
            this.addLayers(<PythonLayerVersion>PythonUvFunction.martLayer.get(scope))
        }

        if (props.includeIcav2Layer) {
            /* Set the environment variables for the icav2 resources */
            this.setIcav2Resources(props.icav2Resources ?? {})

            /* Build the icav2 layer */
            this.buildIcav2Layer(scope)
            this.addLayers(<PythonLayerVersion>PythonUvFunction.icav2Layer.get(scope))
            // Add nag suppression
            // Since the lambda will need to access the SSM parameters
            NagSuppressions.addResourceSuppressions(
              this,
              [
                {
                  id: 'AwsSolutions-IAM5',
                  reason: 'The lambda iam role needs to access the ssm parameters.',
                },
              ],
              true
            );
        }

        if (props.includeFastApiLayer) {
            /* Build the fastapi layer */
            this.buildFastApiLayer(scope)
            this.addLayers(<PythonLayerVersion>PythonUvFunction.fastApiLayer.get(scope))
        }
    }

    private buildOrcabusApiToolsLayer(scope: Construct) {
        // Only build orcabus api layer if it doesn't exist
        if (!PythonUvFunction.orcabusApiToolsLayer.has(scope)) {
            const layer = new PythonLayerVersion(scope, 'orcabusApiToolsLayer', {
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
                                // Delete the tests directory from pandas
                                `rm -rf ${outputDir}/pandas/tests`,
                                // Delete the *pyc files and __pycache__ directories
                                `find ${outputDir} -type f -name '*.pyc' -delete`,
                                // Delete the __pycache__ directories contents
                                `find ${outputDir} -type d -name '__pycache__' -exec rm -rf {}/* \\;`,
                                // Delete the __pycache__ directories themselves
                                `find ${outputDir} -type d -name '__pycache__' -delete`,
                            ];
                        },
                    },
                },
            });

            PythonUvFunction.orcabusApiToolsLayer.set(scope, layer);
        }
    }

    private buildMartToolsLayer(scope: Construct) {
        // Only build the layer if it doesn't exist
        if (!PythonUvFunction.martLayer.has(scope)) {
            const layer = new PythonLayerVersion(scope, 'martToolsLayer', {
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
                                // Delete the tests directory from pandas
                                `rm -rf ${outputDir}/pandas/tests`,
                                // Delete the *pyc files and __pycache__ directories
                                `find ${outputDir} -type f -name '*.pyc' -delete`,
                                // Delete the __pycache__ directories contents
                                `find ${outputDir} -type d -name '__pycache__' -exec rm -rf {}/* \\;`,
                                // Delete the __pycache__ directories themselves
                                `find ${outputDir} -type d -name '__pycache__' -delete`,
                            ];
                        },
                    },
                },
            });
            PythonUvFunction.martLayer.set(scope, layer);
        }
    }

    private buildIcav2Layer(scope: Construct) {
        // Only build the layer if it doesn't exist
        if (!PythonUvFunction.icav2Layer.has(scope)) {
            const layer = new PythonLayerVersion(scope, 'icav2ToolsLayer', {
                entry: path.join(__dirname, 'layers/icav2_tools'),
                compatibleRuntimes: [lambda.Runtime.PYTHON_3_12],
                compatibleArchitectures: [lambda.Architecture.ARM_64],
                license: 'GPL3',
                description: 'icav2ToolsLayer',
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
                                // Delete the tests directory from pandas
                                `rm -rf ${outputDir}/pandas/tests`,
                                // Delete the *pyc files and __pycache__ directories
                                `find ${outputDir} -type f -name '*.pyc' -delete`,
                                // Delete the __pycache__ directories contents
                                `find ${outputDir} -type d -name '__pycache__' -exec rm -rf {}/* \\;`,
                                // Delete the __pycache__ directories themselves
                                `find ${outputDir} -type d -name '__pycache__' -delete`,
                                // Uninstall boto3 & botocore to avoid bloating the image
                                // pip is aliased to 'uv pip' so no need to include --yes parameter
                                `pip uninstall boto3 botocore`,
                                `rm -rf ${outputDir}/boto3 ${outputDir}/botocore`,
                            ];
                        },
                    },
                },
            });
            PythonUvFunction.icav2Layer.set(scope, layer);
        }
    }

    private buildFastApiLayer(scope: Construct) {
        // Only build the layer if it doesn't exist
        if (!PythonUvFunction.fastApiLayer.has(scope)) {
            const layer = new PythonLayerVersion(scope, 'fastApiLayer', {
                entry: path.join(__dirname, 'layers/fastapi_tools'),
                compatibleRuntimes: [lambda.Runtime.PYTHON_3_12],
                compatibleArchitectures: [lambda.Architecture.ARM_64],
                license: 'GPL3',
                description: 'fastApiLayer',
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
                                // Delete the tests directory from pandas
                                `rm -rf ${outputDir}/pandas/tests`,
                                // Delete the *pyc files and __pycache__ directories
                                `find ${outputDir} -type f -name '*.pyc' -delete`,
                                // Delete the __pycache__ directories contents
                                `find ${outputDir} -type d -name '__pycache__' -exec rm -rf {}/* \\;`,
                                // Delete the __pycache__ directories themselves
                                `find ${outputDir} -type d -name '__pycache__' -delete`,
                            ];
                        },
                    },
                },
            });
            PythonUvFunction.fastApiLayer.set(scope, layer);
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
        // Resolve the stage name by performing a reverse lookup using cdk.Aws.ACCOUNT_ID on ACCOUNT_ID_ALIAS
        const stageName = resolveStageName(this)

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
            // After
            if (props[key as keyof MartEnvironmentVariables] !== undefined) {
                this.addEnvironment(key, props[key as keyof MartEnvironmentVariables]!);
            } else {
                this.addEnvironment(key, value);
            }
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
                resources: [`arn:aws:athena:${REGION}:${ACCOUNT_ID_ALIAS[stageName]}:*`],
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
                    `arn:aws:athena:${REGION}:${ACCOUNT_ID_ALIAS[stageName]}:workgroup/${MART_ENV_VARS.athenaWorkgroupName}`,
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

    private setIcav2Resources(
        props: Icav2ResourcesProps
    ) {
        // Resolve the stage name by performing a reverse lookup using cdk.Aws.ACCOUNT_ID on ACCOUNT_ID_ALIAS
        const stageName = resolveStageName(this)

        // Set secret object
        const icav2AccessTokenSecretIdObject = secretsManager.Secret.fromSecretNameV2(
            this, 'ICAV2_ACCESS_TOKEN_SECRET_ID',
            props.icav2AccessTokenSecretId ?? ICAV2_ACCESS_TOKEN_SECRET_ID[stageName]
        );

        // Add permissions for the secret and SSM parameter
        // To the current version
        icav2AccessTokenSecretIdObject.grantRead(this.currentVersion);

        // Add configuration paths
        const icav2StorageConfigurationSsmParameterPathPrefix = (
          props.icav2StorageConfigurationSsmParameterPathPrefix ?? ICAV2_STORAGE_CONFIGURATION_SSM_PARAMETER_PATH_PREFIX
        )
        const icav2ProjectToStorageConfigurationsSsmParameterPathPrefix = (
          props.icav2ProjectToStorageConfigurationsSsmParameterPathPrefix ?? ICAV2_PROJECT_TO_STORAGE_CONFIGURATIONS_SSM_PARAMETER_PATH_PREFIX
        )
        const icav2StorageCredentialsSsmParameterPathPrefix = (
          props.icav2StorageCredentialsSsmParameterPathPrefix ?? ICAV2_STORAGE_CREDENTIALS_SSM_PARAMETER_PATH_PREFIX
        )

        // Provide access to the ssm parameter paths
        this.currentVersion.addToRolePolicy(
            new iam.PolicyStatement({
                // We may need to get the parameters individually or by path
                actions: ['ssm:GetParametersByPath', 'ssm:GetParameter'],
                resources: [
                    `arn:aws:ssm:${REGION}:${ACCOUNT_ID_ALIAS[stageName]}:parameter${icav2StorageConfigurationSsmParameterPathPrefix.replace(/\/$/, "")}/*`,
                    `arn:aws:ssm:${REGION}:${ACCOUNT_ID_ALIAS[stageName]}:parameter${icav2ProjectToStorageConfigurationsSsmParameterPathPrefix.replace(/\/$/, "")}/*`,
                    `arn:aws:ssm:${REGION}:${ACCOUNT_ID_ALIAS[stageName]}:parameter${icav2StorageCredentialsSsmParameterPathPrefix.replace(/\/$/, "")}/*`,
                ],
            })
        );

        // Add environment variables
        this.addEnvironment(
            'ICAV2_ACCESS_TOKEN_SECRET_ID', icav2AccessTokenSecretIdObject.secretName,
        )
        this.addEnvironment(
            'ICAV2_BASE_URL', ICAV2_BASE_URL,
        )
    }

}




