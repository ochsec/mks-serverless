"""A minimal MSK setup"""

import pulumi
import pulumi_aws as aws

pulumi_config = pulumi.Config()
aws_region = "us-west-2"
aws_provider = aws.Provider('awsProvider', profile="replmade", region=aws_region)

# VPC
vpc = aws.ec2.Vpc("mskVpc",
                  cidr_block="10.0.0.0/16",
                  enable_dns_support=True,
                  enable_dns_hostnames=True)

# Subnets
subnet1 = aws.ec2.Subnet("mskSubnet1",
                         vpc_id=vpc.id,
                         cidr_block="10.0.1.0/24",
                         availability_zone="us-west-2a")

subnet2 = aws.ec2.Subnet("mskSubnet2",
                         vpc_id=vpc.id,
                         cidr_block="10.0.2.0/24",
                         availability_zone="us-west-2b")

# Security Group
security_group = aws.ec2.SecurityGroup("mskSecurityGroup",
                                       vpc_id=vpc.id,
                                       description="Allow all inbound traffic",
                                       ingress=[{
                                           'protocol': '-1',
                                           'from_port': 0,
                                           'to_port': 0,
                                           'cidr_blocks': ['0.0.0.0/0'],
                                       }],
                                       egress=[{
                                           'protocol': '-1',
                                           'from_port': 0,
                                           'to_port': 0,
                                           'cidr_blocks': ['0.0.0.0/0'],
                                       }])

# Serverless MSK cluster
msk_cluster = aws.msk.ServerlessCluster("mskServerlessCluster",
                              cluster_name="msk-serverless-tutorial-cluster",
                              client_authentication=aws.msk.ClusterClientAuthenticationArgs(
                                  sasl=aws.msk.ServerlessClusterClientAuthenticationSaslArgs(
                                      iam=aws.msk.ServerlessClusterClientAuthenticationSaslIamArgs(
                                          enabled=True,
                                      ),
                                  ),
                              ),
                              vpc_configs=[aws.msk.ServerlessClusterVpcConfigArgs(
                                  subnet_ids=[subnet1.id, subnet2.id],
                                  security_group_ids=[security_group.id],
                              )])

pulumi.export("vpc_id", vpc.id)
pulumi.export("subnet1_id", subnet1.id)
pulumi.export("subnet2_id", subnet2.id)
pulumi.export("security_group_id", security_group.id)

