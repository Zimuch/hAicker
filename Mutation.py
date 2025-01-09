import random

# Parametri iniziali
mutation_rate = 0.02
fitness_threshold = 0.02  # 2% miglioramento minimo

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
    """Esegue la mutazione su un individuo."""
    mutated_individual = individual[:]
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            mutated_value = individual[i] + random.randint(-10, 10)
            # Assicura che il valore mutato non sia negativo, non sia minore di 20 e sia intero
            mutated_value = max(20, mutated_value)
            mutated_individual[i] = mutated_value
    return mutated_individual

