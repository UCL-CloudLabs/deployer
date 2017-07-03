# Deployer
This is a proof of concept that will deploy a VM in UCL RSDG's Azure
subscription given a series of parameters and a Dockerfile entered on a
web form .

In order to run this PoC you'll need to:

1. Clone this repo.
1. Make sure you have Python installed in your system.
1. Install project's requirements:
    `pip install -r requirements`
1. Set up the following env vars with relevant content:
    * AZURE_TENANT_ID
    * AZURE_CLIENT_ID
    * AZURE_CLIENT_SECRET
    * AZURE_SUBSCRIPTION_ID
1. Run the flask app:
    ```bash
    cd Deployer
    export FLASK_APP=run.py
    flask run
    ```
1. Open browser on URL returned by previous command.
