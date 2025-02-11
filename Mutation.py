import random

def calculate_fitness_change(previous_fitness, current_fitness):
    """Calcola il cambiamento relativo della fitness tra due generazioni."""
    if previous_fitness == 0:  # Evita la divisione per zero
        return float('inf')
    return (current_fitness - previous_fitness) / abs(previous_fitness)


def scramble_mutation(individual):
    """Applicazione della mutazione scramble: scambiare due valori nella lista dell'individuo."""
    i,j ,f ,g ,h, e = random.sample(range(1,len(individual)), 6) # Escludi la cella 0
    individual[i], individual[j] = individual[j], individual[i]
    individual[f], individual[g] = individual[g], individual[f]
    individual[h], individual[e] = individual[e], individual[h]
    return individual

def adaptive_mutation(population, previous_fitness, current_fitness, mutation_rate, fitness_threshold):
    """
    Modifica il tasso di mutazione in base al cambiamento della fitness,
    e applica la mutazione scramble con il tasso di mutazione adattivo a ogni individuo della popolazione.
    """
    # Calcolare il cambiamento nella fitness
    fitness_change = calculate_fitness_change(previous_fitness, current_fitness)

    # Adattare il tasso di mutazione
    if fitness_change < fitness_threshold:
        # Aumento del tasso di mutazione
        mutation_rate += 0.02
    elif fitness_change >= fitness_threshold:
        # Diminuzione del tasso di mutazione
        mutation_rate -= 0.02

    # Limita il tasso di mutazione tra 0 e 1
    mutation_rate = max(0, min(1, mutation_rate))

    # Applicare la mutazione scramble a ciascun individuo della popolazione
    new_population = []
    for individual in population:
        # Applicare la mutazione con probabilità basata sul tasso di mutazione
        if random.random() < mutation_rate:
            individual = scramble_mutation(individual)
        new_population.append(individual)

    return new_population, mutation_rate
