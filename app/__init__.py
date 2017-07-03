from flask import Flask, render_template
from .forms.DeployForm import DeployForm
from .deployer.deployer import Deployer

# Create Flask app
app = Flask(__name__)

# Configure Flask app
app.config.from_object('config')

@app.route('/')
def show_deploy_options():
    '''
    Present form for user to fill in with information to deploy a VM on Azure.
    '''
    form = DeployForm()
    return render_template('deploy_options.html', form=form)

@app.route('/deploy/<vm_name>')
def deploy_vm(vm_name):
    '''
    Deploy machine on Azure based on user info from deploy form.
    '''
    deployer = Deployer()
    return render_template('deploy_vm.html',
                           deployer=deployer,
                           vm_name=vm_name)
