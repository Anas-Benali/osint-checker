def parse_email(email):
    """
    Parse un email et en extrait les composants principaux.

    :param email: (str) L'adresse email à analyser
    :return: (dict) Un dictionnaire contenant les clés suivantes :
             - "mail" (str) : l'email original
             - "name" (str) : la partie avant le @
             - "domain" (str) : la partie après le @
             - "is_valid" (bool) : True si l'email est valide, False sinon

    Exemples :

    >>> parse_email("john.doe@gmail.com")
    {'mail': 'john.doe@gmail.com', 'name': 'john.doe', 'domain': 'gmail.com', 'is_valid': True}

    >>> parse_email("contact@entreprise.org")
    {'mail': 'contact@entreprise.org', 'name': 'contact', 'domain': 'entreprise.org', 'is_valid': True}

    >>> parse_email("emailsansarobase")
    {'mail': 'emailsansarobase', 'name': '', 'domain': 'emailsansarobase', 'is_valid': False}

    >>> parse_email(12345)
    Traceback (most recent call last):
        ...
    AssertionError : email doit etre un str
    """
    assert isinstance(email,str),'email doit etre un str'
    dict = {}
    arobase = email.find("@")
    username = email[:arobase]
    domaine = email[arobase+1:]
    valide = True

    if arobase == -1:
        valide = False
    elif ".com" not in email and ".org" not in email and ".net" not in email:
        valide = False
    
    dict["mail"] = email
    dict["name"] = username
    dict["domain"] = domaine 
    dict["is_valid"] = valide

    return dict
