# Algoritmo di selezione K-Way Tournament
def k_way_tournament(population, k, fitness_function):
    selected = []
    for _ in range(len(population)):
        tournament = random.sample(population, k)
        winner = max(tournament, key=fitness_function)
        selected.append(winner)
    return selected