[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [ecs](../README.md) / FargateEcsTaskConstructProps

# Interface: FargateEcsTaskConstructProps

Defined in: [packages/ecs/index.ts:42](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/ecs/index.ts#L42)

## Properties

### architecture?

> `readonly` `optional` **architecture**: [`Architecture`](../type-aliases/Architecture.md)

Defined in: [packages/ecs/index.ts:68](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/ecs/index.ts#L68)

The architecture of the container. If not provided, the default is @DEFAULT_ARCHITECTURE.

***

### containerName

> `readonly` **containerName**: `string`

Defined in: [packages/ecs/index.ts:74](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/ecs/index.ts#L74)

The name of the container. This is a required property

***

### dockerPath

> `readonly` **dockerPath**: `string`

Defined in: [packages/ecs/index.ts:79](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/ecs/index.ts#L79)

The path to the Dockerfile. This is a required property

***

### memoryLimitGiB

> `readonly` **memoryLimitGiB**: `number`

Defined in: [packages/ecs/index.ts:63](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/ecs/index.ts#L63)

The memory limit in GiB. If not provided, the default is @DEFAULT_MEMORY_GB.
The memory limit must be between 0.5 and 120 GiB.
But please note that the memory limit varies depending on the number of CPUs, please refer to the table above.

***

### nCpus

> `readonly` **nCpus**: `number`

Defined in: [packages/ecs/index.ts:56](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/ecs/index.ts#L56)

The number of CPUs to use, between 0.25 and 16. If not provided, the default is @DEFAULT_VCPUS.

***

### runtimePlatform?

> `readonly` `optional` **runtimePlatform**: `CpuArchitecture`

Defined in: [packages/ecs/index.ts:51](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/ecs/index.ts#L51)

The runtime CPU architecture, either X86_64 or ARM64. If not provided, the default is @DEFAULT_ARCHITECTURE.

***

### vpcName?

> `readonly` `optional` **vpcName**: `string`

Defined in: [packages/ecs/index.ts:46](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/ecs/index.ts#L46)

The name of the VPC to use. If not provided, the @DEFAULT_MAIN_VPC_NAME will be used.
