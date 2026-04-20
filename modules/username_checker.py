import hashlib
import requests
from outils.email_parser import parse_email
def hash_password(password):
    """
    Hache un mot de passe en SHA-1.

    :param password: (str) Le mot de passe à hacher
    :return: (str) Le hash SHA-1 en majuscules

    >>> hash_password("password")
    '5BAA61E4C9B93F3F0682250B6CF8331B7EE68FD8'

    >>> hash_password("")
    'DA39A3EE5E6B4B0D3255BFEF95601890AFD80709'

    >>> hash_password(12345)
    Traceback (most recent call last):
        ...
    AssertionError: password doit être un str
    """
    assert isinstance(password,str),'password doit etre un str'
    return hashlib.sha1(password.encode()).hexdigest()

def check_password(password):
    """
    Vérifie si un mot de passe a fuité via l'API HaveIBeenPwned Passwords.
    Utilise le k-anonymity : seuls les 5 premiers caractères du hash sont envoyés.

    :param password: (str) Le mot de passe à vérifier
    :return: (int) Le nombre de fois que le mot de passe a été trouvé dans des fuites, 0 si jamais vu

    >>> check_password("password")
    52256179

    >>> check_password("xK9$mL2#pQr7")
    0

    >>> check_password(12345)
    Traceback (most recent call last):
        ...
    AssertionError: password doit être un str
    """
    assert isinstance (password,str),'password doit etre un str'
    i=0
    password_hashed = hash_password(password)
    password_for_api = password_hashed.upper()
    url = "https://api.pwnedpasswords.com/range/" + password_for_api[:5]
    response_api = requests.get(url).text
    l = response_api.split("\n")
    t = []
    for elem in l:
        t.append(elem.split(":"))
    
    for elem in t:
        if elem[0] == password_for_api[5:]:
            i += int(elem[1])
    return i
        


def generate_username(mail):
    assert isinstance (mail,str),'mail doit etre un str'
    res = []
    separate = 0
    username = parse_email(mail)["name"]
    if "-" in username:
        separate = username.find("-")
    elif "." in username:
        separate = username.find(".")
    elif "_" in username:
        separate = username.find("_")
    
    if separate == 0:
        res.append(username)
    else:
        part1 = username[:separate]
        part2 = username[separate+1:]
        res.append(part1)
        res.append(part2)
        res.append(username)
        res.append(part1[0]+part2)
        res.append(part2[0]+part1)
        res.append(part1+part2[0])
        res.append(part2+part1[0])
        #avec un .
        res.append(part1[0]+"."+part2)
        res.append(part2[0]+"."+part1)
        res.append(part1+"."+part2[0])
        res.append(part2+"."+part1[0])
        res.append(part1+"."+part2)
        res.append(part2+"."+part1)
        #avec un _
        res.append(part1[0]+"_"+part2)
        res.append(part2[0]+"_"+part1)
        res.append(part1+"_"+part2[0])
        res.append(part2+"_"+part1[0])
        res.append(part1+"_"+part2)
        res.append(part2+"_"+part1)
        #avec un -
        res.append(part1[0]+"-"+part2)
        res.append(part2[0]+"-"+part1)
        res.append(part1+"-"+part2[0])
        res.append(part2+"-"+part1[0])
        res.append(part1+"-"+part2)
        res.append(part2+"-"+part1)
    return res

