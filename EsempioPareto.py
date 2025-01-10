# Ciclo evolutivo con selezione basata sulla dominanza di Pareto
for generation in range(MAX_GENERATIONS):
    # Inizio della generazione corrente
    print(f"\nGenerazione {generation}")
    
    # Valutazione della popolazione
    # Eseguiamo la valutazione di tutti gli individui della popolazione (calcolando la fitness)
    fitnesses = list(toolbox.map(toolbox.evaluate, population))  # Calcola la fitness per ogni individuo
    for ind, fit in zip(population, fitnesses):  # Assegniamo il valore di fitness calcolato a ciascun individuo
        ind.fitness.values = fit

    # Selezione della nuova generazione basata sulla dominanza di Pareto
    # Calcoliamo il primo fronte di Pareto (l'insieme di soluzioni non dominate)
    front = pareto_front(population)  # Funzione che restituisce il fronte di Pareto
    selected = front[:POP_SIZE]  # Selezioniamo il primo fronte. Se necessario, la selezione può essere mescolata

    # Applicazione di crossover e mutazione sugli individui selezionati
    # Selezioniamo i genitori per la generazione successiva
    offspring = toolbox.select(selected, len(selected))  # Selezione dei genitori
    offspring = list(toolbox.map(toolbox.clone, offspring))  # Creiamo una copia degli individui selezionati

    # Crossover: applichiamo il crossover a coppie di individui
    for child1, child2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < 0.9:  # Probabilità di crossover (90%)
            toolbox.mate(child1, child2)  # Applichiamo il crossover tra i genitori
            del child1.fitness.values, child2.fitness.values  # Rimuoviamo la fitness precedente per calcolare di nuovo

    # Mutazione: applichiamo la mutazione con probabilità
    for mutant in offspring:
        if random.random() < 0.2:  # Probabilità di mutazione (20%)
            toolbox.mutate(mutant)  # Applichiamo la mutazione
            del mutant.fitness.values  # Rimuoviamo la fitness precedente per calcolare di nuovo

    # Valutazione della nuova generazione (i figli appena creati)
    # Verifichiamo se i figli sono validi (se non sono stati valutati) e li valutiamo
    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]  # Selezioniamo gli individui non validi
    fitnesses = list(toolbox.map(toolbox.evaluate, invalid_ind))  # Calcoliamo la fitness per gli individui non validi
    for ind, fit in zip(invalid_ind, fitnesses):  # Assegniamo la fitness calcolata a ciascun individuo
        ind.fitness.values = fit

    # Sostituzione della popolazione con la nuova generazione (figli)
    # Sostituiamo tutta la popolazione con i nuovi figli generati
    population[:] = offspring

    # Output per monitorare i progressi
    # Mostriamo quante soluzioni sono nel primo fronte di Pareto per vedere i progressi
    print(f"Numero di soluzioni nel primo fronte: {len(front)}")
