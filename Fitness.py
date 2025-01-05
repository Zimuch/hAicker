import random

# Prima funzione di fitness
def fitness_function1(chromosome):
    # Esempio: Massimizzazione della somma degli elementi
    return sum(chromosome)

# Seconda funzione di fitness
def fitness_function2(chromosome, intermediate_value):
    # Esempio: Minimizzazione della deviazione dai vincoli forniti dall'intermediate_value
    return abs(sum(chromosome) - intermediate_value)

# Algoritmo di selezione K-Way Tournament
def k_way_tournament(population, k, fitness_function):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, k)
        winner = max(tournament, key=fitness_function)
        selected.append(winner)
    return selected

# Algoritmo di K-point Crossover
def k_point_crossover(parent1, parent2, k):
    length = len(parent1)
    crossover_points = sorted(random.sample(range(1, length), k))
    child1, child2 = parent1[:], parent2[:]
    toggle = False
    for i in range(length):
        if i in crossover_points:
            toggle = not toggle
        if toggle:
            child1[i], child2[i] = child2[i], child1[i]
    return child1, child2

# Creazione di una popolazione iniziale casuale
def initialize_population(pop_size, chromosome_length):
    return [[random.randint(0, 10) for _ in range(chromosome_length)] for _ in range(pop_size)]

# Implementazione dell'algoritmo evolutivo adattato
def evolutionary_algorithm(
    population_size, chromosome_length, generations, k_tournament, k_crossover
):
    population = initialize_population(population_size, chromosome_length)

    for generation in range(generations):
        # Valutazione della prima funzione di fitness
        population_fitness1 = [fitness_function1(ind) for ind in population]

        # Mitigazione: Trasferimento dei valori intermedi alla seconda funzione di fitness
        intermediate_values = population_fitness1
        population_fitness2 = [
            fitness_function2(ind, intermediate_value)
            for ind, intermediate_value in zip(population, intermediate_values)
        ]

        # Determinazione del fitness complessivo (esempio di bilanciamento)
        overall_fitness = [
            f1 - f2  # Ponderazione personalizzabile: bilanciare o sommare f1 e f2
            for f1, f2 in zip(population_fitness1, population_fitness2)
        ]

        # Stampa di informazioni sulla generazione corrente
        best_fitness = max(overall_fitness)
        print(f"Generation {generation}: Best overall fitness = {best_fitness}")

        # Selezione tramite K-Way Tournament basata su fitness complessivo
        selected_population = k_way_tournament(population, k_tournament, lambda ind: overall_fitness[population.index(ind)])

        # Crossover
        next_generation = []
        while len(next_generation) < population_size:
            parents = random.sample(selected_population, 2)
            children = k_point_crossover(parents[0], parents[1], k_crossover)
            next_generation.extend(children)

        # Troncamento della nuova generazione alla dimensione della popolazione
        population = next_generation[:population_size]

    # Restituzione della migliore soluzione trovata
    best_index = overall_fitness.index(max(overall_fitness))
    best_individual = population[best_index]
    return best_individual, overall_fitness[best_index]

# Parametri dell'algoritmo
population_size = 1000
chromosome_length = 100
generations = 50
k_tournament = 10
k_crossover = 3

# Esecuzione dell'algoritmo evolutivo
best_solution, best_fitness = evolutionary_algorithm(
    population_size, chromosome_length, generations, k_tournament, k_crossover
)

print("Best solution:", best_solution)
print("Best fitness:", best_fitness)