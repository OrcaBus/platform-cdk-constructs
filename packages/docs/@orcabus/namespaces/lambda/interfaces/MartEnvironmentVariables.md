[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [lambda](../README.md) / MartEnvironmentVariables

# Interface: MartEnvironmentVariables

Defined in: [packages/lambda/index.ts:46](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/lambda/index.ts#L46)

## Properties

### athenaDatabaseName?

> `readonly` `optional` **athenaDatabaseName**: `string`

Defined in: [packages/lambda/index.ts:60](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/lambda/index.ts#L60)

Provide the athenaDatabaseName, otherwise it will default to @MART_ENV_VARS.ATHENA_DATABASE_NAME

***

### athenaDatasourceName?

> `readonly` `optional` **athenaDatasourceName**: `string`

Defined in: [packages/lambda/index.ts:55](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/lambda/index.ts#L55)

Provide the athenaDatasourceName, otherwise it will default to @MART_ENV_VARS.athenaDatasourceName

***

### athenaWorkgroupName?

> `readonly` `optional` **athenaWorkgroupName**: `string`

Defined in: [packages/lambda/index.ts:50](https://github.com/OrcaBus/platform-cdk-constructs/blob/c976adc64e129e16931e5f8794549bfec6d441a5/packages/lambda/index.ts#L50)

Provide the athenaWorkgroupName, otherwise it will default to @MART_ENV_VARS.ATHENA_WORKGROUP_NAME
