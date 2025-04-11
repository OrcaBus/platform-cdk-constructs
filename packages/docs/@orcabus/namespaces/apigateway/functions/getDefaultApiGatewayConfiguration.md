[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../globals.md) / [apigateway](../README.md) / getDefaultApiGatewayConfiguration

# Function: getDefaultApiGatewayConfiguration()

> **getDefaultApiGatewayConfiguration**(`stage`): `object`

Defined in: [packages/api-gateway/config.ts:34](https://github.com/OrcaBus/platform-cdk-constructs/blob/6e1fbcef98a7681c26e26c873ce8916f8c6809dd/packages/api-gateway/config.ts#L34)

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
