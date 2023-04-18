import digitalocean

TOKEN="dop_v1_97a246562ed5172e8c7d35fffdf47fb40c6b2ec1029f72d5992f7f960a33f7c3"
domain = digitalocean.Domain(token=TOKEN, name="manoriarealestate.com")
IP = "196.188.137.145"


def createsubdomain(name, port):
    new_record =  domain.create_new_domain_record(type='A',name=name,data=IP, port=port)

    if new_record['domain_record']:
        return True
    else:
        return False

