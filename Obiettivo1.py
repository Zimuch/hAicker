import numpy as np

def calcola_vulnerabilita(celle, lambd, risorse):
    """
    Calcola la vulnerabilità per ciascuna cella.

    :param celle: Lista o array dei ranking delle celle.
    :param lambd: Costante che determina il peso del ranking.
    :param risorse: Lista o array delle risorse allocate alle celle.
    :return: Lista delle vulnerabilità delle celle.
    """
    n = len(celle)
    print("Numero di celle: ", n)
    vulnerabilita = (n / (rankings[j] * (resources_allocated[j] ** 0.5)))
    print("Vulnerabilità: ", vulnerabilita)
    return vulnerabilita

def calcola_danni_potenziali(celle, risorse, vulnerabilita):
    """
    Calcola i danni potenziali per ciascuna cella.

    :param celle: Lista o array dei ranking delle celle.
    :param risorse: Lista o array delle risorse allocate alle celle.
    :param vulnerabilita: Lista delle vulnerabilità delle celle.
    :return: Lista dei danni potenziali.
    """
    danni_potenziali = [r_i * a_i / v_i for r_i, a_i, v_i in zip(celle, risorse, vulnerabilita)]
    print("Danni potenziali: ", danni_potenziali)
    return danni_potenziali

def obiettivo1_danni(risorse, lambd):
    """
    Calcola la funzione di fitness per il sistema.

    :param risorse: Lista o array delle risorse allocate alle celle.
    :param lambd: Costante che determina il peso del ranking.
    :return: Valore della funzione di fitness.
    """
    n = len(risorse)
    celle = list(range(1, n + 1))  # Ranking delle celle basato sull'indice (1, 2, ..., n)
    
    vulnerabilita = calcola_vulnerabilita(celle, lambd, risorse)
    danni_potenziali = calcola_danni_potenziali(celle, risorse, vulnerabilita)
    
    totale_danni = sum(danni_potenziali)
    print("Totale danni: ", totale_danni)

    # Funzione di fitness
    fitness = totale_danni 

    return fitness