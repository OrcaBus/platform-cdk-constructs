[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [apigateway](../README.md) / OrcaBusApiGatewayProps

# Interface: OrcaBusApiGatewayProps

Defined in: [packages/api-gateway/api-gateway.ts:39](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L39)

## Properties

### apiGwLogsConfig

> `readonly` **apiGwLogsConfig**: [`ApiGwLogsConfig`](ApiGwLogsConfig.md)

Defined in: [packages/api-gateway/api-gateway.ts:65](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L65)

The configuration for aws cloudwatch logs

***

### apiName

> `readonly` **apiName**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:43](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L43)

The name of the API.

***

### cognitoClientIdParameterNameArray

> `readonly` **cognitoClientIdParameterNameArray**: `string`[]

Defined in: [packages/api-gateway/api-gateway.ts:61](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L61)

Array of SSM parameter names containing Cognito client IDs.

API Gateway uses these client IDs to validate JWT tokens. Each parameter
should contain a valid Cognito application client ID that is authorized
to access this API.

***

### cognitoUserPoolIdParameterName?

> `readonly` `optional` **cognitoUserPoolIdParameterName**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:53](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L53)

The cognito user pool id parameter name.

#### Default

```ts
DEFAULT_COGNITO_USER_POOL_ID_PARAMETER_NAME
```

***

### corsAllowOrigins

> `readonly` **corsAllowOrigins**: `string`[]

Defined in: [packages/api-gateway/api-gateway.ts:69](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L69)

Allowed CORS origins.

***

### customDomainNamePrefix

> `readonly` **customDomainNamePrefix**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:47](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L47)

The prefix for the custom domain name
