import sys
import numpy as np
import random
from deap import base, creator, tools, algorithms
from Fitness import fitness_function1
from Fitness2 import fitness_function2
from Mutation import adaptive_mutation, calculate_fitness_change  # Importa la funzione di mutazione adattiva

# Parametri iniziali
POP_SIZE = 100
NUM_CELLS = 25
TOTAL_RESOURCES = 2000
MIN_RESOURCES = 20
CROSSOVER_POINTS = 4
MAX_GENERATIONS = 100
TARGET_FITNESS_1 = 30
TARGET_FITNESS_2= 23  # Soglia di fitness target
LAMBDA_VALUE = 50  # Valore di lambda
LAMBDA_VALUE2 = 1  # Valore di lambda per la seconda funzione di fitness
OMEGA1 = 0.6  # Peso per l'obiettivo 1
OMEGA2 = 0.4  # Peso per l'obiettivo 2

# Parametri di mutazione adattiva
fitness_threshold = 0.02  # 2% miglioramento minimo
previous_fitness = 1  # Fitness media iniziale
threshold = 0.1  # Distanza minima tra le soluzioni nell'archivio

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
toolbox.register("evaluate", lambda ind: (fitness_function1(ind, LAMBDA_VALUE), fitness_function2(ind, LAMBDA_VALUE2, OMEGA1, OMEGA2)))
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

    if best_ind.fitness.values[0] <= TARGET_FITNESS_1 and best_ind.fitness.values[1] <= TARGET_FITNESS_2:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        sys.exit()


    # Selezione con NSGA-II per trovare la frontiera di Pareto
    print("Selezione con NSGA-II per trovare la frontiera di Pareto...")
    pareto_front = tools.sortNondominated(population, len(population), first_front_only=True)[0]
    print(f"  Numero di individui nella frontiera di Pareto: {len(pareto_front)}")
    
    # Archiviazione delle soluzioni migliori per aumentare la diversità
    archive = []
    for ind in population:
        if len(archive) < 10:
            archive.append(ind)
        else:
            # Mantieni solo le soluzioni che sono abbastanza diverse
            dist = [np.linalg.norm(np.array(ind) - np.array(a)) for a in archive]
            if min(dist) > threshold:
                archive.append(ind)

    # Crossover con logica per aggiungere genitori dall'archivio se necessario
    print("Crossover...")

    # Crea una lista di figli clonati dalla frontiera di Pareto
    offspring = list(map(toolbox.clone, pareto_front))

    # Diagnostica sulla dimensione della popolazione
    print(f"Popolazione alla generazione {generation}: {len(offspring)}")
    if (len(offspring) % 2 == 1):
        print("Numero dispari di individui, aggiungo uno dall'archivio per ottenere un numero pari.")
        # Scegli uno degli individui più diversi nell'archivio
        diverse_individuals = [ind for ind in archive if ind not in pareto_front]
        if diverse_individuals:
            selected_parent = random.choice(diverse_individuals)
            offspring.append(selected_parent)  # Aggiungi questo genitore all'offspring
            print(f"  Aggiunto genitore dall'archivio: {selected_parent}")
        else:
            print("  Nessun genitore diverso trovato nell'archivio.")

    # Se il numero di individui nella frontiera di Pareto è inferiore a 6 e la generazione è meno della metà del numero massimo di generazioni
    if (len(offspring) < 4) :
        print("Numero di individui nella frontiera di Pareto è inferiore a 6. Aggiungo un individuo dall'archivio.")
    
        # Scegli uno degli individui più diversi nell'archivio
        diverse_individuals = [ind for ind in archive if ind not in pareto_front]
        #se la offspring è pari allora aggiungi due individui dall'archivio
        if len(offspring) % 2 == 0:
            if diverse_individuals:
                selected_parent = random.choice(diverse_individuals)
                offspring.append(selected_parent)  # Aggiungi questo genitore all'offspring
        if diverse_individuals:
            selected_parent = random.choice(diverse_individuals)
            offspring.append(selected_parent)  # Aggiungi questo genitore all'offspring
            
            print(f"  Aggiunto genitore dall'archivio: {selected_parent}")
        else:
            print("  Nessun genitore diverso trovato nell'archivio.")

    # Crossover tra le coppie
    crossover_count = 0
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        rd = random.random()
        print(f"Generato rd: {rd}")  # Per verificare i valori di random
        if rd < 0.85:  # Probabilità di crossover
            print(f"  Prima del crossover: {child1}, {child2}")
        
            # Esegui il crossover
            toolbox.mate(child1, child2)
        
            # Rimuovi il fitness dai figli
            del child1.fitness.values, child2.fitness.values
        
            # Incrementa il contatore del crossover
            crossover_count += 1
        
            print(f"  Dopo il crossover: {child1}, {child2}")

    # Stampa il numero totale di crossover eseguiti in questa generazione
    print(f"  Numero di crossover effettuati in questa generazione: {crossover_count}")
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
    #funzione che mantiene l'individuo con la fitness migliore e anche la fitness rispetto a tutte le generazioni
    best_ind = tools.selBest(population, 1)[0]

print("\n>>> Evoluzione terminata.")
print(f"  Miglior individuo: {best_ind}")
#stampa miglior fitness
print(f"  Fitness: {best_ind.fitness.values}")