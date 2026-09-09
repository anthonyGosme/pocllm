# Tableau d'ablation

> **TABLEAU INVALIDE — conservé pour trace.** Mesuré contre une vérité terrain
> dont 42 spans sur 56 étaient faux : `locate()` remappait la position de la sonde
> du texte replié vers le texte brut par une règle de trois, alors que le repliement
> ne supprime pas les caractères uniformément. Les spans tombaient à côté du passage
> visé. Cela explique notamment le 0,00 des questions conceptuelles.


38 questions · corpus 23 615 chunks (canon 21 600 / maison 2 015)

| configuration | recall@1 | recall@5 | recall@10 | recall@20 | MRR | nDCG@10 | latence/q |
|---|---|---|---|---|---|---|---|
| `sparse_seul` | 0.118 | 0.289 | 0.395 | 0.408 | 0.235 | 0.252 | 0.00 s |
| `dense_seul` | 0.053 | 0.132 | 0.197 | 0.250 | 0.105 | 0.119 | 0.17 s |
| `hybride_sans_fusion` | 0.053 | 0.197 | 0.276 | 0.461 | 0.161 | 0.169 | 0.16 s |
| `hybride_rrf60` | 0.066 | 0.211 | 0.303 | 0.382 | 0.182 | 0.191 | 0.16 s |
| `hybride_rrf10` | 0.092 | 0.211 | 0.329 | 0.447 | 0.202 | 0.207 | 0.16 s |
| `hybride_rrf30` | 0.066 | 0.211 | 0.303 | 0.382 | 0.182 | 0.190 | 0.16 s |
| `hybride_rrf120` | 0.066 | 0.211 | 0.303 | 0.382 | 0.181 | 0.190 | 0.16 s |
| `sparse_sans_codes` | 0.145 | 0.289 | 0.368 | 0.408 | 0.258 | 0.261 | 0.00 s |
| `dense_symetrique` | 0.039 | 0.079 | 0.092 | 0.171 | 0.069 | 0.067 | 0.14 s |
| `hybride_rrf60_pondere` | 0.118 | 0.263 | 0.276 | 0.408 | 0.215 | 0.204 | 0.16 s |
| `hybride_rrf60_rerank` | 0.145 | 0.329 | 0.342 | 0.408 | 0.257 | 0.258 | 3.06 s |

## recall@10 par type de question

| configuration | conceptuel | faux_ami_lexical | multi_hop | neologisme_maison | piege_attribution | reference_exacte |
|---|---|---|---|---|---|---|
| `sparse_seul` | 0.00 | 0.33 | 0.33 | 0.50 | 0.67 | 0.40 |
| `dense_seul` | 0.00 | 0.17 | 0.00 | 0.00 | 0.50 | 0.23 |
| `hybride_sans_fusion` | 0.00 | 0.25 | 0.17 | 0.25 | 0.67 | 0.23 |
| `hybride_rrf60` | 0.00 | 0.17 | 0.17 | 0.25 | 0.67 | 0.33 |
| `hybride_rrf10` | 0.00 | 0.17 | 0.17 | 0.25 | 0.67 | 0.40 |
| `hybride_rrf30` | 0.00 | 0.17 | 0.17 | 0.25 | 0.67 | 0.33 |
| `hybride_rrf120` | 0.00 | 0.17 | 0.17 | 0.25 | 0.67 | 0.33 |
| `sparse_sans_codes` | 0.00 | 0.33 | 0.33 | 0.50 | 0.67 | 0.33 |
| `dense_symetrique` | 0.00 | 0.08 | 0.00 | 0.00 | 0.33 | 0.07 |
| `hybride_rrf60_pondere` | 0.00 | 0.17 | 0.17 | 0.25 | 0.67 | 0.27 |
| `hybride_rrf60_rerank` | 0.00 | 0.17 | 0.25 | 0.25 | 0.67 | 0.40 |
