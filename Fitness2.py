def fitness_function2(individual, lambda_value, omega1, omega2):
    """
    Calcola il punteggio fitness di un individuo.

    Args:
        individual: Lista di risorse allocate per ogni ranking, dove individual[0] rappresenta il totale di risorse.
        lambda_value: Valore di correzione per la vulnerabilità.

    Returns:
        Punteggio fitness calcolato.
    """
    # Risorse totali disponibili (prima cella dell'individuo)
    total_resources = individual[0]

    # Risorse allocate per ogni cella, eccetto la prima
    resources_allocated = individual[1:]

    # Ranking: indice + 1 (la cella 1 ha ranking più alto, la cella n ha ranking più basso)
    rankings = list(range(1, len(resources_allocated) + 1))

    # Risorse totali allocate
    total_allocated = sum(resources_allocated)

    # Obiettivo 1: Costo relativo
    if total_resources > 0:  # Prevenire divisione per zero
        C = total_allocated / total_resources
    else:
        C = 1  # Se nessuna risorsa è disponibile, il costo è massimo

    # Obiettivo 2: Distribuzione pesata
    distribution_weight = 0
    for i in range(len(rankings)):
        if rankings[i] > 0 and resources_allocated[i] > 0:
            vulnerability_corrected = lambda_value * (len(rankings) / (rankings[i] * (resources_allocated[i] ** 0.5)))
            weight = resources_allocated[i] / total_allocated if total_allocated > 0 else 0
            distribution_weight += weight * rankings[i] / vulnerability_corrected

    # Funzione di fitness: bilanciamento tra i due obiettivi
    fitness = omega1 * C + omega2 * distribution_weight


    return fitness
