import random

def k_point_crossover(parent1, parent2, k, TOTAL_RESOURCES):
    """
    Esegue un crossover a k punti tra due genitori per generare due figli,
    assicurandosi che le risorse massime allocabili non vengano superate.

    :param parent1: Lista o array del primo genitore.
    :param parent2: Lista o array del secondo genitore.
    :param k: Numero di punti di crossover.
    :param max_resources: Risorse massime allocabili.
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
            segment1, segment2 = parent1[start:end], parent2[start:end]
        else:
            segment1, segment2 = parent2[start:end], parent1[start:end]

        # Verifica se l'aggiunta del segmento supererebbe le risorse massime
        if sum(child1) + sum(segment1) <= TOTAL_RESOURCES and sum(child2) + sum(segment2) <= TOTAL_RESOURCES:
            child1.extend(segment1)
            child2.extend(segment2)
        else:
            # Prova a scambiare le celle successive
            for j in range(len(segment1)):
                if sum(child1) + segment2[j] <= TOTAL_RESOURCES and sum(child2) + segment1[j] <= TOTAL_RESOURCES:
                    child1.append(segment2[j])
                    child2.append(segment1[j])
                else:
                    child1.append(segment1[j])
                    child2.append(segment2[j])

    return child1, child2