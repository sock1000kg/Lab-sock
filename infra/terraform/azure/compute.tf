# Public IP
# Static SKU ensures the IP doesn't change if you reboot the VM.
# If wanna add a Load Balancer later, move this Public IP to the LB
# and give the VM a private IP only.
resource "azurerm_public_ip" "gateway_ip" {
  name                = "pip-${var.project_name}-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  allocation_method   = "Static"
  sku                 = "Standard" # Required for some availability zones
}

# Network Interface (NIC)
# The virtual network card. It connects the VM to the VNet and Public IP.
resource "azurerm_network_interface" "gateway_nic" {
  name                = "nic-${var.project_name}-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.internal.id # WIRING to Networking
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = azurerm_public_ip.gateway_ip.id
  }
}

# Connect Firewall (NSG) to NIC
# could also wire the NSG to the Subnet
# if want it to apply to all VMs in that subnet.
resource "azurerm_network_interface_security_group_association" "gateway_firewall_assoc" {
  network_interface_id      = azurerm_network_interface.gateway_nic.id
  network_security_group_id = azurerm_network_security_group.gateway_firewall.id
}

# The Virtual Machine
resource "azurerm_linux_virtual_machine" "gateway_vm" {
  name                = "vm-${var.project_name}-gateway"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_B1s" # RENAMABLE: No. This is an Azure SKU.
  admin_username      = "sockadmin"    # RENAMABLE: Yes.
  
  network_interface_ids = [
    azurerm_network_interface.gateway_nic.id,
  ]

  admin_ssh_key {
    username   = "sockadmin"
    public_key = file(var.admin_ssh_key_path) # Reads from variable
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }

  # Tagging is vital for cost tracking in Prod
  tags = {
    environment = var.environment
    role        = "vpn-gateway"
  }
}
