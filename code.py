import random

user = ""

class Auth:
    pass

#CODE
#GENERATE AND SAVE
def send_code(user):
    generate_code()
    #sendo to e-mail
    return True
    
def generate_code():
    code = ""
    check = False
    while check == False:
        code = random.sample(range(1, 100), 5)
        check = check_if_code_unique(code)
    save_code(code, user)
    
def check_if_code_unique(code):
    return True

def save_code(code, user):
    return True
    

    
#RECEIVE AND CONFIRM
def check_code():
    pass
    
    