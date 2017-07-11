from flask import Flask, render_template, redirect, url_for, request
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
        # Code 307 needed so all browsers use HTTP POST
        return redirect(url_for('deploy_vm'), code=307)
    return render_template('deploy_options.html', form=form)


@app.route('/deploy', methods=['POST'])
def deploy_vm():
    '''
    Deploy machine on Azure based on user info from deploy form.
    '''
    deployer = Deployer(app.instance_path)
    return render_template('deploy_vm.html',
                           deployer=deployer,
                           name=request.form['name'],
                           dnsname=request.form['dnsname'],
                           username=request.form['username'],
                           passwd=request.form['passwd'],
                           public_key=request.form['public_key'])
