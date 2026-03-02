import os
import argparse
import sys

from vpn_manager.ansible import AnsibleManager
from vpn_manager.inventory import update_ansible_inventory
from vpn_manager.terraform import TerraformManager

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), "../../../..")
PROJECT_ROOT_ABS = os.path.abspath(PROJECT_ROOT)
TF_DIR = os.path.join(PROJECT_ROOT_ABS, "infra/terraform/azure")
ANS_DIR = os.path.join(PROJECT_ROOT_ABS, "infra/ansible")
BOOTSTRAP_INV = os.path.join(ANS_DIR, "inventory/wireguard-bootstrap.ini")
REGULAR_INV = os.path.join(ANS_DIR, "inventory/wireguard.ini")
BOOTSTRAP_PLAYBOOK = os.path.join(ANS_DIR, "playbooks/bootstrap-wireguard.yaml")


print("CWD:", os.getcwd())
print("FILE:", __file__)
print("PROJECT_ROOT:", PROJECT_ROOT)
print("PROJECT_ROOT_ABS:", PROJECT_ROOT_ABS)
print("TF_DIR:", TF_DIR)
print("ANSIBLE_DIR:", ANS_DIR)
print("BOOTSTRAP_INV:", BOOTSTRAP_INV)
print("REGULAR_INV:", REGULAR_INV)
print("BOOTSTRAP_PLAYBOOK:", BOOTSTRAP_PLAYBOOK)



def bootstrap():
    tf = TerraformManager(TF_DIR)
    ans = AnsibleManager(ANS_DIR)

    print("\nRunning Terraform apply")
    tf.apply()

    print("\nExtracting public IP")
    try:
        hub_pub_ip = tf.get_gateway_ip()
    except ValueError as error:
        print(error)
        sys.exit(1)

    print("\nUpdating inventory")
    update_ansible_inventory(BOOTSTRAP_INV, hub_pub_ip)
    print("Inventory updated")

    print("\nRunning bootstrap-wireguard playbook")
    ansible_output = ans.run_playbook_live("inventory/wireguard-bootstrap.ini",BOOTSTRAP_PLAYBOOK)

    print("\nExtrating Hub Pulbic Key")
    hub_pub_key = ans.extract_public_key(ansible_output)

    if hub_pub_key:
        print("\n" + "=" * 60)
        print("WireGuard Hub is now live, please copy the hub's public key and IP to your GUI interface")
        print("HUB PUBLIC KEY: ", hub_pub_key)
        print("HUB_PUB_IP: ", hub_pub_ip)
        print("\n" + "=" * 60)
    else:
        print("Extracting hub's public key from ansible output failed")

def check_connection():
    ans = AnsibleManager(ANS_DIR)

    print("\nRunning ping playbook over the VPN tunnel")
    ans.run_ping(REGULAR_INV)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["bootstrap", "verify"])
    args = parser.parse_args()

    if args.command == "bootstrap":
        bootstrap()
    elif args.command == "verify":
        check_connection()

if __name__ == "__main__":
    main()
