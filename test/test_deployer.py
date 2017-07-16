from urllib.request import urlopen
from app.deployer.deployer import Deployer
from app.deployer.host import Host
from pathlib import Path
from haikunator import Haikunator


class TestDeployer:
    def setup_method(self):
        self.d = Deployer(Path('app').absolute())
        haiku = Haikunator()
        self.resource_name = haiku.haikunate(delimiter='', token_length=4)
        self.dnsname = haiku.haikunate(delimiter='', token_length=4)

    def test_deployer_config(self):
        assert self.d.tf_path == Path('app/deployer/terraform').absolute()

    def test_deployer(self):
        host = self._create_host()
        self.d.deploy(self.host)
        url = "http://{}.ukwest.cloudapp.azure.com:5000".format(self.dnsname)
        print('Checking if {} is live... '.format(url))
        print('Website returned code {}.'.format(urlopen(url).getcode()))
        assert 200 == urlopen(url).getcode()

    def teardown_method(self):
        # self.d.destroy(self.resource_name)
        self.d.destroy()

    def _create_host(self):
        username = 'testuser'
        passwd = 'Password123'
        # Read public key contents from encrypted file, ignore newline
        with open(Path('test/id_rsa_travis_azure.pub').absolute()) as f:
            public_key = f.read().rstrip('\n')
        # Path to private key
        private_key_path = Path('test/id_rsa_travis_azure').absolute()
        self.host = Host(name=self.resource_name, dnsname=self.dnsname,
                         username=username, passwd=passwd,
                         public_key=public_key,
                         private_key_path=private_key_path)
