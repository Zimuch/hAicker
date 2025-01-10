import sys
import numpy as np
import random
from deap import base, creator, tools, algorithms
from Fitness import fitness_function1
from Fitness2 import fitness_function2
from Mutation import adaptive_mutation, calculate_fitness_change  # Importa la funzione di mutazione adattiva

# Parametri iniziali
POP_SIZE = 50
NUM_CELLS = 25
TOTAL_RESOURCES = 2000
MIN_RESOURCES = 20
CROSSOVER_POINTS = 4
MAX_GENERATIONS = 100
TARGET_FITNESS = 20  # Soglia di fitness target
LAMBDA_VALUE = 50  # Valore di lambda
LAMBDA_VALUE2 = 1  # Valore di lambda per la seconda funzione di fitness
OMEGA1 = 0.5  # Peso per l'obiettivo 1
OMEGA2 = 0.5  # Peso per l'obiettivo 2
ALPHA = 0.5  # Peso per i danni potenziali
BETA = 0.5  # Peso per la vulnerabilità

# Parametri di mutazione
mutation_rate = 0.02  # Tasso di mutazione iniziale
fitness_threshold = 0.02  # 2% miglioramento minimo
previous_fitness = 1  # Fitness media iniziale

# Creazione delle classi per la fitness multiobiettivo
creator.create("FitnessMulti", base.Fitness, weights=(1.0, -1.0))  # Massimizzazione e minimizzazione
creator.create("Individual", list, fitness=creator.FitnessMulti)

# Definizione della toolbox
toolbox = base.Toolbox()

# Funzione per creare un individuo
def create_individual():
    individual = [TOTAL_RESOURCES]  # Prima cella
    remaining_resources = TOTAL_RESOURCES
    for _ in range(NUM_CELLS - 1):
        allocation = random.randint(MIN_RESOURCES, 100)
        individual.append(allocation)
        remaining_resources -= allocation
    return creator.Individual(individual)

# Registra le funzioni nella toolbox
toolbox.register("individual", create_individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("evaluate", lambda ind: (fitness_function1(ind, LAMBDA_VALUE, ALPHA, BETA), fitness_function2(ind, LAMBDA_VALUE2, OMEGA1, OMEGA2)))
toolbox.register("select", tools.selNSGA2)
toolbox.register("mate", tools.cxTwoPoint)

# Generazione della popolazione iniziale
population = toolbox.population(n=POP_SIZE)

# Ciclo evolutivo
previous_fitness_values = [float('inf')] * POP_SIZE  # Precedenti fitness degli individui
mutation_rate = 0.02  # Tasso di mutazione iniziale

for generation in range(MAX_GENERATIONS):
    print(f"\nGenerazione {generation}\n")

    # Valutazione della fitness degli individui
    print("Valutazione della fitness degli individui...")
    fitnesses = list(map(toolbox.evaluate, population))
    for ind, fit in zip(population, fitnesses):
        ind.fitness.values = fit

    # Stampa migliori fitness
    best_ind = tools.selBest(population, 1)[0]
    print(f"  Miglior individuo: {best_ind}")
    print(f"  Fitness: {best_ind.fitness.values}")

    if best_ind.fitness.values[0] <= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        break

    # Selezione con NSGA-II per trovare la frontiera di Pareto
    print("Selezione con NSGA-II per trovare la frontiera di Pareto...")
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
    print(f"  Numero di individui nella frontiera di Pareto: {len(pareto_front)}")

    # Crossover
    print("Crossover...")
    offspring = list(map(toolbox.clone, pareto_front))
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.85:  # Probabilità di crossover
            print(f"  Prima del crossover: {child1}, {child2}")
            toolbox.mate(child1, child2)
            del child1.fitness.values, child2.fitness.values
            print(f"  Dopo il crossover: {child1}, {child2}")
    print("  Crossover completato.")

     # Mutazione adattiva
    print("Mutazione adattiva...")
    for i, mutant in enumerate(offspring):
        previous_fitness = previous_fitness_values[i]  # Fitness della generazione precedente
        # Ricalcola il valore di fitness se necessario
        if not mutant.fitness.valid:  # Se la fitness è stata eliminata o non è più valida
            mutant.fitness.values = toolbox.evaluate(mutant)
        current_fitness = mutant.fitness.values[0]  # Fitness attuale
        print(f"  Prima della mutazione: {mutant}")
        # Calcolare il cambiamento della fitness
        fitness_change = calculate_fitness_change(previous_fitness, current_fitness)
        
        # Applicare la mutazione adattiva
        mutant, mutation_rate = adaptive_mutation(mutant, previous_fitness, current_fitness, mutation_rate, fitness_threshold)
        
        # Aggiornare la fitness precedente dell'individuo
        previous_fitness_values[i] = mutant.fitness.values[0]
        
        del mutant.fitness.values
        print(f"  Dopo la mutazione: {mutant}")
    print("  Mutazione completata.")

    # Valutazione della nuova generazione
    print("Valutazione della nuova generazione...")
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
    fitnesses = list(map(toolbox.evaluate, invalid_ind))
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit
    print("  Valutazione completata.")

    # Sostituzione della popolazione con la nuova generazione
    population[:] = offspring
    print("  Popolazione aggiornata.")

print("\n>>> Evoluzione terminata.")
