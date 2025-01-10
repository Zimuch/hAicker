def dominates(ind1, ind2):
    """
    Verifica se l'individuo ind1 domina l'individuo ind2 in un contesto multi-obiettivo.
    Ogni individuo è un array di valori di risorse allocate.
    
    :param ind1: primo individuo (lista dei valori di fitness per ogni cella)
    :param ind2: secondo individuo (lista dei valori di fitness per ogni cella)
    :return: True se ind1 domina ind2, False altrimenti
    """
    # Supponiamo che entrambi gli individui abbiano la stessa lunghezza (NUM_CELLS)
    # Confrontiamo i valori in ciascuna cella per determinare la dominanza
    better_in_one = False
    for r1, r2 in zip(ind1, ind2):
        if r1 < r2:
            # ind1 è peggiore di ind2 in questo obiettivo
            return False
        elif r1 > r2:
            # ind1 è migliore di ind2 in questo obiettivo
            better_in_one = True

    # Se ind1 è migliore in almeno un obiettivo e non peggiore in nessun obiettivo, domina ind2
    return better_in_one
