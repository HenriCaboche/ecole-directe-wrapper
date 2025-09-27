import requests
import json
import base64
import re
import datetime

session = requests.Session()

heads = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

def get_gtk_cookie():
    url = "https://api.ecoledirecte.com/v3/login.awp"
    params = {"gtk": "1", "v": "4.75.0"}

    response = session.get(url, headers={"User-Agent": heads["User-Agent"]}, params=params)
    response.raise_for_status()


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
    response = session.post(url="https://api.ecoledirecte.com/v3/connexion/doubleauth.awp?verbe=get",headers=heads,data=data)  
    if response.status_code == 200:
        
        response = response.json()
    else:
        return False

    question: str = base64.b64decode(response["data"]["question"])

    proposition : list = []
    for i in range(len(response["data"]["propositions"])):
        proposition.append(base64.b64decode(response["data"]["propositions"][i]))
        proposition[i] =proposition[i].decode('unicode_escape').encode('latin1').decode('utf8')

    question = question.decode('unicode_escape').encode('latin1').decode('utf8')
    return (question,proposition)

def final_login(answer, UID, password) -> tuple:
    get_gtk_cookie()
    encoded_answer = base64.b64encode(answer.encode()).decode()
    data = f'data={{"choix":"{encoded_answer}"}}'

    req = session.post(
        url='https://api.ecoledirecte.com/v3/connexion/doubleauth.awp?verbe=post',
        headers=heads,
        data=data
    ).json()
    

    cn = req['data']['cn']
    cv = req['data']['cv']

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



    final_resp = session.post(
        "https://api.ecoledirecte.com/v3/login.awp?v=4.75.0",
        headers=heads,
        data={"data": json_login}
    ).json()
    if final_resp["code"] == 200:
        token = final_resp["token"]
        heads["X-Token"] = token  
        return (True,final_resp["data"]["accounts"][0]["id"],token)
    else:
        return (False)
    
def notes(id,token):
    print(heads)
    data={'token':token,
    "anneeScolaire": ""}
    jsond = json.dumps(data)
    req = session.get(f"https://api.ecoledirecte.com/v3/eleves/{id}/notes.awp?verbe=get",headers=heads,data={'data': jsond}).json() 
    return req

def homework(id,token):

    print(token)
    data= {
}

    jsond = json.dumps(data)
    req = session.post(f"https://api.ecoledirecte.com/v3/Eleves/{id}/cahierdetexte.awp?verbe=get",headers=heads,data={'data': jsond}).json()
    dates = list(req["data"].keys())
    print(dates)
    data = []
    homework = []
    for day in dates:
        print(day)
        req = session.post(f"https://api.ecoledirecte.com/v3/Eleves/{id}/cahierdetexte/{day}.awp?verbe=get",headers=heads,data={'data': jsond}).json()
        data=(req["data"]["matieres"])
        for e in data:
            day_keys=e.keys()
            if 'aFaire' in day_keys:
                homework.append(f'{e["matiere"]} -- {e["nomProf"]}')
                homework.append(f'\n\n { re.sub(r"<.*?>", "",base64.b64decode(e["aFaire"]["contenu"]).decode("unicode_escape").encode("latin1").decode("utf8"))}\n\n\n-------------')
            else:
                break
    return homework
    

def timetable(id,token):
    x = str(datetime.datetime.now()).split()
    print(x[0])
    datefin = int(x[0].split("-")[2])+4
    datefin = x[0].split("-")[0]+"-"+x[0].split("-")[1]+"-"+str(datefin)
    print(datefin)
    data={'token':token,
        "dateDebut": x[0],
        "dateFin": datefin,
        "avecTrous": True}
    jsond = json.dumps(data)
    req = session.post(f"https://api.ecoledirecte.com/v3/E/{id}/emploidutemps.awp?verbe=get",headers=heads,data={'data': jsond}).json()
    previous_date = 0
    timetable  = []
    for x in range(len(req['data'])):
  
            horaire = req['data'][x]['start_date']
            horaire= str(horaire).split()
            horaire2 = req['data'][x]['end_date']
            horaire2= str(horaire2).split()

            if not horaire2[0] == previous_date:
                print("--------------")

            timetable(req['data'][x]['text'])
            timetable.append(horaire[1]+"--"+horaire2[1])
            previous_date = horaire2[0]
    return timetable



def callable(username,password,func):

        second_auth(username,password)
        answer= input("answer:  ")
        final = final_login(answer,username,password)
        token = final[2]
        id=final[1]
        if func == "homework":
            return homework(id,token)
        
callable("Gabvas","Gab+2803","homework")