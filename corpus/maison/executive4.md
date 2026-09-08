Ontodynamique — Résumé exécutif
## De la physique fondamentale à la subjectivité — théorie formellement vérifiée de l'individuation et de la clôture
## Deux axiomes étagés, au-delà du débat substance/processus

L’Ontodynamique part de deux axiomes étagés explicites (Axiome 0 sur le Tout, I sur les déterminations finies) pour reconstruire, dans un seul cadre, l’individuation, la clôture opérationnelle, la normativité, la composition et certains seuils de subjectivité. Son ambition n’est pas d’ajouter une spéculation de plus sur l’être, mais de construire une chaîne contrôlable : axiomes, théorèmes, prédictions, protocoles de réfutation. Il ne demande pas d’être cru ; il demande d’être suivi, puis éprouvé.

Le système attaque un manque précis. Les cadres existants décrivent la clôture, la régulation, la cognition ou les processus, mais ne dérivent pas ensemble, à partir d’un même noyau, un gradient unique de composition, un test capable de distinguer formellement autonomie, portage, porté et agrégat, et une extension trans-domaniale suffisamment explicite pour être mise à l’épreuve. L’autopoïèse de Maturana et Varela décrit la clôture biologique sans la dériver d’axiomes plus primitifs ; la closure of constraints de Mossio et Montévil formalise un critère puissant sans fournir un opérateur unique étendu aux institutions, aux artefacts computationnels ou à la clinique ; le Free Energy Principle tend à traiter sous une même grammaire des systèmes dont le lieu d’endossement matériel reste indifférencié ; l’externalisme de Clark étend fonctionnellement le cognitif sans toujours trancher ce qui est proprement endogène de ce qui est simplement porté. L’Ontodynamique répond à ce triple manque.
*positionnement.* Le système ne se situe pas dans le débat
entre ontologie de la substance (Lowe) et philosophie du
processus (Rescher) — il le dissout. Les cadres substantialiste
et processualiste décrivent des régimes limites d'un principe
unique : seul le régime intermédiaire combine adaptabilité et
rigidité — propriété exclusive, inaccessible aux limites
(ModalRegimes.lean, 81 théorèmes, 0 sorry). La dérivation de V
depuis I confirme que la structure extérieure n'est pas un
second fondement posé à côté de l'acte — elle en sort. L'axiome
I n'est ni substratiste ni processualiste : il identifie être
et faire, au lieu de réduire l'un à l'autre.

Son point de départ est minimal. 
Axiome 0 : un seul réel — le Tout se fonde, tout fini se fait. Le Tout se fonde inconditionnellement (pas de dehors, aucun coût d'être) ; tout être fini doit se faire — se maintenir à coût sur marge finie, sous peine de cesser d'être. Le fini n'est pas un morceau du Tout ni son produit : "un seul réel" pose le monisme, pas une genèse. Axiome I : être, c'est se faire un — toute détermination finie est constitutivement en acte coûteux et irréversible, la pierre comme l'organisme. Deux axiomes co-posés à vocabulaire disjoint, indépendance prouvée (`Axiom0Axiom1Prime`, T1–T3), sans passage 0→I. Le contenu opératoire d'I est I-β ; l'identité être/faire est nécessaire, pas contingente (I-ν ∎, `act_is_necessary` dans `INu_Necessity.lean`, dérivé de I-α + I-β ; l'Axiome 0 est condition structurale, non prémisse — `T3_corollary_no_axiom0_needed`).

V — l'extériorité admet des degrés (dérivé d'I). L'acte fini
déterminé (I-γ) engendre son complémentaire modal ; la non-autarcie
(I-β₂) force la dépendance métabolique à ce complémentaire ;
l'auto-fondation opératoire de la clôture implique que ce complémentaire n'est pas
contrôlé — il peut varier. Cette variation est V. [...]
L'indépendance formelle I ⊥ V (InterAxiomIndependence.lean)
est un résultat de l'encodage initial de I-β₁ sans source
spécifiée ; quand I-β₁ est encodé fidèlement (régénération =
transfert, VDerived.lean), V est dérivable et l'indépendance
tombe.


D'I dérivent finitude, coût incompressible (IV), irréversibilité,
pression extérieure (V), pression de dissolution, économie constitutive — le coûteux se dissout avant l'économe : tout surplus est un drain actif sur marge finie (XVII-bis ∎) — puis le théorème directeur du système : être soi, c'est se refaire — tout être fini exposé se refait ou se défait. Les prémisses — épuisement et mortalité constitutive — tiennent sur tout substrat, discret ou continu, physique ou biologique. La quadripartition requiert en plus l'individuation.

| Régime | Est (I) | Est soi (XXXII) | Se refait |
|---|---|---|---|
| Clôture | ✓ | ✓ | ✓ — régénère ses propres conditions |
| Portage | ✓ | ✗ | ✗ — compose et maintient, externalise le coût |
| Porté | ✓ | ✗ | ✗ — forme inscrite, maintenue par un portage |
| Agrégat | ✓ | ✗ | ✗ — se défait |

