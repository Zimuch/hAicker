def normalize(values):
    min_value = min(values)  # Trova il valore minimo tra tutti i valori di W
    max_value = max(values)  # Trova il valore massimo tra tutti i valori di W
    if max_value == min_value:
        return [0.0 for _ in values]  # Se tutti i valori sono uguali, restituisci un campo di zeri
<<<<<<< HEAD
    return [(x - min_value) / (max_value - min_value) for x in values]
=======
    return [(x - min_value) / (max_value - min_value) for x in values]
>>>>>>> bc723030643b27944c30e31c1e6da9459172c4fb
