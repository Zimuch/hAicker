import numpy as np
import random
from KWay_Tournament import k_way_tournament_min
from KPoint_Crossover import k_point_crossover
from Fitness2 import fitness_function
from Fitness_Genitore_Figlio import fitness_function_parent
from Mutation import mutate, calculate_fitness_change, adaptive_mutation


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
            individual[i] = base_resource

        remaining_resources = risorse_totali - base_resource * (num_cells - 1)

        for i in range(1, num_cells):
            if remaining_resources > 0:
                max_possible = remaining_resources
                resources = random.randint(0, 100)
                individual[i] += resources
                remaining_resources -= resources

        population.append(individual)

    return population


# Parametri iniziali
POP_SIZE = 40
NUM_CELLS = 25
TOTAL_RESOURCES = 2000
MIN_RESOURCES = 20
TOURNAMENT_SIZE = 4
CROSSOVER_POINTS = 4
TARGET_FITNESS = 28  # Soglia di fitness target
MAX_GENERATIONS = 10  # Limite massimo di generazioni

# Parametri di mutazione
initial_mutation_rate = 0.02
fitness_threshold = 0.02  # 2% miglioramento minimo
previous_fitness = 1.0  # Fitness media iniziale

# Inizializzazione
mutation_rate = initial_mutation_rate
population = generate_population(POP_SIZE, NUM_CELLS, TOTAL_RESOURCES, MIN_RESOURCES)

# Ciclo evolutivo
for generation in range(MAX_GENERATIONS):
    print(f"Generazione {generation}")

    # Calcolo della fitness degli individui
    lambda_value = 1.0  # Puoi scegliere il valore di lambda secondo le esigenze
    fitness_values = [fitness_function(individual, lambda_value, index) for index, individual in enumerate(population)]

    # Stampa migliori fitness
    min_fitness = min(fitness_values)
    print(f"  Fitness migliore: {min_fitness}")

    if min_fitness <= TARGET_FITNESS:
        print("\n>>> Soluzione ottimale trovata!")
        break

    # Selezione con K-Way Tournament
    selected_individuals = k_way_tournament_min(population, fitness_values, TOURNAMENT_SIZE)

    # Generazione della nuova popolazione
    new_population = []
    while len(new_population) < POP_SIZE:

        # Seleziona due genitori
        parent1, parent2 = random.sample(selected_individuals, 2)

        # Crossover
        child1, child2 = k_point_crossover(parent1, parent2, CROSSOVER_POINTS)

        # Applica mutazione ai figli
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)

        new_population.extend([child1, child2])

    # Calcola la fitness corrente
    current_fitness = sum(fitness_function(individual, lambda_value, idx) for idx, individual in enumerate(new_population)) / len(new_population)

    # Calcolo del cambiamento di fitness e aggiornamento del tasso di mutazione
    fitness_change = calculate_fitness_change(previous_fitness, current_fitness)
    mutation_rate = adaptive_mutation(mutation_rate, fitness_change, fitness_threshold)

    print(f"  Fitness Change: {fitness_change:.4f}, Mutation Rate: {mutation_rate:.4f}")
    previous_fitness = current_fitness  # Aggiorna la fitness precedente

print("\n>>> Evoluzione terminata.")
