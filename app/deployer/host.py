class Host:
    '''
    Contains all variables introduced by the user used to create a VM in Azure.
    '''
    def __init__(self, name=None, dnsname=None, username=None, passwd=None,
                 public_key=None, private_key_path=None):
        self.name = name
        self.dnsname = dnsname
        self.username = username
        self.passwd = passwd
        self.public_key = public_key
        self.private_key_path = private_key_path
