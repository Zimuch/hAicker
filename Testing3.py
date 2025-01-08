import numpy as np
import random

# Configurazioni
POPULATION_SIZE = 100
NUM_GENERATIONS = 5
CROSSOVER_RATE = 0.95
MUTATION_RATE = 0.05
K_TOURNAMENT = 10
CROSSOVER_POINTS = 3



# Costanti per il calcolo delle vulnerabilità e dei danni
LAMBDA = 1  # Costante per il peso del ranking
ALPHA = 0.5  # Peso per i danni potenziali nella fitness
BETA = 0.5   # Peso per la vulnerabilità nella fitness

# Inizializzazione popolazione
def initialize_population(size, individual_length):
    population = []
    for _ in range(size):
        individual = [random.randint(10, 100)] + [random.randint(0, 10) for _ in range(individual_length - 1)]
        population.append(individual)
    return np.array(population)

# Funzioni per il calcolo di vulnerabilità e danni
def calculate_vulnerability(rank, n, resources=0):
    if resources == 0:
        return LAMBDA * n / rank
    return LAMBDA * n / (rank * np.sqrt(resources))

def calculate_damage(rank, resources, vulnerability):
    return (rank * resources) / vulnerability

def calculate_total_damage(population, ranks):
    total_damage = 0
    n = len(ranks)
    for i, individual in enumerate(population):
        rank = ranks[i]
        resources = sum(individual[1:])
        vulnerability = calculate_vulnerability(rank, n, resources)
        damage = calculate_damage(rank, resources, vulnerability)
        total_damage += damage
    return total_damage

def calculate_total_vulnerability(population, ranks):
    total_vulnerability = 0
    n = len(ranks)
    for i, individual in enumerate(population):
        rank = ranks[i]
        resources = sum(individual[1:])
        vulnerability = calculate_vulnerability(rank, n, resources)
        total_vulnerability += vulnerability
    return total_vulnerability

# Fitness Function
def fitness_function(population, ranks):
    total_damage = calculate_total_damage(population, ranks)
    total_vulnerability = calculate_total_vulnerability(population, ranks)
    return ALPHA * total_damage + BETA * total_vulnerability

# Selezione - K-way tournament
def tournament_selection(population, fitness_scores, k):
    selected = []
    for _ in range(len(population)):
        competitors = random.sample(range(len(population)), k)
        winner = min(competitors, key=lambda idx: fitness_scores[idx])
        selected.append(population[winner])
    return np.array(selected)

# Crossover - K-point
def k_point_crossover(parent1, parent2, k):
    if random.random() < CROSSOVER_RATE:
        points = sorted(random.sample(range(1, len(parent1)), k))
        child1, child2 = parent1.copy(), parent2.copy()
        for i in range(len(points)):
            if i % 2 == 0:
                child1[points[i]:points[i+1] if i+1 < len(points) else None] = parent2[points[i]:points[i+1] if i+1 < len(points) else None]
                child2[points[i]:points[i+1] if i+1 < len(points) else None] = parent1[points[i]:points[i+1] if i+1 < len(points) else None]
        return child1, child2
    return parent1, parent2

# Mutazione - Adaptive
def adaptive_mutation(individual, generation, max_generations):
    if random.random() < MUTATION_RATE:
        mutation_probability = 1 - (generation / max_generations)  # Probabilità adattiva
        for i in range(1, len(individual)):  # Non modifica la prima cella
            if random.random() < mutation_probability:
                individual[i] = max(0, individual[i] + random.randint(-2, 2))
    return individual

# Vincolo: somma delle celle <= valore della prima cella
def apply_constraints(individual):
    max_value = individual[0]
    while sum(individual[1:]) > max_value:
        for i in range(1, len(individual)):
            if individual[i] > 0:
                individual[i] -= 1
                if sum(individual[1:]) <= max_value:
                    break
    return individual

# Algoritmo principale
def genetic_algorithm():
    individual_length = 25  # Lunghezza degli individui
    population = initialize_population(POPULATION_SIZE, individual_length)

    # Placeholder per ranks
    ranks = np.random.randint(1, 10, size=POPULATION_SIZE)

    for generation in range(NUM_GENERATIONS):
        for i in range(len(population)):
            population[i] = apply_constraints(population[i])

        fitness_scores = [fitness_function([ind], ranks) for ind in population]

        # Selezione
        selected_population = tournament_selection(population, fitness_scores, K_TOURNAMENT)

        # Crossover
        next_generation = []
        for i in range(0, len(selected_population), 2):
            parent1, parent2 = selected_population[i], selected_population[min(i+1, len(selected_population)-1)]
            child1, child2 = k_point_crossover(parent1, parent2, CROSSOVER_POINTS)
            next_generation.extend([child1, child2])

        # Mutazione
        next_generation = [adaptive_mutation(ind, generation, NUM_GENERATIONS) for ind in next_generation]

        # Applica vincoli
        next_generation = [apply_constraints(ind) for ind in next_generation]

        # Assicura che la dimensione della popolazione rimanga costante
        population = np.array(next_generation[:POPULATION_SIZE])

    # Risultato finale
    fitness_scores = [fitness_function([ind], ranks) for ind in population]
    best_individual = population[np.argmin(fitness_scores)]  # Minimizza la fitness
    return best_individual, min(fitness_scores)

# Esegui l'algoritmo
if __name__ == "__main__":
    best, best_fitness = genetic_algorithm()
    print("Miglior individuo:", best)
    print("Valore fitness migliore:", best_fitness)
