from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np

from initialisation import methode_cout_minimal
from stepping import (trouver_cycle, calculer_couts_marginaux,
                      calculer_details_indices, corriger_degenerescence)
from graphe import generer_graphe

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class DonneesTransport(BaseModel):
    couts:    list[list[float]]
    offres:   list[float]
    demandes: list[float]


def convertir_numpy(obj):
    if isinstance(obj, np.integer):  return int(obj)
    if isinstance(obj, np.floating): return float(obj)
    if isinstance(obj, np.ndarray):  return obj.tolist()
    if isinstance(obj, list):        return [convertir_numpy(i) for i in obj]
    if isinstance(obj, tuple):       return [convertir_numpy(i) for i in obj]
    if isinstance(obj, dict):        return {k: convertir_numpy(v) for k, v in obj.items()}
    return obj

@app.get("/")
def health_check():
    return {"status": "online", "message": "API de Recherche Opérationnelle fonctionnelle"}

@app.post("/resoudre")
def resoudre_complet(data: DonneesTransport):
    cost  = np.array(data.couts)
    offer = np.array(data.offres,   dtype=float)
    need  = np.array(data.demandes, dtype=float)

    if cost.shape != (len(offer), len(need)):
        return {"erreur": f"La matrice doit être {len(offer)}x{len(need)}"}
    if round(float(sum(offer)), 6) != round(float(sum(need)), 6):
        return {"erreur": f"Problème non équilibré : offre={sum(offer):.0f} ≠ demande={sum(need):.0f}"}

    l_cost, c_cost    = cost.shape
    noms_sources      = [f"Usine {i+1}"  for i in range(len(offer))]
    noms_destinations = [f"Client {j+1}" for j in range(len(need))]

    # ── INITIALISATION ────────────────────────────────────────────────────────
    flux, historique_init = methode_cout_minimal(cost, offer, need)

    # Pas encore d'epsilon pendant l'init
    for etp in historique_init:
        etp["graphe"]        = generer_graphe(np.array(etp["flux"]), noms_sources, noms_destinations)
        etp["cases_epsilon"] = []

    # ── DÉGÉNÉRESCENCE ────────────────────────────────────────────────────────
    flux, cases_epsilon = corriger_degenerescence(flux, l_cost, c_cost)

    etape_degenere = None
    if cases_epsilon:
        etape_degenere = {
            "type":          "DEGENERESCENCE",
            "cases_epsilon": [list(ce) for ce in cases_epsilon],
            # flux ICI contient déjà les epsilon → c'est le flux à afficher
            "flux":          flux.copy().tolist(),
            "message": (
                f"Dégénérescence : {int(np.sum(flux > 1e-12)) - len(cases_epsilon)} cases "
                f"au lieu de {l_cost + c_cost - 1} requises. "
                f"{len(cases_epsilon)} nœud(s) ε ajouté(s) : "
                + ", ".join(f"[U{i+1},C{j+1}]" for i, j in cases_epsilon)
            ),
            "graphe": generer_graphe(flux.copy(), noms_sources, noms_destinations)
        }

    # ── OPTIMISATION ──────────────────────────────────────────────────────────
    historique_opti = []
    cout_courant    = float(np.sum(flux * cost))
    max_iter        = 50

    for iteration in range(max_iter):

        indices, u, v   = calculer_couts_marginaux(cost, flux)
        details_indices = calculer_details_indices(cost, flux, u, v)

        # Sélection par GAIN MAXIMAL = |Δ| × θ
        # candidats = [d for d in details_indices if d["gain"] > 1e-9]
        candidats = [d for d in details_indices if d["gain"] < -1e-9]
        # ── Cas optimal ───────────────────────────────────────────────────────
        if not candidats:
            historique_opti.append({
                "type":            "OPTIMISATION",
                "iteration":       iteration + 1,
                "optimal":         True,
                "potentiels":      {"u": [float(x) if x is not None else None for x in u],
                                    "v": [float(x) if x is not None else None for x in v]},
                "details_indices": details_indices,
                "meilleur_indice": None,
                "cycle":           None,
                "theta":           None,
                "flux_avant":      flux.copy().tolist(),
                "cout_avant":      cout_courant,
                "flux_apres":      flux.copy().tolist(),
                "cout_apres":      cout_courant,
                "reduction_cout":  0.0,
                # Epsilon encore vivants à cette étape
                "cases_epsilon":   [list(ce) for ce in cases_epsilon],
                "graphe":          generer_graphe(flux.copy(), noms_sources, noms_destinations)
            })
            break

        # ── Pivot : case avec le gain maximal ─────────────────────────────────
        meilleur = candidats[0]    # trié par gain décroissant
        i_start  = meilleur["i"]
        j_start  = meilleur["j"]

        for d in details_indices:
            d["est_meilleur"] = (d["i"] == i_start and d["j"] == j_start)

        # Cycle
        cycle = trouver_cycle(flux, (i_start, j_start))
        if not cycle or len(cycle) < 4:
            break
        cycle_natif = [(int(r), int(c)) for r, c in cycle]

        # Theta et case sortante
        cases_moins   = [(r, c) for idx, (r, c) in enumerate(cycle_natif) if idx % 2 == 1]
        valeurs_moins = [float(flux[r, c]) for r, c in cases_moins]
        theta         = float(min(valeurs_moins))
        case_sortante = cases_moins[valeurs_moins.index(theta)]
        gain_reel     = float(indices[i_start, j_start]) * theta

        flux_avant   = flux.copy().tolist()
        cout_avant   = cout_courant
        graphe_avant = generer_graphe(flux.copy(), noms_sources, noms_destinations)
        # Epsilon AVANT le pivot (pour que la matrice/graphe les montre pendant ce pivot)
        epsilon_avant = [list(ce) for ce in cases_epsilon]

        # Mise à jour flux
        for idx, (r, c) in enumerate(cycle_natif):
            if idx % 2 == 0:
                flux[r, c] += theta
            else:
                flux[r, c] -= theta
                if flux[r, c] < 1e-10:
                    flux[r, c] = 0.0

        # Retirer les epsilon qui ont été éliminés (flux → 0)
        cases_epsilon = [
            ce for ce in cases_epsilon
            if flux[ce[0], ce[1]] > 1e-12
        ]

        cout_apres   = float(np.sum(flux * cost))
        reduction    = cout_avant - cout_apres
        cout_courant = cout_apres

        historique_opti.append({
            "type":      "OPTIMISATION",
            "iteration": iteration + 1,
            "optimal":   False,

            "potentiels": {"u": [float(x) if x is not None else None for x in u],
                           "v": [float(x) if x is not None else None for x in v]},
            "details_indices": details_indices,

            "meilleur_indice": {
                "i":            i_start,
                "j":            j_start,
                "valeur":       float(indices[i_start, j_start]),
                "formule":      meilleur["formule"],
                "theta":        theta,
                "gain":         gain_reel,
                "formule_gain": f"{indices[i_start,j_start]:.2f} × {theta:.2f} = {gain_reel:.2f}"
            },

            "cycle":         cycle_natif,
            "theta":         theta,
            "case_sortante": [int(case_sortante[0]), int(case_sortante[1])],

            "flux_avant":     flux_avant,
            "cout_avant":     cout_avant,
            "flux_apres":     flux.copy().tolist(),
            "cout_apres":     cout_apres,
            "reduction_cout": reduction,

            # Epsilon AVANT ce pivot (visibles dans la matrice/graphe pendant cette étape)
            "cases_epsilon": epsilon_avant,

            "graphe": graphe_avant
        })

    # ── ASSEMBLAGE FINAL ──────────────────────────────────────────────────────
    etapes = historique_init
    if etape_degenere:
        etapes = etapes + [etape_degenere]
    etapes = etapes + historique_opti

    reponse = {
        "config":   {"couts": cost.tolist(), "offres": offer.tolist(), "demandes": need.tolist()},
        "metadata": {"sources": noms_sources, "destinations": noms_destinations},
        "etapes":   etapes,
        "final": {
            "flux":          flux.tolist(),
            "cout_total":    float(np.sum(flux * cost)),
            "cases_epsilon": []
        }
    }
    return convertir_numpy(reponse)