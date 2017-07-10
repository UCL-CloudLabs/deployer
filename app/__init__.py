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
                                name=form.name.data,
                                dnsname=form.dnsname.data,
                                username=form.username.data,
                                passwd=form.passwd.data,
                                public_key=form.public_key.data))
    return render_template('deploy_options.html', form=form)

@app.route('/deploy/<name>/<dnsname>/<username>/<passwd>/<public_key>')
def deploy_vm(name, dnsname, username, passwd, public_key):
    '''
    Deploy machine on Azure based on user info from deploy form.
    '''
    deployer = Deployer(app.instance_path)
    return render_template('deploy_vm.html',
                           deployer=deployer,
                           name=name,
                           dnsname=dnsname,
                           username=username,
                           passwd=passwd,
                           public_key=public_key)
