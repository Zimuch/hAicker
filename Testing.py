import sys
import numpy as np
from Popolazione import generate_population
from KWay_Tournament import k_way_tournament_min
from KPoint_Crossover import k_point_crossover
from Obiettivo1 import obiettivo1_danni
from Obiettivo2 import obiettivo2_costo
from Obiettivo3 import obiettivo3_distribuzione
from FitnessCombinata import fitness_combinata
from Mutation import  calculate_fitness_change, adaptive_mutation


# Parametri iniziali
POP_SIZE = 31 # Dimensione della popolazione
NUM_CELLS = 25  # Numero di celle per individuo
TOTAL_RESOURCES = 2000 # Risorse totali disponibili
MIN_RESOURCES = 20 # Risorse minime per cella (esclusa la cella 0)
RANDOM_RESOURCES = int(TOTAL_RESOURCES/NUM_CELLS) * 1.25 # Risorse casuali per la distribuzione [NON MODIFICARE]
TOURNAMENT_SIZE = int(POP_SIZE/10) # Dimensione del torneo [NON MODIFICARE]
NUM_WINNERS = int(POP_SIZE) # Numero di vincitori [NON MODIFICARE]
CROSSOVER_POINTS = 4 # Numero di punti di crossover
MAX_GENERATIONS = 5 # Numero massimo di generazioni
TARGET_FITNESS = 7 # Soglia di fitness target
LAMBDA_VALUE1 = 80  # Valore di lambda per danni [NON MODIFICARE]
LAMBDA_VALUE2 = 0.02 # Valore di lambda per costo [NON MODIFICARE]
LAMBDA_VALUE3 = 6.7 # Valore di lambda per distribuzione risorse [NON MODIFICARE]
OMEGA1 = 0.33  # Peso per l'obiettivo danni
OMEGA2 = 0.33  # Peso per l'obiettivo costi
OMEGA3 = 0.33  # Peso per l'obiettivo distribuzione pesata
STAMPE_DEBUG = False  # Stampa di debug per visualizzare dettagli sulla popolazione e i vari processi nel dettaglio

# Parametri di mutazione
mutation_rate = 0.20  # % Tasso di mutazione iniziale
fitness_threshold = 0.02  # % miglioramento minimo
previous_fitness = 0  # Fitness media iniziale

