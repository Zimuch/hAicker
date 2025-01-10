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
    vulnerabilita = [lambd * (n / r_i) / np.sqrt(a_i) if a_i > 0 else float("inf") for r_i, a_i in zip(celle, risorse)]
    return vulnerabilita

def calcola_danni_potenziali(celle, risorse, vulnerabilita):
    """
    Calcola i danni potenziali per ciascuna cella.

    :param celle: Lista o array dei ranking delle celle.
    :param risorse: Lista o array delle risorse allocate alle celle.
    :param vulnerabilita: Lista delle vulnerabilità delle celle.
    :return: Lista dei danni potenziali.
    """
    danni_potenziali = [r_i * (a_i / v_i) for r_i, a_i, v_i in zip(celle, risorse, vulnerabilita)]
    return danni_potenziali

def fitness_function1(risorse, lambd, alpha, beta):
    """
    Calcola la funzione di fitness per il sistema.

    :param risorse: Lista o array delle risorse allocate alle celle.
    :param lambd: Costante che determina il peso del ranking.
    :param alpha: Peso dei danni potenziali nella funzione di fitness.
    :param beta: Peso della vulnerabilità nella funzione di fitness.
    :return: Valore della funzione di fitness.
    """
    n = len(risorse)
    celle = list(range(1, n + 1))  # Ranking delle celle basato sull'indice (1, 2, ..., n)
    
    vulnerabilita = calcola_vulnerabilita(celle, lambd, risorse)
    danni_potenziali = calcola_danni_potenziali(celle, risorse, vulnerabilita)

    totale_danni = sum(danni_potenziali)
    totale_vulnerabilita = sum(vulnerabilita)

    # Funzione di fitness
    fitness = alpha * totale_danni + beta * totale_vulnerabilita

    return fitness


