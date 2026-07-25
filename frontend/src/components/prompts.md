**ASK**

Modifie chaque fichier dans ce repertoire pour reparer un bug

**CONTEXT**

- Je devellope un Application frontend sous vueJS + TailWindCSS
- le mode sombre bug
- Certains fichier sont de format dark:classCSS
- un variable isDark gere deja le mode sombre
- ton but et de reparer ce bug

**CONTRAINT**

- ne modifie que seulement les fichier dans ce repertoire
- la modificaiton doit correspondre a l'example que je donne
- ne copie pas exactement l'example

**EXEMPLE**

- avant :
<h3 class="text-xs font-semibold text-stone-500 dark:text-stone-400 uppercase tracking-wider mb-3">

- apres :
<h3 class="text-xs font-semibold uppercase tracking-wider mb-3" :class="isDark ? 'text-stone-400': 'text-stone-500'">
