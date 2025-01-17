import random
from Obiettivo1 import obiettivo1_danni

def k_point_crossover(parents, k, num_winners, total_resources):
    """
    Esegue un crossover a k punti tra coppie di genitori per generare due figli per ogni coppia,
    assicurandosi che le risorse massime allocabili non vengano superate.

    :param parents: Lista di genitori.
    :param k: Numero di punti di crossover.
    :param num_winners: Numero di vincitori/genitori.
    :param total_resources: Risorse massime allocabili.
    :return: Lista di nuovi individui (figli).
    """
    # Se il numero di vincitori è dispari, aggiungi un genitore casuale
    if num_winners % 2 != 0:
        parents.append(random.choice(parents))

    children = []

    for i in range(0, num_winners, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]

        # Assicurati che i genitori non siano identici
        while parent1 is parent2:
            parent2 = random.choice(parents)

        # Assicurati che i genitori abbiano la stessa lunghezza
        if len(parent1) != len(parent2):
            raise ValueError("I genitori devono avere la stessa lunghezza")

        length = len(parent1)
               
        # Assicurati che il numero di punti di crossover non superi la lunghezza del genitore
        if k >= length:
            raise ValueError("Il numero di punti di crossover non può essere maggiore o uguale alla lunghezza del genitore")

        # Genera k punti di crossover casuali unici e ordinati
        cut_points = sorted(random.sample(range(1, length), k))

        # Aggiungi l'inizio e la fine per facilitare gli scambi
        cut_points = [0] + cut_points + [length]
        
        child1, child2 = [], []

        # Alterna tra genitori nelle sezioni definite dai punti di taglio
        for j in range(len(cut_points) - 1):
            start, end = cut_points[j], cut_points[j + 1]
            segment1, segment2 = parent1[start:end], parent2[start:end]
            
            # Verifica se l'aggiunta del segmento supererebbe le risorse massime
            if sum(child1) + sum(segment1) <= total_resources and sum(child2) + sum(segment2) <= total_resources:
                child1.extend(segment1)
                child2.extend(segment2)
            else:
                # Prova a scambiare le celle successive
                for m in range(len(segment1)):
                    if sum(child1) + segment2[m] <= total_resources and sum(child2) + segment1[m] <= total_resources:
                        child1.append(segment2[m])
                        child2.append(segment1[m])
                    else:
                        child1.append(segment1[m])
                        child2.append(segment2[m])

     # Converti gli elementi dell'array in normali interi Python
        child1 = [int(x) for x in child1]
        child2 = [int(x) for x in child2]

    # Calcola e stampa la fitness dei figli
        fitness_child1 = fitness1_function(child1,50)
        fitness_child2 = fitness1_function(child2,50)
        print(f"Figlio {len(children) + 1}: {child1} \ncon Fitness: {fitness_child1} ... (total resources: {sum(child1)- child1[0]})")
        print(f"Figlio {len(children) + 2}: {child2} \ncon Fitness: {fitness_child2} ... (total resources: {sum(child2)- child2[0]})")                

        children.append(child1)
        children.append(child2)

    return children