#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance, InstanceConfig
from cdktf_cdktf_provider_cloudinit.provider import CloudinitProvider
from cdktf_cdktf_provider_cloudinit.data_cloudinit_config import DataCloudinitConfig, DataCloudinitConfigPart


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        AwsProvider(self, "AWS", region="eu-central-1")
        CloudinitProvider(self, "Cloudinit")

        shscript = DataCloudinitConfigPart(
            content="""#!/bin/bash
set -x
echo "foobar batz" > /home/ubuntu/foobar.txt
""",
            content_type="text/x-shellscript",
            filename="foobar.sh"
        )

        cloudinitdata = DataCloudinitConfig(self, "DataCloudinit",
            part=[shscript],
            base64_encode=False,
            gzip=False
        )

        #cfg = InstanceConfig(self, "InstanceConfig")
        instance = Instance(self, "compute",
                            ami="ami-0d1ddd83282187d18",
                            instance_type="t3.micro",
                            subnet_id="subnet-08eb6daaa70fdf686",
                            user_data=cloudinitdata.rendered
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
