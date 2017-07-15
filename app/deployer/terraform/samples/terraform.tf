# Configure Azure provider
provider "azurerm" {
  subscription_id = "${var.azure_subscription_id}"
  client_id       = "${var.azure_client_id}"
  client_secret   = "${var.azure_client_secret}"
  tenant_id       = "${var.azure_tenant_id}"
}

# create a resource group if it doesn't exist
resource "azurerm_resource_group" "rg" {
    name = "orangebreeze2189rg"
    location = "ukwest"
}

# create virtual network
resource "azurerm_virtual_network" "vnet" {
    name = "tfvnet"
    address_space = ["10.0.0.0/16"]
    location = "ukwest"
    resource_group_name = "${azurerm_resource_group.rg.name}"
}

# create subnet
resource "azurerm_subnet" "subnet" {
    name = "tfsub"
    resource_group_name = "${azurerm_resource_group.rg.name}"
    virtual_network_name = "${azurerm_virtual_network.vnet.name}"
    address_prefix = "10.0.2.0/24"
    #network_security_group_id = "${azurerm_network_security_group.nsg.id}"
}

# create public IPs
resource "azurerm_public_ip" "ip" {
    name = "tfip"
    location = "ukwest"
    resource_group_name = "${azurerm_resource_group.rg.name}"
    public_ip_address_allocation = "dynamic"
    domain_name_label = "royalmode2149"

    tags {
        environment = "staging"
    }
}

# create network interface
resource "azurerm_network_interface" "ni" {
    name = "tfni"
    location = "ukwest"
    resource_group_name = "${azurerm_resource_group.rg.name}"

    ip_configuration {
        name = "ipconfiguration"
        subnet_id = "${azurerm_subnet.subnet.id}"
        private_ip_address_allocation = "static"
        private_ip_address = "10.0.2.5"
        public_ip_address_id = "${azurerm_public_ip.ip.id}"
    }
}

# create storage account
resource "azurerm_storage_account" "storage" {
    name = "orangebreeze2189storage"
    resource_group_name = "${azurerm_resource_group.rg.name}"
    location = "ukwest"
    account_type = "Standard_LRS"

    tags {
        environment = "staging"
    }
}

# create storage container
resource "azurerm_storage_container" "storagecont" {
    name = "vhd"
    resource_group_name = "${azurerm_resource_group.rg.name}"
    storage_account_name = "${azurerm_storage_account.storage.name}"
    container_access_type = "private"
    depends_on = ["azurerm_storage_account.storage"]
}



# create virtual machine
resource "azurerm_virtual_machine" "vm" {
    name = "orangebreeze2189vm"
    location = "ukwest"
    resource_group_name = "${azurerm_resource_group.rg.name}"
    network_interface_ids = ["${azurerm_network_interface.ni.id}"]
    vm_size = "Standard_A0"

    storage_image_reference {
        publisher = "Canonical"
        offer = "UbuntuServer"
        sku = "16.04-LTS"
        version = "latest"
    }

    storage_os_disk {
        name = "myosdisk"
        vhd_uri = "${azurerm_storage_account.storage.primary_blob_endpoint}${azurerm_storage_container.storagecont.name}/myosdisk.vhd"
        caching = "ReadWrite"
        create_option = "FromImage"
    }

    os_profile {
        computer_name = "orangebreeze2189"
        admin_username = "testuser"
        admin_password = "Password123"
    }

    os_profile_linux_config {
      disable_password_authentication = false
      ssh_keys = [{
        path     = "/home/testuser/.ssh/authorized_keys"
        key_data = "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQDIjSk9W1iu8Nq01i0Ng/U4L+nFPHpU44czXqnY8I9+szOo8ZpbvaoC52hVFQRCmsGTiPhLJYzhUR90DGyXDC9+1tpybHrDO4VvabuLnae/8I2QkGbbrDPm3iNFgmx01N4odUwAn7bi5S49e0fSqnzJkNDNUXf+wtIpvgxxXM6rMBr3nWR/OYHvo1/ZGaFbtS9wKvQHn7fP8OmiJnCnfGCJfT2UylyRAjKb5D9PnrRSgsrWBbUGrwq7svuG+tNtRI+w97f//evKubyUGBNeaOSbtlhu7pPWDtvyCcYAWaRcAusdS4C9KClX/y/gvg4Zyrlh3/jSwLsY1gpZlHHWFjjSKpQz25FvGNJbGkYaVSzfHDUN3VSJZgJO5oX8W0tsYbDuKSBSADSP/D3BjJD11RhUXv0DSB9mhdXbemyVdS9QkBdBhJLxzQ8AVYwiXmTJRP99Y5AS0+UQJqO40u/aWkevUziWDfUj1uB+vylQDmg7qDDcG6ZDMX7EAcmRLhII+U/rc0QVRPQqYB+HC1fWKqyans/D0wgMvmfvjz0aohg97wbvQoldeZHbi/7wLHFFKtlDGiEJYPDR4iOHQQ4kG5ZRv5CYMI88km9rE9Ode2KqIKFRRgFfTJFzE52EpHMBcWcggK0Ua6+vaZ8SfKPg76JFnOluCIGQz+Z3BVDWR89yTQ== r.alegre@ucl.ac.uk"
      }]
    }

    connection {
        host = "royalmode2149.ukwest.cloudapp.azure.com"
        user = "testuser"
        type = "ssh"
        private_key = "${file("~/.ssh/id_rsa_unencrypt")}"
        timeout = "1m"
        agent = true
    }

    provisioner "remote-exec" {
        inline = [
          "sudo apt-get update",
          "sudo apt-get install docker.io -y",
          "git clone https://github.com/UCL-CloudLabs/Docker-sample.git",
          "cd Docker-sample",
          "sudo docker build -t hello-flask .",
          "sudo docker run -d -p 5000:5000 hello-flask"
        ]
    }

    tags {
        environment = "staging"
    }
}
