# Lancement du serveur

L'interface web du cursus se lance depuis cette racine du workspace.

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
