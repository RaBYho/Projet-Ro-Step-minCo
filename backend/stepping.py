import numpy as np
from collections import deque


def trouver_cycle(flux, start_node):
    """
    Trouve le cycle MINIMAL de Stepping Stone (BFS → plus court en premier).
    """
    lignes, colonnes = flux.shape
    base = set(
        (r, c)
        for r in range(lignes)
        for c in range(colonnes)
        if flux[r, c] > 1e-12
    )
    base.add(start_node)

    def voisins(node, axis, path_set):
        return [
            n for n in base
            if n != node
            and n[axis] == node[axis]
            and (n not in path_set or n == start_node)
        ]

    file = deque([([start_node], 0)])
    while file:
        path, axis = file.popleft()
        current    = path[-1]
        path_set   = set(path)

        for neighbor in voisins(current, axis, path_set):
            if neighbor == start_node:
                if len(path) >= 4:
                    return path
                continue
            if flux[neighbor[0], neighbor[1]] <= 1e-12 and neighbor != start_node:
                continue
            new_path = path + [neighbor]
            if len(new_path) <= 2 * (lignes + colonnes):
                file.append((new_path, 1 - axis))
    return None


def calculer_couts_marginaux(cost, flux):
    lignes, colonnes = flux.shape
    u = [None] * lignes
    v = [None] * colonnes
    u[0] = 0

    changed = True
    while (None in u or None in v) and changed:
        changed = False
        for i in range(lignes):
            for j in range(colonnes):
                if flux[i, j] > 1e-12:
                    if u[i] is not None and v[j] is None:
                        v[j] = float(cost[i, j]) - u[i]
                        changed = True
                    elif v[j] is not None and u[i] is None:
                        u[i] = float(cost[i, j]) - v[j]
                        changed = True

    indices = np.zeros((lignes, colonnes))
    for i in range(lignes):
        for j in range(colonnes):
            if flux[i, j] <= 1e-12:
                if u[i] is not None and v[j] is not None:
                    indices[i, j] = cost[i, j] - (u[i] + v[j])

    return indices, u, v


def calculer_details_indices(cost, flux, u, v, theta_preview=None):
    """
    Retourne la liste detaillee des indices marginaux pour les cases vides.
    Le gain = |delta_ij| * theta est calcule si theta_preview est fourni,
    sinon on estime theta en cherchant le cycle pour chaque case candidate.
    Pour la performance, on calcule theta seulement pour les cases negatives.
    """
    lignes, colonnes = flux.shape
    details = []

    for i in range(lignes):
        for j in range(colonnes):
            if flux[i, j] <= 1e-12:
                ui     = u[i] if u[i] is not None else 0.0
                vj     = v[j] if v[j] is not None else 0.0
                cij    = float(cost[i, j])
                indice = cij - (ui + vj)

                # Calculer theta reel pour les cases negatives (candidates au pivot)
                gain   = 0.0
                theta  = 0.0
                if indice < -1e-9:
                    cycle = trouver_cycle(flux, (i, j))
                    if cycle and len(cycle) >= 4:
                        cases_moins   = [
                            (r, c) for idx, (r, c) in enumerate(cycle) if idx % 2 == 1
                        ]
                        valeurs_moins = [float(flux[r, c]) for r, c in cases_moins]
                        theta  = float(min(valeurs_moins))
                        gain   = abs(indice) * theta

                details.append({
                    "i":         int(i),
                    "j":         int(j),
                    "cout":      cij,
                    "u":         float(ui),
                    "v":         float(vj),
                    "indice":    float(indice),
                    "theta":     float(theta),
                    "gain":      float(gain),
                    "formule":   f"{cij:.0f} - ({ui:.0f} + {vj:.0f})",
                    "formule_gain": f"|{indice:.2f}| × {theta:.2f}" if gain > 0 else "—"
                })

    # Trier par gain décroissant (meilleur gain en tête), puis par indice croissant
    details.sort(key=lambda x: (-x["gain"], x["indice"]))
    return details


def corriger_degenerescence(flux, n_lignes, n_colonnes):
    """
    Ajoute des epsilon sur des cases vides pour atteindre m+n-1 cases de base.
    Retourne (flux_corrige, cases_epsilon) où cases_epsilon est la liste
    des cases [i, j] auxquelles un epsilon a été ajouté.
    """
    n_cases_remplies = int(np.sum(flux > 1e-12))
    n_requises       = n_lignes + n_colonnes - 1
    cases_epsilon    = []

    if n_cases_remplies < n_requises:
        for i in range(n_lignes):
            for j in range(n_colonnes):
                if flux[i, j] <= 1e-12:
                    flux[i, j]  = 1e-10
                    cases_epsilon.append([int(i), int(j)])
                    n_cases_remplies += 1
                    if n_cases_remplies == n_requises:
                        return flux, cases_epsilon

    return flux, cases_epsilon