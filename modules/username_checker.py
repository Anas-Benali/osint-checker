import hashlib
import requests
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
        



