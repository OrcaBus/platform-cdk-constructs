[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [lambda](../README.md) / MartEnvironmentVariables

# Interface: MartEnvironmentVariables

Defined in: [packages/lambda/index.ts:43](https://github.com/orcabus/platform-cdk-constructs/blob/d147e1d3dfea325d03b6788743df722bc7755f87/packages/lambda/index.ts#L43)

## Properties

### ATHENA\_DATABASE\_NAME?

> `readonly` `optional` **ATHENA\_DATABASE\_NAME**: `string`

Defined in: [packages/lambda/index.ts:57](https://github.com/orcabus/platform-cdk-constructs/blob/d147e1d3dfea325d03b6788743df722bc7755f87/packages/lambda/index.ts#L57)

Provide the athenaDatabaseName, otherwise it will default to @MART_ENV_VARS.ATHENA_DATABASE_NAME

***

### ATHENA\_DATASOURCE\_NAME?

> `readonly` `optional` **ATHENA\_DATASOURCE\_NAME**: `string`

Defined in: [packages/lambda/index.ts:52](https://github.com/orcabus/platform-cdk-constructs/blob/d147e1d3dfea325d03b6788743df722bc7755f87/packages/lambda/index.ts#L52)

Provide the athenaDatasourceName, otherwise it will default to @MART_S3_BUCKET.A

***

### ATHENA\_WORKGROUP\_NAME?

> `readonly` `optional` **ATHENA\_WORKGROUP\_NAME**: `string`

Defined in: [packages/lambda/index.ts:47](https://github.com/orcabus/platform-cdk-constructs/blob/d147e1d3dfea325d03b6788743df722bc7755f87/packages/lambda/index.ts#L47)

Provide the athenaWorkgroupName, otherwise it will default to @MART_ENV_VARS.ATHENA_WORKGROUP_NAME
