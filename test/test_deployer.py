from app.deployer.deployer import Deployer
from app.deployer.host import Host
from pathlib import Path, PosixPath
from haikunator import Haikunator


class TestDeployer:
    def setup_method(self):
        self.d = Deployer(Path('app').absolute())
        haiku = Haikunator()
        self.resource_name = haiku.haikunate()

    def test_deployer_config(self):
        assert self.d.tf_path == Path('app/deployer/terraform').absolute()

    # def test_deployer(self):
    #     host = self._create_host()
    #     self.d.deploy(self.host)
    #     # ping machine? Get URL from state.
    #     assert self.d.tf_path == Path('app/deployer/terraform').absolute()

    def teardown_method(self):
        self.d.destroy(self.resource_name)

    def _create_host(self):
        haiku = Haikunator()
        dnsname = haiku.haikunate(delimiter='', token_length=10)
        username = 'testuser'
        passwd = 'Password123'
        public_key = 'ssh-rsa aaaaaa email@host.com'
        private_key_path = '~/.ssh/id_rsa'
        self.host = Host(name=self.resource_name, dnsname=dnsname,
                         username=username, passwd=passwd,
                         public_key=public_key,
                         private_key_path=private_key_path)