# Generazione della popolazione iniziale
population = generate_population(POP_SIZE, NUM_CELLS, TOTAL_RESOURCES, MIN_RESOURCES, RANDOM_RESOURCES)
best_individual = [] # Miglior individuo globale
best_fitness = 0 # Miglior fitness globale

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
    
    #Salva il miglior individuo e la sua fitness a livello globale
    if best_fitness < max(fitness_combinata_values):
        best_individual = population[fitness_combinata_values.index(max(fitness_combinata_values))]
        best_fitness = max(fitness_combinata_values)
    
    # individuo con fitness migliore globale
    best_individual = population[fitness_combinata_values.index(max(fitness_combinata_values))]

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
    print(f"\nSelezione con K-Way Tournament:\n")
    parents = k_way_tournament_min(population, fitness_combinata_values, TOURNAMENT_SIZE, NUM_WINNERS) 
    fitness_combinata_parents= [fitness_combinata(parent, LAMBDA_VALUE1, LAMBDA_VALUE2, LAMBDA_VALUE3, OMEGA1, OMEGA2, OMEGA3) 
                                 for parent in parents]
    print(f"Sono stati selezionati {len(parents)} vincitori.\n")
    
    # Stampa i genitori generati con la relativa fitness combinata
    for i, parent in enumerate(parents):
        if STAMPE_DEBUG == True : print(f"Genitore {i+1}: {parent} \ncon Fitness: {fitness_combinata_parents[i]} ... risorse totali: {sum(parent)- parent[0]} ")
    print("K-Way Tournament completato...\n")

    # Selezione con il K-Point Crossover
    print("\n\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
    print(f"\nEsecuzione del Crossover con {CROSSOVER_POINTS} punti sui vincitori del Torneo:\n")
    children = k_point_crossover(parents, CROSSOVER_POINTS, NUM_WINNERS, TOTAL_RESOURCES)
    
    fitness_combinata_children= [fitness_combinata(child, LAMBDA_VALUE1, LAMBDA_VALUE2, LAMBDA_VALUE3, OMEGA1, OMEGA2, OMEGA3) 
                                 for child in children]
    
    print(f"Crossover applicato su {len(parents)} genitori.\n")

    # Stampa i figli generati con la relativa fitness combinata
    for i, child in enumerate(children):
        if STAMPE_DEBUG == True : print(f"Figlio {i+1}: {child} \ncon Fitness: {fitness_combinata_children[i]} ... risorse totali: {sum(child)- child[0]} ")
    print("Crossover completato...\n")

    # Controlla se la fitness dei figli soddisfa la soglia
    if max(fitness_combinata_children) >= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        print(f"\nFiglio con la fitness ottimale: {max(fitness_combinata_children)} \n Individuo: {children[fitness_combinata_children.index(max(fitness_combinata_children))]} ... risorse totali: {sum(children[fitness_combinata_children.index(max(fitness_combinata_children))])-children[fitness_combinata_children.index(max(fitness_combinata_children))][0]}")
        sys.exit()

    # Calcolo della fitness corrente prima della mutazione
    current_fitness = sum(fitness_combinata_children) / len(fitness_combinata_children)

    # Applica mutazione ai figli
    print("\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
    print("\nMutazione Scramble Adattiva in corso:\n")
    children_mutate, children_mutation_rate = adaptive_mutation(children, previous_fitness, current_fitness, mutation_rate, fitness_threshold)
    fitness_combinata_mutation= [fitness_combinata(child, LAMBDA_VALUE1, LAMBDA_VALUE2, LAMBDA_VALUE3, OMEGA1, OMEGA2, OMEGA3) 
                                 for child in children_mutate]
    print(f"Mutazione tentata su {len(children_mutate)} figli.\n")
    # Stampa dei valori di fitness per i figli mutati
    for i, child in enumerate(children_mutate):
        if STAMPE_DEBUG == True : print(f"Figlio Mutato {i+1}: {child} \ncon Fitness: {fitness_combinata_mutation[i]} ... risorse totali: {sum(child)- child[0]} ")
    print("Mutazione completata...\n")

    # Calcolo del cambiamento di fitness e aggiornamento del tasso di mutazione
    if previous_fitness != 0:  # Evita la divisione per zero
        fitness_change = calculate_fitness_change(previous_fitness, current_fitness)
    else:
        fitness_change = 0
    mutation_rate = children_mutation_rate
    print("\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
    print(f"  Fitness Change: {fitness_change:.4f}, Mutation Rate: {mutation_rate:.4f}")
    previous_fitness = current_fitness  # Aggiorna la fitness precedente

          # Controlla se la fitness dei figli mutati soddisfa la soglia
    if max(fitness_combinata_mutation) >= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        print(f"\nFiglio mutato con la fitness ottimale: {max(fitness_combinata_mutation)}\nIndividuo: {children_mutate[fitness_combinata_mutation.index(max(fitness_combinata_mutation))]} ... risorse totali: {sum(children_mutate[fitness_combinata_mutation.index(max(fitness_combinata_mutation))])-children_mutate[fitness_combinata_mutation.index(max(fitness_combinata_mutation))][0]}")
        sys.exit()

    # Sostituisce la popolazione con i figli e i figli mutati
    population = children_mutate

print("\n///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///  ///\n")
print("\n>>> Generazione di individui terminata.")
print("\n>>> Soluzione ottimale non trovata.")
print(" \nIl miglior individuo trovato e': ", best_individual , " \nFitness: ", best_fitness , "  \nRisorse:", sum(best_individual)-best_individual[0])