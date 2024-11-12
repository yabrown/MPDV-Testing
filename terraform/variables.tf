variable "vultr_api_key" {
  description = "Vultr API Key"
  type        = string
  sensitive   = true
  default =     "YOUR_VULTR_API_KEY_HERE"
}

variable "ssh_key_id" {
  description = "SSH Key ID with which to set up privisioned servers"
  type        = string
  sensitive   = true
  default =     "YOUR_SSH_KEY_ID_HERE"
}