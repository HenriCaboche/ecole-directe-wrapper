import requests
import json

# Session globale partagée
session = requests.Session()

heads = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
}

def get_gtk_cookie():
    url = "https://api.ecoledirecte.com/v3/login.awp"
    params = {"gtk": "1", "v": "4.75.0"}

    response = session.get(url, headers=heads, params=params)
    response.raise_for_status()

    gtk = session.cookies.get("GTK")
    if not gtk:
        raise Exception("GTK cookie non trouvé")
    gtk = gtk.replace("\r", "").replace("\n", "")
    heads["X-Gtk"] = gtk
    return gtk

def login(user_id, password):
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
    )
    response.raise_for_status()
    return response.json()

print(login())
