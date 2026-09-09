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
| 1 · Baseline contexte complet | bloqué — pas de clé API |
| 2 · RAG dense seul | fait, puis invalidé et refait (voir Enseignement 1) |
| 3 · Sparse + RRF + reranker ablatables | **en cours** — 11 configurations |
| 4 à 10 | non commencés ; 4, 8 et 10 bloqués sans clé API |

---

## Corpus

| | chunks | tokens | documents |
|---|---|---|---|
| Canon — Wikisource FR, 23 œuvres | 21 600 | 7,52 M | 863 |
| Maison — Ontodynamique | 2 015 | 0,40 M | 41 |

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

| configuration | recall@10 | MRR | nDCG@10 |
|---|---|---|---|
| `sparse_seul` | **0,461** | 0,278 | 0,296 |
| `sparse_sans_codes` | 0,447 | 0,315 | 0,319 |
| `hybride_rrf60_rerank` | 0,421 | **0,331** | **0,329** |
| `hybride_rrf10` | 0,382 | 0,244 | 0,250 |
| `hybride_rrf60` | 0,368 | 0,227 | 0,238 |
| `hybride_rrf60_pondere` | 0,368 | 0,263 | 0,260 |
| `hybride_sans_fusion` | 0,316 | 0,186 | 0,197 |
| `dense_seul` (e5-small) | 0,171 | 0,117 | 0,115 |
| `dense_symetrique` (paraphrase) | 0,079 | 0,047 | 0,050 |

recall@10 par type, aux deux extrêmes :

| type | `sparse_seul` | `dense_seul` |
|---|---|---|
| neologisme_maison | **1,00** | 0,00 |
| piege_attribution | 0,67 | 0,50 |
| reference_exacte | 0,53 | 0,17 |
| multi_hop | 0,33 | 0,00 |
| faux_ami_lexical | 0,25 | 0,17 |
| conceptuel | **0,00** | **0,00** |

Deux tableaux invalidés sont conservés dans `evals/results/` avec la cause en
tête : `ablation_INVALIDE_dense_mixte.md` et `ablation_INVALIDE_spans_faux.md`.

### 10. L'hybride ne bat jamais le sparse seul en rappel sur ce corpus

`sparse_seul` tient 0,461 ; la meilleure configuration hybride plafonne à 0,421.
Ajouter le dense **coûte du rappel**. Ce qu'il achète est ailleurs : le
reranking porte le MRR de 0,278 à 0,331 et le nDCG de 0,296 à 0,329.

Autrement dit, sur un corpus saturé de codes formels et de vocabulaire
idiosyncratique, l'hybride n'est pas un gain de couverture mais un **arbitrage
couverture contre précision de rang**. Le tableau agrégé seul ne le dit pas ; il
faut la ventilation par type.

Le pari central du cadrage est confirmé sans ambiguïté sur un point : sur les
questions à néologismes, le sparse fait **1,00 et le dense 0,00**. La
complémentarité est démontrée, pas postulée — mais elle joue dans un seul sens.

### 11. Le vrai réglage du dense n'est pas le modèle, c'est la profondeur

Les similarités e5 s'écrasent : sur ce corpus, tous les chunks tiennent entre
0,81 et 0,88. Pour q006, le chunk d'or est à 0,843 contre 0,875 pour le premier
— **0,032 d'écart, mais 4 091 rangs**. Et q007 place ses chunks d'or aux rangs
**54, 61 et 115**, c'est-à-dire juste au-delà du `top_k: 50` par défaut.

Le dense n'échouait donc pas : il était **tronqué trop tôt**. La recette usuelle
« récupérer 50, reranker 10 » est mauvaise dans un espace de similarités
compressé. La profondeur de candidats devient un paramètre de premier plan,
au même titre que le `k` du RRF.

### 12. Deux ablations invalides avant la bonne

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
