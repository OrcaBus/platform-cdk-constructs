/**
 * The identifier for the OrcaBus RDS database cluster.
 */
export const DB_CLUSTER_IDENTIFIER = "orcabus-db";
/**
 * SSM parameter name storing the RDS cluster resource ID.
 */
export const DB_CLUSTER_RESOURCE_ID_PARAMETER_NAME = "/orcabus/db-cluster-resource-id";
/**
 * SSM parameter name storing the RDS cluster endpoint host.
 */
export const DB_CLUSTER_ENDPOINT_HOST_PARAMETER_NAME =
  "/orcabus/db-cluster-endpoint-host";
/**
 * The port number used by the OrcaBus PostgreSQL database.
 */
export const DATABASE_PORT = 5432;
/**
 * The name of the AWS Secrets Manager secret for the RDS master user.
 */
export const RDS_MASTER_SECRET_NAME = "orcabus/master-rds"; // pragma: allowlist secret
