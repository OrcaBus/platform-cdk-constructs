import {Construct} from "constructs";
import {DEFAULT_ARCHITECTURE, DEFAULT_MEMORY_GB, DEFAULT_VCPUS} from "./config";
import * as ec2 from "aws-cdk-lib/aws-ec2";
import * as ecs from "aws-cdk-lib/aws-ecs";
import {ContainerInsights} from "aws-cdk-lib/aws-ecs";
import * as lambda from "aws-cdk-lib/aws-lambda";
import * as ecrAssets from "aws-cdk-lib/aws-ecr-assets";
import * as iam from "aws-cdk-lib/aws-iam";
import {RetentionDays} from "aws-cdk-lib/aws-logs";
import {VPC_NAME} from "../shared-config/networking";
import {ManagedPolicy} from "aws-cdk-lib/aws-iam";

// Memory and CPU limits for Fargate tasks
/*
256 (.25 vCPU) - Available memory values: 512 (0.5 GB), 1024 (1 GB), 2048 (2 GB)

512 (.5 vCPU) - Available memory values: 1024 (1 GB), 2048 (2 GB), 3072 (3 GB), 4096 (4 GB)

1024 (1 vCPU) - Available memory values: 2048 (2 GB), 3072 (3 GB), 4096 (4 GB), 5120 (5 GB), 6144 (6 GB), 7168 (7 GB), 8192 (8 GB)

2048 (2 vCPU) - Available memory values: Between 4096 (4 GB) and 16384 (16 GB) in increments of 1024 (1 GB)

4096 (4 vCPU) - Available memory values: Between 8192 (8 GB) and 30720 (30 GB) in increments of 1024 (1 GB)

8192 (8 vCPU) - Available memory values: Between 16384 (16 GB) and 61440 (60 GB) in increments of 4096 (4 GB)

16384 (16 vCPU) - Available memory values: Between 32768 (32 GB) and 122880 (120 GB) in increments of 8192 (8 GB)
*/

export type Architecture = 'X86_64' | 'ARM64'

export const CPU_ARCHITECTURE_MAP: Record<Architecture, ecs.CpuArchitecture> = {
    ['X86_64']: ecs.CpuArchitecture.X86_64,
    ['ARM64']: ecs.CpuArchitecture.ARM64
}

export const LAMBDA_ARCHITECTURE_MAP: Record<Architecture, lambda.Architecture> = {
    ['X86_64']: lambda.Architecture.X86_64,
    ['ARM64']: lambda.Architecture.ARM_64
}

export interface FargateEcsTaskConstructProps {
    /**
     * The name of the VPC to use. If not provided, the @DEFAULT_MAIN_VPC_NAME will be used.
     */
    readonly vpcName?: string

    /**
     * The runtime CPU architecture, either X86_64 or ARM64. If not provided, the default is @DEFAULT_ARCHITECTURE.
     */
    readonly runtimePlatform?: ecs.CpuArchitecture

    /**
     * The number of CPUs to use, between 0.25 and 16. If not provided, the default is @DEFAULT_VCPUS.
     */
    readonly nCpus: number // Number of CPUs (0.25, 0.5, 1, 2, 4, 8, 16)

    /**
     * The memory limit in GiB. If not provided, the default is @DEFAULT_MEMORY_GB.
     * The memory limit must be between 0.5 and 120 GiB.
     * But please note that the memory limit varies depending on the number of CPUs, please refer to the table above.
     */
    readonly memoryLimitGiB: number

    /**
     * The architecture of the container. If not provided, the default is @DEFAULT_ARCHITECTURE.
     */
    readonly architecture?: Architecture


    /**
     * The name of the container. This is a required property
     */
    readonly containerName: string

    /**
     * The path to the Dockerfile. This is a required property
     */
    readonly dockerPath: string
}

export class EcsFargateTaskConstruct extends Construct {
    public readonly cluster: ecs.ICluster
    public readonly taskDefinition: ecs.FargateTaskDefinition
    public readonly securityGroup: ec2.ISecurityGroup
    public readonly containerDefinition: ecs.ContainerDefinition

    constructor(scope: Construct, id: string, props: FargateEcsTaskConstructProps) {
        super(scope, id);

        // Set architecture if not provided
        const architecture: Architecture = props.architecture ?? DEFAULT_ARCHITECTURE

        // Set up the main vpc
        const mainVpc = ec2.Vpc.fromLookup(
            this, 'MainVpc', {
                vpcName: props.vpcName ?? VPC_NAME
            }
        )

        // Set up the ECS cluster
        this.cluster = new ecs.Cluster(this, 'FargateCluster', {
            vpc: mainVpc,
            enableFargateCapacityProviders: true,
            containerInsightsV2: ContainerInsights.ENABLED
        })

        // Allow the task definition role ecr access to the guardduty agent
        // https://docs.aws.amazon.com/guardduty/latest/ug/prereq-runtime-monitoring-ecs-support.html#before-enable-runtime-monitoring-ecs
        // Which is in another account - 005257825471.dkr.ecr.ap-southeast-2.amazonaws.com/aws-guardduty-agent-fargate
        const taskExecutionRole = new iam.Role(this, `task-execution-role`, {
          assumedBy: new iam.ServicePrincipal('ecs-tasks.amazonaws.com'),
          managedPolicies: [ManagedPolicy.fromAwsManagedPolicyName('service-role/AmazonECSTaskExecutionRolePolicy')],
        })

        // Set up the Fargate task definition
        this.taskDefinition = new ecs.FargateTaskDefinition(this, 'FargateTaskDef', {
            cpu: (props.nCpus ?? DEFAULT_VCPUS) * 1024,
            // Convert memory limit from GiB to MiB (1 GiB = 1024 MiB)
            memoryLimitMiB: (props.memoryLimitGiB ?? DEFAULT_MEMORY_GB) * 1024,
            runtimePlatform: {
                cpuArchitecture: props.runtimePlatform ?? CPU_ARCHITECTURE_MAP[architecture],
            },
            executionRole: taskExecutionRole
        })

        // Set up the security group
        this.securityGroup = new ec2.SecurityGroup(this, 'FargateSecurityGroup', {
            vpc: mainVpc,
            description: 'Security group for Fargate tasks'
        })

        this.containerDefinition = this.taskDefinition.addContainer('FargateContainer', {
            containerName: props.containerName,
            image: ecs.ContainerImage.fromDockerImageAsset(
                new ecrAssets.DockerImageAsset(this, 'FargateDockerImage', {
                    directory: props.dockerPath,
                    buildArgs: {
                        TARGETPLATFORM: LAMBDA_ARCHITECTURE_MAP[architecture].dockerPlatform
                    }
                })
            ),
            logging: ecs.LogDriver.awsLogs({
                streamPrefix: props.containerName,
                logRetention: RetentionDays.ONE_WEEK
            })
        });
    }
}
