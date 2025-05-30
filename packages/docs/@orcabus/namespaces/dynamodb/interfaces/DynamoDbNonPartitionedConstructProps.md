[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [dynamodb](../README.md) / DynamoDbNonPartitionedConstructProps

# Interface: DynamoDbNonPartitionedConstructProps

Defined in: [packages/dynamodb/index.ts:20](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/dynamodb/index.ts#L20)

## Extends

- `TablePropsV2`

## Properties

### billing?

> `readonly` `optional` **billing**: `Billing`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:225

The billing mode and capacity settings to apply to the table.

#### Default

```ts
Billing.onDemand()
```

#### Inherited from

`TablePropsV2.billing`

***

### contributorInsights?

> `readonly` `optional` **contributorInsights**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:101

Whether CloudWatch contributor insights is enabled.

#### Default

```ts
false
```

#### Inherited from

`TablePropsV2.contributorInsights`

***

### deletionProtection?

> `readonly` `optional` **deletionProtection**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:107

Whether deletion protection is enabled.

#### Default

```ts
false
```

#### Inherited from

`TablePropsV2.deletionProtection`

***

### dynamoStream?

> `readonly` `optional` **dynamoStream**: `StreamViewType`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:213

When an item in the table is modified, StreamViewType determines what information is
written to the stream.

#### Default

```ts
- streams are disabled if replicas are not configured and this property is
not specified. If this property is not specified when replicas are configured, then
NEW_AND_OLD_IMAGES will be the StreamViewType for all replicas
```

#### Inherited from

`TablePropsV2.dynamoStream`

***

### encryption?

> `readonly` `optional` **encryption**: `TableEncryptionV2`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:257

The server-side encryption.

#### Default

```ts
TableEncryptionV2.dynamoOwnedKey()
```

#### Inherited from

`TablePropsV2.encryption`

***

### globalSecondaryIndexes?

> `readonly` `optional` **globalSecondaryIndexes**: `GlobalSecondaryIndexPropsV2`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:243

Global secondary indexes.

Note: You can provide a maximum of 20 global secondary indexes.

#### Default

```ts
- no global secondary indexes
```

#### Inherited from

`TablePropsV2.globalSecondaryIndexes`

***

### kinesisStream?

> `readonly` `optional` **kinesisStream**: `IStream`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:132

Kinesis Data Stream to capture item level changes.

#### Default

```ts
- no Kinesis Data Stream
```

#### Inherited from

`TablePropsV2.kinesisStream`

***

### localSecondaryIndexes?

> `readonly` `optional` **localSecondaryIndexes**: `LocalSecondaryIndexProps`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:251

Local secondary indexes.

Note: You can only provide a maximum of 5 local secondary indexes.

#### Default

```ts
- no local secondary indexes
```

#### Inherited from

`TablePropsV2.localSecondaryIndexes`

***

### partitionKey

> `readonly` **partitionKey**: `Attribute`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:186

Partition key attribute definition.

#### Inherited from

`TablePropsV2.partitionKey`

***

### partitionKeyName?

> `readonly` `optional` **partitionKeyName**: `string`

Defined in: [packages/dynamodb/index.ts:24](https://github.com/OrcaBus/platform-cdk-constructs/blob/eb710b2f105d22a64c8abea3b2245773c2378377/packages/dynamodb/index.ts#L24)

Optional, name of the partition key, but by default set to 'id'

***

### ~~pointInTimeRecovery?~~

> `readonly` `optional` **pointInTimeRecovery**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:113

Whether point-in-time recovery is enabled.

#### Deprecated

use `pointInTimeRecoverySpecification` instead

#### Default

```ts
false - point in time recovery is not enabled.
```

#### Inherited from

`TablePropsV2.pointInTimeRecovery`

***

### pointInTimeRecoverySpecification?

> `readonly` `optional` **pointInTimeRecoverySpecification**: `PointInTimeRecoverySpecification`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:120

Whether point-in-time recovery is enabled
and recoveryPeriodInDays is set.

#### Default

```ts
- point in time recovery is not enabled.
```

#### Inherited from

`TablePropsV2.pointInTimeRecoverySpecification`

***

### removalPolicy?

> `readonly` `optional` **removalPolicy**: `RemovalPolicy`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:219

The removal policy applied to the table.

#### Default

```ts
RemovalPolicy.RETAIN
```

#### Inherited from

`TablePropsV2.removalPolicy`

***

### replicas?

> `readonly` `optional` **replicas**: `ReplicaTableProps`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:235

Replica tables to deploy with the primary table.

Note: Adding replica tables allows you to use your table as a global table. You
cannot specify a replica table in the region that the primary table will be deployed
to. Replica tables will only be supported if the stack deployment region is defined.

#### Default

```ts
- no replica tables
```

#### Inherited from

`TablePropsV2.replicas`

***

### resourcePolicy?

> `readonly` `optional` **resourcePolicy**: `PolicyDocument`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:144

Resource policy to assign to DynamoDB Table.

#### See

https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dynamodb-globaltable-replicaspecification.html#cfn-dynamodb-globaltable-replicaspecification-resourcepolicy

#### Default

```ts
- No resource policy statements are added to the created table.
```

#### Inherited from

`TablePropsV2.resourcePolicy`

***

### sortKey?

> `readonly` `optional` **sortKey**: `Attribute`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:192

Sort key attribute definition.

#### Default

```ts
- no sort key
```

#### Inherited from

`TablePropsV2.sortKey`

***

### tableClass?

> `readonly` `optional` **tableClass**: `TableClass`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:126

The table class.

#### Default

```ts
TableClass.STANDARD
```

#### Inherited from

`TablePropsV2.tableClass`

***

### tableName?

> `readonly` `optional` **tableName**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:198

The name of the table.

#### Default

```ts
- generated by CloudFormation
```

#### Inherited from

`TablePropsV2.tableName`

***

### tags?

> `readonly` `optional` **tags**: `CfnTag`[]

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:138

Tags to be applied to the primary table (default replica table).

#### Default

```ts
- no tags
```

#### Inherited from

`TablePropsV2.tags`

***

### timeToLiveAttribute?

> `readonly` `optional` **timeToLiveAttribute**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:204

The name of the TTL attribute.

#### Default

```ts
- TTL is disabled
```

#### Inherited from

`TablePropsV2.timeToLiveAttribute`

***

### warmThroughput?

> `readonly` `optional` **warmThroughput**: `WarmThroughput`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.195.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:263

The warm throughput configuration for the table.

#### Default

```ts
- no warm throughput is configured
```

#### Inherited from

`TablePropsV2.warmThroughput`
