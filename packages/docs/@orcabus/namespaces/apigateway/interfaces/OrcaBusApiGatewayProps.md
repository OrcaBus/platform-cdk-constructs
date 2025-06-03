[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [apigateway](../README.md) / OrcaBusApiGatewayProps

# Interface: OrcaBusApiGatewayProps

Defined in: [packages/api-gateway/api-gateway.ts:40](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L40)

## Properties

### apiGwLogsConfig

> `readonly` **apiGwLogsConfig**: [`ApiGwLogsConfig`](ApiGwLogsConfig.md)

Defined in: [packages/api-gateway/api-gateway.ts:66](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L66)

The configuration for aws cloudwatch logs

***

### apiName

> `readonly` **apiName**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:44](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L44)

The name of the API.

***

### cognitoClientIdParameterNameArray?

> `readonly` `optional` **cognitoClientIdParameterNameArray**: `string`[]

Defined in: [packages/api-gateway/api-gateway.ts:62](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L62)

The parameter name for the cognito client id in array.
In order API Gateway to validate the JWT token, it needs to know the client id which usually
stored in SSM Parameter. This will accept multiple parameter name in an array.

#### Default

```ts
DEFAULT_COGNITO_CLIENT_ID_PARAMETER_NAME_ARRAY
```

***

### cognitoUserPoolIdParameterName?

> `readonly` `optional` **cognitoUserPoolIdParameterName**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:54](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L54)

The cognito user pool id parameter name.

#### Default

```ts
DEFAULT_COGNITO_USER_POOL_ID_PARAMETER_NAME
```

***

### corsAllowOrigins

> `readonly` **corsAllowOrigins**: `string`[]

Defined in: [packages/api-gateway/api-gateway.ts:70](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L70)

Allowed CORS origins.

***

### customDomainNamePrefix

> `readonly` **customDomainNamePrefix**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:48](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/api-gateway/api-gateway.ts#L48)

The prefix for the custom domain name
