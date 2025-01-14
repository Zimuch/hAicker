import random
from Fitness import fitness1_function
def k_way_tournament_min(population, fitness_values, k, num_winners):
    """
    Esegue una selezione a torneo k-way dalla popolazione basata sui valori di fitness.

    Parametri:
    population (list): Lista di individui (array numpy).
    fitness_values (list): Lista di valori di fitness corrispondenti agli individui.
    k (int): Dimensione del torneo.
    num_winners (int): Numero di vincitori da selezionare.

    Ritorna:
    list: Lista di tuple contenenti individui selezionati dalla popolazione e i loro valori di fitness.
    """
    selected_individuals = []

    for _ in range(num_winners):
        # Seleziona casualmente k individui
        tournament_indices = random.sample(range(len(population)), k)
        tournament_contestants = [population[i] for i in tournament_indices]
        tournament_fitnesses = [fitness_values[i] for i in tournament_indices]

        # Trova l'individuo con la fitness migliore (minore)
        best_index = tournament_indices[tournament_fitnesses.index(min(tournament_fitnesses))]
        selected_individuals.append((population[best_index]))

    # Stampa i vincitori con i relativi valori di fitness
    for i, (individual) in enumerate(selected_individuals):
        fitness_value = fitness1_function(individual, 50)
        print(f"Vincitore {i + 1}: {individual} con Fitness: {fitness_value} ... (total resources: {sum(individual)- individual[0]})")

    return selected_individuals