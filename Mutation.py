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
            # Esempio: inverte il valore del gene (binary flip)
            mutated_individual[i] = 1 - mutated_individual[i]  # Cambia secondo il tuo caso
    return mutated_individual

# Esempio di utilizzo in un ciclo generazionale
previous_fitness = 0.0  # Fitness media iniziale
for generation in range(1, 101):  # 100 generazioni
    # Valuta la fitness corrente (esempio: somma fitness di tutti gli individui)
    current_fitness = random.uniform(0.5, 1.0)  # Simulazione di un valore
    
    # Calcola la variazione di fitness
    fitness_change = calculate_fitness_change(previous_fitness, current_fitness)

    # Aggiorna il tasso di mutazione
    mutation_rate = adaptive_mutation(mutation_rate, fitness_change, fitness_threshold)

    print(f"Generazione {generation} - Fitness Change: {fitness_change:.4f}, Mutation Rate: {mutation_rate:.4f}")

    # Aggiorna la fitness precedente per la prossima iterazione
    previous_fitness = current_fitness

