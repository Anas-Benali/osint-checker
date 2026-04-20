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
    



