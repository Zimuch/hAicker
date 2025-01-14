import sys
import numpy as np
import random
from Popolazione import generate_population
from KWay_Tournament import k_way_tournament_min
from KPoint_Crossover import k_point_crossover
from Fitness import fitness1_function
from Fitness2 import fitness2_function
from Fitness3 import fitness3_function
from MutationVecchia import mutate, calculate_fitness_change, adaptive_mutation


# Parametri iniziali
POP_SIZE = 30 # Dimensione della popolazione
NUM_CELLS = 25  # Numero di celle per individuo
TOTAL_RESOURCES = 2000 # Risorse totali disponibili
MIN_RESOURCES = 20 # Risorse minime per cella (esclusa la cella 0)
RANDOM_RESOURCES = (TOTAL_RESOURCES/NUM_CELLS) * 1.25 # Risorse casuali per la distribuzione
TOURNAMENT_SIZE = int(POP_SIZE/10) # Dimensione del torneo
NUM_WINNERS = int(POP_SIZE/2) # Numero di vincitori
CROSSOVER_POINTS = 4 # Numero di punti di crossover
MAX_GENERATIONS = 1 # Numero massimo di generazioni
TARGET_FITNESS = 7 # Soglia di fitness target
LAMBDA_VALUE2 = 1  # Valore di lambda
LAMBDA_VALUE1 = 50 # Valore di lambda 
OMEGA1 = 0.5  # Peso per l'obiettivo 1
OMEGA2 = 0.5  # Peso per l'obiettivo 2

# Parametri di mutazione
mutation_rate = 0.02  # Tasso di mutazione iniziale
fitness_threshold = 0.02  # 2% miglioramento minimo
previous_fitness = 1  # Fitness media iniziale

# Generazione della popolazione iniziale
population = generate_population(POP_SIZE, NUM_CELLS, TOTAL_RESOURCES, MIN_RESOURCES, RANDOM_RESOURCES)

# Ciclo evolutivo
for generation in range(MAX_GENERATIONS):
    print("\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
    print(f"\n                       Generazione {generation}\n")
    print("\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n\n")


    # Stampa alcuni risultati di esempio per vedere la distribuzione delle risorse
    for i, individual in enumerate(population):
        print(f"Individuo {i}: {individual[:25]}... (total resources: {sum(individual)- individual[0]})")
    print("\n")
    print("///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")



    # Valutazione della fitness degli individui
    fitness1_values = [fitness1_function(individual, LAMBDA_VALUE1) for individual in population]
    fitness2_values = [fitness2_function(individual,OMEGA1) for individual in population]
    fitness3_values = [fitness3_function(individual, LAMBDA_VALUE2, OMEGA2) for individual in population]


    # Stampa migliori fitness
    min_fitness = min(fitness1_values)
    print(f"\nFitness1 migliore: {min_fitness}")

    min_fitness = min(fitness2_values)
    print(f"\nFitness2 migliore: {min_fitness}")

    min_fitness = min(fitness3_values)
    print(f"\nFitness3 migliore: {min_fitness}\n")

    if min_fitness <= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!\n")
        sys.exit()



    # Selezione con il K-Way Tournament con numero di vincitori
    print("\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
    print(f"\nSelezione K-Way Tournament con {NUM_WINNERS} vincitori:\n")
    selected_individuals = k_way_tournament_min(population, fitness1_values, TOURNAMENT_SIZE, NUM_WINNERS) 
    fitness1_values_parents = [fitness1_function(parent, LAMBDA_VALUE1) for parent in selected_individuals]
    fitness2_values_parents = [(fitness2_function)(parent, LAMBDA_VALUE2) for parent in selected_individuals]
    fitness3_values_parents = [(fitness3_function)(parent, LAMBDA_VALUE2, OMEGA2) for parent in selected_individuals]

    # Selezione con il K-Point Crossover
    print("\n\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
    print(f"\nCrossover con {CROSSOVER_POINTS} punti:\n")
    children = k_point_crossover(selected_individuals, CROSSOVER_POINTS, NUM_WINNERS, TOTAL_RESOURCES)
    fitness1_values_children = [fitness1_function(child, LAMBDA_VALUE1) for child in children]
    fitness2_values_children = [fitness2_function(child, LAMBDA_VALUE2) for child in children]
    fitness3_values_children = [fitness3_function(child, LAMBDA_VALUE2, OMEGA2) for child in children]

    # Controlla se la fitness dei figli soddisfa la soglia
    if min(fitness3_values_children) <= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        print(f"\nFiglio con la fitness ottimale: {min(fitness3_values_children)}")
        sys.exit()

    # Calcolo della fitness corrente prima della mutazione
    current_fitness = sum(fitness2_values_children) / len(fitness2_values_children)

    # Applica mutazione ai figli
    childmutate1 = mutate(child1, mutation_rate)
    childmutate2 = mutate(child2, mutation_rate)
    childmutate3 = mutate(child3, mutation_rate)
    childmutate4 = mutate(child4, mutation_rate)
    childmutate5 = mutate(child5, mutation_rate)
    childmutate6 = mutate(child6, mutation_rate)

    # Stampa dei valori di fitness per i figli mutati


    # Calcolo del cambiamento di fitness e aggiornamento del tasso di mutazione
    fitness_change = calculate_fitness_change(previous_fitness, current_fitness)
    mutation_rate = adaptive_mutation(mutation_rate, fitness_change, fitness_threshold)
    print(f"  Fitness Change: {fitness_change:.4f}, Mutation Rate: {mutation_rate:.4f}")
    previous_fitness = current_fitness  # Aggiorna la fitness precedente

          # Controlla se la fitness dei figli mutati soddisfa la soglia
    if min(fitness_values_mutate) <= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        print(f"\nFiglio mutato con la fitness ottimale: {min(fitness_values_mutate)}")
        sys.exit()

    # Sostituisce la popolazione con i figli e i figli mutati
    population = [child1, child2, child3, child4, child5, child6, childmutate1, 
                  childmutate2, childmutate3, childmutate4, childmutate5, childmutate6]

print("\n>>> Generazione di individui terminata.")
print("\n>>> Soluzione ottimale non trovata.")