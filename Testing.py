import sys
import numpy as np
import random
from KWay_Tournament import k_way_tournament_min
from KPoint_Crossover import k_point_crossover
from Fitness2 import fitness_function
from Fitness import funzione_di_fitness
from Fitness_Genitore_Figlio import fitness_function_parent
from Mutation import mutate, calculate_fitness_change, adaptive_mutation


def generate_population(pop_size, num_cells, total_resources, min_resources):
    """
    Genera una popolazione iniziale di dimensione `pop_size` con ciascun individuo
    composto da `num_cells`.

    Parametri:
    pop_size (int): Numero di individui nella popolazione iniziale.
    num_cells (int): Numero di celle per individuo.
    total_resources (int): Numero totale di risorse disponibili.
    min_resources (int): Risorse minime per cella (esclusa la cella 0).

    Ritorna:
    list: Lista di individui (array numpy).
    """
    import random
import numpy as np

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
            individual[i] = base_resource  # Assegniamo 20 a tutte le celle (eccetto la cella 0)
        
        # Ricalcoliamo le risorse da distribuire
        remaining_resources = risorse_totali - base_resource * (num_cells-1)  # Risorse rimanenti dopo l'assegnazione iniziale

        # Distribuire le risorse rimanenti in modo casuale
        for i in range(1, num_cells):
            if remaining_resources > 0:
                max_possible = remaining_resources
                resources = random.randint(0, 100)
                if resources > max_possible:
                    resources = max_possible
                individual[i] += resources  # Assegniamo le risorse alla cella
                remaining_resources -= resources  # Decrementiamo le risorse rimanenti


        population.append(individual)

    return population




# Parametri iniziali
POP_SIZE = 50
NUM_CELLS = 25
TOTAL_RESOURCES = 2000
MIN_RESOURCES = 20
TOURNAMENT_SIZE = 5
CROSSOVER_POINTS = 4
MAX_GENERATIONS = 100
TARGET_FITNESS = 10 # Soglia di fitness target

# Parametri di mutazione
mutation_rate = 0.02  # Tasso di mutazione iniziale
fitness_threshold = 0.02  # 2% miglioramento minimo
previous_fitness = 1  # Fitness media iniziale

# Generazione della popolazione iniziale
population = generate_population(POP_SIZE, NUM_CELLS, TOTAL_RESOURCES, MIN_RESOURCES)

