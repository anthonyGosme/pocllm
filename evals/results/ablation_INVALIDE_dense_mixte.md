# Tableau d'ablation

> **TABLEAU INVALIDE — conservé pour trace.** La condition d'attente de ma chaîne
> cherchait « 384) en », motif que la ligne `[maison] (2015, 384)` satisfaisait déjà :
> l'ablation a démarré avant la fin de l'embedding du canon. Les questions maison ont
> été mesurées contre e5-small, les questions canon contre l'ancienne matrice
> paraphrase. Seules les lignes `sparse_seul` et `sparse_sans_codes`, qui ne touchent
> pas au dense, sont valides.


38 questions · corpus 23 615 chunks (canon 21 600 / maison 2 015)

| configuration | recall@1 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 | latence/q |
|---|---|---|---|---|---|---|---|
| `sparse_seul` | 0.118 | 0.289 | 0.395 | 0.408 | 0.235 | 0.252 | 0.00 s |
| `dense_seul` | 0.053 | 0.105 | 0.132 | 0.171 | 0.084 | 0.089 | 0.43 s |
| `hybride_sans_fusion` | 0.053 | 0.171 | 0.276 | 0.421 | 0.147 | 0.160 | 0.40 s |
| `hybride_rrf60` | 0.066 | 0.197 | 0.289 | 0.355 | 0.165 | 0.176 | 0.40 s |
| `hybride_rrf10` | 0.092 | 0.184 | 0.316 | 0.408 | 0.183 | 0.193 | 0.39 s |
| `hybride_rrf30` | 0.066 | 0.197 | 0.289 | 0.355 | 0.166 | 0.176 | 0.46 s |
| `hybride_rrf120` | 0.066 | 0.197 | 0.289 | 0.355 | 0.164 | 0.176 | 0.40 s |
| `sparse_sans_codes` | 0.145 | 0.289 | 0.368 | 0.408 | 0.258 | 0.261 | 0.00 s |
| `dense_symetrique` | 0.039 | 0.079 | 0.092 | 0.171 | 0.069 | 0.067 | 0.33 s |
| `hybride_rrf60_pondere` | 0.118 | 0.276 | 0.289 | 0.382 | 0.221 | 0.211 | 0.37 s |
| `hybride_rrf60_rerank` | 0.118 | 0.303 | 0.329 | 0.368 | 0.231 | 0.237 | 35.15 s |

## recall@10 par type de question

| configuration | conceptuel | faux_ami_lexical | multi_hop | neologisme_maison | piege_attribution | reference_exacte |
|---|---|---|---|---|---|---|
| `sparse_seul` | 0.00 | 0.33 | 0.33 | 0.50 | 0.67 | 0.40 |
| `dense_seul` | 0.00 | 0.08 | 0.00 | 0.00 | 0.50 | 0.10 |
| `hybride_sans_fusion` | 0.00 | 0.25 | 0.17 | 0.25 | 0.67 | 0.23 |
| `hybride_rrf60` | 0.00 | 0.25 | 0.17 | 0.25 | 0.67 | 0.27 |
| `hybride_rrf10` | 0.00 | 0.25 | 0.17 | 0.25 | 0.67 | 0.33 |
| `hybride_rrf30` | 0.00 | 0.25 | 0.17 | 0.25 | 0.67 | 0.27 |
| `hybride_rrf120` | 0.00 | 0.25 | 0.17 | 0.25 | 0.67 | 0.27 |
| `sparse_sans_codes` | 0.00 | 0.33 | 0.33 | 0.50 | 0.67 | 0.33 |
| `dense_symetrique` | 0.00 | 0.08 | 0.00 | 0.00 | 0.33 | 0.07 |
| `hybride_rrf60_pondere` | 0.00 | 0.25 | 0.17 | 0.25 | 0.67 | 0.27 |
| `hybride_rrf60_rerank` | 0.00 | 0.25 | 0.25 | 0.25 | 0.67 | 0.33 |
