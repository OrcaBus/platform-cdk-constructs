import {Construct} from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import {RemovalPolicy} from 'aws-cdk-lib';
import {TablePropsV2} from "aws-cdk-lib/aws-dynamodb";
import {DEFAULT_PARTITION_KEY_NAME, DEFAULT_SORT_KEY_NAME, DEFAULT_TIME_TO_LIVE_EXPIRY_KEY_NAME} from "./config";

export interface DynamoDbPartitionedPipelineConstructProps extends TablePropsV2 {
    tableName: string
    partitionKeyName?: string
    sortKeyName?: string
}


export interface DynamoDbNonPartitionedPipelineConstructProps extends TablePropsV2 {
    tableName: string
    partitionKeyName?: string
}


export class DynamoDbPartitionedPipelineConstruct extends Construct {
    public readonly table: dynamodb.TableV2;
    constructor(scope: Construct, id: string, props: DynamoDbPartitionedPipelineConstructProps) {
        super(scope, id);

        this.table = new dynamodb.TableV2(this, props.tableName, {
            ...props,
            /* Set the table name */
            tableName: props.tableName,
            /* Unique id across the sort key */
            partitionKey: {
                name: props.partitionKeyName ?? DEFAULT_PARTITION_KEY_NAME,
                type: dynamodb.AttributeType.STRING,
            },
            /* Categorical key */
            sortKey: {
                name: props.sortKeyName ?? DEFAULT_SORT_KEY_NAME,
                type: dynamodb.AttributeType.STRING,
            },
            /* Backup / removal policies */
            removalPolicy: props.removalPolicy || RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
            pointInTimeRecoverySpecification: {
                pointInTimeRecoveryEnabled: true,
            },
            /* Time to live attribute - helps keep the database a healthy size */
            timeToLiveAttribute: props.timeToLiveAttribute ?? DEFAULT_TIME_TO_LIVE_EXPIRY_KEY_NAME
        });
    }
}

export class DynamoDbNonPartitionedPipelineConstruct extends Construct {
    public readonly table: dynamodb.TableV2;
    constructor(scope: Construct, id: string, props: DynamoDbNonPartitionedPipelineConstructProps) {
        super(scope, id);

        this.table = new dynamodb.TableV2(this, props.tableName, {
            /* Set the table name */
            tableName: props.tableName,
            /* A globally unique identifier */
            partitionKey: {
                name: props.partitionKeyName ?? DEFAULT_PARTITION_KEY_NAME,
                type: dynamodb.AttributeType.STRING,
            },
            /* Backup / removal policies */
            removalPolicy: props.removalPolicy || RemovalPolicy.RETAIN_ON_UPDATE_OR_DELETE,
            pointInTimeRecoverySpecification: {
                pointInTimeRecoveryEnabled: true,
            },
            /* Time to live attribute - helps keep the database a healthy size */
            timeToLiveAttribute: props.timeToLiveAttribute ?? DEFAULT_TIME_TO_LIVE_EXPIRY_KEY_NAME
        });
    }
}




