# CLAUDE.md — Cursus allemand (workspace `teach`)

## 1. Autorité

Ce fichier gouverne tout le dépôt `cursus-allemand` (racine = ce dossier). Aucun `CLAUDE.md` parent n'existe (vérifié le 2026-09-21 jusqu'à quatre niveaux au-dessus) ; si un jour ce dossier est déplacé sous un autre dépôt, **ce fichier prévaut sur le parent pour tout ce qui touche à la pédagogie, aux fichiers du workspace et au site**, et seules les conventions git du parent pourraient s'appliquer, après décision explicite notée ici.

Ce dépôt n'est pas une application : c'est un **workspace d'apprentissage** (skill `teach`, définition dans `.claude/skills/teach/SKILL.md`) doublé d'un **site statique de suivi** publié sur GitHub Pages. Les « livrables » sont des leçons, des fiches, des cartes Anki et des enregistrements d'apprentissage. Les règles ci-dessous protègent la cohérence de cet ensemble.

## 2. Identité du projet

| Élément | Valeur | Source | Statut |
|---|---|---|---|
| Apprenant | Borel Tene, Douala (Cameroun), francophone, anglais basique, développeur logiciel | NOTES.md, LR-0002 | gelé |
| Objectif | Goethe-Zertifikat B2 (4 modules), puis TestDaF / C1 seulement après | MISSION.md | gelé |
| Pourquoi | Emploi de développeur en Allemagne | MISSION.md | gelé |
| Départ | Zéro allemand au 2026-09-03 | LR-0001 | gelé |
| Horizon B2 | 12 à 15 mois, soit sept.–déc. 2027 (examen blanc B2 semaine 63, session officielle déc. 2027 ou janv. 2028) | reference/parcours.html | convention projet |
| Rythme | 5 à 10 h / semaine ; calendrier calé sur 7 h/semaine | MISSION.md, parcours.html | convention projet (**présomption** : 7 h effectives ; si le rythme réel reste sous 5 h, le calendrier est refait, pas les portes) |
| Budget | Zéro : ressources gratuites uniquement | MISSION.md | gelé |
| Langue d'enseignement | Français, bascule progressive vers l'allemand à partir de B1 | NOTES.md | convention projet |
| Pratique orale réelle | Acceptée à partir de la fin de l'A2 (mars 2027) | MISSION.md, RESOURCES.md | convention projet |
| Site en ligne | https://relbolio.github.io/cursus-allemand/site/ (Pages, branche `main`, racine, `.nojekyll`) | SERVEUR.md | gelé |
| Serveur local | `serveur.bat` → `python serveur.py`, port 8080, `/site/` + route `/config.json` (IP LAN) | serveur.py | convention projet |
| Build | `python build.py` : découvre leçons/fiches/records, régénère Anki, synchronise `status.json` | build.py | convention projet |
| Dépôt | `origin` = github.com/Relbolio/cursus-allemand, branche `main` | git | gelé |
| Dépendances | Aucune hors bibliothèque standard Python 3.10+ (site : HTML/JS vanille, aucun CDN) | serveur.py, build_anki.py | gelé |

## 3. Documents de référence — l'ordre de préséance fait foi

Un conflit entre deux documents se règle **par le rang**, jamais par la date ni par le niveau de détail. Ce fichier n'arbitre rien lui-même : il rend les autres opposables.

| Rang | Document | Ce qu'il tranche |
|---|---|---|
| 1 | `MISSION.md` | Le pourquoi, les critères de réussite, les contraintes, le hors-périmètre. Toute leçon s'y rattache. Ne change qu'avec l'accord explicite de l'apprenant + un learning-record. |
| 2 | `learning-records/NNNN-*.md` | Ce que l'apprenant sait, a compris, a mal compris. Détermine la zone proximale de développement. Un record n'est jamais supprimé : il est marqué `superseded by LR-NNNN`. |
| 3 | `NOTES.md` | Préférences de l'apprenant, consignes de travail données au professeur, décisions pédagogiques, journal daté. |
| 4 | `reference/parcours.html` | Calendrier A1→B2, porte de passage entre niveaux, programme de grammaire par niveau, structure officielle du B2. |
| 5 | `RESOURCES.md` | Les seules sources autorisées pour les faits (examens, grammaire, vocabulaire) et les communautés. Une URL absente d'ici doit être vérifiée avant usage. |
| 6 | `.claude/skills/teach/SKILL.md` et les `*-FORMAT.md` | Philosophie et formats (mission, ressources, learning-records, glossaire). |
| 7 | `status.json`, `anki/index.json` | État machine lu par le site. **Dérivés** : ils reflètent les fichiers, ils ne décident de rien. |
| 8 | `SERVEUR.md`, `anki/README.md` | Modes d'emploi du site et de la chaîne Anki. |

