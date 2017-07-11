# Deployer
This is a proof of concept that will deploy a VM in UCL RSDG's Azure
subscription given a series of parameters and a Dockerfile entered on a
web form .

In order to run this PoC you'll need to:

1. Clone this repo.
1. Make sure you have Python3 installed in your system.
1. Install project's requirements:
    `pip install -r requirements`
1. You'll need `variables.tf`, a Terraform file containing the values of the cloud provider secrets needed to access your subscription. See [Terraform's sample for AWS](https://www.terraform.io/intro/getting-started/variables.html#using-variables-in-configuration).
1. Set up the following env vars for Flask WTForms' CSRF configuration to a value of your choice:
    * CSRF_SESSION_KEY
    * CSRF_SECRET_KEY
1. Run the flask app:
    ```bash
    cd Deployer
    export FLASK_APP=run.py
    flask run
    ```
1. Open browser on URL returned by previous command and input parameters to deploy a sample webapp on your cloud subscription.
1. The details to ssh into the machine and browse your website will appear after a successful deployment. 
