# Le genre résiste : ma méthode était en cause, et une de mes règles était fausse

Le 9 octobre 2026, Borel signale une note moyenne à la leçon 3 (genre des noms) et l'explique par un vocabulaire
encore faible et par des règles de terminaison mal retenues. Vérification faite sur la source officielle, la cause
principale était ma méthode d'enseignement, pas sa mémoire.

## Ce qui a été mesuré

Extraction des 297 noms de la [Wortliste Goethe A1](https://www.goethe.de/pro/relaunch/prf/de/A1_SD1_Wortliste_02.pdf)
vers `reference/data/goethe-a1-noms.json` (méthode : `pdftotext -layout -enc UTF-8`), puis test de mes propres règles :

- **43 %** seulement des noms ont un genre prévisible par une terminaison. Enseigner les terminaisons comme méthode
  principale ne pouvait donc pas suffire : plus d'un nom sur deux doit être encodé autrement.
- **La règle « -er donne der » que j'avais écrite est fausse en général** : sur les 24 noms en -er de la liste,
  10 seulement sont masculins. Contre-exemples vérifiés : das Fenster, das Wasser, das Wetter, das Zimmer, das Papier,
  das Bier, das Feuer, das Alter, das Fieber, das Meer, die Butter, die Nummer, die Schwester, die Mutter. La règle ne
  vaut que pour les noms dérivés d'un verbe (der Fahrer, der Drucker, der Entwickler).
- **La règle du mot composé, que je n'avais jamais enseignée, est la plus rentable** : le genre est celui du dernier
  élément, juste 21 fois sur 21 sur les composés testables de la liste. Elle couvre une grande partie du vocabulaire
  technique, qui est presque entièrement composé.
- Répartition des genres dans la liste : der 41 %, die 35 %, das 25 %. En cas de doute total à l'oral, parier sur der.

## Ce que ça change

- `reference/genre-pluriel-kein.html` corrigé : règle -er restreinte, règle du composé ajoutée, correction datée et visible.
- Nouvelle fiche `reference/genre-methode.html` : règles classées par fiabilité réelle, quatre techniques d'encodage
  (article collé au mot, phrase plutôt que mot, couleur, lieu mental), plan de travail de deux semaines.
- Nouvel entraîneur `exercices/genre-intensif.html` : 56 items générés depuis la liste officielle, trois niveaux
  (appliquer une terminaison, reconnaître un composé, mots sans règle dont les faux amis en -er).
- **Décision assumée : aucun paquet Anki de genres supplémentaire.** L'apprenant a déjà près de 300 cartes et le
  problème n'est pas le nombre de mots mais leur encodage. Ajouter des listes aurait aggravé la cause diagnostiquée.
- La progression continue : le genre s'acquiert par exposition répétée, pas en bloc. La leçon 5 a été écrite de façon
  à faire produire le genre pour choisir le pronom (ihn, sie, es), ce qui en fait un exercice de genre déguisé.

## Implications

- Mesurer une règle sur la source officielle avant de l'enseigner, chaque fois que les données le permettent.
  L'invariant I2 de CLAUDE.md interdisait déjà d'inventer un fait ; il faut aussi vérifier les règles que je crois connaître.
- Indicateur à suivre : le score au niveau difficile de l'entraîneur de genre, une fois par semaine. C'est lui qui dira
  si la nouvelle méthode fonctionne, et non la note d'une leçon.
