import subprocess
import sys
from typing import List

def run_cmd(command: List[str], cwd: str|None = None, capture: bool = False) -> str|None:
    """
    Helper func to run shell cmd with error checking

    Args:
        command: commands with args as a list
        cwd: dir to run it from
        capture: if true, return stdout as str (and not print it out)
    """

    try:
        if capture:
            result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=True)
            return result.stdout
        else:
            subprocess.run(command, cwd=cwd, check=True)
            return None
    except subprocess.CalledProcessError as error:
        print(f"\n[ERROR] '{" ".join(command)}' failed")
        if capture:
            print(error.stderr)
        sys.exit(1)

