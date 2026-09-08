# Provenance des documents

## `canon_*.txt` — 1 013 fichiers

Extraits de **fr.wikisource.org** par `src/pocllm/ingest/canon.py`, une requête
par seconde, en suivant les redirections d'édition.

Les œuvres sont dans le **domaine public** : c'est le critère d'admission de
Wikisource. Les traductions retenues le sont aussi — Jules Barni (†1878) pour
Kant, Charles Appuhn (†1942) pour Spinoza. La couche éditoriale du wiki
(annotations, structure) est sous CC BY-SA ; l'attribution est ci-dessous.

Traitement appliqué : suppression du chrome balisé `ws-noexport`, conservation
des titres, et **conservation de la pagination imprimée sous forme d'ancres
`[[p.N]]`** — ce sont elles qui rendent solubles les questions à référence
exacte du jeu d'évaluation.

23 œuvres : Spinoza (*Éthique*, trad. Appuhn 1913) · Kant (*Critique de la
raison pure*, *Critique de la raison pratique*, *Fondements de la métaphysique
des mœurs*, *La religion dans les limites de la raison*) · Descartes
(*Méditations*, *Discours de la méthode*) · Rousseau (*Du contrat social*,
*Émile*, *Discours sur l'inégalité*) · Pascal (*Pensées*) · Locke (*Essai sur
l'entendement humain*) · Malebranche (*De la recherche de la vérité*) · Leibniz
(*Monadologie*) · Nietzsche (*Zarathoustra*, *Par delà le bien et le mal*,
*Généalogie de la morale*) · Montesquieu (*De l'esprit des lois*) ·
Schopenhauer (*Le Monde comme volonté et comme représentation*) · Platon
(*Œuvres*, trad. Cousin) · Bergson (*L'Évolution créatrice*) · Montaigne
(*Essais*) · Hume (*Essais philosophiques sur l'entendement humain*).

## `maison_*.txt` — 42 fichiers

Normalisés depuis `corpus/maison/` par `src/pocllm/ingest/maison.py`. Ils sont
régénérables, mais versionnés quand même : les spans du jeu d'évaluation y
pointent, et une renormalisation les décalerait silencieusement.

## Pourquoi ces fichiers sont versionnés

`data/docs/` est la couche **stable** du pipeline. `data/chunks/` et
`data/index/` en dérivent et se recalculent ; eux ne sont pas versionnés.

La vérité terrain du jeu d'évaluation est ancrée sur `(doc_id, span)` dans ces
fichiers. Toute modification d'un document décale les spans : les régénérer
impose de relancer `evals/bind_sources.py --write`.
