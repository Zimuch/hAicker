
def obiettivo2_costo(individual,LAMBDA_VALUE2):
    """
    Calcola il punteggio fitness di un individuo.

    
    Args:
        individual: Lista di risorse allocate per ogni ranking, dove individual[0] rappresenta il totale di risorse.
        lambda_value: Valore di correzione.

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
    C = total_resources - total_allocated

    # Funzione di fitness: Costo relativo
    fitness =  C * LAMBDA_VALUE2 

    return fitness
