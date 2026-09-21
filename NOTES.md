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
