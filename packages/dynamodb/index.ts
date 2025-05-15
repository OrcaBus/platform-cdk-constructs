import {Construct} from 'constructs';
import * as dynamodb from 'aws-cdk-lib/aws-dynamodb';
import {RemovalPolicy} from 'aws-cdk-lib';
import {TablePropsV2} from "aws-cdk-lib/aws-dynamodb";
import {DEFAULT_PARTITION_KEY_NAME, DEFAULT_SORT_KEY_NAME, DEFAULT_TIME_TO_LIVE_EXPIRY_KEY_NAME} from "./config";

export interface DynamoDbPartitionedConstructProps extends TablePropsV2 {
     /**
     * Optional, name of the partition key, but by default set to 'id'
     */
    readonly partitionKeyName?: string

    /**
    *  Optional, name of the sort key, but by default set to 'id_type'
    */
    readonly sortKeyName?: string
}


export interface DynamoDbNonPartitionedConstructProps extends TablePropsV2 {
    /**
     * Optional, name of the partition key, but by default set to 'id'
    */
    readonly partitionKeyName?: string
}


export class DynamoDbPartitionedConstruct extends Construct {
    public readonly table: dynamodb.TableV2;
    constructor(scope: Construct, id: string, props: DynamoDbPartitionedConstructProps) {
        super(scope, id);

        // We cannot override the tableName property type in the interface
        // So instead we need to force tableName to be a string rather than an optional string
        if (props.tableName === undefined) {
            throw new Error('tableName is required');
        }

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

export class DynamoDbNonPartitionedConstruct extends Construct {
    public readonly table: dynamodb.TableV2;
    constructor(scope: Construct, id: string, props: DynamoDbNonPartitionedConstructProps) {
        super(scope, id);

        // We cannot override the tableName property type in the interface
        // So instead we need to force tableName to be a string rather than an optional string
        if (props.tableName === undefined) {
            throw new Error('tableName is required');
        }

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




