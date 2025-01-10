import numpy as np

def fitness_function_2(popolazione, risorse_totali, omega1, omega2):
    """
    Funzione di fitness aggiornata per minimizzare il costo C e la distribuzione pesata W.
    
    :param allocazioni: Lista delle risorse allocate ai punti vulnerabili (a_i)
    :param risorse_totali: Valore totale delle risorse disponibili (A)
    :param omega1: Peso associato alla minimizzazione del costo (C)
    :param omega2: Peso associato alla massimizzazione della distribuzione pesata (W)
    :return: Valore della funzione di fitness minimizzabile
    """
    # Calcolo del costo relativo C
    somma_popolazione = np.sum(popolazione)  # Somma delle risorse allocate
    costo_relativo = somma_popolazione / risorse_totali  # Costo C, valori più bassi sono migliori
    
    # Calcolo del ranking di vulnerabilità basato sull'indice della cella
    ranking_vulnerabilita = np.arange(1, len(popolazione) + 1)  # Indici da 1 a n
    
    # Calcolo di P_i e W
    if somma_popolazione > 0:
        p_i = (popolazione * ranking_vulnerabilita) / somma_popolazione  # P_i per ogni punto
        w = np.sum(p_i)  # Somma globale W
    
    # Funzione di fitness
    fitness = omega1 * costo_relativo - omega2 * w
    return fitness
