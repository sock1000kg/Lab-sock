# Outputs for Ansible

output "gateway_public_ip" {
  description = "The public IP of the VPN Gateway. Use this in Ansible inventory."
  value       = azurerm_public_ip.gateway_ip.ip_address
}

output "gateway_ssh_user" {
  value = azurerm_linux_virtual_machine.gateway_vm.admin_username
}
