import numpy as np
import random
from deap import base, creator, tools, algorithms

# Parametri iniziali
POP_SIZE = 50
NUM_CELLS = 25
TOTAL_RESOURCES = 2000
MIN_RESOURCES = 20
MAX_GENERATIONS = 100
TOURNAMENT_SIZE = 5
CROSSOVER_POINTS = 4
ADAPTIVE_MUTATION_RATE = 0.02  # Tasso base di mutazione

# Creazione delle classi per la fitness multiobiettivo
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))  # Massimizzazione e minimizzazione
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Definizione della toolbox
toolbox = base.Toolbox()

# Individuo: la prima cella è fissata a TOTAL_RESOURCES, il resto è casuale
def init_individual():
    individual = [TOTAL_RESOURCES]  # Prima cella
    individual += [random.randint(MIN_RESOURCES, TOTAL_RESOURCES // NUM_CELLS) for _ in range(NUM_CELLS - 1)]
    return creator.Individual(individual)

toolbox.register("individual", init_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

# Funzione per calcolare la vulnerabilità
def calcola_vulnerabilita(rankings, lambda_value, resources):
    n = len(rankings)
    return [
        lambda_value * (n / rank) / np.sqrt(resource) if resource > 0 else float("inf")
        for rank, resource in zip(rankings, resources)
    ]

# Funzione per calcolare i danni potenziali
def calcola_danni(rankings, resources, vulnerabilities):
    return [rank * resource / vulnerability for rank, resource, vulnerability in zip(rankings, resources, vulnerabilities)]

# Funzione di fitness multiobiettivo
def evaluate(individual):
    resources = individual[1:]  # Ignorare la prima cella
    lambda_value = 1.0
    rankings = list(range(1, len(resources) + 1))
    vulnerabilities = calcola_vulnerabilita(rankings, lambda_value, resources)
    damages = calcola_danni(rankings, resources, vulnerabilities)
    return sum(damages), sum(vulnerabilities)

toolbox.register("evaluate", evaluate)

# Crossover a 4 punti
def k_point_crossover(ind1, ind2, k=4):
    size = min(len(ind1), len(ind2))
    points = sorted(random.sample(range(1, size), k))
    for i in range(0, len(points), 2):
        if i + 1 < len(points):
            ind1[points[i]:points[i + 1]], ind2[points[i]:points[i + 1]] = ind2[points[i]:points[i + 1]], ind1[points[i]:points[i + 1]]
    return ind1, ind2

toolbox.register("mate", k_point_crossover, k=CROSSOVER_POINTS)

# Mutazione adattiva
def adaptive_mutation(individual):
    # Calcolo tasso adattivo
    fitness_threshold = 0.2
    # Check if fitness values are available, otherwise use a default value
    if individual.fitness.valid: 
        mutation_rate = ADAPTIVE_MUTATION_RATE * (1 - (individual.fitness.values[0] / fitness_threshold))
    else:
        mutation_rate = ADAPTIVE_MUTATION_RATE # Default mutation rate when fitness is not yet evaluated
        
    for i in range(1, len(individual)):  # Ignora la prima cella
        if random.random() < mutation_rate:
            individual[i] = random.randint(MIN_RESOURCES, TOTAL_RESOURCES // NUM_CELLS)
    return individual,

toolbox.register("mutate", adaptive_mutation)

# Selezione NSGA2
toolbox.register("select", tools.selNSGA2)

# Generazione della popolazione iniziale
population = toolbox.population(n=POP_SIZE)

# Registro degli operatori
toolbox.register("map", map)

# Ciclo evolutivo
for generation in range(MAX_GENERATIONS):
    print(f"\nGenerazione {generation}")
    
    # Valutazione della popolazione
    fitnesses = list(toolbox.map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    # Selezione dei genitori
    offspring = toolbox.select(population, len(population))
    offspring = list(toolbox.map(toolbox.clone, offspring))

    # Applicazione del crossover e della mutazione
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.9:  # Probabilità di crossover
            toolbox.mate(child1, child2)
            del child1.fitness.values, child2.fitness.values
    for mutant in offspring:
        if random.random() < 0.2:  # Probabilità di mutazione
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Valutazione della nuova generazione
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(toolbox.map(toolbox.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Sostituzione della popolazione con la nuova generazione
    population[:] = offspring

    # Output per monitorare i progressi
    front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
    print(f"Numero di soluzioni nel primo fronte: {len(front)}")

# Risultati finali
front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
print("\nSoluzioni Pareto-ottimali:")
for ind in front:
    print(f"Individuo: {ind}, Fitness: {ind.fitness.values}")
