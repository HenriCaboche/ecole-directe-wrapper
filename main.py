import requests
import json
import base64
import time

# Session globale partagée
session = requests.Session()

heads = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

def get_gtk_cookie():
    url = "https://api.ecoledirecte.com/v3/login.awp"
    params = {"gtk": "1", "v": "4.75.0"}

    # Requête GET avec la session globale
    response = session.get(url, headers={"User-Agent": heads["User-Agent"]}, params=params)
    response.raise_for_status()

    # Affiche tous les cookies reçus

    gtk = session.cookies.get("GTK")
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
        proposition[i] =proposition[i].decode('unicode_escape').encode('latin1').decode('utf8')

    question = question.decode('unicode_escape').encode('latin1').decode('utf8')
    return (question,proposition)

def final_login(answer, UID, password) -> bool:
    get_gtk_cookie()
    encoded_answer = base64.b64encode(answer.encode()).decode()
    data = f'data={{"choix":"{encoded_answer}"}}'
    
    # Double auth réponse
    req = session.post(
        url='https://api.ecoledirecte.com/v3/connexion/doubleauth.awp?verbe=post',
        headers=heads,
        data=data
    ).json()
    

    cn = req['data']['cn']
    cv = req['data']['cv']

    # Re-login final avec cn/cv
    login_data = {
        "uuid": "",
        "identifiant": UID,
        "isRelogin": False,
        "motdepasse": password,
        "fa": [
            {
                "cn": cn,
                "cv": cv
            }
        ]
    }

    json_login = json.dumps(login_data)

    # Important: retirer ancien X-Token s'il existe
    if "X-Token" in heads:
        del heads["X-Token"]

    final_resp = session.post(
        "https://api.ecoledirecte.com/v3/login.awp?v=4.75.0",
        headers=heads,
        data={"data": json_login}
    ).json()

    print("FINAL LOGIN:", final_resp)

    if final_resp["code"] == 200:
        token = final_resp["token"]
        heads["X-Token"] =token
        return True
    else:
        raise Exception(f"Erreur finale login: {final_resp['message']}")

if __name__ == "__main__":
    try:
        print(second_auth("Gabvas","Gab+2803"))
        answer= input("answer:  ")
        final_login(answer,"Gabvas","Gab+2803")
        time.sleep(1000)
    except Exception as e:
        print(e)
        input()