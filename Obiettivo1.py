import math

def obiettivo1_danni(array, lambda_value):
    """
    Calcola il danno potenziale per ogni cella in base alla formula aggiornata,
    saltando la cella con indice 0.

    :param array: array di risorse allocate in ogni cella
    :param lambda_: parametro di scala
    :return: lista dei danni potenziali per ogni cella, esclusa la cella 0
    """
    # Lunghezza dell'array
    n = len(array)
    
    danni = []
    
    # Calcolare il danno per ogni cella, saltando la cella 0
    for i, risorse in enumerate(array):
        if i == 0:  # Salta la cella con indice 0
            continue
        ranking = i  # L'indice dell'array è il ranking
        vulnerabilità = lambda_value * (n / (ranking * math.sqrt(risorse)))
        danno = vulnerabilità / (ranking * risorse)
        danni.append(danno)

  
    return sum(danni)





