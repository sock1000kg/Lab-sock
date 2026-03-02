from typing import Any, Dict
from .shell import run_cmd
import json


class TerraformManager:
    def __init__(self, tf_dir: str) -> None:
        self.tf_dir = tf_dir

    def apply(self) -> None:
        run_cmd(["terraform", "apply", "-auto-approve"], self.tf_dir)

    def get_outputs(self) -> Dict[str, Any]:
        """Fetch and return tf outputs as a Dict"""
        output = run_cmd(["terraform", "output", "-json"], self.tf_dir, capture=True)
        if not output:
            return {}
        else:
            return json.loads(output)

    def get_gateway_ip(self) -> str:
        output = self.get_outputs()

        try:
            return str(output["gateway_public_ip"]["value"])
        except KeyError:
            raise ValueError("[ERROR] Could not find 'gateway_public_ip' in TF outputs")
