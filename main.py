import requests
import json
import base64
import html
from getpass import getpass


#login

heads = {
            "User-Agent": "Mozilla 5.0/HTML, like gecko",
        }

def login():
    User_ID = input("user Id:")
    password = getpass("password")

    data = {
        "uuid": "",
        "identifiant": User_ID,
        "isRelogin": False,
        "motdepasse": password
    }

    response = requests.post("https://api.ecoledirecte.com/v3/login.awp?v=4.38.0",data={'data': json},headers=heads).text
    return response


print(login())