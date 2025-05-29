import {
  ISecurityGroup,
  IVpc,
  SecurityGroup,
  Vpc,
  VpcLookupOptions,
} from "aws-cdk-lib/aws-ec2";
import { Construct } from "constructs";

export const VPC_NAME = "main-vpc";
export const VPC_STACK_NAME = "networking";

export const VPC_LOOKUP_PROPS: VpcLookupOptions = {
  vpcName: VPC_NAME,
  tags: {
    Stack: VPC_STACK_NAME,
  },
};

export class OrcaBusVpc {
  public static fromLookup(scope: Construct): IVpc {
    return Vpc.fromLookup(scope, "OrcaBusMainVpc", VPC_LOOKUP_PROPS);
  }
}

const SHARED_SECURITY_GROUP_NAME = "OrcaBusSharedComputeSecurityGroup";
export class OrcaBusSharedComputeSecurityGroup {
  public static fromLookup(scope: Construct, vpc: IVpc): ISecurityGroup {
    return SecurityGroup.fromLookupByName(
      scope,
      "SharedSecurityGroup",
      SHARED_SECURITY_GROUP_NAME,
      vpc,
    );
  }
}

const EVENT_BUS_NAME = "OrcaBusMain";
