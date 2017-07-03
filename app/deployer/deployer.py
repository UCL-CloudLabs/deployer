import os

class Deployer:
    '''
    Deploys a VM on an Azure subscription using a tenant ID and secret stored
    on the machine running this app. The needed env vars can be found on
    Azure's portal:
     * AZURE_TENANT_ID: 'cloudlabs' Azure Active Directory tenant id.
     * AZURE_CLIENT_ID: 'cloudlabs' Azure AD Application Client ID.
     * AZURE_CLIENT_ID: with your Azure AD Application Secret.
     * AZURE_SUBSCRIPTION_ID: UCL RSDG's Azure subscription ID.
    '''
    def __init__(self):
        self.env = self.load_env_vars()
        self.ssh_key = self.load_ssh_key()

    def load_env_vars(self):
        '''
        Load Azure's env vars from local environment.
        '''
        env = {}
        for var in ['AZURE_TENANT_ID', 'AZURE_CLIENT_ID',
                    'AZURE_CLIENT_SECRET', 'AZURE_SUBSCRIPTION_ID']:
            try:
                env[var] = os.environ[var]
            except KeyError:
                print("Environmental variable {} not found. Please set it up "
                      "with the relevant value found in Azure's portal.")
        return env

    def load_ssh_key(self):
        '''
        User's default SSH keys. Needed to be able to configure the machine
        for loging in.
        '''
        return os.path.expanduser('~/.ssh/id_rsa.pub')

    def deploy(self):
        '''
        Deploy machine with given parameters on Azure.
        '''
        return "Deploying... "
