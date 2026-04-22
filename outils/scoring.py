def calculate_score(hibp_result, username_result, domain_result):
    """
    Calcule un score d'exposition numérique de 0 à 100 basé sur les résultats des modules HIBP, username et domain.

    :param hibp_result: (dict) Résultat de check_email() — contient "found", "fields", "sources"
    :param username_result: (dict) Résultat de check_email_username() — contient "platform_email_check"
    :param domain_result: (dict) Résultat de lookup_domain() — contient "is_free_provider"
    :return: (dict) Un dictionnaire contenant :
             - "score" (int) : score de 0 à 100
             - "level" (str) : "Faible", "Modéré", "Élevé" ou "Critique"
             - "détails" (tuple) : message + liste des éléments qui ont contribué au score

    >>> calculate_score({'found': 0, 'fields': [], 'sources': []}, {'platform_email_check': {'spotify': False, 'duolingo': False, 'firefox': False}}, {'is_free_provider': True})
    {'score': 0, 'level': 'Faible', 'détails': ('ce score est dû à', [])}

    >>> calculate_score({'found': 2, 'fields': ['password', 'phone'], 'sources': [{'name': 'LinkedIn', 'date': '2021-06'}]}, {'platform_email_check': {'spotify': True, 'duolingo': False, 'firefox': True}}, {'is_free_provider': False})
    {'score': 61, 'level': 'Élevé', 'détails': ('ce score est dû à', [...])}
    """
    d = {
        "score" : None,
        "level" : None,
        "détails" : None
    }
    score = 0
    détails = []
    score += 10* hibp_result["found"]
    for elem in hibp_result["fields"]:
        détails.append("votre " + elem + " à fuité")
        if elem == "password":
            score+= 15
        elif elem == "phone":
            score += 10
        elif elem == "address":
            score += 10
    for elem in hibp_result["sources"]:
        détails.append("une fuite viens de "+str(elem["name"]))
    if not domain_result["is_free_provider"]:
        détails.append("vous avez un email pro")
        score += 10
    for elem in username_result["platform_email_check"]:
        if username_result["platform_email_check"][elem]:
            détails.append("vous avez un compte chez " + str(elem))
            score += 8
    if score<25:
        d["level"] = "Faible"
    elif score < 50:
        d["level"] = "Modéré"
    elif score < 75:
        d["level"] = "Elevé"
    else:
        d["level"] = "Critique"
        if score > 100:
            score = 100
    d["score"] = score
    d["détails"] = "ce score est dû à", détails
    return d
    
    