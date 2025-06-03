[**@orcabus/platform-cdk-constructs**](../../../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../../../README.md) / [sharedConfig](../../../README.md) / [networking](../README.md) / OrcaBusSharedComputeSecurityGroup

# Class: OrcaBusSharedComputeSecurityGroup

Defined in: [packages/shared-config/networking.ts:54](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/shared-config/networking.ts#L54)

Helper for looking up the shared compute security group by name.

## Constructors

### Constructor

> **new OrcaBusSharedComputeSecurityGroup**(): `OrcaBusSharedComputeSecurityGroup`

#### Returns

`OrcaBusSharedComputeSecurityGroup`

## Methods

### fromLookup()

> `static` **fromLookup**(`scope`, `vpc`): `ISecurityGroup`

Defined in: [packages/shared-config/networking.ts:61](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/shared-config/networking.ts#L61)

The shared security group that is used by compute resources to access the database.

#### Parameters

##### scope

`Construct`

##### vpc

`IVpc`

#### Returns

`ISecurityGroup`

ISecurityGroup
