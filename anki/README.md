# Cartes Anki du cours

Une source unique par leçon : `leconNN-general.txt` (vocabulaire général et phrases modèles) et
`leconNN-it.txt` (vocabulaire informatique / travail). Format `recto;verso`, UTF-8, avec un en-tête
de métadonnées en commentaires `#` (titre, deck, niveau, leçon, type). Anki ignore les lignes `#`.

À partir de ces fichiers, `python build_anki.py` (racine du workspace, aucune dépendance) génère :

| Fichier | Contenu |
|---|---|
| `leconNN-*.apkg` | un paquet Anki par fichier texte, deck hiérarchisé (`Allemand A1::L02 …`, `Allemand IT::L02 …`) |
| `allemand-tout.apkg` | tous les decks en un seul paquet |
| `index.json` | manifeste lu par l'onglet **Anki** du site (titres, compteurs, chemins) |

Chaque note produit deux cartes : **Français → Allemand** (production, prioritaire) et **Allemand → Français**.
Les identifiants sont stables : réimporter un paquet régénéré n'ajoute que les nouvelles cartes et conserve la progression.

## Réviser à distance (site)

Onglet **Anki** du site (`site/index.html`, en ligne sur GitHub Pages) :

- **Réviser ici** : réviseur intégré (répétition espacée type SM-2, quatre boutons Encore / Difficile / Bien / Facile,
  voix allemande si le navigateur en a une, raccourcis Espace et 1-4). La progression est stockée dans le navigateur ;
  boutons Exporter / Importer pour la transférer d'un appareil à l'autre.
- **.apkg** : un clic télécharge le paquet ; l'ouvrir l'importe dans Anki (PC) ou AnkiDroid (Android).
  Sur iPhone, AnkiMobile est payant : utiliser le réviseur intégré.
- **.txt** : la source brute, importable à la main (séparateur point-virgule).

## Règle du cours

10 minutes par jour, tous les jours, dans le sens français → allemand d'abord. Dire la réponse à voix haute avant
de la retourner. Les noms sont donnés avec leur article et leur pluriel : apprendre le genre avec le mot, jamais séparément.

## Ajouter une leçon (professeur)

1. Écrire `anki/leconNN-general.txt` et `anki/leconNN-it.txt` avec l'en-tête `#`.
2. `python build_anki.py`
3. Commit + push : le site et les paquets sont à jour en ligne.
