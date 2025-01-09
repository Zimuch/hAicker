import numpy as np

def calcola_vulnerabilita(celle, lambd, risorse):
    """
    Calcola la vulnerabilità di ciascuna cella.

    :param celle: Lista o array dei ranking delle celle.
    :param lambd: Costante che determina il peso del ranking.
    :param risorse: Lista o array delle risorse allocate alle celle.
    :return: Lista delle vulnerabilità delle celle.
    """
    n = len(celle)
    vulnerabilita = []
    for i, r_i in enumerate(celle):
        v_i = lambd * (n / r_i) * (1 / np.sqrt(risorse[i])) if risorse[i] > 0 else lambd * (n / r_i)
        vulnerabilita.append(v_i)
    return vulnerabilita

def calcola_danni_potenziali(celle, risorse, vulnerabilita):
    """
    Calcola i danni potenziali per ciascuna cella.

    :param celle: Lista o array dei ranking delle celle.
    :param risorse: Lista o array delle risorse allocate alle celle.
    :param vulnerabilita: Lista delle vulnerabilità delle celle.
    :return: Lista dei danni potenziali.
    """
    danni_potenziali = []
    for i, r_i in enumerate(celle):
        d_i = r_i * risorse[i] / vulnerabilita[i]
        danni_potenziali.append(d_i)
    return danni_potenziali

def funzione_di_fitness(celle, risorse, lambd, alpha, beta):
    """
    Calcola la funzione di fitness per il sistema.

    :param celle: Lista o array dei ranking delle celle.
    :param risorse: Lista o array delle risorse allocate alle celle.
    :param lambd: Costante che determina il peso del ranking.
    :param alpha: Peso dei danni potenziali nella funzione di fitness.
    :param beta: Peso della vulnerabilità nella funzione di fitness.
    :return: Valore della funzione di fitness.
    """
    vulnerabilita = calcola_vulnerabilita(celle, lambd, risorse)
    danni_potenziali = calcola_danni_potenziali(celle, risorse, vulnerabilita)

    totale_danni = sum(danni_potenziali)
    totale_vulnerabilita = sum(vulnerabilita)

    fitness = alpha * totale_danni + beta * totale_vulnerabilita
    
    return fitness