## 4. Workflow projet (obligatoire)

Ce projet n'utilise pas le cycle spec → plan → tests du guide `~/.claude/commands/WORKFLOW_GUIDE.md` (il n'y a pas de feature logicielle à livrer, hors évolutions du site, voir plus bas). Le cycle obligatoire est le **cycle de leçon**, puis le **cycle de niveau**.

### 4.1 Cycle de leçon (à chaque session d'enseignement)

1. **Lire** `MISSION.md`, `NOTES.md`, les `learning-records/` et `status.json` : où en est l'apprenant, quelle est la prochaine étape annoncée.
2. **Corriger** d'abord la production envoyée par l'apprenant (texte, score de drill) ; si elle révèle une compréhension ou une misconception non triviale → nouveau `learning-records/NNNN-slug.md`.
3. **Écrire la leçon** `lessons/NNNN-slug.html` : une seule compétence, 20 à 35 min, tirée de la zone proximale, exemples personnalisés (Borel, Kamerun, Douala, Softwareentwickler), quiz à correction immédiate, exercice de production avec vérificateur, source primaire liée, rappel « pose tes questions au professeur », liens vers la leçon précédente et les fiches.
4. **Écrire ou enrichir la fiche** `reference/*.html` correspondante (l'essence compressée ; c'est ce qui sera relu, pas la leçon).
5. **Écrire les cartes** `anki/leconNN-general.txt` et `anki/leconNN-it.txt` avec l'en-tête `#` (titre, deck, niveau, lecon, type).
6. **Générer** : `python build.py` (paquets `.apkg` + `anki/index.json`, puis `status.json` : `lecons[]`, `references[]`, `records[]`, `compteurs`, `anki`, `misAJour` découverts depuis les fichiers).
7. **Compléter à la main dans `status.json`** ce que le build ne déduit pas : `positionActuelle`, `prochaineEtape`, `niveau`, `semaine`, `gates`, et `etat: "faite"` + `faiteLe` quand l'apprenant a rendu sa production.
8. **Journal** : une ligne datée dans `NOTES.md`, section Journal.
9. **Vérifier** (porte de leçon, §11), **ouvrir la leçon** dans le navigateur (`cmd //c start "" lessons\NNNN-*.html`), **commit**. Le **push** est fait par l'apprenant ou sur sa demande explicite.

Règle d'or : **la leçon N+1 n'est pas générée tant que l'apprenant n'a pas rendu la production de la leçon N** (ou dit explicitement qu'il l'a faite). Sinon les leçons s'empilent sans retour et la zone proximale est perdue.

**Exception d'avance, décidée par l'apprenant le 2026-09-23** : quand il annonce une absence (retour prévu le week-end), **une seule** leçon d'avance peut être publiée pour qu'il ne reste pas bloqué. Limite stricte : jamais deux leçons d'avance, et les productions des deux leçons sont corrigées **ensemble** au retour, avant toute leçon suivante. *Raison* : l'apprenant travaille hors session et le site est son seul support à distance ; le coût d'une leçon d'avance mal calibrée est inférieur au coût de plusieurs jours sans support.

### 4.2 Cycle de niveau (A1 → A2 → B1 → B2)

Un niveau se clôt par la **porte de passage** (`reference/parcours.html` §3), trois conditions cumulatives : Modellsatz Goethe officiel du niveau ≥ 60 % **par compétence**, test de grammaire maison ≥ 80 %, production orale enregistrée jugée « réussi » avec compte rendu écrit. Résultats consignés dans un learning-record, `status.json.gates[niveau]` passe à `reussi`, le suivant à `en-cours`. Sinon : 1 à 2 semaines de remédiation ciblée, nouvel essai sur un autre jeu d'épreuves.

