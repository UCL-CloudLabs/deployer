from app.deployer.deployer import Deployer
from pathlib import Path


class TestDeployer:
    def setup_method(self):
        self.d = Deployer(Path('../app').absolute())

    def test_deployer1(self):
        assert self.d.tf_path == Path('app/deployer/terraform').absolute()

    def teardown_method(self):
        pass
