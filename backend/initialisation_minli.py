import numpy as np

def methode_cout_minimal(cost, offer, need):
    l_cost, c_cost = cost.shape
    flux = np.zeros((l_cost, c_cost))
    
    # On travaille sur des copies pour ne pas détruire les données originales
    s = offer.copy()
    n = need.copy()
    historique_init = []

    for j in range(c_cost):
        while n[j] > 0:
            col_temp = cost[:, j].copy().astype(float)
            # On ignore les usines sans stock
            col_temp[s <= 0] = np.inf#in ty?
            
            i = int(np.argmin(col_temp))#
            
            if col_temp[i] == np.inf:
                break
                
            qty = float(min(s[i], n[j]))
            flux[i, j] += qty
            s[i] -= qty
            n[j] -= qty

            # On enregistre chaque étape pour l'interface Vue.js
            historique_init.append({
                "type": "INITIALISATION",
                "message": f"Source {i} -> Destination {j}",
                "flux": flux.copy().tolist(),
                "offre_restante": s.tolist(),
                "demande_restante": n.tolist(),
                "case_active": [i, j]
            })
            
    return flux, historique_init