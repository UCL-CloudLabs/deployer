# Deployer
This is a proof of concept that will deploy a VM in UCL RSDG's Azure
subscription given a series of parameters and a Dockerfile entered on a
web form .

In order to run this PoC you'll need to:

1. Clone this repo.
1. Make sure you have Python3 installed in your system.
1. Install Terraform following [these instructions](https://www.terraform.io/intro/getting-started/install.html). I'm on a Mac, so I had to:
    1. Download appropriate zip (in my case version 0.9.11)
    1. Unzip and extract binary.
    1. Modify PATH so it points to terraform's binary.
1. Install project's requirements:
    `pip install -r requirements.txt`
1. You'll need `variables.tf`, a Terraform file containing the values of the cloud provider secrets needed to access your subscription. There's a template of this file in [app/deployer/terraform/samples](app/deployer/terraform/samples). You'll need to place this file once it's filled in with appropriate details in `Deployer/app/deployer/terraform/variables.tf`.
1. Set up the following env vars for Flask WTForms' CSRF configuration with a value of your choice:
    * CSRF_SESSION_KEY
    * CSRF_SECRET_KEY
1. Run the flask app:
    ```bash
    cd Deployer
    export FLASK_APP=run.py
    flask run
    ```
1. Open browser on URL returned by previous command and input parameters to deploy a sample webapp on your cloud subscription. E.g.
    * hostname: "mywebserver"
    * domain prefix: "mywebapp"
    * username: "MyUsername"
    * password: "MyPasswd1234"
    * public key: "ssh-rsa ..."
1. The details to ssh into the machine and browse your website will appear after a successful deployment.
