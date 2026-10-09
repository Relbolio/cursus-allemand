# Notes de travail (professeur)

## Profil de l'apprenant
- Borel Tene, de Douala (Cameroun). Francophone, anglais basique, aucune connaissance de l'allemand au départ (2026-09-03).
- Développeur logiciel ; objectif : emploi en Allemagne.
- Cible : Goethe-Zertifikat B2 dans 12 à 15 mois (souhait initial 6-9 mois, assoupli après discussion sur les ~600-800 h nécessaires).
- 5 à 10 h/semaine. Budget zéro. Oral avec germanophones à partir de A2/B1.

## Préférences / consignes
- Parcours strictement par niveaux CECRL : A1 → A2 → B1 → B2 (→ C1). Chaque niveau se termine par un
  examen blanc approfondi (Modellsatz Goethe + test de grammaire maison) ; on ne passe pas au niveau
  suivant sans l'avoir réussi.
- Veut connaître **explicitement** les règles de grammaire (pas seulement l'usage intuitif).
- Format Goethe prioritaire ; telc secondaire.
- Leçons en français ; introduire l'allemand comme langue de consigne progressivement (B1+).
- Poser des questions quand quelque chose est ambigu : l'apprenant l'a demandé explicitement.

## Consignes ajoutées le 2026-09-21
- Liens DW : utiliser les URL de LEÇON en français (`learngerman.dw.com/fr/<slug>/l-<id>`), jamais l'URL du cours.
  L'index complet des 77 leçons A1 est dans `reference/nicos-weg-a1.html` (données brutes : `reference/data/nicos-weg-a1-fr.json`,
  API GraphQL `learngerman.dw.com/graphql`, cours FR id 47994036). Refaire la même extraction pour A2 et B1 le moment venu.
