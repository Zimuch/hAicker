import random
import numpy as np
from deap import base, creator, tools, algorithms
from Fitness import funzione_di_fitness
from Fitness2 import fitness_function

# Parametri iniziali
POP_SIZE = 50
NUM_CELLS = 25
TOTAL_RESOURCES = 2000
MIN_RESOURCES = 20
MAX_GENERATIONS = 100
TOURNAMENT_SIZE = 5
CROSSOVER_POINTS = 4
ALPHA = 0.5
BETA = 0.5
LAMBDA = 1
ADAPTIVE_MUTATION_RATE = 0.02  # Tasso base di mutazione
TARGET_FITNESS = 50  # Soglia di fitness target

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

# Funzione di fitness multiobiettivo
def evaluate(individual):
    resources = individual[1:]  # Ignorare la prima cella
    lambda_value = 1.0
    fitness1 = funzione_di_fitness(resources, resources, LAMBDA, ALPHA, BETA)
    fitness2 = fitness_function(resources, LAMBDA, index)
    return fitness1, fitness2

toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.2)
toolbox.register("select", tools.selTournament, tournsize=TOURNAMENT_SIZE)

# Generazione della popolazione iniziale
population = toolbox.population(n=POP_SIZE)

# Ciclo evolutivo
for generation in range(MAX_GENERATIONS):
    print(f"\nGenerazione {generation}\n")

    # Valutazione della fitness degli individui
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = list(map(toolbox.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Selezione degli individui vincenti
    offspring = toolbox.select(population, len(population))
    offspring = list(map(toolbox.clone, offspring))

    # Applicazione del crossover
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.5:  # Probabilità di crossover
            toolbox.mate(child1, child2)
            del child1.fitness.values, child2.fitness.values

    # Applicazione della mutazione
    for mutant in offspring:
        if random.random() < ADAPTIVE_MUTATION_RATE:  # Probabilità di mutazione
            toolbox.mutate(mutant)
            del mutant.fitness.values

    # Valutazione della nuova generazione
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(map(toolbox.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # Sostituzione della popolazione con la nuova generazione
    population[:] = offspring

    # Output per monitorare i progressi
    front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
    print(f"Numero di soluzioni nel primo fronte: {len(front)}")

    # Controllo del criterio di arresto
    if any(ind.fitness.values[0] >= TARGET_FITNESS for ind in population):
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        break

# Risultati finali
front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
print("\nSoluzioni Pareto-ottimali:")
for ind in front:
    print(f"Individuo: {ind}, Fitness: {ind.fitness.values}")