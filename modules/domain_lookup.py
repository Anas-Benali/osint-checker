import socket
import whois
FREE_PROVIDERS = [
    "gmail.com", "googlemail.com",
    "hotmail.com", "outlook.com", "live.com", "msn.com", "hotmail.fr",
    "outlook.fr", "live.fr", "hotmail.co.uk", "live.co.uk",
    "yahoo.com", "yahoo.fr", "yahoo.co.uk", "yahoo.de", "yahoo.es",
    "yahoo.it", "yahoo.com.br", "ymail.com",
    "icloud.com", "me.com", "mac.com",
    "protonmail.com", "proton.me", "tutanota.com", "tutamail.com",
    "mailfence.com", "fastmail.com", "fastmail.fm",
    "laposte.net", "orange.fr", "free.fr", "sfr.fr", "bbox.fr",
    "wanadoo.fr", "neuf.fr", "numericable.fr", "bouyguestelecom.fr",
    "aol.com", "mail.com", "gmx.com", "gmx.fr", "gmx.de",
    "zoho.com", "yandex.com", "yandex.ru", "mail.ru",
    "inbox.com", "rediffmail.com", "web.de", "libero.it",
    "tempmail.com", "guerrillamail.com", "mailinator.com",
    "throwam.com", "sharklasers.com", "trashmail.com"
]
def lookup_domain(domain):
    """
    Récupère les informations publiques sur un nom de domaine via WHOIS et DNS.

    :param domain: (str) Le nom de domaine à analyser (ex: "github.com")
    :return: (dict) Un dictionnaire contenant :
             - "domain" (str) : le domaine analysé
             - "registrar" (str | None) : l'organisme qui a enregistré le domaine
             - "creation_date" (str | None) : date de création au format JJ/MM/AAAA
             - "expiration_date" (str | None) : date d'expiration au format JJ/MM/AAAA
             - "country" (str | None) : pays d'enregistrement
             - "ip" (str | None) : adresse IP associée au domaine
             - "is_free_provider" (bool) : True si c'est un provider email gratuit connu

    >>> lookup_domain("github.com")
    {'domain': 'github.com', 'registrar': 'MarkMonitor, Inc.', 'creation_date': '09/10/2007', 'expiration_date': '09/10/2026', 'country': 'US', 'ip': '140.82.121.4', 'is_free_provider': False}

    >>> lookup_domain("gmail.com")
    {'domain': 'gmail.com', 'registrar': 'MarkMonitor, Inc.', 'creation_date': '13/08/1995', 'expiration_date': '12/08/2026', 'country': 'US', 'ip': '142.251.39.197', 'is_free_provider': True}

    >>> lookup_domain("domainequinexistepas999.com")
    {'domain': 'domainequinexistepas999.com', 'registrar': None, 'creation_date': None, 'expiration_date': None, 'country': None, 'ip': None, 'is_free_provider': False}

    >>> lookup_domain(12345)
    Traceback (most recent call last):
        ...
    AssertionError: domain doit être un str
    """
    assert isinstance(domain,str), 'domain doit être un str'
    d = {
        "domain" : domain,
        "registrar" : None,
        "creation_date" : None,
        "expiration_date" : None,
        "country" : None,
        "ip" : None,
        "is_free_provider" : False
    }
    if domain in FREE_PROVIDERS:
        d["is_free_provider"] = True
    try:
        d["ip"] = socket.gethostbyname(domain)
    except Exception:
        d["ip"] = None
    try:
        qui_cest = whois.whois(domain)
        d["registrar"] = qui_cest['registrar']
        d["country"] = qui_cest["country"]
        if type(qui_cest['creation_date']) is list:
            d["creation_date"] = qui_cest["creation_date"][0].strftime("%d/%m/%Y")
        else:
            d["creation_date"] = qui_cest["creation_date"].strftime("%d/%m/%Y")
        if type(qui_cest['expiration_date']) is list:
            d["expiration_date"] = qui_cest["expiration_date"][0].strftime("%d/%m/%Y")
        else:
            d["expiration_date"] = qui_cest["expiration_date"].strftime("%d/%m/%Y")
    except Exception:
        pass
    
    return d
    