- À CHAQUE leçon, livrer des cartes Anki en fichiers importables dans `anki/` : `leconNN-general.txt` + `leconNN-it.txt`
  (vocabulaire informatique / travail). Format `recto;verso`, en-tête `#` (titre, deck, niveau, lecon, type), noms toujours avec article et pluriel.
  Puis lancer `python build_anki.py` (génère les .apkg + `anki/index.json` lus par l'onglet Anki du site) et mettre à jour `status.json`
  (leçons, références, records) : le site `site/index.html` (GitHub Pages : relbolio.github.io/cursus-allemand/site/) en dépend.
  Fin de séance : commit ; le push est fait par l'apprenant (ou sur sa demande).
- Exemples personnalisés : Borel, Kamerun, Douala, Softwareentwickler.

## Consigne ajoutée le 2026-10-05
- **Approfondir DANS la leçon.** Ne plus lister des questions à poser au professeur : y répondre directement
  dans une section « Pour aller plus loin : les questions que tu allais poser », placée après le quiz.
  L'apprenant veut le maximum de connaissances disponibles dans une seule leçon, sans dépendre d'un aller-retour.
  L'encart final ne garde que ce que le professeur attend de lui, plus une invitation à signaler une réponse peu claire.
- Format des leçons inchangé par ailleurs : même structure, même palette, pas de mécanisme de déverrouillage.

## Consigne ajoutée le 2026-10-05 (soir)
- **Une série d'exercices par leçon**, dans `exercices/`, en plus des mini-exercices intégrés aux leçons (qui restent).
  Trois niveaux : facile, intermédiaire, difficile. Correction immédiate, comme dans les leçons.
  À produire désormais à chaque nouvelle leçon (étape 5 bis du cycle, CLAUDE.md §4.1).

## Diagnostic du 2026-10-09 : le genre
- L'apprenant a eu une note moyenne sur le genre. Cause réelle : **ma méthode** (listes de mots avec article),
  pas sa mémoire. Mesuré sur la Wortliste Goethe A1 : seulement 43 % des noms ont un genre prévisible par terminaison.
- **Ma règle « -er donne der » était fausse** (10 masculins sur 24 dans la liste) : restreinte aux noms dérivés d'un verbe.
- **La règle du mot composé** (le dernier élément décide, 21 sur 21) est la plus rentable et manquait : ajoutée.
- Désormais : toute règle de grammaire ou de lexique que je crois connaître est **mesurée sur la source officielle**
  avant d'être enseignée, quand les données le permettent (`reference/data/goethe-a1-noms.json`).
- **Pas de nouveau paquet Anki de vocabulaire** tant que l'encodage n'est pas réglé : l'apprenant a environ 300 cartes
  et le problème est la méthode d'encodage, pas le nombre de mots. L'entraîneur de genre remplace les listes.
- Indicateur de suivi : score au niveau difficile de `exercices/genre-intensif.html`, une fois par semaine.

## Décisions pédagogiques
- S'appuyer sur le français comme levier : genres, cas et conjugaison sont des concepts déjà connus
  (le français a des genres et des conjugaisons ; les cas s'expliquent par les pronoms le/lui).
- Utiliser le vocabulaire IT / entretien d'embauche comme fil rouge pour les exemples dès A2.
- Anki quotidien dès la leçon 1 (répétition espacée) : vocabulaire + phrases modèles.
- Rythme prévu : A1 ≈ 10-12 semaines, A2 ≈ 10-12 semaines, B1 ≈ 14-16 semaines, B2 ≈ 16-20 semaines.
- Chaque leçon : ~20-30 min, une seule compétence, quiz à réponses de longueur égale, lien vers une source primaire.

## Journal
- 2026-09-03 : création du workspace, mission fixée, première leçon (prononciation + se présenter).
- 2026-09-03 : RESOURCES.md rédigé à partir d'une recherche vérifiée (Goethe, DW, VHS, grammaires, communautés). Structure B2 et estimations UE confirmées. Prochaine leçon prévue : 0002 nombres, alphabet, haben.
- 2026-09-21 : leçon 1 terminée (présentation correcte, erreurs ß/b et majuscules corrigées, LR-0002). Liens DW corrigés. Leçon 2 livrée (nombres, alphabet, haben) + fiche nombres-alphabet + Anki. Retard d'environ 2 semaines sur le calendrier : viser 3 leçons/semaine pour le rattraper d'ici fin octobre.
- 2026-09-21 (suite) : intégration Anki au site : `build_anki.py` (apkg sans dépendance, ids stables), onglet Anki avec réviseur intégré (SM-2, localStorage, export/import), manifeste `anki/index.json`. Import .apkg réel non testé sur cette machine : à confirmer par l'apprenant au premier import.
- 2026-09-21 (soir) : l'apprenant ne trouvait pas la leçon 2 dans le site (liste plate, bandeau mobile). Créé `build.py` (découverte automatique leçons/fiches/records → status.json) ; onglet Leçons groupé par niveau, prochaine leçon présélectionnée, mode liste/lecteur sur mobile, cache Pages contourné. Désormais : `python build.py` à chaque fin de séance, plus jamais d'édition manuelle des listes de status.json.
- 2026-09-23 : leçon 3 publiée en avance (genre der/die/das, pluriel, kein/nicht, vocabulaire bureau et ordinateur) à la demande de l'apprenant, absent jusqu'au week-end. Corrections des leçons 2 ET 3 attendues ensemble à son retour (présentation v2, scores des drills, six phrases). Exception d'avance consignée dans CLAUDE.md §4.1. Fiche `reference/genre-pluriel-kein.html` + 75 cartes Anki (43 générales, 32 IT).
- 2026-10-05 : retour de l'apprenant après 12 jours. Présentation v2 corrigée (3 fautes : jahre, Französich, Softwarrentwickler ; ß et nombres composés acquis) → LR-0003. Leçons 2 et 3 marquées faites (exercices au score complet ; les six phrases de la leçon 3 n'ont pas été rendues). Leçon 4 publiée : accusatif, avec section d'approfondissement intégrée (8 questions traitées d'avance). 234 cartes Anki. Rythme réel : 3 leçons en 5 semaines, très en dessous des 7 h/semaine présumées — à surveiller avant de refaire le calendrier.
- 2026-10-05 (soir) : création de la plateforme d'exercices. Moteur commun `exercices/moteur.js` (QCM, trous, saisie, traduction, dictée vocale, scores localStorage, minuteur), 4 séries (leçons 1 à 4), 155 exercices au total. Onglet Exercices dans le site, découverte automatique par `build.py`. Vérifié au navigateur avec Playwright : QCM, saisie, dictée, bilan de fin, mémorisation des scores, et logique de correction testée en 13 cas.
- 2026-10-09 : diagnostic du genre (LR-0004). Fiche `genre-methode.html`, entraîneur `genre-intensif.html` (56 items generes depuis la Wortliste officielle), fiche genre corrigee. Lecon 5 publiee (pronoms a l'accusatif et les cinq prepositions) avec sa serie d'exercices et ses cartes. Verifie au navigateur.
