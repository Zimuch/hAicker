import sys
import numpy as np
import random
from Popolazione import generate_population
from KWay_Tournament import k_way_tournament_min
from KPoint_Crossover import k_point_crossover
from Obiettivo1 import obiettivo1_danni
from Obiettivo2 import obiettivo2_costo
from Obiettivo3 import obiettivo3_distribuzione
from FitnessCombinata import fitness_combinata
from Mutation import scramble_mutation, calculate_fitness_change, adaptive_mutation


# Parametri iniziali
POP_SIZE = 50 # Dimensione della popolazione
NUM_CELLS = 25  # Numero di celle per individuo
TOTAL_RESOURCES = 2000 # Risorse totali disponibili
MIN_RESOURCES = 20 # Risorse minime per cella (esclusa la cella 0)
RANDOM_RESOURCES = int(TOTAL_RESOURCES/NUM_CELLS) * 1.25 # Risorse casuali per la distribuzione
TOURNAMENT_SIZE = int(POP_SIZE/10) # Dimensione del torneo
NUM_WINNERS = int(POP_SIZE/2) # Numero di vincitori
CROSSOVER_POINTS = 4 # Numero di punti di crossover
MAX_GENERATIONS = 5 # Numero massimo di generazioni
TARGET_FITNESS = 9 # Soglia di fitness target
LAMBDA_VALUE1 = 80  # Valore di lambda per danni
LAMBDA_VALUE2 = 0.02 # Valore di lambda per costo
LAMBDA_VALUE3 = 6.7 # Valore di lambda per distribuzione risorse
OMEGA1 = 0.33  # Peso per l'obiettivo danni
OMEGA2 = 0.33  # Peso per l'obiettivo costi
OMEGA3 = 0.33  # Peso per l'obiettivo distribuzione pesata
STAMPE_DEBUG = False  # Stampa di debug per visualizzare dettagli sulla popolazione e i vari processi nel dettaglio

