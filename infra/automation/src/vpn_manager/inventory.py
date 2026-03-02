import re

def update_ansible_inventory(file_path: str, new_ip: str) -> None:
    """Update ansible inventory in file_path"""
    with open(file_path, "r") as file:
        content = file.read()

    updated = re.sub(
        r'(azure-gateway\s+ansible_host=)[0-9\.]+', 
        rf'\g<1>{new_ip}', 
        content
    )

    with open(file_path, "w") as file:
        file.write(updated)
