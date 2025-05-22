[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [apigateway](../README.md) / OrcaBusApiGatewayProps

# Interface: OrcaBusApiGatewayProps

Defined in: [packages/api-gateway/api-gateway.ts:37](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/api-gateway/api-gateway.ts#L37)

## Properties

### apiGwLogsConfig

> `readonly` **apiGwLogsConfig**: [`ApiGwLogsConfig`](ApiGwLogsConfig.md)

Defined in: [packages/api-gateway/api-gateway.ts:63](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/api-gateway/api-gateway.ts#L63)

The configuration for aws cloudwatch logs

***

### apiName

> `readonly` **apiName**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:41](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/api-gateway/api-gateway.ts#L41)

The name of the API.

***

### cognitoClientIdParameterNameArray?

> `readonly` `optional` **cognitoClientIdParameterNameArray**: `string`[]

Defined in: [packages/api-gateway/api-gateway.ts:59](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/api-gateway/api-gateway.ts#L59)

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

Defined in: [packages/api-gateway/api-gateway.ts:51](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/api-gateway/api-gateway.ts#L51)

The cognito user pool id parameter name.

#### Default

```ts
DEFAULT_COGNITO_USER_POOL_ID_PARAMETER_NAME
```

***

### corsAllowOrigins

> `readonly` **corsAllowOrigins**: `string`[]

Defined in: [packages/api-gateway/api-gateway.ts:67](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/api-gateway/api-gateway.ts#L67)

Allowed CORS origins.

***

### customDomainNamePrefix

> `readonly` **customDomainNamePrefix**: `string`

Defined in: [packages/api-gateway/api-gateway.ts:45](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/api-gateway/api-gateway.ts#L45)

The prefix for the custom domain name
