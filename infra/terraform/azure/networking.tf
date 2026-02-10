# Resource Group
# Container for all resources. Deleting this deletes EVERYTHING.
resource "azurerm_resource_group" "main" {
  name     = "rg-${var.project_name}-${var.environment}" 
  location = var.location
  # RENAMABLE: "main" is the internal Terraform name. can rename it, 
  # but references below must update too.
}

# Virtual Network (VNet)
# The isolated cloud network. 
resource "azurerm_virtual_network" "main" {
  name                = "vnet-${var.project_name}"
  address_space       = ["10.0.0.0/16"] # Capacity: 65,536 IPs
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}

# Subnet
# A segmentation of the VNet. 
# Azure subnets are neutral. Public access is defined by the Public IP attached to the NIC.
resource "azurerm_subnet" "internal" {
  name                 = "snet-internal"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"] # Capacity: 256 IPs avail (Minus Azure reserved IPs)
}

# Network Security Group -> Firewall
# Applying this to the NIC (in compute.tf) or Subnet limits traffic.
resource "azurerm_network_security_group" "gateway_firewall" {
  name                = "nsg-${var.project_name}-gateway"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  # Security Rule: SSH
  security_rule {
    name                       = "AllowSSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = var.my_home_ip # LOCKED TO ME
    destination_address_prefix = "*"
  }

  # Security Rule: WireGuard VPN
  security_rule {
    name                       = "AllowWireGuard"
    priority                   = 110
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Udp" # VPNs use UDP for speed
    source_port_range          = "*"
    destination_port_range     = "51820"
    source_address_prefix      = "*" 
    destination_address_prefix = "*"
  }
}
