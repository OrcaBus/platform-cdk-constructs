[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [provider](../README.md) / ProviderFunctionProps

# Interface: ProviderFunctionProps

Defined in: [packages/provider-function/index.ts:11](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/provider-function/index.ts#L11)

Props for the resource invoke construct.

## Properties

### additionalHash?

> `readonly` `optional` **additionalHash?**: `string`

Defined in: [packages/provider-function/index.ts:43](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/provider-function/index.ts#L43)

An additional hash property that can be used to determine if the custom resource should be updated. By default,
this is the s3Key of the Lambda code asset, which is derived from the asset hash. This is used to ensure that
the custom resource is updated whenever the Lambda function changes, so that the function gets called again.
Add a constant value here to override this behaviour.

***

### function

> `readonly` **function**: `IFunction`

Defined in: [packages/provider-function/index.ts:19](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/provider-function/index.ts#L19)

The provider function.

***

### isCompleteHandler?

> `readonly` `optional` **isCompleteHandler?**: `IFunction`

Defined in: [packages/provider-function/index.ts:24](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/provider-function/index.ts#L24)

The AWS Lambda function to invoke in order to determine if the operation is complete. Used to create
an asynchronous operation for the provider.

***

### queryInterval?

> `readonly` `optional` **queryInterval?**: `Duration`

Defined in: [packages/provider-function/index.ts:28](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/provider-function/index.ts#L28)

The interval between calls to the `isCompleteHandler`.

***

### resourceProperties?

> `readonly` `optional` **resourceProperties?**: `Record`\<`string`, `unknown`\>

Defined in: [packages/provider-function/index.ts:36](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/provider-function/index.ts#L36)

Properties that get defined in the template and passed to the Lambda function via `ResourceProperties`.

***

### totalTimeout?

> `readonly` `optional` **totalTimeout?**: `Duration`

Defined in: [packages/provider-function/index.ts:32](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/provider-function/index.ts#L32)

The total timeout for the entire operation.

***

### vpc

> `readonly` **vpc**: `IVpc`

Defined in: [packages/provider-function/index.ts:15](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/provider-function/index.ts#L15)

Vpc for the function.
