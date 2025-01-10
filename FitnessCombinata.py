import numpy as np

def calcola_vulnerabilita(rankings, lambda_value, resources):
    n = len(rankings)
    return [
        lambda_value * (n / rank) / np.sqrt(resource) if resource > 0 else float("inf")
        for rank, resource in zip(rankings, resources)
    ]

def calcola_danni(rankings, resources, vulnerabilities):
    return [rank * resource * vulnerability for rank, resource, vulnerability in zip(rankings, resources, vulnerabilities)]

def fitness_combinata(individual, risorse_totali, omega1, omega2, lambda_value):
    """
    Funzione di fitness combinata che utilizza la formula fornita.

    :param individual: Lista delle risorse allocate ai punti vulnerabili (a_i)
    :param risorse_totali: Valore totale delle risorse disponibili (A)
    :param omega1: Peso associato alla minimizzazione del costo (C)
    :param omega2: Peso associato alla massimizzazione della distribuzione pesata (W)
    :param lambda_value: Valore di lambda per la funzione di vulnerabilità
    :return: Valore della funzione di fitness combinata
    """
    resources = individual[1:]  # Ignorare la prima cella
    n = len(resources)
    
    # Calcolo del costo relativo C
    somma_allocazioni = np.sum(resources)  # Somma delle risorse allocate
    costo_relativo = somma_allocazioni / risorse_totali  # Costo C, valori più bassi sono migliori
    
    # Calcolo del ranking di vulnerabilità basato sull'indice della cella
    rankings = np.arange(1, n + 1)  # Indici da 1 a n
    
    # Calcolo di P_i e W
    if somma_allocazioni > 0:
        p_i = (resources * rankings) / somma_allocazioni  # P_i per ogni punto
        w = np.sum(p_i)  # Somma globale W
    else:
        w = 0  # Se nessuna risorsa è allocata, W è 0
    
    # Calcolo della vulnerabilità
    vulnerabilities = calcola_vulnerabilita(rankings, lambda_value, resources)
    
    # Calcolo dei danni potenziali
    danni_potenziali = calcola_danni(rankings, resources, vulnerabilities)
    dt = np.sum(danni_potenziali)  # Somma dei danni potenziali Dt
    
    # Funzione di fitness combinata
    fitness = omega1 * costo_relativo + omega2 * w + (1 - omega1 - omega2) * dt

    # Stampa del valore della funzione di fitness calcolato
    print(f"Fitness Score per Individuo : {fitness}")
    
    return fitness