import random

# Parametri iniziali
mutation_rate = 0.02
fitness_threshold = 0.02  # 2% miglioramento minimo

def scramble_mutation(individual):
    """Applicazione della mutazione scramble: scambiare due valori nella lista dell'individuo."""
    i, j , f , g = random.sample(range(1,len(individual)), 4) # Escludi la cella 0
    individual[i], individual[j] = individual[j], individual[i]
    individual[f], individual[g] = individual[g], individual[f]
    return individual,


def calculate_fitness_change(previous_fitness, current_fitness):
    """Calcola il cambiamento relativo della fitness tra due generazioni."""
    if previous_fitness == 0:  # Evita la divisione per zero
        return float('inf')
    return (current_fitness - previous_fitness) / abs(previous_fitness)

def adaptive_mutation(mutation_rate, fitness_change, fitness_threshold):
    """Modifica il tasso di mutazione in base al cambiamento della fitness."""
    if fitness_change < fitness_threshold:
        # Aumento del tasso di mutazione
        mutation_rate += 0.02
    elif fitness_change >= fitness_threshold:
        # Diminuzione del tasso di mutazione
        mutation_rate -= 0.02
    # Limita il tasso di mutazione tra 0 e 1
    mutation_rate = max(0, min(1, mutation_rate))
    return mutation_rate

def mutate(individual, mutation_rate):
    if random.random() < mutation_rate:
        scramble_mutation(individual)
    return individual
