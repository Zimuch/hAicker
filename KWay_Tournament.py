import random
from FitnessCombinata import fitness_combinata
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


    if(num_winners%2!=0):
        num_winners=num_winners+1

    for _ in range(num_winners):
        # Seleziona casualmente k individui
        tournament_indices = random.sample(range(len(population)), k)
        tournament_contestants = [population[i] for i in tournament_indices]
        tournament_fitnesses = [fitness_values[i] for i in tournament_indices]

        # Trova l'individuo con la fitness migliore (maggiore)
        best_index = tournament_indices[tournament_fitnesses.index(max(tournament_fitnesses))]
        selected_individuals.append((population[best_index]))

    return selected_individuals