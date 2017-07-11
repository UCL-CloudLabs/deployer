from flask import Flask, render_template, redirect, url_for, request
from .forms.deploy_form import DeployForm
from .deployer.deployer import Deployer
from .deployer.host import Host

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
        # Code 307 needed so all browsers use HTTP POST
        return redirect(url_for('deploy_vm'), code=307)
    return render_template('deploy_options.html', form=form)


@app.route('/deploy', methods=['POST'])
def deploy_vm():
    '''
    Deploy host on Azure based on user input from deploy form.
    '''
    deployer = Deployer(app.instance_path)
    host = Host(name=request.form['name'],
                dnsname=request.form['dnsname'],
                username=request.form['username'],
                passwd=request.form['passwd'],
                public_key=request.form['public_key'],
                private_key_path=request.form['private_key_path'])
    return render_template('deploy_vm.html',
                           deployer=deployer,
                           host=host)
