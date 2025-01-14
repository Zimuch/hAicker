import random
import numpy as np

def generate_population(pop_size, num_cells, total_resources, min_resources, RANDOM_RESOURCES):
    """
    Genera una popolazione iniziale di dimensione `pop_size` con ciascun individuo
    composto da `num_cells`.

    Parametri:
    pop_size (int): Numero di individui nella popolazione iniziale.
    num_cells (int): Numero di celle per individuo.
    total_resources (int): Numero totale di risorse disponibili.
    min_resources (int): Risorse minime per cella (esclusa la cella 0).
    RANDOM_RESOURCES (int): Risorse casuali per la distribuzione.

    Ritorna:
    list: Lista di individui (array numpy).
    """

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
                resources = random.randint(0, RANDOM_RESOURCES)
                if resources > max_possible:
                    resources = max_possible
                individual[i] += resources  # Assegniamo le risorse alla cella
                remaining_resources -= resources  # Decrementiamo le risorse rimanenti


        population.append(individual)

    return population