### 4.3 Évolutions du site (`site/`, `serveur.py`, `build_anki.py`)

Petites évolutions outillées, sans cycle spec/plan : modifier, `node --check` sur le script extrait, servir en local et vérifier les chemins (`python -m http.server` ou `serveur.bat`), commit. Une évolution qui change le **schéma** de `status.json` ou de `anki/index.json` est une zone gelée (§8) : le site et les fichiers changent dans le même commit.

## 5. Invariants non négociables

**I1 — Pas de niveau suivant sans porte franchie.** Statut : posée (règle) / contrôle à poser.
*Raison* : l'apprenant l'a demandé explicitement ; c'est ce qui distingue ce cursus d'une consommation de leçons. Un B1 entamé sur un A2 poreux coûte des mois au B2.
*Contrôle* : `status.json.gates` — un niveau ne passe à `en-cours` que si le précédent est `reussi` **et** qu'un learning-record cite les trois scores. Aucun script ne le vérifie aujourd'hui : **A DEFINIR** — ajouter à `build_anki.py` (ou un `check.py`) une vérification de cohérence des gates avant le premier examen A1 (semaine 12).

**I2 — Aucun fait sur les examens, la grammaire ou le vocabulaire sans source dans `RESOURCES.md`.** Statut : posée.
*Raison* : la connaissance paramétrique se trompe sur les détails (durées d'épreuves, seuils, URL) et l'apprenant prépare un examen réel. La structure B2 et les estimations d'heures ont été vérifiées sur les PDF officiels le 2026-09-03.
*Contrôle* : relecture — toute leçon cite une source primaire dans son pied de page ; une URL nouvelle est testée (`curl -sL -o /dev/null -w "%{http_code}"`) avant d'être écrite. Le 2026-09-21, un lien Lingolia inventé a renvoyé 404 et a été corrigé : c'est exactement le cas que cet invariant interdit.

**I3 — Les liens Deutsche Welle pointent vers une URL de LEÇON (`/fr/<slug>/l-<id>`), jamais vers la page du cours.** Statut : posée.
*Raison* : l'apprenant a perdu du temps sur le premier lien (page cours au lieu de la leçon « Hallo! ») et l'a signalé. Les 77 URL A1 françaises sont extraites de l'API et stockées dans `reference/data/nicos-weg-a1-fr.json` ; l'index lisible est `reference/nicos-weg-a1.html`.
*Contrôle* : `grep -n "nicos-weg/c-" lessons/*.html` doit ne rien renvoyer (seul `RESOURCES.md` et l'index peuvent citer la page cours).

**I4 — `anki/*.txt` est la source unique des cartes ; les `.apkg` et `index.json` sont générés, jamais édités à la main.** Statut : posée.
*Raison* : les identifiants (deck, modèle, GUID) sont dérivés des noms dans `build_anki.py` ; une édition manuelle casse la stabilité qui permet à l'apprenant de réimporter sans perdre sa progression.
*Contrôle* : `python build_anki.py` régénère tout ; un `.apkg` modifié à la main est écrasé au prochain build. Vérification : `git diff --stat anki/*.apkg` n'est jamais non vide sans modification d'un `.txt` dans le même commit.

**I5 — Ce que le site affiche vient des fichiers, pas de valeurs saisies.** Statut : posée.
*Mécanisme* : `build.py` lit `<title>`, le kicker (« Niveau A1 · ≈ 35 minutes ») et « Leçon créée le … » des leçons, `<meta name="niveau">` des fiches, la première ligne `# ` des records ; une leçon sans kicker conforme est classée A1 par défaut, une fiche sans meta est « Transversal ».
*Raison* : `site/index.html` lit `status.json`, `anki/index.json`, `NOTES.md`, `RESOURCES.md`, les records et les leçons par `fetch` en chemins relatifs `../`. Une valeur codée en dur dans le site diverge à la leçon suivante.
*Contrôle* : `status.json.anki.cartes` est recalculé au chargement depuis `anki/index.json` ; toute nouvelle donnée affichée passe par un fichier du dépôt.

**I6 — Les learning-records sont en ajout seul.** Statut : posée.
*Raison* : l'historique d'une compréhension (y compris ses erreurs) est le signal qui calibre la zone proximale ; le supprimer refait apprendre la même chose.
*Contrôle* : `git log --diff-filter=D -- learning-records/` doit rester vide ; une correction se fait par un nouveau record + `Status: superseded by LR-NNNN` sur l'ancien.

**I7 — Dans un quiz, les options d'une question ont la même longueur (mots, et si possible caractères) et l'ordre est mélangé au chargement.** Statut : posée.
*Raison* : règle du skill `teach` ; une option plus longue ou toujours première trahit la réponse et mesure la lecture d'indices, pas le savoir.
*Contrôle* : relecture du tableau `questions` de chaque leçon ; la fonction `shuffle` est présente dans chaque leçon (`grep -c "function shuffle" lessons/*.html` = nombre de leçons).

## 6. Conventions

### Transversales
- Tout est en **français** pour l'apprenant (leçons, fiches, notes, commits) ; l'allemand apparaît en gras/`.de`, la prononciation « à la française » en italique rouge `.say`, le français d'appui en gris `.fr`.
- Dates absolues partout (jamais « la semaine prochaine ») ; le workspace a démarré le 2026-09-03.
- Chemins relatifs depuis la racine du dépôt ; dans les leçons, `../reference/…`, `../MISSION.md` ; dans le site, `../` vers la racine.
- Numérotation `NNNN-slug-en-kebab.html` (leçons) et `NNNN-slug.md` (records), incrément strict, jamais de réutilisation.
- Noms allemands **toujours** avec article et pluriel (`die Datei, die Dateien`) dans les fiches et les cartes.
- Le vocabulaire de l'informatique et de l'entretien d'embauche est le **fil rouge** des exemples dès l'A2 ; dès l'A1 chaque leçon a un fichier `-it.txt`.

### Leçons (`lessons/*.html`)
- Auto-contenues (CSS et JS inline, aucune dépendance externe, aucun CDN) ; palette et typographie identiques à celles de `site/index.html` (`--paper #fffff8`, `--accent #a52a2a`, Palatino/Georgia).
- Structure : kicker (numéro, niveau, durée) → objectif concret (`.goal`) → écoute (lien DW de leçon) → savoir minimal → pratique à boucle de rétroaction immédiate → production vérifiée → auto-enregistrement → Anki → « ce que tu dois retenir » → encart « ton professeur est disponible » → pied de page (source primaire, références, prochaine leçon, date).
- Les drills audio utilisent `speechSynthesis` avec une voix `de-*` et **dégradent proprement** (message + renvoi Forvo) si aucune voix n'est installée.
- Les vérificateurs de production ne jugent que la structure et les majuscules, jamais les noms propres.

### Fiches (`reference/*.html`)
- Imprimables (`@media print`), tableaux compacts, pièges « pour francophone » explicites, pied de page daté et lié aux autres fiches.

### Cartes Anki (`anki/*.txt`)
- `recto;verso`, recto = allemand, verso = français ; en-tête obligatoire :
  `# titre:` / `# deck: Allemand A1::LNN …` ou `Allemand IT::LNN …` / `# niveau:` / `# lecon:` / `# type: general|it`.
- Le modèle génère deux cartes par note ; la révision se fait **français → allemand d'abord**.

### Python (`serveur.py`, `build_anki.py`)
- Bibliothèque standard uniquement, exécutable par double-clic ou `python x.py` depuis la racine, messages console en français sans accents pour `serveur.py` (console Windows cp850).

### Site (`site/index.html`)
- Un seul fichier, JS vanille `"use strict"`, aucun framework ; mini-rendu Markdown maison (titres, puces, liens, gras, code : rien d'autre, donc les Markdown du dépôt s'en tiennent à ça).
- Progression du réviseur intégré dans `localStorage` (`cursus.anki.progress.v1`, `cursus.anki.settings.v1`) : locale à l'appareil, export/import JSON.

## 7. Pièges déjà payés

### Sources et liens
1. **Lien DW qui ouvre la page du cours au lieu de la leçon** → l'URL `nicos-weg/c-<id>` est le cours ; les leçons ont leur propre `l-<id>` et des id différents par langue d'interface (FR ≠ DE) → utiliser `reference/data/nicos-weg-a1-fr.json` ; pour A2/B1, refaire la requête GraphQL `learngerman.dw.com/graphql` : `{ content(id:<coursFR>, lang:FRENCH) { ... on Course { lessons { id name namedUrl } } } }` (l'id du cours FR se trouve dans le HTML d'une leçon FR, motif `/fr/nicos-weg/c-\d+`).
2. **`WebFetch` échoue sur dw.com et goethe.de** → ces domaines bloquent le fetcher → utiliser `curl -sL` (fonctionne) ou les PDF officiels Goethe directement ; garder la trace dans `RESOURCES.md`.
3. **Lien Lingolia 404** → URL composée de mémoire (`/fr/grammaire/les-verbes/present`) → ne jamais écrire une URL sans l'avoir testée (I2) ; la page qui existe est `https://deutsch.lingolia.com/fr/grammaire/les-temps`.

### Outillage
4. **Heredoc bash qui casse (`unexpected EOF while looking for matching`)** sur un gros HTML français → apostrophes et guillemets du contenu → écrire les fichiers HTML avec l'outil Write ; réserver le heredoc aux petits fichiers texte.
5. **Compteurs faux dans le site** (« 12 cartes » alors qu'il y en a 84) → valeur saisie à la main dans `status.json` → le site recalcule depuis `anki/index.json` (I5) ; ne plus saisir de compteur dérivable.
6. **Import `.apkg` jamais testé sur cette machine** (Anki non installé) → le format est vérifié par relecture SQLite seulement → **A DEFINIR** : l'apprenant confirme le premier import ; en cas d'échec, comparer avec un paquet `genanki` de référence.

### Pédagogie
7. **« ich heibe »** → l'apprenant a lu ß comme un b → l'alphabet, l'Eszett et les codes Alt sont enseignés dès la leçon 2 et rappelés dans `reference/nombres-alphabet.html` ; surveiller ß/b dans chaque production.
8. **Noms sans majuscule (« softwarentwickler »)** → réflexe francophone → chaque vérificateur de production contrôle les majuscules ; rappel dans chaque fiche jusqu'à automatisation.
9. **Retard de calendrier silencieux** (leçon 1 prévue semaine 1, rendue semaine 3) → pas de rythme imposé → le journal `NOTES.md` note l'écart à chaque séance et propose une cadence de rattrapage (3 leçons/semaine) au lieu de déplacer les dates de portes.

## 8. Zones gelées

| Zone | Conséquence si modifiée |
|---|---|
| Schéma de `status.json` (`niveau, semaine, positionActuelle, gates{A1..B2}, prochaineEtape, lecons[].{numero,titre,fichier,niveau,duree,date,etat,faiteLe}, references[].{titre,fichier,niveau,date}, records[], anki, compteurs`) — généré par `build.py` sauf champs manuels | Le site en ligne casse silencieusement (sections vides) ; modifier le schéma dans `build.py` **et** `site/index.html` dans le même commit. |
| Marqueurs lus par `build.py` : `<div class="kicker">Leçon N · Niveau XX · ≈ NN minutes</div>`, `<p>Leçon créée le J mois AAAA.</p>`, `<meta name="niveau" content="XX">` dans les fiches | Une leçon sans ces marqueurs est mal classée ou mal datée dans le site. |
| Schéma de `anki/index.json` (`decks[].{id,titre,deck,niveau,lecon,type,cartes,fichierTxt,fichierApkg}`, `tout.{fichierApkg,cartes,decks}`) | Onglet Anki vide ; même règle. |
| Noms de decks Anki (`Allemand A1::LNN …`, `Allemand IT::LNN …`) et texte des rectos | Les identifiants sont dérivés de ces noms : renommer duplique les decks/notes chez l'apprenant et perd sa progression. |
| Chemins `lessons/NNNN-*.html`, `reference/*.html`, `anki/*.txt` déjà publiés | Référencés par `status.json`, par d'autres leçons et par des favoris/phone ; ne pas renommer, ajouter. |
| Formats du skill `teach` (`.claude/skills/teach/*-FORMAT.md`) | Les records, la mission et les ressources deviennent illisibles pour les prochaines sessions du skill. |
| Palette / typographie des leçons et du site | Cohérence visuelle voulue pour l'impression et la relecture ; changer partout ou nulle part. |

## 9. Commandes de développement

```bash
# depuis la racine du dépôt
serveur.bat                       # site local : http://localhost:8080/site/ (+ IP LAN pour le téléphone)
python build.py                   # découvre leçons/fiches/records, régénère anki/*.apkg + index.json, synchronise status.json
python build_anki.py              # (appelé par build.py) paquets Anki seuls
python -m http.server 8765 --bind 127.0.0.1   # smoke test alternatif (pas de /config.json)
node --check <script extrait>     # syntaxe JS du site (extraire le contenu de <script> dans un .js temporaire)
cmd //c start "" "lessons\\NNNN-slug.html"     # ouvrir une leçon (Git Bash sous Windows)
grep -n "nicos-weg/c-" lessons/*.html          # contrôle I3 : doit être vide
```

## 10. Commits

- Format observé et conservé : `<emoji> <type>: <description en français>` (`🎉 init`, `🚀 feat`, `✨ feat`), corps en puces si utile, atomique par séance ou par évolution du site.
- Le pied `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` est ajouté quand Claude est l'auteur du commit (attribution demandée par le harnais ; l'apprenant peut l'interdire ici).
- **Commit** à la fin de chaque séance ; **push** uniquement par l'apprenant ou sur sa demande explicite (le push publie sur GitHub Pages).
- Les `.apkg` générés sont versionnés (ils doivent être servis par Pages) ; `__pycache__/`, `*.pyc`, `Thumbs.db`, `desktop.ini` sont ignorés.

## 11. Porte de validation

### Une leçon est « livrée » quand
1. Elle s'ouvre depuis le fichier et depuis l'onglet Leçons du site (chemin relatif correct).
2. Toutes ses URL externes répondent 200 (ou un code de redirection suivi vers 200) au `curl` du jour.
3. Son quiz corrige immédiatement, mélange les options, et affiche un score final ; ses drills dégradent proprement sans voix allemande.
4. `python build.py` passe sans erreur ; `anki/index.json` compte la nouvelle leçon ; `status.json` la liste avec le bon niveau, la durée et la date (sinon le kicker ou le pied de page est mal formé).
5. Les champs manuels de `status.json` (`prochaineEtape`, `positionActuelle`, états) sont à jour.
6. `NOTES.md` a sa ligne de journal ; un learning-record existe si une compréhension ou une misconception a été observée.
7. Commit effectué.

Ce que cette porte **ne mesure pas** : que l'apprenant a appris. Cela se mesure à la production rendue (leçon suivante) et à la porte de niveau.

### Un niveau est « validé » quand (chiffres de `reference/parcours.html`)
1. Modellsatz Goethe officiel du niveau ≥ 60 % dans **chacune** des 4 compétences (seuil officiel de réussite au B1/B2 ; volontairement plus strict que l'officiel aux A1/A2 qui n'exigent que 60 % au total).
2. Test de grammaire maison couvrant toutes les règles du niveau ≥ 80 % (**convention projet**, pas un seuil officiel : le Goethe ne teste pas la grammaire séparément).
3. Production orale enregistrée jugée « réussi » sur les critères Goethe, avec compte rendu écrit.
4. Un learning-record consigne les trois résultats ; `status.json.gates` mis à jour.

Ce que cette porte **ne mesure pas** : la tenue dans le temps (storage strength). Elle est contrôlée par le taux de réussite Anki et par les rappels interleavés dans les leçons du niveau suivant.

---

### A DEFINIR (ouverts au 2026-09-21)
- **Contrôle mécanique de I1** (cohérence des gates) : à ajouter dans `build.py` avant l'examen A1, semaine 12 (23–29 novembre 2026).
- **Import réel d'un `.apkg`** dans Anki Desktop et AnkiDroid : confirmation par l'apprenant au premier import ; tant qu'elle manque, le réviseur intégré est la voie garantie.
- **Rythme réel** (h/semaine) : mesuré sur les dates de rendu des leçons 2 à 5 ; si < 5 h, refaire le calendrier de `parcours.html` (pas les portes).
- **Extraction des URL DW pour A2 et B1** (procédure au piège n° 1) : à faire à la fin de l'A1 et de l'A2.