# Ciclo evolutivo
for generation in range(MAX_GENERATIONS):
    print(f"\nGenerazione {generation}\n")


    # Stampa alcuni risultati di esempio per vedere la distribuzione delle risorse
    for i, individual in enumerate(population):
        print(f"Individuo {i}: {individual[:25]}... (total resources: {sum(individual)- individual[0]})")
    print("\n")
    # Valutazione della fitness degli individui
    lambda_value = 1.0  # Puoi scegliere il valore di lambda_value secondo le tue esigenze
    fitness_values = [fitness_function(individual, lambda_value, index)for index, individual in enumerate(population)]

        # Stampa migliori fitness
    min_fitness = min(fitness_values)
    print(f"\n  Fitness migliore: {min_fitness}")

    if min_fitness <= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        sys.exit()

    # Selezione con il K-Way Tournament
    selected_individuals = k_way_tournament_min(population, fitness_values, TOURNAMENT_SIZE) 

    # Crossover tra i primi due individui selezionati
    parent1 = selected_individuals[0]
    parent2 = selected_individuals[1]
    parent3 = selected_individuals[2]
    parent4 = selected_individuals[3]
    parent5 = selected_individuals[4]
    parent6 = selected_individuals[5]
    fitness_values_parent = [fitness_function_parent(parent1, lambda_value), fitness_function_parent(parent2, lambda_value), 
                             fitness_function_parent(parent3, lambda_value), fitness_function_parent(parent4, lambda_value), 
                             fitness_function_parent(parent5, lambda_value), fitness_function_parent(parent6, lambda_value)]

    # Converti i figli in liste di interi normali per la stampa
    child1, child2 = k_point_crossover(parent1, parent2, CROSSOVER_POINTS, TOTAL_RESOURCES)
    child3, child4 = k_point_crossover(parent3, parent4, CROSSOVER_POINTS, TOTAL_RESOURCES)
    child5, child6 = k_point_crossover(parent5, parent6, CROSSOVER_POINTS, TOTAL_RESOURCES)
    child1 = [int(x) for x in child1]
    child2 = [int(x) for x in child2]
    child3 = [int(x) for x in child3]
    child4 = [int(x) for x in child4]
    child5 = [int(x) for x in child5]
    child6 = [int(x) for x in child6]

    # Output per verificare
    print("\nGenitore 1 scelto dal K-Way Tournament:", parent1)
    print("\nGenitore 2 scelto dal K-Way Tournament:", parent2)
    print("\nGenitore 3 scelto dal K-Way Tournament:", parent3)
    print("\nGenitore 4 scelto dal K-Way Tournament:", parent4)
    print("\nGenitore 5 scelto dal K-Way Tournament:", parent5)
    print("\nGenitore 6 scelto dal K-Way Tournament:", parent6)
    print(f"\nFitness Genitore 1: {fitness_values_parent[0]}")
    print(f"Fitness Genitore 2: {fitness_values_parent[1]}")
    print(f"Fitness Genitore 3: {fitness_values_parent[2]}")
    print(f"Fitness Genitore 4: {fitness_values_parent[3]}")
    print(f"Fitness Genitore 5: {fitness_values_parent[4]}")
    print(f"Fitness Genitore 6: {fitness_values_parent[5]}")


    # Conserva i valori di fitness dei figli
    print(f"\nFiglio 1: {child1} ... (total resources: {sum(child1)- child1[0]})")
    print(f"\nFiglio 2: {child2} ... (total resources: {sum(child2)- child2[0]})")
    print(f"\nFiglio 3: {child3} ... (total resources: {sum(child3)- child3[0]})")
    print(f"\nFiglio 4: {child4} ... (total resources: {sum(child4)- child4[0]})")
    print(f"\nFiglio 5: {child5} ... (total resources: {sum(child5)- child5[0]})")
    print(f"\nFiglio 6: {child6} ... (total resources: {sum(child6)- child6[0]})\n")

    fitness_values_children = [fitness_function_parent(child1, lambda_value), fitness_function_parent(child2, lambda_value), 
                               fitness_function_parent(child3, lambda_value), fitness_function_parent(child4, lambda_value), 
                               fitness_function_parent(child5, lambda_value), fitness_function_parent(child6, lambda_value)]
    
    print(f"\nFitness Figlio 1: {fitness_values_children[0]}")
    print(f"Fitness Figlio 2: {fitness_values_children[1]}")
    print(f"Fitness Figlio 3: {fitness_values_children[2]}")
    print(f"Fitness Figlio 4: {fitness_values_children[3]}")
    print(f"Fitness Figlio 5: {fitness_values_children[4]}")
    print(f"Fitness Figlio 6: {fitness_values_children[5]}")

      # Controlla se la fitness dei figli soddisfa la soglia
    if min(fitness_values_children) <= TARGET_FITNESS:
        print(f"\n>>> Soluzione ottimale trovata alla generazione {generation}!")
        print(f"\nFiglio con la fitness ottimale: {min(fitness_values_children)}")
        sys.exit()

    # Calcolo della fitness corrente prima della mutazione
    current_fitness = (fitness_function_parent(child1, lambda_value) + fitness_function_parent(child2, lambda_value)+
                       fitness_function_parent(child3, lambda_value)+fitness_function_parent(child4, lambda_value)+
                       fitness_function_parent(child5, lambda_value)+fitness_function_parent(child6, lambda_value)) / 6

    # Applica mutazione ai figli
    childmutate1 = mutate(child1, mutation_rate)
    childmutate2 = mutate(child2, mutation_rate)
    childmutate3 = mutate(child3, mutation_rate)
    childmutate4 = mutate(child4, mutation_rate)
    childmutate5 = mutate(child5, mutation_rate)
    childmutate6 = mutate(child6, mutation_rate)

    # Calcolo dei valori di fitness per i figli mutati
    fitness_values_mutate = [
    fitness_function_parent(childmutate1, lambda_value),
    fitness_function_parent(childmutate2, lambda_value),
    fitness_function_parent(childmutate3, lambda_value),
    fitness_function_parent(childmutate4, lambda_value),
    fitness_function_parent(childmutate5, lambda_value),
    fitness_function_parent(childmutate6, lambda_value)
]

    # Stampa dei valori di fitness per i figli mutati
    print(f"\nFiglio 1 (Mutato): {childmutate1} ... (total resources: {sum(childmutate1)- childmutate1[0]})")
    print(f"\nFiglio 2 (Mutato): {childmutate2} ... (total resources: {sum(childmutate2)- childmutate2[0]})")
    print(f"\nFiglio 3 (Mutato): {childmutate3} ... (total resources: {sum(childmutate3)- childmutate3[0]})")
    print(f"\nFiglio 4 (Mutato): {childmutate4} ... (total resources: {sum(childmutate4)- childmutate4[0]})")
    print(f"\nFiglio 5 (Mutato): {childmutate5} ... (total resources: {sum(childmutate5)- childmutate5[0]})")
    print(f"\nFiglio 6 (Mutato): {childmutate6} ... (total resources: {sum(childmutate6)- childmutate6[0]})")
    print(f"\nFitness Figlio 1 (Mutato): {fitness_values_mutate[0]}")
    print(f"Fitness Figlio 2 (Mutato): {fitness_values_mutate[1]}")
    print(f"Fitness Figlio 3 (Mutato): {fitness_values_mutate[2]}")
    print(f"Fitness Figlio 4 (Mutato): {fitness_values_mutate[3]}")
    print(f"Fitness Figlio 5 (Mutato): {fitness_values_mutate[4]}")
    print(f"Fitness Figlio 6 (Mutato): {fitness_values_mutate[5]}")

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