# Algoritmo di K-point Crossover
def k_point_crossover(parent1, parent2, k):
    length = len(parent1)
    crossover_points = sorted(random.sample(range(1, length), k))
    child1, child2 = parent1[:], parent2[:]
    toggle = False
    for i in range(length):
        if i in crossover_points:
            toggle = not toggle
        if toggle:
            child1[i], child2[i] = child2[i], child1[i]
    return child1, child2