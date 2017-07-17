import requests
from time import sleep
from pathlib import Path
from haikunator import Haikunator
from app.deployer.deployer import Deployer
from app.deployer.host import Host


class TestDeployer:
    '''
    Test the app's Deployer class.
    '''
    def setup_method(self):
        '''
        Before tests, create random name of resource groups and url prefix.
        '''
        self.d = Deployer(Path('app').absolute())
        self.resource_name = self._haikunate()
        self.dnsname = self._haikunate()

    def test_deployer_config(self):
        '''
        Check the path where the terraform files are is setup correctly.
        '''
        assert self.d.tf_path == Path('app/deployer/terraform').absolute()

    def test_deployer(self):
        '''
        Create a test host with made up parameters, deploy on azure and ping.
        '''
        self.d.deploy(self._create_host())
        # Wait for 10 secs so we make sure app has had the time to be deployed.
        sleep(10)
        # Sample URL is exposing the webapp on port 5000
        url = "http://{}.ukwest.cloudapp.azure.com:5000".format(self.dnsname)
        # Check website is live
        response = requests.get(url)
        assert 200 == response.status_code

    def teardown_method(self):
        '''
        Destroy test resources.
        TODO: Destroy self.resource_name instead
        '''
        self.d.destroy()


    def _haikunate(self, delimiter=''):
        '''
        Helper method to create random strings to use on the Terraform file.
        '''
        haiku = Haikunator()
        return haiku.haikunate(delimiter=delimiter, token_length=3)

    def _create_host(self):
        '''
        Helper method to create a VM with randome username/passwd and test
        SSH keys.
        '''
        # Make up username/passwd within Azure restrictions
        username = self._haikunate()
        passwd = self._haikunate('!')

        # Read public key contents from encrypted file, ignore newline
        with open(Path('test/id_rsa_travis_azure.pub').absolute()) as f:
            public_key = f.read().rstrip('\n')

        # Path to private key
        private_key_path = Path('test/id_rsa_travis_azure').absolute()
        return Host(name=self.resource_name, dnsname=self.dnsname,
                         username=username, passwd=passwd,
                         public_key=public_key,
                         private_key_path=private_key_path)
