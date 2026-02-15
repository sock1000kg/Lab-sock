# MANDATORY ARCHITECTURE VARIABLES 

variable "location" {
  description = "The physical Azure region. Determines latency and cost."
  type        = string
  default     = "Southeast Asia"
  # RENAMABLE: No (Azure defines region names).
  # Changing this triggers a full destroy + recreate of resources.
}

variable "project_name" {
  description = "A prefix for naming consistency"
  type        = string
  default     = "sock-lab"
  # RENAMABLE: Yes, keep it short.
}

variable "environment" {
  description = "Environment stage (prod, dev, staging)."
  type        = string
  default     = "prod"
  # RENAMABLE: Yes. Used in tagging and naming.
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}

# SECRET VARIABLES 

variable "admin_ssh_key_path" {
  description = "Path to local public key."
  type        = string
}

variable "my_home_ip" {
  description = "Specialized IP for SSH access."
  type        = string
}
