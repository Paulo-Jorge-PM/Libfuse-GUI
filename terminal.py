from getpass import getpass

user = False

print("==MEI Ultra Filesystem==\n\r")
print("Please login before proceeding:\n\r\n\r")

def check_login(username,password):
    return True

while user == False:
    username = input("Input your username:")
    password = getpass("Input your Password:")
    check = check_login(username,password)
    if check == True:
        print("\n\rCorrect login! Welcome!\n\r\n\r")
        user="xx"
    else:
        print("\n\rWrong login, please try again:\n\r\n\r")
    
    
