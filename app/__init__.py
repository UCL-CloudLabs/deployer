from flask import Flask, render_template, redirect, url_for
from .forms.DeployForm import DeployForm
from .deployer.deployer import Deployer

# Create Flask app
app = Flask(__name__)

# Configure Flask app
app.config.from_object('config')

@app.route('/', methods=['POST', 'GET'])
def show_deploy_options():
    '''
    Present form for user to fill in with information to deploy a VM on Azure.
    '''
    form = DeployForm()
    if form.validate_on_submit():
        return redirect(url_for('deploy_vm',
                                vm_name=form.vm_name.data,
                                username=form.username.data))
    return render_template('deploy_options.html', form=form)

@app.route('/deploy/<vm_name>/<username>')
def deploy_vm(vm_name, username):
    '''
    Deploy machine on Azure based on user info from deploy form.
    '''
    deployer = Deployer()
    return render_template('deploy_vm.html',
                           deployer=deployer,
                           vm_name=vm_name,
                           username=username)
