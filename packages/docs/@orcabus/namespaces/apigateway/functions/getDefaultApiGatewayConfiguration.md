[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [apigateway](../README.md) / getDefaultApiGatewayConfiguration

# Function: getDefaultApiGatewayConfiguration()

> **getDefaultApiGatewayConfiguration**(`stage`): `object`

Defined in: [packages/api-gateway/config.ts:34](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/api-gateway/config.ts#L34)

## Parameters

### stage

[`StageName`](../../utils/type-aliases/StageName.md)

## Returns

`object`

### apiGwLogsConfig

> **apiGwLogsConfig**: \{ `removalPolicy`: `RemovalPolicy`; `retention`: `RetentionDays`; \} \| \{ `removalPolicy`: `RemovalPolicy`; `retention`: `RetentionDays`; \} \| \{ `removalPolicy`: `RemovalPolicy`; `retention`: `RetentionDays`; \}

### cognitoClientIdParameterNameArray

> **cognitoClientIdParameterNameArray**: `string`[] = `DEFAULT_COGNITO_CLIENT_ID_PARAMETER_NAME_ARRAY`

### corsAllowOrigins

> **corsAllowOrigins**: `string`[]
