[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [provider](../README.md) / ProviderFunctionProps

# Interface: ProviderFunctionProps

Defined in: [packages/provider-function/index.ts:11](https://github.com/OrcaBus/platform-cdk-constructs/blob/1a0d52719d4b2246664b571e66b62333030eb6c7/packages/provider-function/index.ts#L11)

Props for the resource invoke construct.

## Properties

### additionalHash?

> `optional` **additionalHash**: `string`

Defined in: [packages/provider-function/index.ts:30](https://github.com/OrcaBus/platform-cdk-constructs/blob/1a0d52719d4b2246664b571e66b62333030eb6c7/packages/provider-function/index.ts#L30)

An additional hash property that can be used to determine if the custom resource should be updated. By default,
this is the s3Key of the Lambda code asset, which is derived from the asset hash. This is used to ensure that
the custom resource is updated whenever the Lambda function changes, so that the function gets called again.
Add a constant value here to override this behaviour.

***

### function

> **function**: `IFunction`

Defined in: [packages/provider-function/index.ts:19](https://github.com/OrcaBus/platform-cdk-constructs/blob/1a0d52719d4b2246664b571e66b62333030eb6c7/packages/provider-function/index.ts#L19)

The provider function.

***

### resourceProperties?

> `optional` **resourceProperties**: `Record`\<`string`, `unknown`\>

Defined in: [packages/provider-function/index.ts:23](https://github.com/OrcaBus/platform-cdk-constructs/blob/1a0d52719d4b2246664b571e66b62333030eb6c7/packages/provider-function/index.ts#L23)

Properties that get defined in the template and passed to the Lambda function via `ResourceProperties`.

***

### vpc

> **vpc**: `IVpc`

Defined in: [packages/provider-function/index.ts:15](https://github.com/OrcaBus/platform-cdk-constructs/blob/1a0d52719d4b2246664b571e66b62333030eb6c7/packages/provider-function/index.ts#L15)

Vpc for the function.
