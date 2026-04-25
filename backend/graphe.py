def generer_graphe(flux, noms_sources, noms_destinations):
    liens = []
    lignes, colonnes = flux.shape
    for i in range(lignes):
        for j in range(colonnes):
            if flux[i, j] > 0:
                liens.append({
                    "source": noms_sources[i],
                    "target": noms_destinations[j],
                    "valeur": float(flux[i, j])
                })
    return liens