# Lancement du serveur

L'interface web du cursus se lance depuis cette racine du workspace.

## Accès en ligne (GitHub Pages)

Une fois le repo public et Pages activé (branche `main`, racine), l'interface est aussi accessible sans serveur local :

- **En ligne** : https://relbolio.github.io/cursus-allemand/site/
- Différences : l'icône 📱 (IP locale) est masquée — normal, `/config.json` n'existe qu'avec `serveur.py` ; l'onglet Leçons, le journal et les ressources fonctionnent à l'identique.

## Démarrer

Double-cliquez sur **`serveur.bat`** depuis l'Explorateur Windows, ou en ligne de commande :

```
serveur.bat
```

Cela exécute `python serveur.py` (Python 3.10+, bibliothèque standard uniquement).

- Première fois : le pare-feu Windows demande l'accès — cochez **Réseaux privés** puis Autoriser.
- La console affiche les deux URLs :
  - **PC** : http://localhost:8080/site/
  - **Téléphone** (même Wi-Fi) : `http://IP-du-PC:8080/site/` — l'IP est détectée automatiquement et affichée, ainsi qu'en haut de l'interface (icône 📱).

## Utiliser

- Onglets : **Tableau** (gates A1→B2, prochaine étape, compteurs), **Leçons** (sidebar leçons + références, lecture intégrée), **Journal** (NOTES.md + learning-records), **Ressources** (RESOURCES.md, recherche filtrante).
- L'onglet actif est mémorisé dans l'URL (`#tableau`, `#lecons`, …).

## Arrêter

`Ctrl+C` dans la console, ou fermez-la.

## Dépannage

- `python` absent → essayez `py serveur.py`.
- Lien téléphone absent (icône 📱 vide) → le serveur lancé est `http.server` brut ; relancez via `serveur.bat`.
- Le port 8080 est occupé → fermez l'autre serveur python, ou changez `PORT` dans `serveur.py`.
