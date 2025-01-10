def pareto_front(population):
    """
    Calcola il primo fronte di Pareto dalla popolazione.
    
    :param population: lista di individui (ogni individuo è una tupla di fitness)
    :return: lista degli individui che formano il primo fronte di Pareto
    """
    front = []
    for ind1 in population:
        dominated = False
        for ind2 in population:
            if dominates(ind2, ind1):
                dominated = True
                break
        if not dominated:
            front.append(ind1)
    return front