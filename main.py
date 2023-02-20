#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        AwsProvider(self, "AWS", region="eu-central-1")

        instance = Instance(self, "compute",
                            ami="ami-0d1ddd83282187d18",
                            instance_type="t3.micro",
                            subnet_id="subnet-02e07fa43d120a60d"
                            )

        TerraformOutput(self, "public_ip",
                        value=instance.public_ip,
                        )


def main():
    app = App()
    MyStack(app, "hello")
    app.synth()


if __name__ == "__main__":
    main()
