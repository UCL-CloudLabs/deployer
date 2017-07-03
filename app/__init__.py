from flask import Flask, render_template
from .forms.DeployForm import DeployForm

app = Flask(__name__)

app.config.from_object('config')

@app.route('/')
def show_deploy_options():
    form = DeployForm()
    return render_template('deploy_options.html', form=form)

@app.route('/deploy')
def deploy_vm():
    return render_template('deploy_vm.html')
