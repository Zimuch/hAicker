import random

def k_point_crossover(parent1, parent2, k):
    """
    Esegue un crossover a k punti tra due genitori per generare due figli.

    :param parent1: Lista o array del primo genitore.
    :param parent2: Lista o array del secondo genitore.
    :param k: Numero di punti di crossover.
    :return: Due nuovi individui (figli).
    """
    # Assicurati che i genitori abbiano la stessa lunghezza
    if len(parent1) != len(parent2):
        raise ValueError("I genitori devono avere la stessa lunghezza")

    length = len(parent1)
    # Genera k punti di crossover casuali unici e ordinati
    cut_points = sorted(random.sample(range(1, length), k))

    # Aggiungi l'inizio e la fine per facilitare gli scambi
    cut_points = [0] + cut_points + [length]
    
    child1, child2 = [], []

    # Alterna tra genitori nelle sezioni definite dai punti di taglio
    for i in range(len(cut_points) - 1):
        start, end = cut_points[i], cut_points[i + 1]
        if i % 2 == 0:
            child1.extend(parent1[start:end])
            child2.extend(parent2[start:end])
        else:
            child1.extend(parent2[start:end])
            child2.extend(parent1[start:end])

    return child1, child2
