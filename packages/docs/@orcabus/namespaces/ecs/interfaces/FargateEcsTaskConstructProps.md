[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [ecs](../README.md) / FargateEcsTaskConstructProps

# Interface: FargateEcsTaskConstructProps

Defined in: [packages/ecs/index.ts:39](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/ecs/index.ts#L39)

## Properties

### architecture

> `readonly` **architecture**: [`Architecture`](../type-aliases/Architecture.md)

Defined in: [packages/ecs/index.ts:65](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/ecs/index.ts#L65)

The architecture of the container. If not provided, the default is @DEFAULT_ARCHITECTURE.

***

### containerName

> `readonly` **containerName**: `string`

Defined in: [packages/ecs/index.ts:71](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/ecs/index.ts#L71)

The name of the container. This is a required property

***

### dockerPath

> `readonly` **dockerPath**: `string`

Defined in: [packages/ecs/index.ts:76](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/ecs/index.ts#L76)

The path to the Dockerfile. This is a required property

***

### memoryLimitGiB

> `readonly` **memoryLimitGiB**: `number`

Defined in: [packages/ecs/index.ts:60](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/ecs/index.ts#L60)

The memory limit in GiB. If not provided, the default is @DEFAULT_MEMORY_GB.
The memory limit must be between 0.5 and 120 GiB.
But please note that the memory limit varies depending on the number of CPUs, please refer to the table above.

***

### nCpus

> `readonly` **nCpus**: `number`

Defined in: [packages/ecs/index.ts:53](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/ecs/index.ts#L53)

The number of CPUs to use, between 0.25 and 16. If not provided, the default is @DEFAULT_VCPUS.

***

### runtimePlatform

> `readonly` **runtimePlatform**: `CpuArchitecture`

Defined in: [packages/ecs/index.ts:48](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/ecs/index.ts#L48)

The runtime CPU architecture, either X86_64 or ARM64. If not provided, the default is @DEFAULT_ARCHITECTURE.

***

### vpcName?

> `readonly` `optional` **vpcName**: `string`

Defined in: [packages/ecs/index.ts:43](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/ecs/index.ts#L43)

The name of the VPC to use. If not provided, the @DEFAULT_MAIN_VPC_NAME will be used.
