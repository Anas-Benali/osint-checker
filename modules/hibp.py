import requests
def check_email(mail):
    """
    Vérifie si un email apparaît dans des fuites de données via l'API publique LeakCheck.

    :param mail: (str) L'adresse email à vérifier
    :return: (dict) Un dictionnaire contenant :
             - "found" (int) : le nombre de fuites trouvées
             - "fields" (list) : les types de données exposées
             - "sources" (list) : la liste des sources, chaque source est un dict avec "name" et "date"

    >>> check_email("example@example.com")
    {'found': 3, 'fields': ['username', 'first_name', 'address'], 'sources': [...]}

    >>> check_email("emailquinexistepas@domaineinconnu123.com")
    {'found': 0, 'fields': [], 'sources': []}

    >>> check_email(12345)
    Traceback (most recent call last):
        ...
    AssertionError: mail doit être un str
    """
    assert isinstance(mail,str),'mail doit être un str'
    d = {}
    url = "https://leakcheck.io/api/public?check=" + mail
    response_api = requests.get(url).json()
    if not response_api["success"]:
        d["found"] = 0
        d["fields"] = []
        d["sources"] = []
    else:
        d["found"] = response_api["found"]
        d["fields"] = response_api["fields"]
        d["sources"] = response_api["sources"]
    return d
