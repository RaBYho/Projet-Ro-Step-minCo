# Probleme de transport — Méthode du coût minimal + Stepping Stone

Application web pédagogique de résolution du **problème de transport** en Recherche Opérationnelle. Elle implémente la méthode du coût minimal pour l'initialisation et l'algorithme du Stepping Stone pour l'optimisation, avec une visualisation étape par étape.

---

## Aperçu

| Saisie des données | Résolution étape par étape | Graphe de flux |
|---|---|---|
| Tableau dynamique m×n | Navigation avant/arrière + lecture auto | Potentiels u, v sur les nœuds |

**Fonctionnalités principales :**
- Saisie interactive du tableau (2×2 à 6×6), avec exemples prédéfinis dont un cas dégénéré 5×4
- Initialisation par la méthode du coût minimal
- Détection et correction automatique de la dégénérescence (ajout de nœuds ε visibles)
- Optimisation par Stepping Stone avec sélection du pivot par gain minimal (Δ × θ)
- Affichage détaillé des potentiels u, v, des indices marginaux Δ et des gains à chaque itération
- Visualisation matricielle et graphe biparti SVG avec les potentiels sur les nœuds
- Mode clair / mode sombre
- Interface responsive (mobile et desktop)

---

## Architecture

```
projet/
├── backend/
│   ├── main.py              # API FastAPI — endpoint POST /resoudre
│   ├── initialisation.py    # Méthode du coût minimal
│   ├── stepping.py          # Potentiels, indices marginaux, cycle BFS, dégénérescence
│   └── graphe.py            # Génération des liens pour le graphe
│
└── frontend/
    └── src/
        ├── App.vue                      # Orchestration des phases + dark mode
        └── components/
            ├── FormulaireTransport.vue  # Saisie du tableau
            ├── AffichageEtapes.vue      # Navigation étapes + barre de progression
            ├── PanneauOptimisation.vue  # Détail d'une itération Stepping Stone
            ├── PanneauDegenerescence.vue# Visualisation du cas dégénéré
            ├── MatriceFlux.vue          # Matrice avec surbrillance cycle / ε
            ├── GrapheFlux.vue           # Graphe SVG biparti (flux ou potentiels)
            ├── LoaderAnimation.vue      # Animation de chargement
            └── DimControle.vue          # Boutons +/− dimensions
```

---

## Algorithme

### 1. Initialisation — méthode du coût minimal

À chaque étape, on cherche la colonne libre avec le **coût le plus bas** dans toute la matrice, on y affecte `min(offre_restante, demande_restante)`, puis on met à jour les offres et demandes. On répète jusqu'à ce que tout soit alloué.

### 2. Dégénérescence

Un problème m×n doit avoir exactement **m + n − 1** cases de base. Si une ligne et une colonne s'épuisent simultanément lors de l'initialisation, on se retrouve avec trop peu de cases. On ajoute alors des cases **epsilon ε** (flux fictif ≈ 10⁻¹⁰) pour atteindre le nombre requis, ce qui permet de calculer les potentiels sans bloquer l'algorithme.

### 3. Optimisation — Stepping Stone

À chaque itération :

**a) Calcul des potentiels u, v**
La case de base avec le **coût maximal** reçoit `u = 0`. On propage ensuite :
```
v[j] = u[i] + c[i][j]
u[i] = v[j] - c[i][j]
```

**b) Calcul des indices marginaux**
Pour chaque case vide :
```
rho(U,C) = u[i] + c[i][j] − v[j]
```

**c) Sélection du pivot**
On calcule le **gain** de chaque case candidate (ρ < 0) :
```
Gain = rho × θ   (négatif — le plus petit = meilleur)
```
La case avec le gain minimal entre dans la base.

**d) Cycle Stepping Stone (BFS)**
On trouve le cycle minimal (≥ 4 nœuds) qui alterne lignes et colonnes via un parcours en largeur — ce qui garantit de trouver le rectangle le plus court.

**e) Mise à jour du flux**
```
Cases + (positions paires)  : flux += θ
Cases - (positions impaires) : flux -= θ
```
La case qui atteint 0 sort de la base. Les ε éliminés disparaissent également.

**f) Critère d'arrêt**
Si tous les ρ≥ 0, la solution est optimale.

---

## Installation

### Prérequis

- Python 3.10+
- Node.js 18+
- npm ou yarn

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install fastapi uvicorn numpy
uvicorn main:app --reload
```

L'API tourne sur `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

L'application tourne sur `http://localhost:5173`.

> **Note :** Tailwind CSS v4 est requis. Les classes `@apply` avec modificateurs responsive ne sont pas utilisées — tout est en classes inline dans les templates Vue.

---

## API

### `POST /resoudre`

**Corps de la requête :**
```json
{
  "couts":    [[2, 3, 1], [5, 4, 8]],
  "offres":   [100, 200],
  "demandes": [80, 120, 100]
}
```

**Réponse :**
```json
{
  "config":   { "couts": [...], "offres": [...], "demandes": [...] },
  "metadata": { "sources": ["Usine 1", ...], "destinations": ["Client 1", ...] },
  "etapes": [
    {
      "type": "INITIALISATION",
      "message": "Source 0 -> Destination 2",
      "flux": [[...]],
      "case_active": [0, 2],
      "offre_restante": [...],
      "demande_restante": [...],
      "cases_epsilon": [],
      "graphe": [...]
    },
    {
      "type": "DEGENERESCENCE",
      "cases_epsilon": [[0, 1]],
      "flux": [[...]],
      "message": "...",
      "graphe": [...]
    },
    {
      "type": "OPTIMISATION",
      "iteration": 1,
      "optimal": false,
      "potentiels": { "u": [0, -4], "v": [3, 8, 1] },
      "details_indices": [
        {
          "i": 0, "j": 1,
          "cout": 3, "u": 0, "v": 8,
          "indice": -5.0,
          "theta": 80.0,
          "gain": -400.0,
          "formule": "0 + 3 - 8",
          "est_meilleur": true
        }
      ],
      "meilleur_indice": { "i": 0, "j": 1, "valeur": -5.0, "formule": "0 + 3 - 8", "gain": -400.0 },
      "cycle": [[0,1],[0,0],[1,0],[1,1]],
      "theta": 80.0,
      "case_sortante": [1, 0],
      "flux_avant": [[...]],
      "cout_avant": 1420.0,
      "flux_apres": [[...]],
      "cout_apres": 1020.0,
      "reduction_cout": 400.0,
      "cases_epsilon": [],
      "graphe": [...]
    }
  ],
  "final": {
    "flux": [[...]],
    "cout_total": 1020.0,
    "cases_epsilon": []
  }
}
```

---

## Stack technique

| Couche | Technologie |
|---|---|
| Backend | Python · FastAPI · NumPy |
| Frontend | Vue 3 (Composition API) · Vite |
| Style | Tailwind CSS v4 |
| Graphe | SVG natif (pas de lib externe) |
| Communication | REST JSON (fetch) |

---

## Exemples prédéfinis

| Nom | Taille | Particularité |
|---|---|---|
| 2×3 Basique | 2 usines · 3 clients | Cas simple |
| 3×3 Classique | 3 usines · 3 clients | Plusieurs itérations |
| 3×4 Grand | 3 usines · 4 clients | Cycle à 6 nœuds possible |
| 2×2 Minimal | 2 usines · 2 clients | Cas trivial |
| 5×4 Cas dégénéré | 5 usines · 4 clients | Déclenche la correction ε |

---

## Auteur
RaBYho
Projet de Recherche Opérationnelle — Problème de Transport
