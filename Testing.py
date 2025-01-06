import numpy as np
import random
from KWay_Tournament import k_way_tournament_selection
from KPoint_Crossover import k_point_crossover
from Fitness2 import fitness_function

def generate_population(pop_size, num_cells, total_resources, min_resources):
    """
    Genera una popolazione iniziale di dimensione `pop_size` con ciascun individuo
    composto da `num_cells`.

    Parametri:
    pop_size (int): Numero di individui nella popolazione iniziale.
    num_cells (int): Numero di celle per individuo.
    total_resources (int): Numero totale di risorse disponibili.
    min_resources (int): Risorse minime per cella (esclusa la cella 0).

    Ritorna:
    list: Lista di individui (array numpy).
    """
    import random
import numpy as np

def generate_population(pop_size, num_cells, total_resources, min_resources):

    population = []

    base_resource = 20  # Risorsa fissa da assegnare inizialmente a tutte le celle
    remaining_resources = total_resources - base_resource * (num_cells - 1)  # Risorse rimanenti per la distribuzione casuale
    
    if remaining_resources < 0:
        raise ValueError("Non ci sono abbastanza risorse per rispettare il minimo per ogni cella!")

    for _ in range(pop_size):
        individual = np.zeros(num_cells, dtype=int)
        individual[0] = total_resources  # La cella 0 contiene il totale delle risorse
        risorse_totali = individual[0]

        # Distribuire 20 risorse iniziali a tutte le celle tranne la cella 0
        for i in range(1, num_cells):
            individual[i] = base_resource  # Assegniamo 20 a tutte le celle (eccetto la cella 0)
        
        # Ricalcoliamo le risorse da distribuire
        remaining_resources = risorse_totali - base_resource * (num_cells-1)  # Risorse rimanenti dopo l'assegnazione iniziale

        # Distribuire le risorse rimanenti in modo casuale
        for i in range(1, num_cells):
            if remaining_resources > 0:
                max_possible = remaining_resources
                resources = random.randint(0, 100)
                if resources > max_possible:
                    resources = max_possible
                individual[i] += resources  # Assegniamo le risorse alla cella
                remaining_resources -= resources  # Decrementiamo le risorse rimanenti


        population.append(individual)

    return population




# Parametri iniziali
POP_SIZE = 20
NUM_CELLS = 25
TOTAL_RESOURCES = 2000
MIN_RESOURCES = 20
TOURNAMENT_SIZE = 10
CROSSOVER_POINTS = 4

# Generazione della popolazione iniziale
population = generate_population(POP_SIZE, NUM_CELLS, TOTAL_RESOURCES, MIN_RESOURCES)

# Stampa alcuni risultati di esempio per vedere la distribuzione delle risorse
for i, individual in enumerate(population):
    print(f"Individuo {i}: {individual[:25]}... (total resources: {sum(individual)- individual[0]})")

# Valutazione della fitness degli individui
lambda_value = 1.0  # Puoi scegliere il valore di lambda_value secondo le tue esigenze
fitness_values = [fitness_function(individual, lambda_value, index)for index, individual in enumerate(population)]

# Selezione con il K-Way Tournament
selected_individuals = k_way_tournament_selection(population, fitness_values, TOURNAMENT_SIZE)

# Crossover tra i primi due individui selezionati
parent1 = selected_individuals[0]
parent2 = selected_individuals[1]
child1, child2 = k_point_crossover(parent1, parent2, CROSSOVER_POINTS)

# Output per verificare
print("\nIndividuo 1:", parent1)
print("\nIndividuo 2:", parent2)
print("\nFiglio 1:", child1)
print("\nFiglio 2:", child2)
