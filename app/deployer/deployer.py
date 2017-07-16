import json
from .host import Host
from python_terraform import Terraform
from jinja2 import Template, TemplateNotFound, Environment, FileSystemLoader
from pathlib import Path


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
    def __init__(self, app_path=Path.cwd()):
        '''
        Set python-terraform's instance with appropriate full path working dir.
        '''
        p = Path(app_path, "deployer", "terraform")
        self.app_path = app_path
        self.tf_path = p.absolute()
        self.tf = Terraform(working_dir=self.tf_path)

    def _render(self, host):
        '''
        Terraform's only possible target is a folder and not a file. So we
        need to save the rendered template on a tf file in the terraform
        folder.
        '''
        # try:
        j2_env = Environment(loader=FileSystemLoader(str(self.tf_path)))
        rendered_template = j2_env.get_template(
                                    'terraform.tf_template').render(host=host)
        # # except TemplateNotFound:
        #     print("Template terraform-main.tf_template not found in {}."
        #               .format(template_path))
        #     return
        #     # TODO raise?

        print(rendered_template)

        # try:
        with open(Path(self.tf_path, "terraform.tf"), "w") as f:
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
            # TODO raise
            return ("Something went wrong with the deployment: {}".format(
                                                                        stderr
                                                                        )
                    )

    def destroy(self, resource=None):
        '''
        Deletes given Terraform resource.
        It has to make sure there is a Terraform state containing the resource
        that will be destroyed.
        After applying a plan, Terraform saves the state on
        "terraform.tfstate". This is a JSON file that contains the list of
        resources deployed and their status.
        '''
        tf_state = Path(self.tf_path, 'terraform.tfstate')

        if tf_state.exists():
            if resource:
                with open(tf_state) as f:
                    tf_data = json.load(f)
                try:
                    res_label = tf_data['modules'][0]['resources'][resource]
                except KeyError:
                    print("Resource not found in Terraform state. The "
                          "available resources for destroying are {}.".format(
                           ', '.join(
                             [r for r in tf_data['modules'][0]['resources']])))
                    # TODO raise
                    return
                return_code, stdout, stderr = self.tf.destroy(
                                                        res_label,
                                                        capture_output=False
                                                        )
            else:
                print("Destroying all resources...")
                return_code, stdout, stderr = self.tf.destroy(
                                                        capture_output=False)

            if return_code == 0:  # All went well
                return ("Resource {} destroyed successfully.".format(resource))
            else:
                # TODO raise
                return ("Something went wrong when destroying {}: {}".format(
                                                                    resource,
                                                                    stderr))
        else:
            print("Terraform state does not exist in {}".format(tf_state))

    def refresh(self):
        '''
        User Terraform to update the current state file against real resources.
        '''
        # First refresh state
        return_code, stdout, stderr = self.tf.refresh()

        if return_code == 0:  # All went well
            return ("Local Terraform state successfully updated.")
        else:
            # TODO raise
            return ("Something went wrong when updating state: {}".format(
                                                                       stderr))
