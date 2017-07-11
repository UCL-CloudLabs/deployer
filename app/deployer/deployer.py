import os
from .host import Host
from python_terraform import Terraform
from flask import render_template
from jinja2 import TemplateNotFound


class Deployer:
    '''
    Deploys a VM on an Azure subscription using a tenant ID and secret stored
    on the machine running this app. The needed variables can be found on
    Azure's portal:
     * AZURE_TENANT_ID: 'cloudlabs' Azure Active Directory tenant id.
     * AZURE_CLIENT_ID: 'cloudlabs' Azure AD Application Client ID.
     * AZURE_CLIENT_ID: with your Azure AD Application Secret.
     * AZURE_SUBSCRIPTION_ID: UCL RSDG's Azure subscription ID.
    TODO: For now these are stored in variables.tf, but they'll be moved to an
    Azure key vault.
    '''
    def __init__(self, instance_path):
        '''
        Find app's root path based in instance path.
        Set python-terraform's instance with appropriate full path working dir.
        '''
        self.app_path = os.path.join(instance_path.split(os.path.sep)[:-1])
        self.tf_path = os.path.join(
                            [self.app_path, "app", "deployer", "terraform"])
        self.tf = Terraform(working_dir=self.tf_path)

    def _render(self, host):
        '''
        Terraform's only possible target is a folder and not a file. So we
        need to save the rendered template on a tf file in the terraform
        folder.
        '''
        # Build full path to Terraform template
        template_path = os.path.sep.join(
                                [self.tf_path, "terraform-main.tf_template"])
        # try:
        rendered_template = render_template("terraform-main.tf_template",
                                            host=host)
        # except TemplateNotFound:
        #     print("Template terraform-main.tf_template not found in {}."
        #               .format(template_path))
        #     return
        #     # TODO raise?

        print(rendered_template)

        # try:
        with open("{}/terraform.tf".format(self.tf_path), "w") as f:
                f.write(rendered_template)
        # except:
        #     # TODO: replace with logging and maybe raise?
        #     print("Error writing terraform's config file.")

    def deploy(self, host):
        '''
        Renders the Terraform template with given user input.
        Then runs "terrraform apply" with appropriate template and displays
        message when it's done.
        '''
        # try:
        self._render(host)
        # except:
        #     # TODO: logging
        #     return "Error when rendering Terraform template."

        # TODO: Do something with the things apply returns.
        #       Any exceptions raised by python_terraform?
        return_code, stdout, stderr = self.tf.apply(capture_output=False)

        if return_code == 0:  # All went well
            return ("Deployed! You can now SSH to it as "
                    "{}@{}.ukwest.cloudapp.azure.com. "
                    "Your website is deployed at."
                    "http://{}.ukwest.cloudapp.azure.com:5000".format(
                                                                host.username,
                                                                host.dnsname,
                                                                host.dnsname))
        else:
            return ("Something went wrong with the deployment: {}".format(
                                                                        stderr
                                                                        )
                    )
