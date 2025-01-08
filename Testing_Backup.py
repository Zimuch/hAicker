import numpy as np
import random
from KWay_Tournament import k_way_tournament_min
from KPoint_Crossover import k_point_crossover
from Fitness2 import fitness_function
from Fitness_Genitore_Figlio import fitness_function_parent
from Mutation import mutate, calculate_fitness_change, adaptive_mutation


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
TOURNAMENT_SIZE = 5
CROSSOVER_POINTS = 4

# Parametri di mutazione
mutation_rate = 0.02
fitness_threshold = 0.02  # 2% miglioramento minimo
previous_fitness = 1  # Fitness media iniziale

# Generazione della popolazione iniziale
population = generate_population(POP_SIZE, NUM_CELLS, TOTAL_RESOURCES, MIN_RESOURCES)

# Stampa alcuni risultati di esempio per vedere la distribuzione delle risorse
for i, individual in enumerate(population):
    print(f"Individuo {i}: {individual[:25]}... (total resources: {sum(individual)- individual[0]})")

# Valutazione della fitness degli individui
lambda_value = 1.0  # Puoi scegliere il valore di lambda_value secondo le tue esigenze
fitness_values = [fitness_function(individual, lambda_value, index)for index, individual in enumerate(population)]

# Selezione con il K-Way Tournament
selected_individuals = k_way_tournament_min(population, fitness_values, TOURNAMENT_SIZE)


# Crossover tra i primi due individui selezionati
parent1 = selected_individuals[0]
parent2 = selected_individuals[1]
fitness_values_parent = [fitness_function_parent(parent1, lambda_value), fitness_function_parent(parent2, lambda_value)]



# Converti i figli in liste di interi normali per la stampa
child1, child2 = k_point_crossover(parent1, parent2, CROSSOVER_POINTS)
child1 = [int(x) for x in child1]
child2 = [int(x) for x in child2]


# Calcolo della fitness corrente prima della mutazione
current_fitness = (fitness_function_parent(child1, lambda_value) + fitness_function_parent(child2, lambda_value)) / 2

# Calcolo del cambiamento di fitness e aggiornamento del tasso di mutazione
fitness_change = calculate_fitness_change(previous_fitness, current_fitness)
mutation_rate = adaptive_mutation(mutation_rate, fitness_change, fitness_threshold)
print(f"\nFitness Change: {fitness_change:.4f}, Updated Mutation Rate: {mutation_rate:.4f}")


# Applica mutazione ai figli
childmutate1 = mutate(child1, mutation_rate)
childmutate2 = mutate(child2, mutation_rate)

# Output per verificare
print("\nGenitore 1 scelto dal K-Way Tournament:", parent1)
print("\nGenitore 2 scelto dal K-Way Tournament:", parent2)
print(f"\nFitness Genitore 1: {fitness_values_parent[0]}")
print(f"Fitness Genitore 2: {fitness_values_parent[1]}")


# Conserva i valori di fitness dei figli
print(f"\nFiglio 1: {child1} ")
print(f"\nFiglio 2: {child2} \n")
fitness_values_children = [fitness_function(child1, lambda_value, 0), fitness_function(child2, lambda_value, 1)]
(fitness_values_children[0])
(fitness_values_children[1])

# Conserva i valori di fitness dei figli
print(f"\nFiglio 1 (mutato): {childmutate1}")
print(f"\nFiglio 2 (mutato): {childmutate2}\n")
fitness_values_children = [fitness_function(childmutate1, lambda_value, 0), fitness_function(childmutate2, lambda_value, 1)]




