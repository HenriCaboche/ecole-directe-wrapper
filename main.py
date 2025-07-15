import requests
import json
import base64

# Session globale partagée
session = requests.Session()

heads = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

def get_gtk_cookie():
    url : str ="https://api.ecoledirecte.com/v3/login.awp"
    params = {"gtk": "1", "v": "4.75.0"}

    response = session.get(url, headers=heads, params=params)
    response.raise_for_status()

    gtk :str = session.cookies.get("GTK")
    if not gtk:
        raise Exception("GTK cookie non trouvé")
    gtk = gtk.replace("\r", "").replace("\n", "")
    heads["X-Gtk"] = gtk
    return gtk

def login(user_id=str, password=str):
    get_gtk_cookie()
    data = {
        "identifiant": user_id,
        "motdepasse": password,
        "uuid": "",
        "isRelogin": False
    }
    json_data = json.dumps(data)


    response = session.post(
        "https://api.ecoledirecte.com/v3/login.awp?v=4.75.0",
        headers=heads,
        data={"data": json_data}
    ).json()
    token = response["token"]

    heads["X-Token"] = token

def second_auth(UID, Password) -> tuple[str,list[str]]:
    login(UID,Password)
    data: str = "data={}"  
    response : str = requests.post(url="https://api.ecoledirecte.com/v3/connexion/doubleauth.awp?verbe=get",headers=heads,data=data)
    response = response.json()
    question: str = base64.b64decode(response["data"]["question"])

    proposition : list = []
    for i in range(len(response["data"]["propositions"])):
        proposition.append(base64.b64decode(response["data"]["propositions"][i]))
    return (question,proposition)
print(second_auth("Gabvas","Gab+2803"))