def check_username(username):
    """
    Vérifie l'existence d'un username sur plusieurs plateformes via leurs URLs de profil.
    Attention : certaines plateformes retournent 200 même si le profil n'existe pas.

    :param username: (str) Le nom d'utilisateur à vérifier
    :return: (dict) Un dictionnaire contenant :
             - "username" (str) : le username vérifié
             - "results" (dict) : un dictionnaire avec le nom de la plateforme comme clé et un booléen comme valeur

    >>> check_username("google")
    {'username': 'google', 'results': {'github': True, 'instagram': True, ...}}

    >>> check_username("usernamequisurementexistepas999999")
    {'username': 'usernamequisurementexistepas999999', 'results': {'github': False, ...}}

    >>> check_username(12345)
    Traceback (most recent call last):
        ...
    AssertionError: username doit être un str
    """
    assert isinstance (username,str),'username doit être un  str'
    d = {
        "username": username,
        "results":{}
    }
    reponse_instagram = requests.get("https://www.instagram.com/" + username)
    reponse_tiktok = requests.get("https://www.tiktok.com/@"+ username)
    reponse_x = requests.get("https://x.com/" + username) 
    reponse_reddit = requests.get("https://www.reddit.com/user/"+username)
    reponse_github = requests.get("https://github.com/"+username)
    reponse_youtube = requests.get("https://www.youtube.com/@"+username)
    reponse_linkedin = requests.get("https://www.linkedin.com/in/"+username)
    reponse_snapchat = requests.get("https://www.snapchat.com/add/"+username)
    reponse_twitch = requests.get("https://www.twitch.tv/"+username)
    reponse_steam = requests.get("https://steamcommunity.com/id/"+username)
    reponse_pinterest = requests.get("https://www.pinterest.com/"+username)
    t = [reponse_github,reponse_instagram,reponse_reddit,reponse_tiktok,reponse_x,reponse_youtube,reponse_linkedin,reponse_snapchat,reponse_twitch,reponse_instagram,reponse_pinterest,reponse_steam]
    for reponse in t:
        if reponse.status_code == 200:
            if "instagram" in reponse.url:
                d["results"]["instagram"] = True
            elif "tiktok" in reponse.url:
                d["results"]["tiktok"] = True
            elif "x" in reponse.url:
                d["results"]["x"] = True
            elif "reddit" in reponse.url:
                d["results"]["reddit"] = True
            elif "github" in reponse.url:
                d["results"]["github"] = True
            elif "youtube" in reponse.url:
                d["results"]["youtube"] = True
            elif "linkedin" in reponse.url:
                d["results"]["linkedin"] = True
            elif "snapchat" in reponse.url:
                d["results"]["snapchat"] = True
            elif "twitch" in reponse.url:
                d["results"]["twitch"] = True
            elif "steam" in reponse.url:
                d["results"]["steam"] = True
            elif "pinterest" in reponse.url:
                d["results"]["pinterest"] = True

        else:
            if "instagram" in reponse.url:
                d["results"]["instagram"] = False
            elif "tiktok" in reponse.url:
                d["results"]["tiktok"] = False
            elif "x" in reponse.url:
                d["results"]["x"] = False
            elif "reddit" in reponse.url:
                d["results"]["rediit"] = False
            elif "github" in reponse.url:
                d["results"]["github"] = False
            elif "youtube" in reponse.url:
                d["results"]["youtube"] = False
            elif "linkedin" in reponse.url:
                d["results"]["linkedin"] = False
            elif "snapchat" in reponse.url:
                d["results"]["snapchat"] = False
            elif "twitch" in reponse.url:
                d["results"]["twitch"] = False
            elif "steam" in reponse.url:
                d["results"]["steam"] = False
            elif "pinterest" in reponse.url:
                d["results"]["pinterest"] = False
    
    return d


    

def check_email_on_platform(email):
    """
    Vérifie si un email est enregistré sur plusieurs plateformes via leurs APIs publiques.

    :param email: (str) L'adresse email à vérifier
    :return: (dict) Un dictionnaire avec le nom de la plateforme comme clé et un booléen comme valeur

    >>> check_email_on_platform("email@gmail.com")
    {'spotify': True, 'duolingo': True, 'firefox': True}

    >>> check_email_on_platform("emailquinexistepas999999@gmail.com")
    {'spotify': False, 'duolingo': False, 'firefox': False}

    >>> check_email_on_platform(12345)
    Traceback (most recent call last):
        ...
    AssertionError: email doit être un str
    """
    assert isinstance (email,str),'email doit être un str'
    d = {
        "spotify" : False,
        "duolingo" : False,
        "firefox" : False
    }
    reponse_spotify = requests.get(
    "https://spclient.wg.spotify.com/signup/public/v1/account", 
    params={"validate": 1, "email": email})

    reponse_duolingo = requests.get( "https://www.duolingo.com/2017-06-30/users", params={"email": email}, headers={"User-Agent": "Mozilla/5.0"} )

    reponse_firefox = requests.post("https://api.accounts.firefox.com/v1/account/status",json={"email": email})
    if reponse_spotify.json()["status"] == 20:
        d["spotify"] = True

    if len(reponse_duolingo.json()["users"]) != 0:
        d["duolingo"] = True
    
    if reponse_firefox.json()["exists"]:
        d["firefox"] = True

    return d

def check_email_username(email):
    """
    Combine generate_username(), check_username() et check_email_on_platform()
    pour retourner une analyse complète de l'exposition d'un email.

    :param email: (str) L'adresse email à analyser
    :return: (dict) Un dictionnaire contenant :
             - "email" (str) : l'email analysé
             - "platform_email_check" (dict) : résultats de check_email_on_platform()
             - "usernames_checked" (list) : liste des résultats de check_username() pour chaque variante

    >>> check_email_username("john.doe@gmail.com")
    {'email': 'john.doe@gmail.com', 'platform_email_check': {...}, 'usernames_checked': [...]}

    >>> check_email_username(12345)
    Traceback (most recent call last):
        ...
    AssertionError: email doit être un str
    """
    assert isinstance (email,str),'email doit être un str'
    d = {
        "email" : email,
        "platform_email_check" :None,
        "usernames_checked" : None
    }
    temp = []
    for elem in generate_username(email):
        temp.append(check_username(elem))
    d["platform_email_check"] = check_email_on_platform(email)
    d["usernames_checked"] = temp
    return d