Le virus se réplique mais ne se refait pas : le coût est externalisé.

La persistance passive n’est pas une individuation ; c’est un sursis — le système la couvre, au titre de l’agrégat, mais ne lui accorde pas le statut d’individu.

La contribution la plus distinctive de l’Ontodynamique est un opérateur unique de démarcation : le lieu d’endossement de l’irréversibilité sous perturbation. La question décisive n’est pas d’abord ce qu’une entité représente, calcule ou reproduit, mais qui paie matériellement le coût de son maintien quand elle est atteinte. De ce critère dérive un gradient de composition à quatre modes : clôture, lorsque le système régénère ses propres conditions en entamant sa marge propre ; portage, lorsqu’un processus compose et maintient un invariant en externalisant son coût sur un support hôte ; porté, la forme inscrite que le portage maintient, à coût marginal d’inscription ; agrégat, lorsqu’il n’y a ni cycle propre ni normativité constitutive. Ce même test vise à trancher, sans changer d’ontologie, entre organisme, virus, LLM, institution, symptôme clinique ou artefact technique : quand ça casse, qui paie ?
Onze instanciations sur des objets-limites (sept cas plus quatre adversariaux) montrent que ce gradient surprend : trois verdicts divergent de l'intuition naïve (dont une auto-correction de l'auteur, les objets mathématiques reclassés en portés — LXXXI), un verdict reste conditionnel (colonie de fourmis : test manquant identifié, pas escamoté).

I-γ (« nul acte sans mode ») est  financé par une théorie des modes formalisée (Lean 4, fichiers autoporteurs, 0 sorry) : le mode d'une entité est sa marge de chocl'espace des modes est ℕ avec pluralité intra-régime dérivée et trois grains se distinguent — profil > mode > régime (entité à quatre flux) localise la divergence avec la convention du corpus sur les seuls profils à marge grevée (porteur, sous-alimenté) : la théorie raffine une convention révisable, elle ne réfute pas le tronc.


cette ambition trans-domaniale n'est pas celle d'un vocabulaire qui absorbe tout — c'est celle d'un noyau qui interdit des configurations précises dans plusieurs domaines.

Le tronc contraint aussi la physique fondamentale. Cinq modèles séparants prouvent que l'OD ne peut pas devenir une physique — pas de métrique, pas de contenu qualitatif, pas de géométrie temporelle. Néanmoins, sept contraintes formalisées identifient des propriétés que toute physique cohérente avec I doit satisfaire : non-commutativité, direction irréversible, asymétrie construction/destruction, économie constitutive, et trois des six conditions de Piron pour un treillis orthomodulaire. La physique réelle satisfait les sept. L'OD dérive la forme ; la physique fournit le contenu. Whitehead ne dérive pas l'irréversibilité de ses 27 catégories ; le FEP ne dérive pas la direction ; l'OD dérive les deux d'I seul.

Ce déplacement permet de dériver une normativité constitutive sans dualisme et de distinguer l’autonomie véritable du simple maintien fonctionnel porté par autre chose. Il donne aussi un traitement commun à des objets que les cadres hérités peinent à comparer rigoureusement : le vivant, l’artificiel, l’institutionnel, le pathologique. Dans son extension clinique, il conduit à une reformulation forte : on ne va pas mal parce qu’on est faible — on va mal parce qu’on survit trop cher.

Le système pousse sa logique jusqu’à la subjectivité. Il dérive mécaniquement une chaîne allant de la clôture à l’auto-affection, de l’auto-affection à la valence, puis de la valence à sa rétroaction sur le cycle. 
La normativité constitutive a deux faces : partition discriminante (face normative) et manque constitutif (même seuil, lu côté déficit). Leur conjonction avec la finitude produit la précarité constitutive ∎. De là : la vie = résolution de sa propre précarité ∎ ; la conscience = épreuve de sa propre précarité ≈₃.


Il prolonge la chaîne mécanique jusqu'à la boucle de second ordre, puis localise le seul saut résiduel : identifier cette boucle comme perspective au sens phénoménal — franchissement de registre 3P→1P structurellement indécidable — indécidabilité stratifiée : non-applicable en dessous du seuil phénoménal, indécidable au-dessus. R-XIX fournit le filtre ∎.R-XIX a été testé par simulation de vie artificielle : S/I = 1.045 pour les agents avec monitoring actif vs S/I ≈ 1 pour les agents sans monitoring (TOST ✓). Gradient de profondeur confirmé (B < A < A2). Robuste sur 94% de l'espace de paramètres.
Sa force est de rendre visible l'endroit exact où la déduction s'arrête. Engagement et agnosticisme y sont rationnels tous deux — non équivalents en rendement : l'engagement ouvre DPDR, les paliers, la clinique ; crédit révocable si DPDR échoue (OSF DOI : 10.17605/OSF.IO/ZMH54).

