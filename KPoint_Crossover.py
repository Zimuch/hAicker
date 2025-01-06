import random
import numpy as np

def k_point_crossover(parent1, parent2, k):
    """
    Esegue un crossover a k punti tra due genitori.

    Parametri:
    parent1 (numpy.ndarray): Primo genitore.
    parent2 (numpy.ndarray): Secondo genitore.
    k (int): Numero di punti di crossover.

    Ritorna:
    tuple: Due figli generati dal crossover (numpy.ndarray, numpy.ndarray).
    """
    if len(parent1) != len(parent2):
        raise ValueError("I genitori devono avere la stessa lunghezza")

    n = len(parent1)
    crossover_points = sorted(random.sample(range(1, n), k))  # Genera k punti di crossover (esclude 0)
    child1, child2 = np.copy(parent1), np.copy(parent2)

    # Alterna tra i segmenti per creare i figli
    for i in range(len(crossover_points)):
        start = crossover_points[i]
        end = crossover_points[i + 1] if i + 1 < len(crossover_points) else n
        if i % 2 == 0:  # Scambia segmenti per figli alternati
            child1[start:end], child2[start:end] = parent2[start:end], parent1[start:end]

    return child1, child2
