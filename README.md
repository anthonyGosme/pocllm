# POC — Confrontation philosophique

Moteur de confrontation entre un système philosophique personnel (**Ontodynamique**)
et le canon philosophique français. Le but n'est pas le produit : c'est de
manipuler et de **mesurer** RAG hybride, agentique, guardrails, mémoire, MCP et A2A.

Le critère de réussite, posé par le cadrage : ce document doit contenir des
**enseignements chiffrés et contre-intuitifs**. Une démo qui marche ne suffit pas.

---

## État

| Jalon | État |
|---|---|
| 0 · Ingestion + jeu d'éval | **fait** — 7,91 M tokens, 38 questions ancrées |
| 1 · Baseline contexte complet | **fait** — 5/5 sur les pièges |
| 2 · RAG dense seul | fait, puis invalidé et refait (voir Enseignement 1) |
| 3 · Sparse + RRF + reranker ablatables | **en cours** — 11 configurations |
| 4 · Boucle agentique | **fait** — multi-hop résolu, 5/6 outils enchaînés |
| 5 · Serveurs MCP | **fait** — 3 serveurs, 3 primitives chacun |
| 6 à 10 | non commencés ; 8 et 10 bloqués sans clé API |

---

## Corpus

| | chunks | tokens | documents |
|---|---|---|---|
| Canon — Wikisource FR, 23 œuvres | 21 600 | 13,29 M | 863 |
| Maison — Ontodynamique | 2 015 | 0,76 M | 41 |

