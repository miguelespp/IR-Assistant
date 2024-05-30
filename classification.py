def classify(requirement):
    functional_keywords = ['función', 'operación', 'ejecución', 'proceso', 'debe', 'necesita']
    non_functional_keywords = ['rendimiento', 'seguridad', 'usabilidad', 'fiabilidad', 'rapido', ]

    requirement = requirement.lower()

    for keyword in functional_keywords:
        if keyword in requirement:
            return 'RF'

    for keyword in non_functional_keywords:
        if keyword in requirement:
            return 'RNF'

    return 'No Clasificado'
