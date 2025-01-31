import numpy as np
from Obiettivo1 import obiettivo1_danni
from Obiettivo2 import obiettivo2_costo
from Obiettivo3 import obiettivo3_distribuzione

def fitness_combinata(individual, lambda_value1, lambda_value2, lambda_value3, omega1, omega2, omega3):
    """
    Calcola il punteggio fitness di un individuo.

    
    Args:
        individual: Lista di risorse allocate per ogni ranking, dove individual[0] rappresenta il totale di risorse.
        lambda_value1: Valore di correzione per la vulnerabilità (obiettivo 1).
        lambda_value2: Valore di correzione per la vulnerabilità (obiettivo 3).
        omega1: Peso per l'obiettivo 1.
        omega2: Peso per l'obiettivo 2.
        omega3: Peso per l'obiettivo 3

    Returns:
        Punteggio fitness calcolato.
    """
    # Calcolo delle fitness per gli obiettivi
    fitness1 = obiettivo1_danni(individual, lambda_value1)
    fitness2 = obiettivo2_costo(individual,lambda_value2)
    fitness3 = obiettivo3_distribuzione(individual, lambda_value3)

    # Calcolo della fitness combinata
    fitness = (omega2 * fitness2 + omega3 * fitness3) - omega1 * fitness1

    return fitness
 