import random

def k_way_tournament_min(population, fitness_values, k):
    """
    Esegue una selezione a torneo k-way dalla popolazione basata sui valori di fitness.

    Parametri:
    population (list): Lista di individui (array numpy).
    fitness_values (list): Lista di valori di fitness corrispondenti agli individui.
    k (int): Dimensione del torneo.

    Ritorna:
    list: Lista di individui selezionati dalla popolazione.
    """
    selected_individuals = []

    for _ in range(len(population)):
        # Seleziona casualmente k individui
        tournament_indices = random.sample(range(len(population)), k)
        tournament_contestants = [population[i] for i in tournament_indices]
        tournament_fitnesses = [fitness_values[i] for i in tournament_indices]

        
        # Trova l'individuo con la fitness migliore (minore)
        best_index = tournament_indices[tournament_fitnesses.index(min(tournament_fitnesses))]
        selected_individuals.append(population[best_index])
        

    return selected_individuals