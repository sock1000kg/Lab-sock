# Sock1000kg Homelab

Infrastructure as Code (IaC) repository for my bare-metal Kubernetes homelab.

## Architecture
* **Hardware:** Dell Inspiron 15-3567 (Ubuntu Server 24.04), Azure B1s (Satellite Node)
* **Orchestrator:** K3s (Single Node)
* **Ingress:** Cloudflare Tunnel -> Traefik Gateway API
* **GitOps:** ArgoCD
* **Secrets:** Bitnami Sealed Secrets

## Quick Start
1.  **Bootstrap Server:**
    ```bash
    cd ansible && ansible-playbook site.yml -i inventory/hosts.ini
    ```
2.  **Bootstrap Cluster:**
    *(This section will be filled when we set up ArgoCD)*

## Structure
* `k8s/`: Kubernetes Manifests (The Desired State)
* `ansible/`: Server Provisioning (The Metal Management)
