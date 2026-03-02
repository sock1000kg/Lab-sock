import re
import subprocess
import sys
from typing import Optional

from vpn_manager.shell import run_cmd


class AnsibleManager:
    def __init__(self, ans_dir: str) -> None:
        self.ans_dir = ans_dir

    def run_playbook_live(self, inventory: str, playbook: str) -> str:
        """Runs playbook and streams output to terminal, returns the full output"""
        process = subprocess.Popen(
            ["ansible-playbook", "-i", inventory, playbook],
            cwd=self.ans_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        full_output = ""
        if process.stdout:
            for line in process.stdout: 
                print(line, end="") 
                full_output += line

        process.wait()
        if process.returncode != 0:
            print(f"\n[ERROR] Playbook {playbook} failed")
            sys.exit(1)
        else: 
            return full_output

    def extract_public_key(self, ansible_output: str) -> Optional[str]:
        """Finds the WireGuard public key from the Ansible stdout."""
        key_match = re.search(r'"azure_pub_key\.stdout":\s*"([^"]+)"', ansible_output)
        if key_match:
            return key_match.group(1)
        return None

    def run_ping(self, inventory: str) -> None:
        """Runs the ping verification playbook."""
        run_cmd(
            ["ansible-playbook", "-i", inventory, "playbooks/ping.yaml"], 
            cwd=self.
            ans_dir
        )