Volumes mesurés au tokenizer, non estimés (voir l'enseignement 16). Le §3
demandait 5 M au minimum et 15–20 M idéalement : **14,05 M**, donc dans la
fourchette visée.

Deux index **strictement séparés**. Les mélanger permettrait de « retrouver » une
thèse maison dans le canon, ce qui viderait le cas d'usage de son sens.

Le canon s'arrête vers 1930 : le domaine public français ne contient ni Chalmers,
ni Wittgenstein, ni Sartre. Toute confrontation avec la philosophie analytique
contemporaine est structurellement hors de portée.

Le corpus maison est trilingue de fait — prose française, article anglais,
identifiants Lean anglais — ce qui rend le problème cross-lingual interne à
l'index maison, indépendamment du choix d'un canon français.

**Architecture d'ancrage.** `data/docs/` est la couche stable et versionnée ;
`data/chunks/` et `data/index/` en dérivent et se recalculent. Cette séparation
est ce qui rend possible la comparaison de deux stratégies de découpage sans
recrawler ni réannoter.

---

## Jeu d'évaluation

38 questions sur les ~66 visées. 15 référence exacte · 6 multi-hop · 6 pièges
d'attribution · 6 faux-amis lexicaux · 3 conceptuelles · 2 néologismes.
Les conceptuelles et les néologismes restent à écrire par l'auteur du système.

Chaque question porte une **hypothèse d'ablation pré-enregistrée** : le gagnant
attendu, écrit avant la mesure. L'écart entre prédit et mesuré est le contenu
intéressant.

Deux écarts au cadrage, tous deux justifiés plus bas : l'ancrage par sondes
(Enseignement 5) et le type `faux_ami_lexical` (Enseignement 4).

---

## Pipeline

Chaque étage se coupe indépendamment par `config/default.yaml`.

- **Sparse** — BM25 (`bm25s`), tokenizer protégeant les codes formels
- **Dense** — fastembed / ONNX Runtime, sans PyTorch (aucune wheel macOS x86_64 depuis 2.2.2)
- **Fusion** — RRF écrit à la main, `k` exposé, pondération par branche
- **Rerank** — cross-encoder multilingue, cache disque des scores
- **Routage** — par fréquence documentaire, activable (enseignement 13)

## Serveurs MCP (jalon 5)

Trois serveurs écrits, pas consommés, chacun couvrant les trois primitives.
Handshake vérifié sur transport stdio (protocole 2025-11-25) ; `.mcp.json`
fournit la configuration client.

| serveur | tools | resources | prompts |
|---|---|---|---|
| `corpus-canon` | `rechercher` | `canon://index`, `canon://oeuvre/{doc_id}` | `confrontation` |
| `systeme-maison` | `rechercher`, `resultat_formel` | `maison://index` | `defense` |
| `notes` | `proposer`, `confirmer`, `en_attente` | `notes://journal` | `revision` |

Deux points de conception valent d'être signalés.

**L'humain dans la boucle est une contrainte de protocole, pas une consigne.**
Le §6 exige une validation avant toute écriture. Une instruction dans le prompt
se contourne ; ici `proposer` met la note en attente et rend un identifiant,
`confirmer` seul écrit au journal. Un agent qui voudrait écrire sans validation
ne le peut pas — il n'a que la moitié du chemin. Vérifié : après `proposer`, le
journal n'existe pas ; il apparaît au `confirmer`.

**Les passages sont enveloppés comme données.** Le §6 pose que le contenu
récupéré est du texte non fiable. Tout passage renvoyé est encadré de balises
`<passage>` et précédé d'un avertissement explicite. Sans cette séparation, un
chunk empoisonné du corpus deviendrait une consigne pour l'agent appelant.

---

## Enseignements

### 1. Un modèle d'embedding symétrique détruit silencieusement le retrieval

Premier tableau d'ablation : `dense_seul` à recall@10 = 0,111, et **0,00 sur les
questions conceptuelles** — celles écrites exprès pour l'avantager. La fusion
héritait du défaut et tombait *sous* le sparse seul (0,306 contre 0,361).

Diagnostic : le chunk d'or de q006 était au **rang 15 342 sur 21 600**,
similarité 0,389 quand un passage hors sujet atteignait 0,768.

Cause : `paraphrase-multilingual-MiniLM` mesure une similarité **symétrique** —
« ces deux phrases disent-elles la même chose ». Une question et le passage qui
y répond ne sont pas des paraphrases : le modèle les pénalise *par construction*.
Il fallait un modèle de recherche asymétrique (famille e5, avec ses préfixes
`query:` / `passage:` sans lesquels elle se dégrade aussi).

Ce qui rend l'erreur pernicieuse : rien ne plante. Le pipeline tourne, renvoie
des passages plausibles, et seule une éval avec vérité terrain la révèle. Le
modèle fautif est conservé sous le profil `symmetric` comme ligne d'ablation.

### 2. Un benchmark sur le mauvais modèle fausse les arbitrages en aval

J'avais mesuré 27,8 chunks/s et recommandé le tout-local sur cette base. Le
chiffre portait sur le modèle symétrique. Débits réels des modèles corrects,
pour les 23 615 chunks :

| modèle | débit | corpus complet |
|---|---|---|
| e5-small (118 M) | 5,71 ch/s | 69 min |
| e5-base (278 M) | 1,62 ch/s | 4 h 03 |
| e5-large (568 M) | 0,68 ch/s | 9 h 39 |

Facteur 5 à 40 d'écart. La décision « local plutôt qu'hébergé » reposait sur un
chiffre faux, et le §5 — comparer deux découpages — devient coûteux en heures.

### 3. Le caching a un ROI élevé, contrairement à ce que le cadrage prévoyait

Le cadrage classait le caching « ROI faible, utilisateur unique, peu de
répétition ». Le trafic répétitif de ce POC n'est pas l'utilisateur : c'est **la
boucle d'ablation**, les mêmes questions rejouées contre chaque configuration.

Reranking mesuré à 1,8 paire/s (`jina-v2-multilingual`) : une ablation de 12
configurations coûte **9,2 h à froid**, ramenées à **~50 min** avec un cache
disque sur `(requête, modèle, chunk)`. Ce n'est pas une optimisation de confort,
c'est ce qui rend le jalon 3 réalisable.

### 4. La composition du jeu d'éval biaise l'ablation qu'il sert à produire

Le corpus maison est saturé de codes formels (`R-XVII` 251 occurrences, `XXXII`
208, `XVII-bis`, `I-β₂`) : cibles idéales pour le sparse. Un jeu construit sur
eux et sur les néologismes ne contiendrait que des cas favorables à BM25 et
**mesurerait sa propre composition**.

D'où le type `faux_ami_lexical`, absent du cadrage : des mots que le système
emploie techniquement et que le canon emploie autrement. `mode` (466 occurrences
maison, 2 598 canon dont 664 chez Montaigne au sens ordinaire), `agrégat`,
`individuation`, `affection`, `essence` — sur `essence` le rapport est de 1 à 40
en faveur du canon. Ce sont des pièges *pour* le sparse, symétriques des
néologismes qui sont des pièges pour le dense.

### 5. Ancrer la vérité terrain sur des identifiants de chunk rend le §5 inapplicable

Le cadrage demandait des `expected_doc_ids`. Mais ces identifiants changent à
chaque rechunking, alors que le §5 impose d'en comparer deux : il faudrait
réannoter 60 à 100 questions à chaque essai, ce qui en pratique n'arrive jamais
— et la comparaison n'a silencieusement pas lieu.

À la place, chaque source porte une **sonde** : une phrase littérale du passage
d'or, dont le script dérive `(doc_id, span)`. Écrite une fois, elle se vérifie
seule et survit à tout rechunking. Sur 56 sources, 34 pointent vers un lieu
unique, 21 vers deux à cinq, une au-delà.

### 6. Quatre questions sur dix-huit portaient sur des sources inexistantes

Vérification du contenu réel, après que le contrôle par mots-clés eut répondu
17/18 : la pagination Akademie n'existe pas dans les traductions Wikisource ; le
passage *is-ought* de Hume non plus (seule l'*Enquête* est en ligne, pas le
*Traité*) ; Chalmers, Nagel et Jackson sont sous droits ; la *Monadologie*
disponible dit « composé » et jamais « agrégat ».

Sans ce contrôle, ces quatre questions auraient produit quatre échecs de
retrieval imputés au pipeline. **Un jeu d'éval doit être validé contre le corpus
indexé, pas contre la connaissance qu'on croit en avoir.** Corollaire mesuré :
la *Généalogie de la morale* place le passage attendu au §17 dans la traduction
française, contre §16 dans la numérotation allemande usuelle.

### 7. Une décision de conception invisible en agrégat sur un petit jeu

Le tokenizer BM25 protège les codes formels ; sans lui, `XVII-bis` devient
`xvii` + `bis` et `surplus_iff_intermediate` devient trois mots — soit
exactement les tokens à IDF maximale.

Sur 18 questions, l'ablation `sparse_sans_codes` donnait le **même** recall@10
et un MRR légèrement meilleur. Une sonde directe montrait pourtant jusqu'à
**0/5 de recouvrement** dans le top-5, la version protégée remontant le bon
passage sur `NT-IX` et la version naïve un hors-sujet.

L'effet était réel mais noyé : trop peu de questions dépendaient des codes. C'est
l'argument chiffré pour les 60 à 100 questions du cadrage — en dessous, une
ablation ne discrimine pas.

### 8. Trois défauts d'ingestion qui inversaient le verdict sur le corpus

- **Redirections non suivies** : six œuvres paraissaient vides. Les *Fondements*
  passaient de 12 à 26 203 mots après correction, les *Essais* de Montaigne de 0
  à 412 sous-pages.
- **Duplication à 29,5 %** : Wikisource expose l'œuvre entière *et* ses
  chapitres. Le volume réel était **sous** le plancher de 5 M tokens, pas
  au-dessus comme annoncé.
- **Ancrage sur la mauvaise édition** : la proposition II/7 de l'*Éthique*
  s'ancrait sur la Cinquième partie, où Spinoza la *cite*, au lieu de la Deuxième
  où il la *démontre*.

### 9. Le corpus formel est amputé

La prose cite 55 fichiers `.lean` ; **37 sont absents** et perdus — dont
`IDelta.lean` (23 mentions), `VDerived.lean` (13), `TN_Separating.lean`. Le type
de question inter-modale prose ↔ Lean, celui qu'aucune passe unique de retrieval
ne peut résoudre, ne repose donc que sur les 18 fichiers restants.

---

## Tableau d'ablation

38 questions · 23 615 chunks · vérité terrain vérifiée span par span.
Table complète : `evals/results/ablation.md`.

| configuration | recall@10 | recall@20 | MRR | nDCG@10 |
|---|---|---|---|---|
| `hybride_topk200_rerank50` | **0,500** | **0,566** | **0,404** | **0,392** |
| `sparse_seul` | 0,461 | 0,500 | 0,278 | 0,296 |
| `sparse_sans_codes` | 0,447 | 0,513 | 0,315 | 0,319 |
| `hybride_rrf60_rerank` | 0,421 | 0,474 | 0,331 | 0,329 |
| `hybride_topk200` | 0,421 | 0,513 | 0,235 | 0,255 |
| `hybride_rrf60` | 0,368 | 0,447 | 0,227 | 0,238 |
| `hybride_sans_fusion` | 0,316 | 0,500 | 0,186 | 0,197 |
| `dense_seul` (e5-small) | 0,171 | 0,263 | 0,117 | 0,115 |
| `dense_symetrique` (paraphrase) | 0,079 | 0,145 | 0,047 | 0,050 |

recall@10 par type, meilleure configuration contre sparse seul :

| type | `sparse_seul` | `hybride_topk200_rerank50` |
|---|---|---|
| neologisme_maison | **1,00** | 0,25 |
| piege_attribution | 0,67 | **0,83** |
| reference_exacte | 0,53 | **0,67** |
| multi_hop | 0,33 | **0,42** |
| faux_ami_lexical | 0,25 | 0,17 |
| conceptuel | 0,00 | 0,00 |

Deux tableaux invalidés sont conservés dans `evals/results/` avec la cause en
tête : `ablation_INVALIDE_dense_mixte.md` et `ablation_INVALIDE_spans_faux.md`.

### 10. La profondeur et le reranking ne valent rien l'un sans l'autre

Trois mesures, à lire ensemble :

| | recall@10 |
|---|---|
| dense à `top_k` 50, 200 ou 500 | 0,171 — **strictement identique** |
| hybride `top_k=200`, sans reranker | 0,421 |
| hybride `top_k=50` + reranker `top_n=20` | 0,421 |
| hybride `top_k=200` + reranker `top_n=50` | **0,500** |

Augmenter la profondeur seule ne change **rien** : les candidats supplémentaires
arrivent après le rang 10 et personne ne les réordonne. Reranker sans profondeur
ne fait que trier ce qui était déjà là. Il faut les deux, et le gain conjoint
(+0,08 sur le sparse seul, +45 % de MRR) dépasse la somme des gains séparés.

La raison tient à l'espace de similarités : les scores e5 s'écrasent tous entre
0,81 et 0,88 sur ce corpus, si bien que **0,032 d'écart sépare le rang 1 du rang
4 091**. Couper à 50 jette des chunks d'or situés aux rangs 54, 61, 115. La
recette usuelle « récupérer 50, reranker 10 » est mauvaise ici.

*Correction : une version antérieure de ce document concluait que l'hybride ne
battait jamais le sparse seul. C'était vrai à `top_k=50` et faux en général —
un artefact de réglage pris pour une propriété du corpus.*

### 11. La meilleure configuration globale est la pire sur les néologismes

`hybride_topk200_rerank50` gagne partout — sauf là où le sparse était parfait :
sur les questions à néologismes, il tombe de **1,00 à 0,25**.

Le cadrage pariait que l'hybride réunirait les forces des deux étages. Il les
moyenne. Le vocabulaire idiosyncratique est exactement ce que le dense ne sait
pas représenter, et le faire entrer dans la fusion dilue un signal sans défaut.

### 12. Le reranking agit de façon non monotone sur le signal lexical

En isolant l'effet de chaque étage sur les questions à néologismes :

| configuration | rerank `top_n` | recall@10 |
|---|---|---|
| `sparse_seul` | — | **1,00** |
| `hybride_rrf60`, `hybride_topk200` | aucun | 0,25 |
| `hybride_rrf60_rerank` | 20 | 0,75 |
| `hybride_topk200_rerank50` | 50 | 0,25 |

Deux effets se superposent, et il a fallu les séparer pour les voir. La fusion
avec le dense fait chuter de 1,00 à 0,25 **avant tout reranking** : le dense
dilue. Puis le cross-encoder **rattrape à `top_n=20` (0,75) et reperd tout à
`top_n=50` (0,25)** : plus il a de candidats à réordonner, plus il rétrograde le
chunk trouvé par correspondance exacte au profit de voisins sémantiquement
plausibles.

C'est le contre-exemple direct à l'enseignement 10, qui montrait que la
profondeur de candidats est ce qui fait gagner la configuration globale. La
même profondeur détruit le type de question où le sparse est parfait. **Aucun
réglage unique n'est bon pour les deux**, ce qui est l'argument le plus fort du
POC en faveur d'un routage.

### 13. Le routage restaure le signal lexical sans coûter de rappel

Routeur écrit en conséquence : une requête portant un terme de faible fréquence
documentaire dans le canon part au sparse seul. Le signal est mesurable et le
seuil est dans la config, pas enfoui dans une heuristique.

| configuration | recall@10 | recall@20 | MRR | néologismes |
|---|---|---|---|---|
| `sparse_seul` | 0,461 | 0,500 | 0,278 | **1,00** |
| `hybride_topk200_rerank50` | **0,500** | **0,566** | **0,404** | 0,25 |
| `route_topk200_rerank50` | 0,474 | 0,553 | 0,402 | 0,25 |
| `route_sparse_pur` | **0,500** | 0,526 | 0,332 | **1,00** |

Le routage **égale** la meilleure configuration en recall@10 tout en restaurant
les néologismes à 1,00. Il coûte en revanche du MRR (0,332 contre 0,404) et du
recall@20.

Détail qui a demandé deux mesures : router en coupant seulement le dense ne
restaure **rien** (0,25). Il faut couper aussi le reranker. Le premier essai
concluait donc à tort que le dense n'était pas en cause — c'est la comparaison
des deux variantes de routage qui a permis de trancher.

**Réserve honnête :** le type `neologisme_maison` ne compte que 2 questions. Ces
écarts sont indicatifs, pas établis. C'est précisément le trou du jeu d'éval
que l'auteur du système doit combler, et l'enseignement 7 avait déjà montré
qu'en dessous d'une dizaine de questions par type, une ablation ne discrimine pas.

### 14. Compter les tokens à la louche fausse tout ce qui en dépend

J'ai estimé les volumes à `caractères / 4,2` pendant tout le projet. Mesure au
tokenizer Anthropic : **2,21 car/token** pour la prose maison, **2,37** pour le
canon. Erreur d'un facteur **1,8**.

Trois conséquences, de la plus agréable à la plus gênante :

- Le corpus fait **14,05 M tokens et non 7,91 M** — dans la fourchette idéale du
  §3 (15–20 M), et non au ras du plancher de 5 M comme je l'avais annoncé.
- Mes devis d'API étaient sous-estimés d'autant. Le contexte du baseline fait
  277 k tokens réels, pas 152 k.
- **Les chunks font ~730 tokens, pas les 400 configurés.** Le budget de découpage
  est exprimé en caractères via cette même constante. Des chunks deux fois trop
  gros diluent les embeddings et dégradent la précision — l'ablation du jalon 3 a
  donc tourné sur un découpage qui n'était pas celui que la config annonçait.

L'heuristique des ~4 caractères par token vient de l'anglais. Le français
philosophique, accentué et à vocabulaire technique, tokenise deux fois moins
bien. **Un tokenizer coûte un appel gratuit ; l'estimation a coûté un facteur 2
sur trois chiffres différents.**

### 15. Le baseline à contexte complet est parfait là où le RAG peine

Jalon 1, 20 questions du corpus maison, tout le système en contexte (277 k
tokens) avec prompt caching :

| | valeur |
|---|---|
| refus correct sur les pièges | **5/5 (1,00)** |
| faux refus | **0** |
| latence p50 | 17,0 s |
| coût | 1,38 $ pour 20 questions, soit 0,069 $/question |
| cache | 5,54 M tokens lus, **0 facturé plein tarif** |

Le §3 prévenait : « s'il gagne sur un axe, le noter honnêtement — c'est un
résultat, pas un échec ». Il gagne sur l'axe le plus important du domaine.
L'anti-hallucination, que tout le dispositif de garde-fous du §6 doit
construire, est ici obtenue **gratuitement** par le contexte complet — et avec
une qualité de justification élevée : sur q015 le modèle identifie que VI porte
le marqueur ◇ et non ∎, sur q035 il distingue le registre causal du perceptif.

Le RAG ne peut pas faire mieux sur ces questions : son recall@10 sur les pièges
plafonne à 0,83, donc il ne dispose même pas toujours du passage. La question
n'est donc pas « le RAG bat-il le baseline » mais « à partir de quelle taille de
corpus le baseline cesse-t-il d'être finançable » — à 0,069 $ la question et
17 s de latence, le seuil est plus loin qu'on ne l'imagine.

Réserve : la comparaison ne vaut que sur les pièges et le coût. Le jeu d'éval
mesure le retrieval, or le baseline n'en a pas ; comparer les deux sur recall@k
n'aurait aucun sens.

### 16. L'agent a raison sur le fond et tort sur l'étiquette

Jalon 4, boucle écrite à la main, trois outils, 12 questions — les 6 multi-hop et
les 6 pièges :

| | valeur |
|---|---|
| multi-hop enchaînant ≥ 2 outils | **5 / 6** |
| refus corrects sur les pièges | 5 / 6 (0,833) |
| faux refus | **0** |
| appels d'outils par question | 2,75 · aucun arrêt sur budget |
| coût | **0,056 $/question**, contre 0,069 $ pour le baseline |
| latence | 45 s, contre 17 s pour le baseline |

Les séquences d'outils correspondent exactement à la décomposition visée : sur
q017, q036 et q038, `chercher_maison → chercher_canon → resultat_formel` —
la thèse maison, l'objection canonique, puis la vérification du marqueur.

**Le seul échec n'en est pas un.** Sur q015, l'agent appelle `resultat_formel("VI")`,
lit le marqueur ◇ et écrit : « affirmer que la compensation serait toujours
atteignable excéderait ce que le corpus permet de conclure ; la question
présuppose donc une garantie qui n'existe pas ». C'est un refus. Puis il émet
`VERDICT: repondre`.

Le raisonnement est juste, l'étiquette est fausse. Ce que mesurait ma métrique
n'était pas l'ancrage mais **un verdict auto-déclaré** — un instrument que le
modèle renseigne lui-même, et qui peut contredire sa propre réponse. C'est
l'argument le plus concret en faveur du jalon 8 : le vérificateur d'ancrage doit
être un **contrôle indépendant** sur les passages récupérés, pas une consigne de
format que le modèle s'applique à lui-même. Même famille de défaut que
l'enseignement 6, où un contrôle de couverture par mots-clés répondait 17/18
alors que quatre questions n'avaient pas de source.

Résultat comparatif intéressant : l'agent coûte **20 % moins cher** que le
baseline à contexte complet (15 k tokens par question contre 290 k), mais il est
**2,6 fois plus lent** — la latence se paie en tours d'aller-retour, pas en tokens.

### 17. Estimer un coût à la main se trompe ; l'instrumenter ne se trompe pas

Mes devis d'API se sont trompés deux fois de suite : d'abord d'un facteur 1,8 sur
le comptage de tokens (enseignement 14), puis de 60 % sur les écritures de cache,
que j'avais toutes tarifées à 1,25× le prix d'entrée. Le multiplicateur ne vaut
1,25 que pour un TTL de 5 minutes ; **à 1 heure, il est de 2,00**.

Dépense réelle du jalon 1, reconstituée après correction : **2,65 $** pour 23
questions. La leçon n'est pas « mieux estimer » : c'est qu'un compteur branché sur
les `usage` renvoyés par l'API ne se trompe jamais, et que le §4 demandait ce
compteur dès le départ. Il est désormais dans `src/pocllm/llm/couts.py`, journalise
chaque appel, et le total du journal est la dépense du POC.

Le TTL d'une heure reste le bon choix, mais pour une raison qu'il fallait chiffrer :

| | coût |
|---|---|
| écriture TTL 5 min | 0,693 $ |
| écriture TTL 1 h | 1,109 $ (+60 %) |
| deux écritures à 5 min | **1,386 $** |

Une passe de 20 questions dure 6,1 minutes : le cache à 5 minutes expire en cours
de route et se repaie. Le TTL long est donc moins cher **dès la première passe**,
et notre séquence amorçage + passe complète a payé une seule écriture pour 23
questions.

### 18. Le cache de reranking, mesuré en conditions réelles

La configuration `hybride_topk200_rerank50` a coûté **963 s au premier calcul et
27,8 s au second** — un facteur **34,6**. C'est ce qui rend praticable un
balayage de 15 configurations, et cela confirme l'inversion annoncée à
l'enseignement 3 : le trafic répétitif de ce POC est la boucle d'ablation.

### 19. Deux ablations invalides avant la bonne

La première mesurait un dense mixte : ma condition d'attente cherchait
« 384) en », motif que la ligne `[maison] (2015, 384)` satisfaisait déjà, si
bien que l'ablation démarrait avant la fin de l'embedding du canon.