# Parametri di mutazione
mutation_rate = 0.20  # Tasso di mutazione iniziale
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
        if STAMPE_DEBUG == True : print(f"Individuo {i}: {individual[:25]}... (total resources: {sum(individual)- individual[0]})")
    print("\n")
    if STAMPE_DEBUG == True : print("///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")



    # Valutazione della fitness degli individui
    fitness1_values = [obiettivo1_danni(individual, LAMBDA_VALUE1) for individual in population]
    fitness2_values = [obiettivo2_costo(individual, LAMBDA_VALUE2) for individual in population]
    fitness3_values = [obiettivo3_distribuzione(individual,LAMBDA_VALUE3) for individual in population]
    fitness_combinata_values = [fitness_combinata(individual, LAMBDA_VALUE1, LAMBDA_VALUE2, LAMBDA_VALUE3, OMEGA1, OMEGA2, OMEGA3) 
                                for individual in population]

    # Stampa migliori fitness
    min_fitness = min(fitness1_values)
    if STAMPE_DEBUG == True :print(f"Obiettivo 1 migliore: {min_fitness} dell'individuo {population[fitness1_values.index(min_fitness)]} \ncon risorse totali {sum(population[fitness1_values.index(min_fitness)]) - population[fitness1_values.index(min_fitness)][0]}\n")

    max_fitness = max(fitness2_values)
    if STAMPE_DEBUG == True :print(f"Obiettivo 2 migliore: {max_fitness} dell'individuo {population[fitness2_values.index(max_fitness)]} \ncon risorse totali {sum(population[fitness2_values.index(max_fitness)]) - population[fitness2_values.index(max_fitness)][0]}\n")

    max_fitness3 = max(fitness3_values)
    if STAMPE_DEBUG == True :print(f"Obiettivo 3 migliore: {max_fitness3} dell'individuo {population[fitness3_values.index(max_fitness3)]} \ncon risorse totali {sum(population[fitness3_values.index(max_fitness3)]) - population[fitness3_values.index(max_fitness3)][0]}\n")

    max_fitness_combinata = max(fitness_combinata_values)
    print(f"\nFitness Combinata migliore: {max_fitness_combinata} dell' individuo {population[fitness_combinata_values.index(max_fitness_combinata)]} \ncon risorse totali {sum(population[fitness_combinata_values.index(max_fitness_combinata)])-population[fitness_combinata_values.index(max_fitness_combinata)][0]}\n")

    if max_fitness_combinata >= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!\n")
        sys.exit()

    # Selezione con il K-Way Tournament con numero di vincitori
    print("\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
    print(f"\nSelezione K-Way Tournament con {NUM_WINNERS} vincitori:\n")
    parents = k_way_tournament_min(population, fitness_combinata_values, TOURNAMENT_SIZE, NUM_WINNERS) 
    fitness_combinata_parents= [fitness_combinata(parent, LAMBDA_VALUE1, LAMBDA_VALUE2, LAMBDA_VALUE3, OMEGA1, OMEGA2, OMEGA3) 
                                 for parent in parents]
    
    # Stampa i genitori generati con la relativa fitness combinata
    for i, parent in enumerate(parents):
        if STAMPE_DEBUG == True : print(f"Genitore {i+1}: {parent} \ncon Fitness: {fitness_combinata_parents[i]} ... risorse totali: {sum(parent)- parent[0]} ")
    print("K-Way Tournament completato...\n")

    # Selezione con il K-Point Crossover
    print("\n\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
    print(f"\nCrossover con {CROSSOVER_POINTS} punti:\n")
    children = k_point_crossover(parents, CROSSOVER_POINTS, NUM_WINNERS, TOTAL_RESOURCES)
    
    fitness_combinata_children= [fitness_combinata(child, LAMBDA_VALUE1, LAMBDA_VALUE2, LAMBDA_VALUE3, OMEGA1, OMEGA2, OMEGA3) 
                                 for child in children]
    
    # Stampa i figli generati con la relativa fitness combinata
    for i, child in enumerate(children):
        if STAMPE_DEBUG == True : print(f"Figlio {i+1}: {child} \ncon Fitness: {fitness_combinata_children[i]} ... risorse totali: {sum(child)- child[0]} ")
    print("Crossover completato...\n")

    # Controlla se la fitness dei figli soddisfa la soglia
    if max(fitness_combinata_children) >= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        print(f"\nFiglio con la fitness ottimale: {max(fitness_combinata_children)}")
        sys.exit()

    # Calcolo della fitness corrente prima della mutazione
    current_fitness = sum(fitness_combinata_children) / len(fitness_combinata_children)

    # Applica mutazione ai figli
    print("\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
    print("\nMutazione Scramble:\n")
    children_mutate, children_mutation_rate = adaptive_mutation(children, previous_fitness, current_fitness, mutation_rate, fitness_threshold)
    fitness_combinata_mutation= [fitness_combinata(child, LAMBDA_VALUE1, LAMBDA_VALUE2, LAMBDA_VALUE3, OMEGA1, OMEGA2, OMEGA3) 
                                 for child in children_mutate]

    # Stampa dei valori di fitness per i figli mutati
    for i, child in enumerate(children_mutate):
        if STAMPE_DEBUG == True : print(f"Figlio Mutato {i+1}: {child} \ncon Fitness: {fitness_combinata_mutation[i]} ... risorse totali: {sum(child)- child[0]} ")
    print("Mutation completata...\n")

    # Calcolo del cambiamento di fitness e aggiornamento del tasso di mutazione
    fitness_change = calculate_fitness_change(previous_fitness, current_fitness)
    mutation_rate = children_mutation_rate
    print(f"  Fitness Change: {fitness_change:.4f}, Mutation Rate: {mutation_rate:.4f}")
    previous_fitness = current_fitness  # Aggiorna la fitness precedente

          # Controlla se la fitness dei figli mutati soddisfa la soglia
    if max(fitness_combinata_mutation) >= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        print(f"\nFiglio mutato con la fitness ottimale: {max(fitness_combinata_mutation)}")
        sys.exit()

    # Sostituisce la popolazione con i figli e i figli mutati
    population = children + children_mutate

print("\n>>> Generazione di individui terminata.")
print("\n>>> Soluzione ottimale non trovata.")