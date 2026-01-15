[**@orcabus/platform-cdk-constructs**](../../../../README.md)

***

[@orcabus/platform-cdk-constructs](../../../../README.md) / [dynamodb](../README.md) / DynamoDbPartitionedConstructProps

# Interface: DynamoDbPartitionedConstructProps

Defined in: [packages/dynamodb/index.ts:7](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/dynamodb/index.ts#L7)

## Extends

- `TablePropsV2`

## Properties

### billing?

> `readonly` `optional` **billing**: `Billing`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:299

The billing mode and capacity settings to apply to the table.

#### Default

```ts
Billing.onDemand()
```

#### Inherited from

`TablePropsV2.billing`

***

### ~~contributorInsights?~~

> `readonly` `optional` **contributorInsights**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:170

Whether CloudWatch contributor insights is enabled.

#### Deprecated

use `contributorInsightsSpecification` instead

#### Default

```ts
false
```

#### Inherited from

`TablePropsV2.contributorInsights`

***

### contributorInsightsSpecification?

> `readonly` `optional` **contributorInsightsSpecification**: `ContributorInsightsSpecification`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:175

Whether CloudWatch contributor insights is enabled and what mode is selected

#### Default

```ts
- contributor insights is not enabled
```

#### Inherited from

`TablePropsV2.contributorInsightsSpecification`

***

### deletionProtection?

> `readonly` `optional` **deletionProtection**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:181

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:287

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:347

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:333

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:206

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:341

Local secondary indexes.

Note: You can only provide a maximum of 5 local secondary indexes.

#### Default

```ts
- no local secondary indexes
```

#### Inherited from

`TablePropsV2.localSecondaryIndexes`

***

### multiRegionConsistency?

> `readonly` `optional` **multiRegionConsistency**: `MultiRegionConsistency`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:325

Specifies the consistency mode for a new global table.

#### Default

```ts
MultiRegionConsistency.EVENTUAL
```

#### Inherited from

`TablePropsV2.multiRegionConsistency`

***

### partitionKey

> `readonly` **partitionKey**: `Attribute`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:260

Partition key attribute definition.

#### Inherited from

`TablePropsV2.partitionKey`

***

### partitionKeyName?

> `readonly` `optional` **partitionKeyName**: `string`

Defined in: [packages/dynamodb/index.ts:11](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/dynamodb/index.ts#L11)

Optional, name of the partition key, but by default set to 'id'

***

### ~~pointInTimeRecovery?~~

> `readonly` `optional` **pointInTimeRecovery**: `boolean`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:187

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:194

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:293

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:309

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:218

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:266

Sort key attribute definition.

#### Default

```ts
- no sort key
```

#### Inherited from

`TablePropsV2.sortKey`

***

### sortKeyName?

> `readonly` `optional` **sortKeyName**: `string`

Defined in: [packages/dynamodb/index.ts:16](https://github.com/OrcaBus/platform-cdk-constructs/blob/main/packages/dynamodb/index.ts#L16)

Optional, name of the sort key, but by default set to 'id_type'

***

### tableClass?

> `readonly` `optional` **tableClass**: `TableClass`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:200

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:272

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:212

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:278

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

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:353

The warm throughput configuration for the table.

#### Default

```ts
- no warm throughput is configured
```

#### Inherited from

`TablePropsV2.warmThroughput`

***

### witnessRegion?

> `readonly` `optional` **witnessRegion**: `string`

Defined in: node\_modules/.pnpm/aws-cdk-lib@2.233.0\_constructs@10.4.2/node\_modules/aws-cdk-lib/aws-dynamodb/lib/table-v2.d.ts:319

The witness Region for the MRSC global table.
A MRSC global table can be configured with either three replicas, or with two replicas and one witness.

Note: Witness region cannot be specified for a Multi-Region Eventual Consistency (MREC) Global Table.
Witness regions are only supported for Multi-Region Strong Consistency (MRSC) Global Tables.

#### Default

```ts
- no witness region
```

#### Inherited from

`TablePropsV2.witnessRegion`
