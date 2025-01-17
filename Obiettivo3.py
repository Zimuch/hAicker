from Obiettivo1 import obiettivo1_danni
from Obiettivo2 import obiettivo2_costo

def obiettivo3_distribuzione(individual, lambda_value, lambda_value2):
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

    # Somma Vulnerabilità
    total_vulnerability = sum(
    lambda_value * (len(rankings) / (rankings[j] * (resources_allocated[j] ** 0.5)))
    for j in range(len(rankings))
    if rankings[j] > 0 and resources_allocated[j] > 0
    )

    # Obiettivo 3: Distribuzione pesata
    distribution_weight = 0
    for i in range(len(rankings)):
        if rankings[i] > 0 and resources_allocated[i] > 0:
            weight = resources_allocated[i] / total_allocated if total_allocated > 0 else 0
            distribution_weight += (weight * (resources_allocated[i] / rankings[i])) / total_vulnerability

    #Normalizza il valore di k rispetto alla media degli altri due obiettivi
    k = 10
    
    # Funzione di fitness: Distribuzione pesata
    fitness = distribution_weight * k

    return fitness