Cette ambition s'adosse à une exigence rare de traçabilité.
L'Ontodynamique est formalisée en Lean 4 avec environ 900 résultats formalisés au total (recompte consolidé en cours : le tronc antérieur en comptait 863, les fichiers du chantier 0/I en ajoutent une centaine), couvrant le tronc structurel, les extensions continues, la dérivation de V, l'unification de β, l'articulation physique fondamentale (programme Φ), les témoins séparants, audits et résultats méta-logiques, le tout avec zéro sorry.
Cette mécanisation ne garantit pas l'adéquation du système au réel ; elle garantit autre chose, plus rare en philosophie : que ses dépendances, ses points de charge, ses sauts et ses pertes puissent être inspectés. Sur ℝ, le linter révèle que IV seul porte l'épuisement — IX est une condition d'applicabilité, non une prémisse logique. Ce résultat renforce le statut de IV comme axiome porteur unique.

Le passage du formel au mesurable n’est pas laissé à l’intuition. Il est concentré dans des hypothèses-ponts explicites, séparées du noyau dur et contraintes par des exigences dérivées du tronc : trace irréversible, prélèvement sur capacité finie, localisation du lieu d’endossement, caractère structurant sous perturbation, pouvoir discriminant entre clôture, portage, porté et agrégat. Une instanciation n’est tenue pour stable que si plusieurs perturbations indépendantes convergent sur le même lieu d’endossement ; sinon, c’est le pont qui est mis en cause, non le tronc.

Le programme a déjà un tribunal empirique substantiel. Cinq sondes dans des domaines causalement disjoints — microbiome, récifs coralliens, pharmacologie du cancer, écosystèmes logiciels, levure S. cerevisiae — retrouvent des signatures compatibles avec sa prédiction centrale ; dans quatre d'entre eux, le ratio entre perturbation structurelle et perturbation d'entrée converge autour de 1,42–1,84×, avec un coefficient de variation de ~10 %. 
R-XIX est confirmé dans un sixième domaine par simulation de vie artificielle (S/I = 1.045, gradient de profondeur confirmé — voir ci-dessus).
Cette convergence est spécifique à la partition R-XVII (disparaît sous partition par intensité, CV = 41 % ; irreproductible sur 100 000 partitions aléatoires trans-domaniales, p < 10⁻⁵). Un test de partitions rivales intra-domaine (§7.2 ter du manuscrit) étend ce résultat : dans chacun des quatre domaines, 0/1 000 partitions aléatoires atteignent le ratio ontodynamique ; des rivales nommées théoriquement motivées font parfois mieux localement (sélectivité 1.93× en GDSC, hub 1.52× en levure) mais aucune ne converge entre domaines ; dans les récifs, les trois rivales sont inversées ou nulles ; l'asymétrie survit à la normalisation par intensité (MDSINE2 : 1.78×, rivale A s'effondre à p = 0.48) et au contrôle par sélectivité (GDSC : 1.64×). La direction est dérivée du tronc ; la convergence quantitative (~1,7×, n = 4) ne l'est pas — si confirmée, régularité de second ordre appelant une explication supplémentaire. Cette convergence reste stable sous split temporel pré-spécifié et validation croisée par unités expérimentales.

Une réplication confirmatoire pré-enregistrée (levure hétérozygote, OSF) satisfait 4/4 critères de décision — première rupture de symétrie méthodologique entre analyses exploratoires et test pré-enregistré. L'objection de sur-ajustement rétrospectif est atténuée mais non éliminée pour les cinq analyses exploratoires ; la réplication indépendante par une équipe tierce reste requise. À ce premier cercle s'ajoute un second : neuf études indépendantes publiées sans connaissance du cadre retrouvent, à l'aveugle, des signatures convergentes dans la littérature. Le système ne produit pas seulement des signatures positives ; il formule aussi cinq interdictions formelles, chacune réfutable par un seul contre-exemple empirique dans un domaine identifié.


L'Ontodynamique n'est pas présentée comme un acquis, mais comme un programme explicitement réfutable. Les preuves conditionnelles sont acquises ;
Le dossier — cinq domaines disjoints exploratoires, une réplication confirmatoire pré-enregistrée, convergence stable, quatre batteries de partitions rivales exécutées (aucune rivale ne converge entre domaines, asymétrie survivante aux contrôles de confondants), neuf études aveugles conformes, cinq interdictions exposées — constitue un tribunal substantiel.
Ce qui reste à faire est identifié : la réplication prospective indépendante et le protocole clinique DPDR pré-enregistré (DOI: 10.17605/OSF.IO/ZMH54). R-XIX est testé et confirmé dans la simulation de vie artificielle (sixième domaine). Le programme Φ (87 thm, 5 fichiers) ferme l'objection de régionalité : le tronc contraint la physique, pas seulement le vivant. Limite documentée : amplitude simulée (1.04–1.05) inférieure au biologique — contrainte du substrat simulé, pas de la prédiction.

R-XIX testé dans la simulation de vie artificielle — confirmé (sixième domaine, premier à tester spécifiquement la boucle de second ordre). Limite documentée : amplitude simulée (1.04–1.05) inférieure au biologique — contrainte du substrat simulé, pas de la prédiction.