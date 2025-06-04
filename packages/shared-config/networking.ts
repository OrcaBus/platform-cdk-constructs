import {
  ISecurityGroup,
  IVpc,
  SecurityGroup,
  Vpc,
  VpcLookupOptions,
} from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

// VPC configuration
/**
 * The main VPC name used by OrcaBus.
 */
export const VPC_NAME = "main-vpc";
/**
 * The stack name where the VPC is defined.
 */
export const VPC_STACK_NAME = "networking";
/**
 * VPC lookup options as needed by CDK for looking up the VPC.
 */
export const VPC_LOOKUP_PROPS: VpcLookupOptions = {
  vpcName: VPC_NAME,
  tags: { Stack: VPC_STACK_NAME },
};

/**
 * Helper for looking up the shared OrcaBus VPC.
 */
export class OrcaBusVpc {
  /**
   * The shared VPC that is used by OrcaBus.
   * @param scope
   * @returns IVpc
   */
  public static fromLookup(scope: Construct): IVpc {
    return Vpc.fromLookup(scope, "OrcaBusMainVpc", VPC_LOOKUP_PROPS);
  }
}

/**
 * Shared security group used by compute resources to access the database.
 */
export const SHARED_SECURITY_GROUP_NAME = "OrcaBusSharedComputeSecurityGroup";

/**
 * Helper for looking up the shared compute security group by name.
 */
export class OrcaBusSharedComputeSecurityGroup {
  /**
   * The shared security group that is used by compute resources to access the database.
   * @param scope
   * @param vpc
   * @returns ISecurityGroup
   */
  public static fromLookup(scope: Construct, vpc: IVpc): ISecurityGroup {
    return SecurityGroup.fromLookupByName(
      scope,
      "SharedSecurityGroup",
      SHARED_SECURITY_GROUP_NAME,
      vpc,
    );
  }
}