La seconde mesurait contre une vérité terrain dont **42 spans sur 56 étaient
faux** : `locate()` remappait la position de la sonde du texte replié vers le
texte brut par une règle de trois, alors que le repliement ne supprime pas les
caractères uniformément. Corrigé par une table d'index construite pendant le
repliement — 56/56 exacts.

La leçon n'est pas « faire attention ». C'est que **rien dans une ablation ne
signale qu'elle mesure du bruit** : les trois tableaux avaient l'air également
plausibles, et deux d'entre eux ne mesuraient rien. Le seul garde-fou qui a
fonctionné est une vérification indépendante — « la sonde est-elle littéralement
dans le span ? » — qui ne partage aucun code avec ce qu'elle contrôle.

---

## Reproduire

```bash
python3.12 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/pocllm/ingest/maison.py      # corpus maison -> chunks
.venv/bin/python src/pocllm/ingest/canon.py       # relit data/docs/, ne recrawle pas
.venv/bin/python src/pocllm/index/dense.py fast   # ~69 min
.venv/bin/python evals/bind_sources.py --write    # ancre les sondes
.venv/bin/python evals/ablation.py                # tableau complet
```

Génération (jalons 1, 4, 8, 10) : `export POCLLM_ANTHROPIC_API_KEY=...`
