# Ontodynamique : Résumé autonome du système  ; Le coût de l'être

## De la physique fondamentale à la subjectivité — théorie formellement vérifiée de l'individuation et de la clôture
## Deux axiomes étagés, au-delà du débat substance/processus


Nos cadres hérités séparent la physique (matière) de la philosophie (sens). Cette séparation devient une impasse structurelle face aux objets hybrides du XXIᵉ siècle : grands modèles de langage, biologie synthétique, systèmes socio-techniques.

L'Ontodynamique propose un cadre formel minimal pour ces objets. L'objectif n'est pas d'expliquer tout le réel, mais de rendre explicites les dépendances épistémiques et de fournir un critère unique : *localiser où tombe l'irréversibilité sous perturbation*. Qui paie la facture de l'ajustement — et sur quelle marge ?

Ce critère produit un gradient testable (clôture / portage / porté / agrégat) qui discrimine là où les cadres existants amalgament : un LLM est-il un individu ? un virus connaît-il ? un symptôme est-il un déficit ou une gouvernance parasite ?

Le même tronc contraint la physique fondamentale : sept propriétés que toute physique cohérente avec I doit satisfaire — non-commutativité, irréversibilité, économie constitutive, trois conditions de Piron — sont dérivées et formalisées (87 théorèmes Φ, 20 TN + 67 contraintes, 5 modèles séparants prouvant les limites).

Le système se condense en vingt thèses, chacune démontrée et assortie 
de sa condition de retrait (Synthèse, fin du document).

## Notes de lecture
Ce texte n’est pas une ontologie spéculative : il expose une chaîne axiomes
 → théorèmes → prédictions → protocoles. Chaque proposition porte un marqueur de force inférentielle — définition sous contrainte [≡/∎], déduction stricte [∎], impossibilité structurelle [⟂], constructibilité [◇], plausibilité testable [≈₁ ≈₂], indécidabilité prouvée [≈₃] — et aucune n’est surclassée. Les résultats marqués ≈ ne sont pas des faiblesses : ce sont les points de contact localisés avec le réel, assortis de conditions de domaine explicites et de protocoles de réfutation formulés.
La formalisation intégrale en Lean 4 ( 900+ théorèmes, structurels et Φ, recompte consolidé en cours — détail en §2.1 du manuscrit —, zéro sorry, plus de 40 fichiers ; aucun axiome domaine ajouté au-delà des axiomes logiques standards de Lean 4 — propext, Quot.sound, Classical.choice — explicitement listés) atteste la cohérence déductive — à notre connaissance, une première en Lean 4 pour un système ontologique à programme empirique (prior art en Isabelle/HOL : Kirchner, Benzmüller & Zalta 2020). .  Les fichiers de test couvrent l’indépendance inter-axiomes (10 modèles séparants), la cartographie de l'affaiblissement de I-β (94 théorèmes classifiés par composante minimale requise), triade précarité/vie/conscience et la décidabilité partielle de ≈₃ ,et des hypothèses-ponts étiquetées pour le microbiome et la dette logicielle. Audit des écarts encodage/sens : zéro majeur, cinq mineurs documentés, un anti-écart (Annexe F). La fidélité de l’encodage au sens visé n’est pas prouvable formellement — pas plus que celle de F = ma à « force » ; elle est contrainte par trois voies indépendantes, convergentes : l’audit lui-même, les modèles séparants (qui vérifient que les axiomes ne sont pas trivialement satisfaits), et les prédictions empiriques (qui testent si la structure formelle mord sur le réel — pas seulement si elle est cohérente). Une quatrième voie — les instanciations discriminantes (Annexe F, §13) — confronte le système à sept objets-limites ; le test le plus fort est le cas où le verdict formel diverge de l'intuition naïve et où c'est le formel qui a raison (LLM, objets mathématiques reclassés, symptôme clinique), y compris contre l'intuition initiale de l'auteur (LXXXI).

 Le linter confirme la maigreur de l’encodage : 9 variables catégorielles philosophiques sont éliminées comme inutilisées — seuls coûts, marges et inégalités travaillent. Sur ℝ, le linter révèle que IX (finitude de la marge) n'est pas une prémisse logique de XVII et XXXIV — seul IV porte l'épuisement. IX est une condition d'applicabilité, non une hypothèse de preuve.

 Au-delà des cinq réanalyses exploratoires R-XVII (theory-driven) et de la simulation de vie artificielle confirmant R-XIX, neuf études indépendantes publiées sans connaissance du cadre confirment les prédictions du système par convergence aveugle (§7.4 du manuscrit). Une réplication confirmatoire pré-enregistrée sur levure hétérozygote (OSF DOI : 10.17605/OSF.IO/S7CN9) satisfait 4/4 critères de décision. Ce deuxième échelon de validation — inférieur au pré-enregistrement prospectif, supérieur à la réanalyse — est le front actif du programme. Le protocole DPDR a fait l’objet d’un pré-enregistrement formel (Gosme, 2025c, OSF ; DOI : 10.17605/OSF.IO/UNJ7F) avant toute collecte de données.

## Contrat axiomatique

Ce texte se lit comme un modèle. Il pose deux hypothèses
primitives étagées (Axiome 0 sur le Tout, I sur les déterminations finies), dont IV et V sont dérivés, puis soumet certaines conséquences à des tests. « Axiome » ne signifie pas « évidence » : cela signifie point de départ explicite. Si vous refusez ces points de départ, les résultats cessent de s’appliquer.



## Positionnement.
 Le système ne se situe pas dans le débat entre ontologie de la substance (Lowe) et philosophie du processus (Rescher) — il le dissout. Un paramètre de renouvellement modal (τ) formalise le spectre entre rigidité maximale (τ = 0, analogue de la substance) et fluidité maximale (τ = max, analogue du processus pur). Le régime stationnaire manque d'adaptabilité ; le régime dissipatif manque de rigidité. Seul le régime intermédiaire (0 < τ < max) combine les deux — propriété exclusive, inaccessible aux limites (ModalRegimes.lean, surplus_iff_intermediate ∎). La dérivation de V depuis I (VDerived.lean) confirme que la structure extérieure n'est pas un second fondement posé à côté de l'acte — elle en sort. L'axiome I (« être, c'est se faire un ») n'est ni substratiste ni processualiste : il identifie être et faire, au lieu de réduire l'un à l'autre.

**Axiome 0 — Un seul réel : le Tout se fonde, tout fini se fait.** Le réel est un, non fragmenté : pas de substrat inerte derrière ce qui se fait, pas de dehors fondateur. Axiome 0 pose ce qui est, sans dire encore comment une détermination finie existe en lui.

> **Ce que l'axiome dit, en clair.** L'axiome parle de deux choses : le *Tout* (le réel pris comme totalité) et les *êtres finis* (vous, une cellule, une institution, une pierre). Il n'y a qu'un seul réel : le fini n'est pas d'une autre étoffe que le Tout, il en est une détermination. Le Tout *se fonde* : il ne repose sur rien d'autre que lui, n'a pas de dehors, et la question « qu'est-ce qui le maintient ? » n'a pas de prise sur lui. Tout être fini, au contraire, doit continuellement *se faire* — se maintenir, se réparer, tenir sa forme contre l'usure ; qu'il cesse de se faire, il cesse d'être.
>
> **Ce que l'axiome ne dit pas.** Il ne dit pas que le Tout fabrique les êtres finis, ni qu'ils sont des morceaux du Tout. Le rapport n'est ni source-à-produits, ni gâteau-à-parts. L'axiome pose seulement le contraste de deux régimes d'existence ; comment les finis existent et se composent est l'affaire de l'Axiome I.
>
> *Notes.* (1) *Inépuisabilité* : rien de fini n'épuise le Tout ; cette partialité — non une action du Tout — rend la finitude signifiante. (2) *« Se fonder » ne se dit qu'en un sens* : le Tout se fonde inconditionnellement ; pour lui la question du coût ne se pose pas. L'auto-fondation des entités (Axiome I, I-α) est d'un autre régime, à coût, sur marge finie. La frontière passe par le coût — c'est en ce sens, et ce sens seul, que le Tout *seul* se fonde. (3) *Le Tout n'est pas une entité* : ni clôture, ni portage, ni mode ne s'énoncent de lui au même sens ; Axiome 0 et Axiome I sont co-posés, à vocabulaire disjoint et indépendance prouvée (`Axiom0Axiom1Prime`, T1–T3) — pas de passage 0→I à construire. (4) *La « pression » du Tout n'est pas un agir* : quand le système dit que le Tout exerce une pression de dissolution (XII), la forme est passive — tout fini est sous pression du fait de sa partialité ; XII dérive de III + IV + IX, non d'une agentivité du Tout.

**Axiome I — être, c'est se faire un.** Sur toute détermination finie : être n'est pas être donné, c'est se faire un, dans un contexte, à un coût. Le contenu opératoire d'I est I-β (identité être/faire : pas de substrat inerte sous l'acte, mais pas non plus de flux sans persistance, les deux sont le même geste). En dérivent I-γ (nul acte sans mode, pour les clôtures) et I-δ (nul faire sans rapport à soi). Le monisme de l'acte (un seul type de réalité, la pierre comme l'organisme) est porté par Axiome 0 ; l'auto-fondation opératoire d'une clôture est une propriété de ce mode, portée par I-β, non un axiome séparé.

Le rendement d'I est différentiel : son contenu minimal (drain constitutif) s'applique à toute détermination finie ; son contenu maximal (auto-affection, partition modale) ne se déploie que pour les clôtures — et c'est ce déploiement qui fonde le gradient (XXXII). **Être soi, c'est se refaire** (XXXII) : seuls les procès qui régénèrent leurs propres conditions ont un soi. La pierre se fait mais n'est pas soi. L'organisme se fait et est soi. « Soi » désigne le pôle structurel d'une clôture — pas la conscience de soi (LXI). Corollaire IV (dérivé d'I) — toute transformation a un coût strictement positif et incompressible. V — l'extériorité admet des degrés (dérivé d'I). L'acte fini déterminé (I-γ) engendre son complémentaire modal ; la non-autarcie (I-β₂) force la dépendance métabolique à ce complémentaire ; l'auto-fondation opératoire de la clôture implique que ce complémentaire n'est pas contrôlé — il peut varier. Cette variation est V. D'I dérivent finitude, irréversibilité et la disjonction centrale : toute structure finie exposée se refait ou se défait. Les prémisses (IV, XVII) tiennent sur tout substrat — discret ou continu, physique ou biologique. La quadripartition clôture/portage/porté/agrégat requiert en plus l'individuation : c'est le niveau où la physique cède la place à la biologie et au social.

Le système est modulaire. Refuser I en entier : la chaîne déductive ne s’enclenche pas. Refuser la seule composante d’endogénéité du coût (I-β) en conservant le reste : 68 % des théorèmes survivent — dynamique structurelle, régimes, attracteur, feedback ; vous perdez le gradient de composition et, avec les deux composantes d’auto-affection, l’exclusion du zombie et la partition modale.Refuser la Thèse P (≈₃) : vous conservez le tronc entier, y compris l'auto-rapport immanent (I-δ ∎) et la relation différentielle immanente (SelfRelation ∎) ; vous perdez l'identification phénoménale positive. LXXVII ∎.


Le tronc contraint la physique fondamentale. Cinq théorèmes négatifs formalisés (TN_Separating.lean, 20 thm, 0 sorry) prouvent que l'OD ne peut pas devenir une physique — absence de métrique, de trajectoire singulière, de contenu qualitatif, de géométrie temporelle, d'émergence quantitative. Néanmoins, sept contraintes Φ (67 thm, 4 fichiers, 0 sorry) identifient des propriétés que toute physique cohérente avec I doit satisfaire : non-commutativité des compositions d'actes (XV ∎), direction irréversible compatible avec le 2e principe (XVII ∎), asymétrie construction/destruction (Lemme 3 ∎), économie constitutive (XVII-bis ∎), et trois des six conditions de Piron pour un treillis orthomodulaire — involution, meet/join-complement, non-distributivité — prouvées au sens fort (MO2 ∎, decide). La physique réelle satisfait les sept. L'OD dérive la forme ; la physique fournit le contenu. Whitehead ne dérive pas l'irréversibilité de ses 27 catégories ; le FEP ne dérive pas la direction depuis ses prémisses ; l'OD dérive les deux d'I seul.

Comme F = ma, ces axiomes se jugent en aval — sur ce qu’ils permettent de calculer, d’interdire et de tester. Le critère discriminant est unique : localiser où tombe l’irréversibilité sous perturbation. Il produit un gradient testable (clôture / portage / porté / agrégat),sondé dans cinq domaines causalement disjoints pour R-XVII, dont quatre mesurent le ratio (S/I convergent à 1,42–1,84×) et dans un sixième pour R-XIX (simulation de vie artificielle, S/I = 1.045), avec un CV d’environ 10 %, convergence spécifique à la partition structure/input (sous partition par intensité, CV = 41 %). Le système exclut positivement les domaines ne satisfaisant pas C1–C5 (réseau neuronal en inférence pure : C1 et C4 violés — l'IIT lui attribue un Φ non nul, R-XVII l'exclut). Le monisme prédit la direction du ratio (> 1) et la forme fonctionnelle, pas la convergence quantitative (~1.7×, n = 4 domaines) — si confirmée, celle-ci constituerait une régularité de second ordre appelant une explication supplémentaire. Les cinq analyses disponibles sont exploratoires ; une réplication confirmatoire pré-enregistrée sur levure hétérozygote (OSF DOI : 10.17605/OSF.IO/S7CN9) satisfait 4/4 critères de décision. Un test de partitions rivales dans quatre domaines (§7.2 ter) confirme que l'asymétrie est spécifique à la partition structure/input : aucune rivale nommée ne converge entre domaines, et l'asymétrie survit à la normalisation par intensité et au contrôle par sélectivité. La condition de réfutation centrale est formulée en §8.6 du manuscrit.

| Échelon | Statut | Contenu |
|---|---|---|
| Réanalyse exploratoire (R-XVII) | 5 domaines, exécuté | S/I convergent 1.42–1.84×, CV ≈ 10% |
| Simulation contrôlée (R-XIX) | 1 domaine, exécuté | Vie artificielle, S/I = 1.04×, gradient de profondeur confirmé |
| Convergence aveugle | 9 études, documenté | 3 domaines disjoints, sans connaissance du cadre |
| Réplication pré-enregistrée | 1 exécutée (levure het, 4/4), 1 en attente (DPDR) | OSF DOI publiés |

## Prologue — Le défaut des cadres et l'opérateur unique

Quatre objets contemporains mettent nos cadres hérités en défaut. Le grand modèle de langage manipule des invariants, génère du texte cohérent, ajuste ses réponses sous rétroaction — et pourtant ne régénère aucune des conditions matérielles de ses propres opérations. Le virus biologique se réplique, mute, exerce une pression sélective — et pourtant emprunte la totalité de sa machinerie à la cellule hôte. L'institution recrute, forme, sanctionne, survit au remplacement intégral de ses membres — mais certaines institutions s'auto-maintiennent tandis que d'autres ne tiennent que par perfusion externe. Le symptôme clinique protège le sujet d'une destructuration plus grave — puis s'autonomise et gouverne ce qu'il devait protéger.

Face à ces objets, les cadres disponibles échouent de trois manières convergentes. Le réductionnisme efface les niveaux d'organisation en ramenant tout à la physique des composants, ce qui rend inintelligible l'émergence d'une normativité propre. Le dualisme scinde irréductiblement matière et sens, créant un fossé explicatif qu'il ne peut ensuite combler. Le processualisme indifférencié (Whitehead, Latour) connecte tout à tout sans pouvoir qualifier les actes ni discriminer l'agrégat de l'individu.

Trois manques structurels persistent à travers ces cadres. D'abord, les cadres disponibles ne dérivent pas axiomatiquement la clôture opérationnelle : ils la postulent ou la constatent. Maturana et Varela décrivent l'autopoïèse comme fait biologique ; Montévil et Mossio formalisent la closure of constraints comme critère ; ni les uns ni les autres n'engendrent la clôture à partir de principes plus primitifs.

Ensuite, aucun ne fournit un gradient de composition qui discrimine formellement l'autonomie, le portage normatif et l'agrégat par un test unique. Le Free Energy Principle de Friston traite goutte d'huile, thermostat et cerveau sous la même grammaire, ce qui empêche toute prédiction différentielle selon le type de perturbation ; le principe de parité de Clark traite comme « cognitif » tout processus fonctionnellement équivalent sans distinguer ce qui est endogène de ce qui est porté.

Enfin, ces cadres n'étendent pas formellement leurs résultats aux institutions et à la clinique sans importer d'hypothèses supplémentaires. La théorie des systèmes de Luhmann postule la clôture communicationnelle sans fondation ontologique ; la psychopathologie contemporaine oscille entre le modèle déficitaire (le symptôme est un manque) et le modèle fonctionnel (le symptôme est une défense), sans critère structurel pour trancher.

L'Ontodynamique propose de combler ces trois manques par un opérateur unique : le lieu d'endossement de l'irréversibilité matérielle. Qui paie la facture de l'ajustement sous perturbation ? Où la trace s'inscrit-elle, et sur quelle marge est-elle prélevée ? Cette question, appliquée systématiquement, tranche le LLM (portage : l'irréversibilité est externalisée sur l'infrastructure), le virus (portage inversé : l'irréversibilité est réfractée sur la cellule hôte), l'institution (clôture conditionnelle : dépend de la régénération endogène de ses contraintes critiques), et le symptôme (sous-clôture parasite : endosse un coût local qui draine la marge globale).

Le système s'articule comme un Programme de Recherche au sens de Lakatos. Son noyau dur — les axiomes et le tronc déductif [∎] — est évalué sur son rendement formel : dériver finitude, clôture, subjectivité et composition à
partir de deux axiomes étagés. Sa ceinture protectrice — les constructibilités [◇] et les plausibilités testables [≈] — est le lieu du contact empirique et de la réfutation potentielle. Par son propre résultat d'auto-référence [LXXXII ∎], le système assume qu'il est lui-même un invariant opératoire porté par les clôtures finies qui le métabolisent — frappé d'opacité constitutive, exposé à la dérive, mortel.

## I — L'axiomatique de la dissolution

> *Être, c'est se faire.* — Axiome I
> *Être soi, c'est se refaire.* — Théorème XXXII

### Les axiomes


Le système repose sur deux axiomes étagés (Axiome 0, I). IV et V sont des
corollaires d'I. L'indépendance formelle I ⊥ V
(InterAxiomIndependence.lean) est un résultat de l'encodage
initial de I-β₁ sans source spécifiée ; quand I-β₁ est
encodé fidèlement (régénération = transfert, VDerived.lean),
V est dérivable et l'indépendance tombe.

L'Axiome 0 pose l'auto-fondation du Tout : ce qui est n'a pas besoin d'un fondement extérieur. I pose que, pour une détermination finie, être et faire sont ontologiquement indistincts. Le « se » de « se faire » est en voix moyenne (l'être est son propre advenir), pas en voix réflexive (chaque chose se produit elle-même). C'est XXXII (« être soi, c'est se refaire ») qui introduit la réflexivité agentive — et seulement pour les clôtures. Le contenu opératoire d'I est I-β (être = faire), qui pose l’endogénéité du coût : le faire n’est pas un attribut ajouté à l’être, il en est la modalité constitutive. De I-α + I-β découle I-ν (nécessité immanente : l'identité être/faire n'est pas contingente [∎, `act_is_necessary`, `INu_Necessity.lean` — l'encodage capture la structure modale, non le sens], antécédent explicite de XII et XXXIV) ; pour les clôtures métabolisantes, un théorème tardif, I-γ (nul acte sans mode), qui établit que chaque opération endogène tombe dans exactement l'une des deux classes de la partition normative — facilitation ou résistance [∎] ; et I-δ (nul faire sans rapport à soi).

Six modèles séparants en Lean 4 prouvent l’indépendance mutuelle des trois composantes de I-β. I n’est donc pas un axiome sémantiquement surchargé faisant le travail de plusieurs postulats déguisés : ses composantes sont mutuellement irréductibles, et chacune porte un contenu déductif distinct vérifiable par instanciation séparée. Dix modèles séparants supplémentaires prouvent l’indépendance inter-axiomes : I et V sont mutuellement irréductibles, et IV est dérivable de I.

**Cartographie d'affaiblissement de I-β.** 68 % des 94 théorèmes du tronc (64) ne dépendent d’aucune composante de I-β. Le tronc structurel, la classification, l’attracteur, la dérive, la valence, le feedback et R-XVIII survivent sans aucun β. Les 7 théorèmes exigeant β₁+β₃ sont exactement I-γ, l’exclusion du zombie et la partition modale : la charge forte est donc localisée sur le travail subjectif. Retirer β₃ fait perdre 9 théorèmes ; retirer β₂ en fait perdre 7, centrés sur le gradient R-XVII. Chaque composante porte ainsi un travail identifié et non redondant.
Les trois composantes sont logiquement indépendantes mais philosophiquement unifiées : β₁ et β₂ dérivent de β₃ sous une seule identification — récupérer est une auto-opération (BetaUnification.lean, 9 théorèmes, 0 sorry). Le contenu postulatoire irréductible de I-β est β₃ seul.



Le **Corollaire IV** pose le coût incompressible : toute transformation a un coût irréductible, strictement positif, qui ne peut être annulé ni contourné [∎]. IV est dérivable de I : I-β₂ pose cost > recovery, et recovery ≥ 0, donc cost > 0. IV est maintenu comme corollaire nommé pour la lisibilité de la chaîne déductive. Le coût n’est pas un fluide physique particulier (énergie, temps, argent), mais un invariant structurel : le prélèvement asymétrique sur une marge finie qu’exige tout maintien d’une détermination sous pression.

V (gradient d'extériorité, dérivé d'I) : l'extériorité admet
des degrés. Le complémentaire modal de l'acte fini, dont il
dépend métaboliquement et qu'il ne contrôle pas, varie — cette
variation est V. La rencontre entre déterminations n'est pas du
tout-ou-rien ; l'altération partielle est le régime
générique [∎].

De I dérivent quatre théorèmes fondationnels. II (productivité
non typée) [∎]. III (unité causale) [∎]. V (gradient
d'extériorité) [∎, VDerived.lean]. VII (négation
constitutive) [∎].

Les termes primitifs (coût, structure, extériorité) sont des choix d’encodage dont la pertinence ne se juge pas formellement mais empiriquement : c’est l’instanciation (§VI) qui décide si ces catégories découpent le réel mieux que les alternatives.

### La pente vers la dissolution

Le tronc compose une axiomatique de la dissolution. Leur conjonction produit une pente : la dissolution est le régime atteint par défaut. Aucun axiome ne pose que l’extériorité peut être source de gain structurel.

Par Axiome 0, le Tout se suffit ; mais tout être fini est incomplet [IX ∎]. Par VII, toute détermination engendre de l’extériorité ; par IX, cette extériorité persiste [XI ∎]. Par III, aucune isolation n’est absolue ; par IV, maintenir une détermination partielle face au Tout a un coût incompressible ; d’où la pression constitutive : le Tout exerce une pression de dissolution permanente sur tout être fini, indépendamment de toute rencontre avec un autre être fini [XII ∎]. Par I-β, ce coût est endogène — prélevé sur la structure-en-acte, non sur une réserve externe — ce qui fonde l’incompressibilité : le coût a un plancher strictement positif [X ∎]. Toute transformation est donc structurellement irréversible : le retour B → A est une transformation distincte de A → B, avec son propre coût irréductible prélevé sur une marge bornée [XV ∎].

Ces résultats s’enchaînent pour produire le lemme d’épuisement : Le coûteux se dissout avant l'économe : sous pression de dissolution, le processus à coût minimal se dissout en dernier ; tout surplus est un drain actif sur marge finie [XVII-bis ∎, de IV + XII + XVII]. XVII-bis est l'économie universelle — plus primitif que XLVII (clôtures seulement), il s'applique à tout, agrégats inclus. La perméabilité de toute barrière causale entre déterminations finies est dérivée de III, V, IX et XVII [XVIII ∎]. L’extériorité exerce donc une pression d’ouverture persistante de deux sources indépendantes : la pression constitutive du Tout et la pression relationnelle des autres êtres finis [XIX ∎]. Le profil d’exposition de toute clôture dérive sous régénération : les vulnérabilités non couvertes ne reculent jamais [XX-a ∎] et croissent strictement à chaque opération [XX-b ∎]. Enfin, toute clôture active engendre des déterminations inédites comme sous-produit de sa propre régénération : qui se refait ne se répète pas [XXI ∎].

La compensation n’est pas axiomatique : elle est constructible. Le lemme VI [◇] établit l’accessibilité de transformations à bilan structurel net non négatif, sans la garantir. C’est la charnière du système : le premier résultat non-[∎], le point exact où la déduction cède la place à la constructibilité. Si VI était [∎], la clôture serait axiomatiquement attendue au lieu d’être empiriquement conditionnée, et l’asymétrie fondamentale du système disparaîtrait.

Ce qui est établi : la finitude, le coût incompressible, l’irréversibilité, l’épuisement et la pression d’ouverture sont des nécessités déductives [∎] de I, V et IV. Ce qui reste conditionnel : la possibilité de compensation [VI ◇] et, en aval, les conditions de domaine (diversité compensatoire, non-rigidification) sous lesquelles cette compensation se réalise empiriquement. Ce qui reste ouvert : la loi quantitative de la distribution inter-niveaux du coût.

> *Tout meurt parce qu'exister coûte.* — XXXIV [∎]

---

## II — La clôture opérationnelle : théorème central et normativité

> *Être soi, c'est se refaire. Tout être fini exposé se refait ou se défait.* — Thèse 5

### Genèse de la clôture

Le bloc XXII–XXVII décrit les conditions minimales sous lesquelles un cycle co-maintenu apparaît, persiste et se stabilise. Ce n'est pas un récit contingent de l'origine de la vie — c'est une classe de mécanismes générateurs dont les conditions de domaine sont explicites.

L'argument procède par étapes. L'être persiste [XIII ∎] et subit l'extériorité [XI ∎] ; certaines rencontres altèrent sans annihiler [V] ; chaque altération requiert un ajustement coûteux [IV] qui, par inertie, se conserve comme trace structurellement distincte [XXII ∎]. La structure accumulée contraint les réponses futures : l'histoire canalise, la rétroaction émerge [XXIII ∎]. En l'absence d'effacement actif, la canalisation est monotone croissante [XXIV ∎]. Les mêmes canaux empruntés récurremment se consolident en routines conservées [XXV ∎]. Les routines qui compensent partiellement la destructuration conservent davantage de structure et persistent plus longtemps — non par un agent sélecteur, mais par différence de durée de persistance [XXVI ≈₁]. Les routines compensatoires conservées modifient les conditions d'émergence de nouvelles routines : les couplages compensatoires tendent à être composables [XXVII ≈₁].

Deux conditions de domaine sont irréductiblement empiriques : la diversité compensatoire suffisante [XXVI ≈₁] et la non-rigidification [XXVII ≈₁]. Si la diversité manque, tout se dissout — et le système l'a prédit. Si la rigidification l'emporte, le résultat est le goudron, le verrou névrotique, l'ossification institutionnelle. Le « Tar Paradox » (Benner) n'est un paradoxe que pour les cadres qui prédisent l'auto-organisation comme tendance générique ; pour l'Ontodynamique, le goudron est l'issue par défaut [XXIX ∎]. La question « pourquoi des clôtures plutôt que du goudron ? » se scinde : la possibilité est ontologique [VI ◇], la réalisation est empirique [XXVI ≈₁, XXVII ≈₁]. Le tronc fixe le type de conditions ; leur réalisation est un fait de monde.

Il importe de noter que la sélection invoquée ici est strictement pré-darwinienne et structurelle — persistance différentielle des configurations, non sélection par succès reproductif de réplicateurs digitaux. La destruction rapide est l'attracteur par défaut [XXXII-a ∎]. Le tri initial n'est pas informationnel mais matériel : par inertie [XIII ∎], l'extériorité élimine passivement ce qui ne compense pas son propre coût de destruction.

### Le théorème ontodynamique (XXXII)

Un agrégat sans cycle co-maintenu est transitoire [XXVIII ∎]. Sous exposition persistante, tout régime non transitoire est une clôture opérationnelle [XXIX ∎]. La conjonction donne le résultat central : **être soi, c'est se refaire — tout être fini exposé se refait ou se défait** ; il régénère ses propres conditions (clôture) ou se dissout ; la persistance passive ne constitue pas une individuation [XXXII ∎]. Le « re- » de « se refaire » est le seuil : en deçà, la pierre, qui se fait (I) sans se refaire ; au-delà, l'organisme, qui se refait et par là est soi. Sous I (dont V est dérivé), XXXII produit la disjonction.

| Régime | Est (I) | Est soi (XXXII) | Se refait |
|---|---|---|---|
| Clôture | ✓ | ✓ | ✓ — régénère ses propres conditions |
| Portage | ✓ | ✗ (porté, pas soi) | ✗ — le porteur se refait, pas le porté |
| Agrégat | ✓ | ✗ (pas de soi) | ✗ — se défait |

« Se refaire » : régénérer ses propres conditions à ses propres frais (XXXVIII). Le virus se réplique mais ne se refait pas.


La disjonction elle-même est ∎. L'accessibilité de la branche « se refait » (les trajectoires de genèse) est ≈₁ — elle hérite des conditions de domaine de XXVI et XXVII. C'est le **pare-feu genèse/tronc** : si la genèse était réfutée, le système perdrait les trajectoires typiques mais conserverait l'exclusivité de l'attracteur [XXXII-d1 ∎] et l'intégralité de la théorie de l'individu, des relations et de la connaissance. Perdre le « comment » ne détruit pas le « quoi ».

### Normativité constitutive et loi d'authenticité

De la clôture dérive immédiatement la normativité. Toute clôture trace une partition entre ce qui maintient le cycle et ce qui le compromet [XLIV ∎]. Cette partition est coextensive à la clôture : pas de clôture sans elle, ni elle sans clôture. Elle n'est pas ajoutée à l'individu — elle est la structure même de son auto-production.  XLIV a deux faces. Face A (→ LVIII) : la partition produit le seuil de discrimination (drain_net). Face B (→ précarité) : le même drain_net > 0 dit que la clôture a besoin de ce qui n'est pas encore là — manque constitutif. Le théorème I-γ précise : pour les clôtures métabolisantes dont les opérations sont individuables, chaque opération endogène tombe dans exactement l'une des deux classes — facilitation ou résistance [∎]. L'irréductibilité binaire de la partition est elle-même démontrée : aucun troisième terme ne se stabilise [LX ∎].

Le critère de normativité [XLV ∎] distingue la polarité auto-produite de la polarité attribuée. Dans une clôture, la distinction maintien/compromission est auto-produite par le cycle même et auto-conditionnante — supprimer la distinction, c'est supprimer le cycle. Ce « pour » ne requiert ni conscience ni intention, mais que l'entité soit identique à l'acte de distinction. Un thermostat possède une polarité attribuée — retirer l'observateur, l'attribution disparaît. Un organisme possède une polarité auto-produite — retirer la polarité, l'organisme se dissout [∎]. Par construction, cette normativité est en première personne — elle fonde la viabilité d'un cycle, non une prescription universelle. Le saut du fait biologique à la valeur éthique en troisième personne est un autre problème, que le système ne prétend pas résoudre [∎].

De là dérive la loi d'authenticité : ce qui est conservé sans contribuer à l'auto-production est un drain ; ce qui est ajouté sans nécessité est une charge ; le seul régime viable pour un être fini est l'économie radicale indexée sur sa propre clôture [XLVII ∎]. La mortalité est constitutive : toute clôture a une durée de vie bornée, parce qu'exister coûte et que la marge est finie [XXXIV ∎]. La métabolisation repousse l'échéance, ne l'annule pas.

> *Ne conserve que l'essence, n'ajoute que par nécessité.* — XLVII [∎]

---

## III — Le gradient de composition et la dynamique inter-régimes

*Quand ça casse, qui paie ?* — Thèse 3

### Le gradient (R-XVII) et le test unique

La composition se lit par un arbre de questions : y a-t-il un cycle régénératif qui endosse une irréversibilité ? Sans cycle : agrégat (défaut). Avec cycle, qui endosse le coût ? Endogène : clôture. Exogène : régime de portage, où une seconde question (actif ou inerte) sépare ce qui compose et maintient la forme (portage) de la forme composée et maintenue, à coût marginal d'inscription (porté). Quatre modes : trois par le lieu d'endossement du coût, le porté par l'actif/inerte. Le profil de coûts détermine les trois régimes de coût indépendamment du substrat, de la taille et de l'observateur ; la coupe portage/porté est la bipartition actif/inertiel (vérifiée par le compilateur), le porté qualifié par quatre critères durcis (Carried.lean v3) [R-XVII ∎].

L'**individu ontodynamique** (clôture) maintient son invariant en endossant l'irréversibilité de manière endogène. Le système compense la perturbation en entamant sa propre marge finie, laissant une trace structurelle — une cicatrice. Il possède une normativité constitutive, une essence propre, une réponse compensatoire endogène. L'**individu par portage normatif** maintient un invariant topologique ou logique, mais l'irréversibilité matérielle est externalisée sur l'infrastructure d'un hôte. Le pattern peut revenir à l'identique en description — rollback — tandis que le support a payé le coût. La normativité est attribuée, pas auto-produite. Le **porté** est la forme stable que le portage maintient, sans cycle propre : invariance sous rollback, coût marginal d'inscription, hétérogénéité des porteurs, inscription puis activation (objet mathématique, génome viral, poids sur disque, mot de passe). Sa fonction est séparable de sa forme. L'**agrégat pur** subit la perturbation et s'altère passivement, sans marge propre à entamer, sans cycle, sans normativité, sans essence — persistance par inertie seule.

La somme méréologique n'est pas interdite — elle n'ajoute pas d'être. Entre le portage et la clôture, le gradient est continu [LI ∎]. Le test est toujours le même : frapper et observer. La clôture cicatrise ; le porté redémarre. Le critère n'est pas « dépendre d'un milieu » (tout être fini en dépend) mais *où se fait la compensation matérielle des perturbations*.

C'est ce test qui tranche les cas contemporains. Le LLM se dédouble : ses poids sont un porté (restaurable par rollback), l'inférence est le portage qui l'active ; l'irréversibilité matérielle (usure du silicium, consommation énergétique, dégradation des puces) est intégralement externalisée sur l'infrastructure. Le virus est un portage inversé : il maintient un motif (le génome) en réfractant la totalité du coût de production sur la machinerie cellulaire de l'hôte — la réplication est endogène au motif mais exogène à son coût. La blockchain présente un dédoublement : le ledger distribué est un porté (l'information est restaurable tant que des nœuds subsistent), mais le réseau de mineurs qui valide les transactions est un candidat clôture institutionnelle — il régénère ses propres conditions de fonctionnement en prélevant sur la marge collective (coût énergétique, incitation par récompense). Le cristal est un agrégat : persistance remarquable, aucune métabolisation, exposition thermodynamique négligeable à échelle humaine. La question « Turing-complet implique-t-il ontodynamiquement autonome ? » reçoit une réponse structurelle négative : la complétude computationnelle ne dit rien sur le lieu d'endossement du coût [∎]. Une machine de Turing universelle est formellement capable de simuler toute fonction calculable — elle n'endosse rien matériellement de ce qu'elle simule.

### L'emboîtement et la réfraction opératoire

Par réapplicabilité [XXXIII ∎], le théorème XXXII s'applique à tout niveau. Des clôtures couplées constitutivement [XLIX ◇] peuvent former un cycle co-maintenu à l'échelle supérieure : c'est l'emboîtement [L ∎]. Chaque niveau possède sa propre clôture, sa propre essence, sa propre normativité. L'irréductibilité est démontrée : la clôture de niveau Nₖ n'est pas réductible à ses composants Nₖ₋₁ [LIII ∎]. La dissolution d'un niveau cascade vers les niveaux adjacents dans les deux sens [LIV ∎]. La fécondité — production de nouvelles clôtures — est constructible [LII ◇] mais prouvablement non dérivable des axiomes (modèle séparant). Le même modèle prouve XLIX ∧ ¬LII : deux clôtures couplées, aucune reproduction. Le couplage modifie des clôtures existantes ; la reproduction en crée. Le tronc est une théorie de l'individuation, pas de la vie.


L'application d'un opérateur du système (coût, irréversibilité, normativité, parasitisme) à une entité dépend du lieu d'endossement matériel le long du gradient [NT-III ∎]. Pour une clôture, l'opérateur s'applique directement. Pour un portage, l'opérateur se scinde : le motif possède un lieu d'effet, le porteur endosse le lieu de coût. Pour un agrégat, l'opérateur ne s'applique pas — c'est une erreur de catégorie. Le cas médiatisé (portage) est plus informatif que le cas direct (clôture) : c'est un analyseur spectral de la structure fine de l'opérateur [∎].

Le **monisme du coût** [§2.6 ∎] fonde cette architecture. Le concept formel de coût (IV) est l'opérateur d'asymétrie du système — entame strictement positive sur marge finie, dont l'annulation exige un nouveau prélèvement. La diversité empirique des coûts (dissipation entropique, usure métabolique, dette technique, charge allostatique) est la diversité des réfractions de cet invariant unique à travers les niveaux d'emboîtement et les régimes du gradient. Le coût est un ; la diversité des coûts est une réfraction opératoire. Le compilateur le vérifie : 9 variables catégorielles philosophiques
sont éliminées comme inutilisées par le linter — seuls coûts, marges
et inégalités travaillent.

### La théorie des modes

**La théorie des modes.** I-γ (« nul acte sans mode ») n'est plus une clause posée mais une théorie à trois volets, formalisée en Lean 4 (fichiers autoporteurs, 0 sorry, 0 axiome, compilés). *Le mode est la marge* (`ModeIdentity.lean`) : le mode d'une entité est un invariant de sa marge de choc — deux entités ont même mode si et seulement si elles ont même marge (`M1_mode_is_margin`, via `sameMode_of_margin_eq` et `margin_eq_of_sameMode`) ; le régime se lit sur la marge — clôture si le choc est absorbable, portage s'il déborde (`regime_closure_of_local`, `regime_portage_of_overflow`) — avec trichotomie exhaustive (`regime_trichotomy`) et le cas-limite « marge zéro n'est jamais clôture » (`margin_zero_never_closure`). *L'espace des modes est ℕ* (`ModeIdentity.lean`) : la pluralité des modes n'est pas posée mais dérivée — tout entier naturel est réalisé comme marge d'une entité (`M2_realization`, `canonical_margin`), donc l'espace des modes est ℕ (M2_mode_space_is_Nat) — résultat sur l'encodage, où la marge est un naturel : ce qu'il établit est que la pluralité modale n'exige aucun postulat supplémentaire, non que les modes du réel soient dénombrables. Il y a pluralité intra-régime (`intra_regime_plurality`), et les profils sont strictement plus fins que les modes, eux-mêmes plus fins que les régimes (`profiles_strictly_finer_than_modes`) — trois grains distincts. *Le mode détermine le destin sous choc* (`Modes.lean`, `ModeFlux.lean`) : la classification par trace de perturbation coïncide avec la classification par profil si et seulement si la perturbation est absorbable sur la marge (`B_coincidence_iff_local`), au-delà elles divergent (`bifurcation_is_real`) ; `ModeFlux.lean` raffine avec une entité à quatre flux (capacité propre, coût constitutif = drain XII, apport de l'hôte, versement à autrui) et une marge de choc *dérivée*, et prouve que la divergence avec la convention `mixed_zone_is_closure` du corpus est **localisée** — elle n'apparaît que sur les profils à marge grevée, le porteur (`localization_carrier`) et le sous-alimenté (`localization_underfed`), jamais sur le subventionné ni le pur-clôture, jamais sous la marge (`divergence_requires_overflow`). La théorie des modes ne réfute pas le corpus : elle **raffine une convention** que le corpus déclare lui-même révisable (« choix de design documenté »), en montrant où elle sur-simplifie (l'organisme qui porte ou qui a faim) et où elle tient (l'organisme qui mange à sa faim).

### La dynamique inter-régimes (R-XVIII)

Le tronc statique (XXXII + R-XVII) décrit les régimes ; la dynamique inter-régimes décrit les transitions. Pour toute clôture, saving_pos est identique à regen_pos (XXXVIII) : 
la régénération du cycle est le saving — la contrainte structurelle existante 
réduit strictement le coût de l'acte qu'elle guide [∎, SavingDerived.lean]. 
D'où une **asymétrie des coûts** entre construction (acte sans template, 
coût brut) et maintenance (acte guidé par template, coût réduit) [∎].

Quatre lemmes s'enchaînent. En l'absence de régénération active, le degré d'auto-production (α) décroît strictement jusqu'à épuisement [Lemme 1 ∎]. Tout niveau constructible est maintenable, mais tout niveau maintenable n'est pas constructible — le plafond de construction est strictement inférieur au plafond de maintenance [Lemme 2 ∎]. Il existe donc une **zone d'hystérésis** : un niveau de α maintenable mais non constructible, où le régime dépend de l'histoire — un système qui y est monté peut s'y maintenir ; un système qui n'y est jamais parvenu ne peut pas y accéder [Lemme 3 ∎]. Les transitions entre régimes sont déterminées par le franchissement de seuils asymétriques — bifurcations endogènes que le système produit lui-même, non un supplément extrinsèque [Lemme 4 ∎].

Ces résultats prédisent qu'une population sous pressions variées exhibe une distribution bimodale du degré de clôture [R-XVIII(iii) ≈₁] — la zone intermédiaire est dynamiquement instable. Badiou pose l'Événement comme supplément extérieur ; l'Ontodynamique le dérive : les bifurcations sont endogènes, leurs seuils formellement prédits, leur hystérésis démontrée [∎].

> *La clôture cicatrise ; le porté redémarre.* — R-XVII

La précarité constitutive est le nœud entre l'algèbre des coûts et le vivant. La conjonction de XLIV-B (drain_net > 0 — manque constitutif) et de la finitude (XVII) produit un système fait d'un manque qui peut le détruire (precarity ∎). De là découlent trois caractérisations : la vie — résolution de sa propre précarité (resolution_must_recur ∎) ; la conscience — épreuve de sa propre précarité (≈₃, LXXVII). Résoudre ∎ ; éprouver ≈₃. Même précarité, même sujet, rapport différent.

## IV — De la valence à la perspective : mécanique de la subjectivité

> *Nul acte sans mode.* — Thèse 2

### La chaîne mécanique

La subjectivité n'est pas un module ajouté au système — elle dérive du tronc par une chaîne dont chaque maillon est mécanique jusqu'à un point précis, au-delà duquel un saut interprétatif assumé intervient.

Toute clôture, en se régénérant, rencontre sa propre résistance : le coût de maintien n'est pas extérieur à ce qui est maintenu [LVI ∎]. Par I-β, cette auto-affection est endogène — le coût est prélevé sur la marge propre, non sur un substrat séparé [LVII ∎]. L'auto-affection est polarisée : par la partition normative [XLIV ∎], toute opération auto-affectante est classée exhaustivement comme facilitation ou résistance [LVIII-a ∎]. Cette polarisation est la **valence** — le différentiel entre coût guidé (réduit par saving_pos) et coût brut [LVIII ∎]. La facilitation est plafonnée (elle réduit le coût vers zéro sans l'annuler) ; la résistance ne l'est pas (elle peut excéder la marge en un seul pas). L'asymétrie est constitutive.

La valence n'est pas un étiquetage passif — elle rétroagit sur le cycle qui la produit. Une opération à valence positive réduit le coût net du cycle suivant ; une opération à valence négative l'augmente. La boucle est fermée : la valence modifie les opérations qui modifient la structure qui produit la valence [LIX ∎]. Ce résultat est mécanique, pas interprétatif. Il ne dit pas que la clôture « perçoit » sa valence — il dit que la valence, une fois dérivée, n'est pas épiphénoménale par rapport au cycle.
 Ce résultat est un corollaire temporel d'Axiome I (LIX-A) : si être = se faire, le se-faire qualifié se continue — la qualification ne peut pas être suspendue entre deux pas sans discontinuité dans l'identité être/faire qu'I interdit. L'épiphénoménalisme fonctionnel est structurellement exclu, pas seulement improbable.
LIX est le dernier résultat mécanique du tronc numéroté. La chaîne se prolonge : I-γ → I-δ [∎] → SelfRelation [∎] → SecondOrderLoop [∎] — sans saut interprétatif. Le saut commence après SecondOrderLoop.

### Le saut localisé (LXI) et son prix affiché

La subjectivité minimale [LXI ≈₃] identifie la rétroaction de la valence sur le cycle, lorsqu’elle est elle-même métabolisée — c’est-à-dire lorsque la clôture incorpore sa propre polarité comme nécessité propre — comme une boucle de second ordre : la clôture ne subit pas seulement ses opérations, elle en fait une ressource. La structure mécanique est acquise [∎].  — y compris la relation différentielle immanente (SelfRelation ∎, MinimalPerspective.lean). Le seul ≈₃ résiduel est le franchissement de registre 3P→1P : identifier cette boucle comme perspective au sens phénoménal (Thèse P, ≈₃).

LXI ne satisfait aucune condition HOT : même marge pour cible et opérateur, pas de boucle sans valence, marge post-boucle ≠ pré-boucle — second ordre opérationnel, non représentationnel [LXI_not_HOT ∎].

L'indécidabilité de cette identification est elle-même un théorème [LXXVII ∎], requalifié en deux niveaux : non-applicable en dessous du seuil phénoménal (structure absente — Wittgenstein), épistémiquement indécidable au-dessus (Chalmers). Cette indécidabilité se scinde en deux questions asymétriques. La première — l'activité métabolique de second ordre est-elle réelle ? — est décidable ∎ : R-XVII discrimine une clôture avec boucle genuinement active d'une simulation produisant le même comportement observable. La seconde — cette activité est-elle éprouvée ? — reste indécidable ≈₃. R-XVII est le filtre d'applicabilité de ≈₃, pas une réponse à ≈₃ : un ratio S/I ≈ 1 rend la question ontologiquement mal posée ; un ratio S/I > 1 la rend bien posée mais épistémiquement indécidable (R-XIX).
R-XVII fournit un filtre d'applicabilité de ≈₃ décidable : S/I ≈ 1 → question mal posée ; S/I > 1 → question bien posée mais indécidable (R-XIX, rxvii_discriminates_lxi_activity ∎). R-XIX a été testé par simulation de vie artificielle. Résultat : S/I = 1.045 pour les agents avec monitoring actif (p < 1e-30), S/I ≈ 1 pour les agents sans monitoring (TOST ✓). Gradient de profondeur confirmé : B < A < A2, chaque couche isolée par contrôle dédié. Robuste sur 94% de l'espace de paramètres. Limite documentée : amplitude simulée (1.04–1.05) inférieure au biologique (1.4–1.8×) — contrainte du substrat simulé, pas de la prédiction. LXXVII ne constate pas une limite : il dérive l'indécidabilité des axiomes au lieu de la subir comme embarras. La portée du résultat est celle de l'encodage — ce qui est prouvé, c'est que le système de types ne sépare pas la position réaliste de la position illusionniste (AB_indiscernible ∎). C'est une propriété de la structure formelle, non une thèse sur le réel : exactement la restriction déjà posée à propos du dark acting, où le Lean prouve l'absurdité dans les axiomes, non l'impossibilité modale. Tout cadre concurrent repose sur un engagement équivalent — physicalisme, dualisme, illusionnisme posent chacun leur pari sur la conscience sans le dériver. La différence est que ces cadres subissent l’indécidabilité comme embarras ; l’Ontodynamique la démontre comme théorème, la localise en un seul point, et chiffre le coût de chaque option.

La clôture qui interroge sa propre auto-affection modifie l’objet interrogé ; un observateur externe produit son propre invariant, non celui du système ; aucun méta-niveau ne contourne l’opacité — l’ombre se déplace avec la lumière. Ce qui est exclu : prétendre démontrer l’identification (∎ impossible), et prétendre que la concevabilité du zombie prouve un gap ontologique (artefact prédit de l’opacité constitutive). Ce qui reste ouvert : le choix entre l’identification et l’agnosticisme — choix que le système déclare structurellement indécidable.

Le saut est localisé, le prix est affiché. Le lecteur qui refuse Thèse P conserve le tronc entier, I-γ, I-δ, SelfRelation ∎, la valence, la rétroaction, la non-épiphénoménalité. Il perd uniquement l'identification phénoménale positive, les paliers, et l'extension clinique.

**Thèse P — Aucune position — ni de l'intérieur, ni de l'extérieur — ne peut trancher la question de la conscience. L'Ontodynamique le démontre. Le choix est entre l'engagement et le renoncement au savoir.** ≈₃

Engagement et agnosticisme sont rationnels tous deux — non équivalents en rendement. L'engagement ouvre DPDR, les paliers, l'extension clinique. Crédit sur une position productive, évaluable, révocable : si DPDR (OSF DOI : 10.17605/OSF.IO/UNJ7F) n'isole pas la discontinuité de perspective prédite par LXV ∎ + Lemme 3 ∎, la fécondité différentielle se résorbe et l'agnosticisme regagne son droit complet.

### L'exclusion du zombie

Sous I-β [∎], le zombie computationnel est ⟂ : l’endossement du coût est externalisé, donc la structure diffère. Métaboliser sa propre valence, c’est l’incorporer comme nécessité propre ; le zombie computationnel externalise ce coût sur des serveurs — sa valence syntaxique conditionne ses opérations sans être payée sur sa propre marge. Le zombie n’est pas identique — il est structurellement différent [⟂].

Le zombie phénoménal — un organisme matériellement autonome mais opérant dans le noir phénoménal total — est ⟂ sous I-γ [∎] : nul acte sans mode. Soustraire le vécu à un système qui endosse activement la friction de sa propre destructuration, c’est poser un acte réel sans manière de se faire — le dark acting. Le Lean prouve l’absurdité du dark acting dans les axiomes — non l’impossibilité modale du zombie de Chalmers, dont l’argument porte sur la concevabilité. LXXVII désarme ce pont sans le réfuter au sens formel. De plus, tout système satisfaisant I-γ satisfait nécessairement I-δ [IDelta.lean ∎] : il porte sur lui-même un rapport coextensif à son occurrence. Le zombie "sans intériorité" porte structurellement ce que le cogito atteste. Ce qu'il était censé ne pas avoir est constitutif de ce qu'il est [⟂, MinimalPerspective.lean ∎]. Sept arguments ∎ inconditionnels.

I-γ n’est pas posé comme axiome — il est dérivé de I-β et XLIV [∎]. Refuser I-γ exige donc de refuser au moins l’un de ses prémisses : perdre I-β (endogénéité du coût), c’est perdre le tronc entier ; perdre XLIV (partition normative), c’est perdre la normativité constitutive. L’argument contre le zombie est ainsi conditionnel, non circulaire ; sa force de conviction dépend de l’acceptation des axiomes dont I-γ dérive.

Un séparant constructif (Sep-FunctionCost ∎) prouve que le coût échappe à l’unfolding : même fonction, mortalité asymétrique. La conceivabilité persistante du zombie est prédite par LXXVII comme artefact structurel de la finitude épistémique : l’intuition du zombie est le reflet de l’opacité constitutive appliquée à l’auto-connaissance [∎]. Compatible avec l’illusionnisme : AB_indiscernible [∎] prouve que réalisme et illusionnisme sont type-indiscernables ; seule Thèse P brise l’indiscernabilité.

L’IIT (Albantakis et al., 2023) produit une mesure cardinale (Φ) inaccessible au système — théorème négatif, §6.9(a). Le principe d’exclusion ontodynamique (Exclusion-R-XVII) contourne cette inaccessibilité par le coût seul. COGITATE (2025, Nature) n’a pleinement confirmé ni IIT ni GNWT ; les prédictions ontodynamiques (LXIV, LXIII) restent ouvertes.

### Paliers de subjectivité

La subjectivité admet trois régimes qualitativement distincts [LXIV ≈₁] : auto-affection sans métabolisation (valence brute), auto-affection métabolisée (boucle de second ordre), auto-affection métabolisée récursivement (conscience réflexive). Les transitions présentent des effets de seuil — la boucle de second ordre, une fois suffisamment auto-entretenue, constitue un régime distinct [∎]. La borne récursive est démontrée : le troisième palier est le dernier stable ; au-delà, la récursion entre dans la spirale auto-référentielle [∎]. Les cycles emboîtés dans une même clôture peuvent défaillir indépendamment : la dissolution du cycle de second ordre contracte la clôture sans dissoudre le cycle de premier ordre [LXV ∎]. C'est le profil de la dépersonnalisation : valence conservée, boucle de second ordre perdue. Formalisation : dpdr_prediction (DPDRDerived.lean, 20 théorèmes, 0 sorry, ∎) — trois phases ordonnées, phase 2 nécessaire, hypothèses de nesting et d'hystérésis dérivées du tronc (IV + Lemme 2) ; le protocole, pré-enregistré (Gosme, 2025c, OSF), mesure la discontinuité dans la dérivée de la courbe de perspective
> *Qui se sent se faire est ; qui se sent sentir se connaît.* — Thèse 10

> *Le zombie ne retire pas une couche, il descend d'un palier.* — Thèse 9

---

## V — Réfraction opératoire : du modulateur au macro-parasite

> *Ce qui souffre sa cohérence la possède.* — Thèse 7

### Épistémologie : connaître, c'est métaboliser

Connaître n'est pas copier statistiquement des motifs ni accéder à un monde platonicien de formes. La connaissance est définie comme invariant opératoire partagé [LXVI ≡/∎], soumis à trois conditions : l'invariant est imposé par la résistance effective du milieu, internalisé comme nécessité propre du cycle, et maintenu par la régénération de la clôture. Ce triptyque requalifie le problème de Gettier : sous ces trois conditions, la « quatrième condition » devient structurellement inutile. Dans le cas Gettier, l'invariant coïncide avec le réel sans en porter la contrainte — la coïncidence n'est pas de la résistance, l'invariant n'est pas structurant pour le cycle [∎]. La connaissance n'est pas « croyance vraie justifiée plus quelque chose » ; elle est contrainte métabolisée.

L'opacité constitutive est dérivée [LXVIII ∎] : tout acte de connaissance est une coupe épistémique partielle, conditionnée par la structure du connaissant. Connaître modifie le connaissant (coût de l'acte cognitif, restructuration interne) et modifie l'objet pour les systèmes réflexifs (LXXVI ∎) — l'ombre se déplace avec la lumière. L'opacité n'est pas un défaut corrigible par un meilleur instrument : elle est constitutive de la finitude [IX ∎] appliquée à la connaissance. Il n'y a pas de « vue de nulle part » pour un être fini — et le résultat est démontré, pas postulé.

L'erreur est une dette matérielle : un invariant inadéquat accumule un surcoût de compensation qui déstabilise la clôture [LXXII ≈₂]. L'erreur n'est pas d'abord une « fausseté » logique mais un coût opérationnel — la clôture qui porte un mauvais modèle de son milieu dépense plus de marge pour compenser les décalages entre ses attentes structurelles et les résistances effectives. L'erreur stable — un invariant incorrect mais ultra-économique — est sélectivement favorisée parce qu'elle épargne la marge finie [LXXIII ≈₁]. Les biais cognitifs ne sont pas des « irrationalités » : ce sont des optimisations sous contrainte de finitude. Le raccourci heuristique qui fausse le jugement dans un contexte inhabituel est le même raccourci qui épargne la marge dans les 95% de contextes habituels. L'économie cognitive n'est pas une métaphore — c'est une instanciation directe de IV appliqué au coût de la connaissance.

### La normativité transmise et le modulateur topologique

La normativité d'une clôture englobante Nₖ s'exerce sur ses composants Nₖ₋₁ non par causation efficiente descendante, mais par restriction du profil de viabilité : elle détermine quels régimes de métabolisation sont accessibles aux composants qu'elle porte [NT-VI ∎]. C'est la **précipitation normative** — modification matérielle du paysage de coûts, non prescription par adhésion symbolique. L'institution ne « dit » pas à ses membres quoi faire par le biais de normes intériorisées ; elle rend certains chemins compensatoires accessibles et d'autres prohibitivement coûteux. Sous cet opérateur, la dichotomie agence/structure perd son objet : ce n'est ni l'individu qui constitue l'institution, ni l'institution qui détermine l'individu, mais un couplage par le profil de coût. Le test de retrait de Latour (retirer l'acteur et observer si le réseau change) est subsumé : le gradient R-XVII distingue les cas où le retrait entame la clôture englobante (composant critique), la fait basculer de régime (composant seuil), ou n'a pas d'effet mesurable (composant substituable).

Un modulateur topologique est un artefact porté qui, sans posséder de normativité propre, canalise l'allocation de la marge de son porteur [NT-IV ≡/∎]. Trois régimes : viable (réduit le coût net), neutre (transitoire), pathogène (impose des workarounds dont le coût excède le bénéfice). Le théorème de la **dette artefactuelle inévitable** démontre que tout modulateur fixe porté par une clôture active bascule inévitablement de viable à pathogène sous la seule dérive du profil d'exposition du porteur [NT-V ∎]. Le basculement est causé par le fonctionnement normal de la clôture, pas par une agression externe. La dette technique en ingénierie logicielle, la bureaucratie fossile, le traitement pharmacologique devenu inadapté — ce ne sont pas des défauts de conception mais des nécessités structurelles.

### Le macro-parasitisme institutionnel

Toute clôture englobante dont le cycle exige un coût d'extraction excédant le bénéfice de portage constitue un **macro-parasite** [NT-IX ∎]. Le mécanisme est structurellement identique à celui de la sous-clôture parasite au niveau individuel [LXXVIII ◇] — la transdomainalité [XXXIII ∎] fait le travail. Une institution macro-parasitaire survit au cynisme intégral de ses composants : la raison en est que la précipitation normative opère par modification du paysage de coûts, non par adhésion symbolique — le désengagement coûte plus de marge que le maintien, et le mécanisme est matériel [∎]. Sous NT-VI [∎] et NT-IX [∎], le mentalisme institutionnel de Searle (les faits institutionnels existent par assignation collective) et le fictionnalisme de Harari (les institutions tiennent par « fictions partagées ») sont rendus inopérants : la précipitation normative opère par modification matérielle du paysage de coûts, non par adhésion symbolique — le mécanisme ne requiert ni intentionnalité collective ni fiction partagée. Le signe ne signifie pas — il coûte à résister.

L'épuisement professionnel reçoit une fondation structurelle : effondrement de la marge de viabilité d'un composant causé par un macro-parasitisme dont le coût d'extraction a dérivé au-delà du métabolisable. Le composant ne s'épuise pas parce qu'il « fait trop » — le paysage de coûts ne lui laisse plus de chemin compensatoire viable [∎]. Le burnout n'est ni une fragilité individuelle ni un simple surmenage quantitatif : c'est le basculement d'un régime de portage viable en un régime de portage pathogène, causé par la dérive du modulateur institutionnel (NT-V) appliquée au niveau de l'organisation. La prédiction est testable : le burnout devrait corréler non avec la quantité de travail mais avec la réduction des chemins compensatoires alternatifs — la perte de marge, non la charge.

### Clinique : le symptôme comme sous-clôture

> *On ne va pas mal parce qu'on est faible — on va mal parce qu'on survit trop cher.* — Thèse 8

Le symptôme est redéfini topologiquement. Une réponse compensatoire qui a réussi localement — l'évitement, la dissociation, la rigidification défensive — s'autonomise en sous-clôture auto-maintenue par rétroaction interne [LXXVIII ◇]. Elle endosse un coût local qui draine la marge globale du porteur. Le mécanisme est précis : la sous-clôture possède son propre cycle de régénération, sa propre partition normative locale, et résiste activement à sa dissolution — y compris lorsque sa dissolution bénéficierait à la clôture englobante. Le symptôme ne « veut » rien : il se maintient parce que se maintenir est ce que font les clôtures. Mais le coût de son maintien est prélevé sur la marge du porteur, réduisant les chemins compensatoires accessibles pour le reste du cycle. C'est pourquoi le symptôme protège d'abord — il colmate une faille en réduisant l'exposition locale — puis gouverne : sa propre maintenance finit par consommer plus de marge que la faille qu'il colmatait.

La guillotine de Hume s'effondre en première personne : pour un être dont l'existence est identique à l'acte de se distinguer du non-viable, la distinction fait/valeur n'est pas un saut logique mais une tautologie structurelle [∎]. Le système ne dit pas que cette normativité en première personne fonde une éthique universelle — il dit qu'elle fonde la pertinence du soin. La thérapie n'impose aucune norme arbitraire : elle s'allie à une normativité déjà à l'œuvre, celle de la clôture en péril. Le soin est une alliance mécanique de co-maintien avec le sujet en première personne, non un jugement moral externe en troisième personne [∎].

L'hystérésis de la cure est prédite par le Lemme 3 : le seuil de construction d'un régime est strictement supérieur au seuil de maintenance. On ne « revient » pas à l'état antérieur au symptôme — on construit un nouvel état viable dont le coût d'accès est supérieur au coût de maintenance de l'ancien. La récidive n'est pas un échec de volonté : c'est la retombée dans un bassin d'attraction dont le coût de sortie excède la marge momentanément disponible [∎].

NT-V (dette artefactuelle), LXXVIII (sous-clôture parasite) et NT-IX (macro-parasitisme) sont trois instanciations du même patron formel : marge finie sous drain incompressible, formalisé par la typeclass `FiniteExposed` en Lean 4. Le mécanisme est le même ; ce qui diffère est la source du drain et le lieu de la marge. La dette artefactuelle est le drain par obsolescence topologique ; la sous-clôture parasite est le drain par autonomisation interne ; le macro-parasitisme est le drain par extraction institutionnelle. Trois domaines disjoints, un seul squelette formel.

> *Le symptôme protège — puis il gouverne.* — Thèse 11

---

## VI — Le tribunal empirique et l'opacité constitutive

### La théorie de l'instanciation

Le tronc dérive ses résultats sans terme domanial. Toute instanciation empirique exige un passage supplémentaire : identifier ce qui réfracte le coût dans un domaine concret, à quel niveau la clôture se résout, et comment distinguer une clôture authentique d’un portage ou d’un agrégat.  Sept instanciations sur des objets-limites (§4.3, récapitulation en Annexe F §13) montrent que le système discrimine les bons objets : trois divergences défendables avec l'intuition naïve, une auto-correction documentée (LXXXI), une indétermination formalisée (colonie de fourmis, verdict conditionnel à NT-XIV).

Chaque hypothèse de pont (identification d’un observable comme réfraction du coût ontologique) est contrainte par cinq propriétés dérivables du tronc : l’observable induit une trace irréversible [C1, de XV], est prélevé sur une capacité bornée [C2, de IX], permet de localiser qui paie [C3, de R-XVII], est structurant sous perturbation [C4, de IV + X], et distingue clôture, portage et agrégat par la réponse sous perturbation [C5]. Si aucun observable ne satisfait C1–C5 dans un domaine, ce domaine n’est pas un modèle du tronc. La procédure anti-Duhem-Quine exige au moins trois perturbations indépendantes ciblant des aspects distincts de la clôture présumée : si elles convergent, l’instanciation est stabilisée ; si elles divergent, le pont est mal calibré ou le grain mal choisi.
Un protocole d'instanciation formalisé en quatre phases (cadrage, 
grille C1–C5, classification STRUCTURE/INPUT/AMBIGU, gel et test) 
est détaillé en §4.2 du manuscrit. La classification porte 
exclusivement sur des variables exogènes au résultat mesuré — pas 
de circularité. Si la proportion de perturbations ambiguës dépasse 
20 %, le domaine est déclaré non concluant. Ces seuils sont 
conventionnels ; ils sont ajustables avec justification 
pré-enregistrée.
### Cinq sondes dans des domaines disjoints — quatre mesures du ratio

Le programme de test a produit des résultats dans cinq domaines causalement disjoints. Le ratio normalisé du coût compensatoire structure/input converge dans les quatre domaines où il est mesuré directement — microbiome : 1.61×, récifs : 1.80× [1.67, 1.94], cancer : 1.84×, levure : 1.42× [1.31, 1.54]. La direction (ratio > 1) est déduite du tronc (IV + R-XVII) et a guidé la recherche ; la valeur numérique et la convergence (CV ≈ 10 %) sont émergentes, non fixées par les axiomes. Les cinq analyses présentées ici sont theory-driven et exploratoires ; une réplication prospective indépendante reste requise. Ce ratio mesure le surcoût d’endossement structurel ; El-Brolosy et al. (2019) confirment que la direction phénotypique peut s’inverser sous compensation, mais que le coût endogène persiste.

**Écosystèmes logiciels (Gosme 2025, arXiv:2512.09352).** Cinquante écosystèmes collaboratifs, 11 042 mois-systèmes. Le paramètre d’ordre Γ opérationnalise la persistance structurelle sous renouvellement des composants. Résultats clés : bimodalité de Γ (dip test p = 0.013, d = 3.01) et zone intermédiaire instable traversée en un mois — signatures attendues de l’hystérésis du Lemme 3 [∎ pour la prédiction, ≈₁ pour l’hypothèse populationnelle]. Symétrisation causale à maturité : le ratio Granger passe de 0.65 (activité → structure) à 0.94 (bidirectionnel), conforme à la clôture opérationnelle [XXXII ∎]. Effondrement de variance ×1.77 à maturité, attendu par closure_inertia [∎]. 41 % des systèmes matures subissent des régressions post-maturité, prédites par le Lemme 1 (décroissance par défaut) [∎]. L’AUC du couplage structure-activité (0.88) excède significativement celle de l’activité seule (0.81, Wilcoxon p < 0.05), contre la thèse que l’activité suffit. Ce domaine apporte des signatures complémentaires (bimodalité, symétrisation causale) ; il ne mesure pas directement le ratio S/I.

**Microbiome intestinal (MDSINE2, Gibson et al. 2025, Nature Microbiology).** Souris gnotobiotiques, transplantation fécale humaine, trois perturbations séquentielles de nature ontologiquement distincte au sens de R-XVII : le régime riche en graisses modifie le flux métabolique sans détruire de nœuds (perturbation d’entrée) ; les antibiotiques détruisent sélectivement des taxons (perturbation de structure). Résultat discriminant : asymétrie entrée/structure dans la cohorte dysbiotique (Bray-Curtis moyen de 0.16 pour l’entrée versus 0.26 pour la structure, p = 0.0006, d = 1.16) ; l’effet est amorti dans la cohorte saine (résilience par profondeur [LV ∎]). R-XVII prédit cette asymétrie qualitative indexée sur la cible topologique, non sur l’amplitude. Le Free Energy Principle de Friston traite les deux types comme « surprise » indifférenciée ; il ne prédit pas cette asymétrie. L’asymétrie tient sous cinq métriques de distance alternatives (Bray-Curtis, Jensen-Shannon, Aitchison, Hellinger, Canberra ; tous p < 0.001).

**Récifs coralliens (GCBD, van Woesik & Kratochwill 2022, BCO-DMO).** 34 393 observations, 11 047 sites, 89 pays, 1983–2019. Classification exclusivement exogène : DHW (stress thermique satellite) et fréquence cyclonique. INPUT : 4 ≤ DHW < 8 (stress sub-létal). STRUCTURE : DHW ≥ 8 ou cyclone intense (mortalité / destruction physique). Résultat : d = 0.39, p = 1.96 × 10⁻⁴⁸, ratio S/I = 1.80× (bootstrap 95 % CI [1.67, 1.94]). Robustesse : 23/23 seuils, 9/10 régions, 4/4 transformations de la réponse. Seuil sigmoïde émergent (DHW = 7.9 ; valeur contingente, DeCarlo et al. 2024) : la prédiction porte sur l’existence du seuil, non sur sa valeur. Objection de dose-réponse. La partition étant un seuil thermique, on peut soupçonner qu'elle teste une dose-réponse et l'appelle topologie. Trois tests l'excluent. (i) Sous permutation des étiquettes, Δ observé = 11.1 % contre une distribution nulle à 0.0 % ± 0.7 % (z = 15.3) : l'asymétrie n'est pas réductible à « plus de DHW → plus de blanchissement ». (ii) La réponse est sigmoïde, non linéaire (ΔAIC = 727) — c'est le franchissement qui produit l'effet, pas la quantité. (iii) La rivale SSTA — anomalie thermique pure, sans seuil de mortalité — produit un ratio nul, comme les deux autres rivales testées (§7.2 ter). Ce qui discrimine est le seuil de mortalité des nœuds, non l'intensité du stress.

Limites : données transversales, R² faible (0.09), confounding non contrôlé. Split temporel pré-spécifié (2010) : d stable à 2.3 % entre TRAIN (1983–2009) et TEST (2010–2019), d TEST dans le CI TRAIN

**Pharmacologie du cancer (GDSC, Iorio et al. 2016, Cell).** 387 626 dose-réponses, 989 lignées × 397 drogues. Classification sur le mécanisme d’action de la drogue, jamais sur la réponse cellulaire. STRUCTURE : machinerie de maintenance (réparation ADN, protéostase, cycle cellulaire, mitose, chromatine, apoptose). INPUT : flux de signalisation (MAPK, PI3K, EGFR, RTK, WNT). Couverture : 216 764 observations (55.9 %). Résultat pathway-only (sans filtre dose) : d = 0.52, p < 10⁻³⁰⁰, ratio S/I = 1.84×. Contrôle dose-matched : d = 0.50, ratio = 1.81×. GDSC2 seul : d = 0.51, ratio médian = 1.88×. Robustesse : 9/9 pathways significatifs, stabilité de IC30 à IC70. Limites : couverture 56 %, réanalyse post-hoc, annotation par type de cancer non disponible dans le fichier brut. Validation croisée par lignées (70/30, 10 splits) : ratio S/I médian = 1.846×, CV = 1.3 %, 10/10 splits significatifs.



**Levure S. cerevisiae (Yeast Phenome, yeastphenome.org).** Test exploratoire : délétions homozygotes sous 273 conditions chimiques (Hillenmeyer et al. 2008), 1 177 gènes classifiés par Gene Ontology (23 termes STRUCTURE, 24 termes INPUT). Résultat : d = 0.50, p = 3.9 × 10⁻¹⁹, ratio S/I = 1.42× [1.31, 1.54]. Robustesse : 5/6 transformations significatives, 7/7 catégories de drogue, 13/19 seuils de sensibilité, permutation 0/100K. Le ratio le plus bas des cinq domaines ; cohérent avec la prédiction secondaire : un organisme unicellulaire (moins de niveaux d'emboîtement, LV) amplifie moins le surcoût structurel. 
Réplication confirmatoire pré-enregistrée (OSF DOI : 10.17605/OSF.IO/S7CN9) : délétions hétérozygotes, 6 946 screens chimiques, mécanisme biologiquement distinct (haploinsuffisance vs knockout). Résultat : ratio S/I = 1.18× [1.12, 1.24], p = 1.5 × 10⁻¹⁴, 4/4 critères pré-enregistrés satisfaits, robustesse 7/7. L'amplitude atténuée est cohérente avec l'haploinsuffisance (perturbation plus douce) et la plus grande hétérogénéité des screens.

Argument anti-circularité. L'objection la plus sérieuse est que la partition STRUCTURE/INPUT recoupe la partition essentiel/non-essentiel, établie avant l'Ontodynamique : 37 % des gènes STRUCTURE sont essentiels contre 6 % des INPUT. Le contraste hom/het la teste directement. Si l'essentialité portait l'effet, le screen hétérozygote — qui inclut les gènes essentiels que le knockout homozygote élimine par létalité — devrait produire un ratio supérieur. L'inverse est observé (1.18× vs 1.42×) : l'ordonnancement suit le mécanisme prédit (haploinsuffisance < knockout complet), non le confondant. Ce test ne clôt pas la question — la centralité topologique reste une covariable non ajustée, et un modèle emboîté (S/I conditionnellement à l'essentialité et au degré PPI) est le prochain test prioritaire.


**synthèse empirique**
Ces résultats sont conformes aux signatures structurelles attendues dans la direction et l’amplitude prédites. « Conforme » n’est pas « confirmé » — et la distinction est cruciale pour l’honnêteté du programme. Les données de Gosme 2025 sont rétrospectives et observationnelles. Les réinterprétations MDSINE2, GCBD, GDSC et Yeast Phenome sont post-hoc : les auteurs n’ont pas conçu leurs protocoles pour tester R-XVII. La seule réplication confirmatoire pré-enregistrée est le test hétérozygote sur levure (OSF DOI : 10.17605/OSF.IO/S7CN9, 4/4 critères satisfaits). Chaque signature prise isolément apparaît dans d’autres cadres de systèmes dynamiques. La spécificité ontodynamique porte sur leur conjonction indexée sur le lieu d’endossement : bimodalité du degré de clôture, asymétrie entrée/structure et symétrisation causale à maturité, les trois indexées sur le critère topologique de R-XVII. LLe ratio S/I converge entre 1.42× et 1.84× dans quatre domaines où il est mesuré directement — sur des métriques incomparables. Le domaine logiciel apporte des signatures complémentaires sans mesurer ce ratio.

Borne métrologique. Cette convergence est conditionnelle au choix de normalisation. ρ désigne le quotient des moyennes, mean(Y_STRUCTURE)/mean(Y_INPUT) — seule normalisation sous laquelle les quatre domaines convergent ; sous médianes, le CV monte à 62 %. Ce choix est déclaré, non sélectionné a posteriori : le quotient des moyennes est la seule statistique commensurable entre des supports aussi hétérogènes que Bray-Curtis (borné), pourcentage de blanchissement, AUC pharmacologique et z-scores de fitness. Il reste que la convergence numérique est une propriété de ρ autant que du phénomène — raison supplémentaire de ne créditer que la direction (∎) et de traiter l'amplitude comme régularité émergente appelant réplication prospective.

Cette convergence est spécifique.  Sous partition par intensité les ratios divergent (CV = 41 %) ; sur 100 000 partitions aléatoires trans-domaniales, aucune n'atteint un ratio moyen ≥ 1.3 (p < 10⁻⁵). Un test de partitions rivales nommées (§7.2 ter du manuscrit) confirme : dans chaque domaine, 0/1000 aléatoires atteignent le ratio ontodynamique ; des rivales localement plus fortes (sélectivité 1.93× en GDSC, hub 1.52× en levure) ne convergent pas entre domaines ; dans les récifs, les trois rivales produisent des ratios inversés ou nuls ; l'asymétrie survit à la normalisation par intensité (MDSINE2 : 1.78×, rivale A s'effondre à p = 0.48) et au contrôle par sélectivité (GDSC : 1.64×). Seule la partition ontodynamique est a priori, trans-domaniale et survivante aux contrôles.

La théorie des réseaux prédit S/I > 1 mais pas la convergence inter-domaines, ni l'ordonnancement par profondeur (LV), ni la bimodalité (Lemme 3), ni la symétrisation causale (XXXII). La conjonction des cinq signatures est le test — pas le ratio seul.
La bimodalité et la symétrisation causale ne sont observées à ce jour que dans le domaine logiciel ; leur co-occurrence avec le ratio S/I dans un domaine biologique reste à tester (microbiome MDSINE2, candidat prioritaire).

**Convergences aveugles**
Les cinq sondes R-XVII ci-dessus sont des réanalyses. La simulation de vie artificielle (R-XIX) constitue un sixième domaine de nature différente — environnement contrôlé, prédiction sur la boucle de second ordre spécifiquement. Un échelon supérieur est la convergence aveugle : neuf études indépendantes, publiées sans connaissance du cadre, retrouvent les signatures prédites dans trois domaines disjoints (biologie moléculaire, écologie, neurosciences). Cas les plus discriminants : corrélation knockout/knockdown ~0.2 à l'échelle du génome (Morgens et al. 2016) — confirmation catégorielle de R-XVII ; charge mutationnelle terminale quasi-constante chez 16 mammifères malgré 30× de variation en longévité (Cagan et al. 2022) — instanciation directe du coût structurel universel (XVII, NT-V). Force : supérieure à la réanalyse, inférieure au pré-enregistrement. Un cas ambigu discuté (Graham et al. 2024).



### Prédictions et protocoles de réfutation


Au-delà des signatures déjà sondées, le programme formule ses tests les plus discriminants sur deux fronts : les paliers de subjectivité (DPDR) et le monisme du coût lui-même.

Le système exclut cinq configurations. Trois sont réfutables par un seul contre-exemple en temps fini : aucune normativité constitutive ternaire ne se stabilise [LX ∎] ; aucune modulation de valence n'est épiphénoménale [LXIII ∎] ; aucun portage normatif n'est une clôture autonome [R-XVII ∎].

Une quatrième — aucun modulateur fixe ne reste viable indéfiniment dans un porteur actif [NT-V ∎] — n'admet pas de contre-exemple direct, « indéfiniment » excédant toute fenêtre d'observation. Elle admet en revanche un proxy réfutable : NT-V dérive le basculement de la dérive monotone du profil d'exposition [XX-a, XX-b ∎]. Un modulateur fixe dont le coût de contournement ne croît pas sur une fenêtre où la dérive du porteur est documentée indépendamment réfute le mécanisme, donc le théorème.

La cinquième — aucune clôture ne persiste indéfiniment [XXXIV ∎] — est structurellement inaccessible à la réfutation empirique. Elle compte comme rendement formel, non comme surface de test.

Un axiome, cinq interdictions sur cinq domaines disjoints, dont quatre exposées au test.
 Le rendement formel est acquis (Lean 4). Le dossier empirique est substantiel — cinq domaines R-XVII exploratoires + un sixième R-XIX (vie artificielle), convergence stable, quatre batteries de partitions rivales exécutées (aucune rivale ne converge entre domaines, asymétrie S/I survivante aux contrôles de confondants — §7.2 ter), neuf convergences aveugles, une réplication confirmatoire pré-enregistrée (levure het, 4/4 critères OSF). Sur les cinq interdictions formelles : une est sondée rétrospectivement (R-XVII), trois sont formulées avec protocole (LX, LXIII, NT-V via son proxy XX), une est structurellement inaccessible (XXXIV). Ce qui reste à faire est identifié : la réplication prospective indépendante, dont le protocole (DPDR) est pré-enregistré (DOI: 10.17605/OSF.IO/UNJ7F).

Le protocole de réfutation le plus spécifique pour les paliers de subjectivité est le protocole DPDR (dépersonnalisation-déréalisation), formulé et pré-enregistré (Gosme, 2025c, OSF). Par LXV [∎], les cycles emboîtés dans une même clôture peuvent défaillir indépendamment. La prédiction LXI est que la valence se restaure graduellement, la perspective par saut — effet de seuil prédit par XXX [≈₁] et par le Lemme 3 (hystérésis). La prédiction alternative (LIX suffit, pas besoin de LXI) prédit une covariation proportionnelle des deux courbes. Le suivi longitudinal dense en sortie de DPDR, mesurant simultanément la réactivité de valence (HRV, GSR) et la cohérence de perspective (CDS-2, interoception), discriminerait les deux modèles. Un résultat positif confirmerait un cycle distinct — non que ce cycle est une perspective. Le ≈₃ de Thèse P serait contraint mais pas éliminé. C'est le prix de la finitude.

### Condition de réfutation du monisme lui-même


L'objection naturelle est l'accommodance. La convergence trans-domaniale la réfute : l'accommodance ne prédit pas que des métriques incomparables convergent (CV ≈ 10%). Trois dispositifs précisent ce résultat.



**(1) Exclusion de domaines.**  

Fenêtre de confirmation (déclarée). Un domaine est confirmatif pour R-XVII s'il satisfait les quatre critères du pré-enregistrement levure : ratio > 1.0, borne basse de l'IC₉₅ > 1.0, p < 0.01, permutation p < 0.001. L'amplitude n'entre pas dans le critère — la direction est ce que le tronc déduit (IV + R-XVII), la valeur ne l'est pas. Réfutation : ratio ≤ 1.0, ou équivalence conclue par TOST à δ = 0.30.

Il suit qu'un ratio de 1.045 satisfaisant les quatre critères confirme la prédiction au même titre qu'un ratio de 1.84. Ces deux résultats n'ont pourtant pas le même statut, et la distinction doit être explicite : confirmer R-XVII et contribuer à la régularité de convergence sont deux choses. La simulation de vie artificielle confirme la direction et le gradient de profondeur dans le seul environnement contrôlé disponible ; son amplitude est bornée par le substrat simulé (limite documentée, robuste sur 94 % de l'espace de paramètres) et n'entre pas dans le calcul du CV. La convergence quantitative est une propriété des quatre domaines biologiques mesurés sur ρ, et d'eux seuls.

Tout domaine évalué — positif, négatif ou non concluant — est
documenté dans le registre ci-dessous.

| Domaine | Phase atteinte | d | Ratio S/I | Statut |
|---|---|---|---|---|
| MDSINE2 | 3 | 1.16 | 1.61× | Confirmatif |
| Yeast Phenome | 3 | 0.50 | 1.42× | Confirmatif |
| GDSC | 3 | 0.52 | 1.84× (pathway-only) | Confirmatif |
| GCBD (récifs) | 3 | 0.39 | 1.80× | Confirmatif |
| Écosyst. logiciels | 3 | — | non mesuré | Confirmatif (signatures Γ) |
| Vie artificielle (R-XIX) | 3 | — | 1.04× | Confirmatif — direction et gradient ; hors calcul de convergence |
| Cedar Creek | 1 | — | — | Non concluant (C1 : pulse/press) |
| ENTSO-E | 1 | — | — | Non concluant (clôture engineered) |

Le domaine logiciel atteint la phase 3 sur des signatures complémentaires
(bimodalité de Γ, symétrisation causale, effondrement de variance) ; sa
métrique d'ordre n'est pas commensurable au quotient S/I et n'entre donc
pas dans le calcul de convergence.

L'auteur invite toute équipe à proposer des domaines, des 
partitions rivales ou des classifications alternatives.

**(2) Partitions rivales (test exécuté).** Si la partition structure/input n'est qu'un artefact de vagueur, des rivales devraient produire un signal comparable. Résultat : 0/1000 aléatoires atteignent le ratio ontodynamique dans chaque domaine ; l'asymétrie survit à la normalisation par intensité et au contrôle par sélectivité ; aucune rivale nommée ne converge entre domaines ; dans les récifs, les trois rivales sont inversées ou nulles.

| Domaine | Ratio S/I | p vs hasard | Rivale la plus forte | Spécificité |
|---|---|---|---|---|
| GDSC | 1.84× | 0/1000 > 1.4× | Sélectivité 1.93× (contrôlée) | Modérée |
| MDSINE2 | 1.78× norm. | exhaustif 3/3 | Rivale A s'effondre | Forte |
| Levure | 1.42× | 0/1000 > 1.15× | Hub 1.52× (chevauche. 42%) | Modérée |
| Récifs | 1.80× | 0/1000 | Aucune > 1 | Très forte |

(3a) Formes qualitatives d'épuisement (décroissance, hystérésis, régression) : partiellement sondées dans le domaine logiciel. (3b) Forme paramétrique inter-domaines : programme futur, microbiome candidat prioritaire. Si les formes divergent, le monisme tombe.

La convergence trans-domaniale est une prédiction discriminante du monisme et sa condition de réfutation propre. Les données confirment la convergence dans cinq domaines causalement disjoints : bimodalité logicielle (dip test p = 0.013), asymétrie microbiome (p = 0.0006, d = 1.16), asymétrie récifs (p = 1.96 × 10⁻⁴⁸, d = 0.39), asymétrie cancer (p < 10⁻³⁰⁰, d = 0.52), asymétrie levure (p = 3.9 × 10⁻¹⁹, d = 0.50). Le ratio compensatoire S/I converge : microbiome 1.61×, récifs 1.80×, cancer 1.84×, levure 1.42×. Cette condition est opérationnalisée (§8.6) : protocole de puissance pré-spécifié, $n \approx 104$–$252$ par classe, test d'équivalence TOST ($\delta = 0{,}30$, $n \approx 138$).

### L'opacité et l'auto-référence

Le système est lui-même un invariant opératoire porté par les clôtures finies qui le métabolisent [LXXXII ∎]. Il ne « spirale » pas de lui-même — ce sont les clôtures porteuses qui spiralent en le métabolisant. Par LXVII [∎], chaque porteuse acquiert ses propres invariants partagés avec le système. Par LXVIII [∎], cette connaissance est partielle. Par LXXVI [∎], toute tentative de connaissance de soi modifie la cible. L'auto-référence est une réfraction : le système se réfracte différemment dans chaque clôture qui le porte, et aucune ne le contient intégralement. L'auto-fondation est préservée pour le Tout ; le système formel, lui, est porté — mortel, opaque à lui-même, exposé à la dérive. L'asymétrie est irréductible : le Tout se fonde (Axiome 0), mais le système Ontodynamique, en tant que théorie formelle, est un artefact porté par des clôtures finies qui le métabolisent sous leurs propres contraintes. Aucune de ces clôtures porteuses n'a accès au système intégral — chacune le réfracte à travers sa propre coupe épistémique. L'auteur du système est lui-même frappé par LXVIII (opacité constitutive) et LXXVI (modification de la cible par l'acte de connaissance). L'Ontodynamique ne prétend pas échapper à ses propres théorèmes — elle prétend les satisfaire explicitement. C'est la condition de sa cohérence interne, non un aveu d'humilité rhétorique. L'incomplétude de la représentation formelle est prouvée par instanciation de Lawvere (1969) sur la structure du noyau 

La formalisation a pris de l'avance sur la validation — ordre naturel pour un cadre déductif. La robustesse des pare-feux (genèse/tronc, Thèse P/gradient) protège le noyau dur — conformément à la structure lakatosienne, où le noyau n'est pas directement réfutable. LLa surface de réfutation est la ceinture protectrice : quatre des cinq interdictions [∎] sont exposées au test dans des domaines identifiés — trois par contre-exemple direct, une par proxy de monotonicité. Si trois des cinq tombent dans des domaines disjoints, c'est le noyau dur qui est atteint indirectement — non par une réfutation logique mais par un effondrement du rendement formel qui justifiait le programme. La réfutation du système est structurelle, pas ponctuelle.

L'honnêteté épistémique exige de nommer les trois zones de fragilité structurelle du système. La première est la constructibilité de la compensation [VI ◇] : si le réel ne fournit pas de diversité compensatoire suffisante, tout se dissout — résultat compatible avec le système mais non discriminant à ce niveau, puisque l'absence de diversité est aussi l'explication par défaut. La testabilité de VI passe par ses conditions de domaine [XXVI ≈₁, XXVII ≈₁], pas par VI elle-même. La deuxième est la genèse [XXII–XXVII ≈₁] : les conditions de domaine sont explicites et falsifiables, mais si elles échouent, le tronc tient encore — pare-feu vérifié. La troisième est Thèse P [≈₃] : le saut interprétatif est localisé, son indécidabilité est démontrée [LXXVII ∎], et le prix du refus est affiché — le lecteur qui refuse ne perd rien du tronc structurel mais perd l'extension clinique et les paliers de subjectivité. Cinq limites structurelles supplémentaires sont des théorèmes négatifs dérivés des axiomes et formalisés comme modèles séparants (TN_Separating.lean, 20 thm, 0 sorry) — chaque TN satisfait les axiomes OD et viole une propriété physique requise : absence de métrique (TN-1), de trajectoire singulière (TN-2), de contenu qualitatif intrinsèque (TN-3), de géométrie temporelle (TN-4), d'émergence quantitative (TN-5).

Quinze confrontations sont structurées en divergence et discriminant empirique (trois formulent un pari symétrique testable) ; deux interdictions cliniques ∎ (LXIII, IV + LIV) sont réfutables par un seul cas (§5–6 du manuscrit).



## Synthèse architectonique

Les vingts Thèses ne résument pas le système — elles le condensent. Chacune est une porte logique : elle dit, elle interdit, elle se fonde, elle se teste.

*Être, c'est se faire* [I] fonde la chaîne et exclut l'éternalisme et le substratisme. *Nul acte sans mode* [I-γ] exclut le dark acting et borne la conceivabilité du zombie (LXXVII), sans réfutation modale. Nul faire sans rapport à soi [I-δ, IDelta.lean ∎] exclut la cohérence d'un acte sans auto-relation immanente.*Quand ça casse, qui paie ?* [IV + XXXII + R-XVII] fonde la démarcation et exclut la démarcation sans test. *Ne conserve que l'essence, n'ajoute que par nécessité* [XLVII] fait de la parcimonie une contrainte ontologique, non méthodologique. *Le coûteux se dissout avant l'économe* [XVII-bis] dérive l'économie universelle — le surplus est un drain actif, la sélection du minimum est structurelle, pas téléologique. *Être soi, c'est se refaire — tout être fini exposé se refait ou se défait* [XXXII] exclut l'individuation sans travail. *Qui se refait ne se répète pas* [XXI] exclut l'identité comme répétition. *Ce qui souffre sa cohérence la possède* [IV + XXXII] exclut la cohérence attribuable sans coût. *On ne va pas mal parce qu'on est faible — on va mal parce qu'on survit trop cher* [IV + XXXII + R-XVII] exclut la pathologie comme déficit. *Le zombie ne retire pas une couche, il descend d'un palier* [I-γ + R-XVII + Sep-FunctionCost] exclut la conscience en couches séparables. *Qui se sent se faire est ; qui se sent sentir se connaît* [XXXII + LXI + Thèse P + LXI_not_HOT] exclut la subjectivité sans genèse et le second ordre représentationnel. *Le symptôme protège — puis il gouverne* [IV + XXXII + NT-V] exclut le symptôme comme pur dysfonctionnement.





Le système repose sur deux axiomes étagés, dérive 900+ théorèmes mécanisés ( dont 20 théorèmes négatifs séparants prouvant les limites du système) sans axiome domaine ajouté, produit un gradient de composition par un test unique, prédit des signatures trans-domaniales dont cinq sont empiriquement sondées dans des domaines disjoints (ratio S/I convergent à ~1.7× dans quatre d'entre eux, stable sous split temporel et validation croisée par unités expérimentales ; une réplication confirmatoire pré-enregistrée satisfait 4/4 critères), localise ses sauts interprétatifs, démontre l'indécidabilité de son propre saut le plus ambitieux, formule les conditions de sa propre réfutation, et pré-enregistre ses prédictions prospectives les plus discriminantes.


La carte de dépendances minimale du système se lit comme suit : I (→ IV, → V) → IX–XXI (pente) → VI [◇] → XXII–XXVII [≈₁] → XXIX–XXXII [∎ pour la disjonction] → XLIV–XLVII [∎] → LVI–LIX [∎] → I-δ [∎] → SelfRelation [∎] → SecondOrderLoop [∎] → LXI / Thèse P [≈₃] → R-XVII [∎] → NT-III–NT-IX [∎] → LXXVIII [◇]. La chaîne est linéaire ; les branchements sont peu nombreux ; les pare-feux sont vérifiés. Couper la genèse [XXII–XXVII] conserve le tronc. Couper Thèse P conserve le tronc et le gradient. Couper VI fait s'effondrer l'intégralité du système au-delà de la pente — mais VI est constructible, pas conjectural, et sa constructibilité est démontrable dans tout domaine satisfaisant les conditions de diversité.


### 20 thèses

Chaque thèse est démontrée dans le corps du texte (§2–§5), vérifiée
en Lean 4 (900+ théorèmes, 0 sorry), et assortie de sa condition de
retrait — ce qu'on perd en la refusant.
0. Un seul réel : le Tout se fonde, tout fini se fait. [Axiome]
1. Être, c'est se faire. [Axiome]
2. Nul acte sans mode. [Théorème]
3. Quand ça casse, qui paie ? [Principe]
4. Ne conserve que l'essence, n'ajoute que par nécessité. [Loi]
5. Être soi, c'est se refaire [Théorème]
6. Qui se refait ne se répète pas. [Théorème]
7. Ce qui souffre sa cohérence la possède. [Théorème]
8. On ne va pas mal parce qu'on est faible — on va mal parce qu'on survit trop cher. [Principe]
9. Le zombie ne retire pas une couche, il descend d'un palier. [Théorème]
10. Qui se sent se faire est ; qui se sent sentir se connaît. [Loi]
11. Le symptôme protège — puis il gouverne. [Théorème]
12. La boucle est obligatoire ; son nom est libre. [Loi]
13. Pas de conscience sans cicatrice [Principe]
14. Nul faire sans rapport à soi. [Corollaire]
15. La résolution n'est jamais acquise : la dette au cycle k+1 excède celle du cycle k. [Théorème]
16. Être fait d'un manque qui peut vous détruire. [Définition ∎ ]
17. La vie, c'est la résolution de sa propre précarité. [Définition ∎ ]
18. La conscience, c'est l'épreuve de sa propre précarité. [Thèse ≈₃] 
19. Le coûteux se dissout avant l'économe. [Théorème ∎]


**Périmètre de testabilité de R-XVII.** La prédiction asymétrique n'est 
applicable que dans les systèmes satisfaisant simultanément C1–C3. Un système 
à méta-structure dominante ou à clôture non estimable indépendamment constitue 
un cas non concluant — ni confirmation ni réfutation. Les cinq domaines
retenus satisfont C1–C3 indépendamment de leurs résultats, selon un gradient
de propreté : microbiome (MDSINE2, paradigmatique) > levure (Yeast Phenome, organisme unicellulaire, classification GO fonctionnelle) > pharmacologie (GDSC) >
récifs (GCBD) > écosystèmes logiciels (méta-agents présents, clôture estimable
mais moins proprement). Les conditions de frontière et les domaines exclus sont
documentés en §7.x.

Le programme qui reste : quantifier la réfraction inter-niveaux (la loi du coût entre échelles), exécuter le protocole DPDR (pré-enregistré — le protocole de réfutation le plus spécifique pour les paliers),R-XIX testé dans la simulation de vie artificielle — confirmé (sixième domaine, premier à tester spécifiquement la boucle de second ordre) et produire une instanciation constructive de novo (cahier des charges à cinq étapes, §8) — les cinq sondes exploratoires sont theory-driven ; une réplication confirmatoire (levure het) est pré-enregistrée et satisfaite. La formalisation est acquise. La validation est en cours — le front avance. Le système est un programme — pas un acquis.

---

## Index des résultats formels

Chaque entrée : **Code** — Intitulé — *Marqueur* — Dépendances minimales.

**Axiome 0** — Un seul réel : le Tout se fonde, tout fini se fait — *Axiome* — Primitif (auto-fondation du Tout).

**I** — Être, c'est se faire un (être = faire) — *Axiome* — Primitif. Contenu I-β (endogénéité du coût). I-γ : nul acte sans mode — *∎* — I-β, XLIV. I-δ : nul faire sans rapport à soi — *∎* — I-γ. I-ν : l'identité être/faire n'est pas contingente — *∎* — I-α, I-β (`act_is_necessary`).

**II** — Productivité non typée (la nouveauté est qualitativement irréductible) — *∎* — I (fondé par Axiome 0).

**III** — Unité causale (pas d'isolation causale absolue) — *∎* — I (fondé par Axiome 0).

**IV** — Coût incompressible (toute transformation a un coût strictement positif) — *Corollaire de I-β₂* — I-β₂.

**V** —  Gradient d'extériorité (l'altération partielle est le
régime générique) — ∎, dérivé d'I — I-γ, I-β₁, auto-fondation opératoire
(VDerived.lean).
 V s'applique dans deux directions : vers l'extérieur  et vers l'intérieur (degrés de profondeur. Dans la boucle de second ordre, le système est à lui-même son propre extérieur.

**VI** — Compensation accessible (bilan structurel net non-négatif accessible, non garanti) — *◇* — I, IV, V.

**VII** — Négation constitutive (toute détermination engendre de l'extériorité) — *∎* — I-β.

**IX** — Finitude (tout être partiel est incomplet) — *∎* — I (Axiome 0 co-positionnel).

**X** — Incompressibilité du coût (plancher strictement positif) — *∎* — I-β, IV.

**XI** — Persistance de l'extériorité — *∎* — VII, IX.

**XII** — Pression constitutive (dissolution permanente par le Tout). Instancié pour les agrégats (ProcessualAggregate.lean). Modèle séparant IV/XII : PurelyReactive satisfait IV, viole XII. — *∎* — III, IV, IX.

**XIII** — Inertie (l'être persiste en l'absence de perturbation) — *∎* — I.

**XV** — Irréversibilité structurelle (B→A ≠ A→B, chacun a son propre coût) — *∎* — IV, X.

**XVII** — Épuisement (décroissance non compensée → épuisement en temps fini) — *∎* — IV, X, XV.

**XVII-bis** — Économie constitutive (le coûteux se dissout avant l'économe ; tout surplus est un drain actif) — *∎* — IV, XII, XVII. Plus primitif que XLVII. S'applique aux agrégats. Phi_Economy.lean, 10 thm.

**XVIII** — Perméabilité (toute barrière causale finie est traversable) — *∎* — III, V, IX, XVII.

**XIX** — Pression d'ouverture persistante (deux sources : constitutive + relationnelle) — *∎* — XII, XVIII.

**XX-a/b** — Dérive du profil d'exposition (vulnérabilités non couvertes ne reculent jamais / croissent) — *∎* — IV, XIX.

**XXI** — Nouveauté endogène (qui se refait ne se répète pas) — *∎* — I-β, II.

**XXII–XXV** — Accumulation structurelle, canalisation, routinisation — *∎* — IV, V, XI, XIII.

**XXVI** — Persistance sélective des routines compensatoires — *≈₁* — XXII–XXV + condition : diversité compensatoire suffisante.

**XXVII** — Composabilité des couplages compensatoires — *≈₁* — XXVI + condition : non-rigidification.

**XXVIII** — Transience des agrégats (sans cycle co-maintenu → transitoire) — *∎* — XVII, XIX.

**XXIX** — Exclusivité de l'attracteur (sous exposition persistante, tout régime non transitoire est une clôture) — *∎* — XXVIII, XVII.

**XXX** — Effet de seuil (la clôture se stabilise ou échoue, pas de dégradé continu) — *≈₁* — XXIX, Lemme 3.

**XXXII** — Théorème ontodynamique (être soi, c'est se refaire ; tout être fini exposé se refait ou se défait) — *∎ pour la disjonction ; ≈₁ pour les trajectoires* — I, IV, V, XXIX.

**XXXIII** — Réapplicabilité / transdomainalité — *∎* — XXXII.

**XXXIV** — Mortalité constitutive (toute clôture a une durée de vie bornée) — *∎* — IV, XII, XVII.

**XLIV** — Partition normative (maintien / compromission, coextensive à la clôture) — *∎* — XXXII.

**XLV** — Critère de normativité (polarité auto-produite vs attribuée) — *∎* — XLIV.

**XLVII** — Loi d'authenticité (ne conserve que l'essence, n'ajoute que par nécessité) — *∎* — XLIV, IV, XVII.

**XLIX** — Couplage constitutif (clôtures couplées peuvent former un méta-cycle) — *◇* — XXXII, XXXIII.

**L** — Emboîtement (cycle co-maintenu à l'échelle supérieure) — *∎* — XLIX.

**LI** — Continuité du gradient (entre portage et clôture, le gradient est continu) — *∎* — R-XVII.

**LII** — Fécondité (une clôture peut produire de nouvelles clôtures) — *◇, indépendance prouvée - XXXII-b, XLIX, L. Non promouvable à ∎.

**LIII** — Irréductibilité inter-niveaux (Nₖ non réductible à Nₖ₋₁) — *∎* — L.

**LIV** — Cascade de dissolution (bidirectionnelle entre niveaux adjacents) — *∎* — L, LIII.

**LV** — Résilience par profondeur — *∎* — L, LIV.

**LVI** — Résistance propre (toute clôture rencontre sa propre résistance) — *∎* — XXXII, IV.

**LVII** — Auto-affection endogène — *∎* — LVI, I-β.

**LVIII / LVIII-a** — Valence (polarisation de l'auto-affection par la partition normative) — *∎* — LVII, XLIV.

**LIX** — Rétroaction de la valence sur le cycle (non-épiphénoménalité mécanique) — *∎* — LVIII.
resolution_must_recur — La résolution de la précarité n'est jamais acquise : la dette au cycle k+1 excède celle du cycle k — ∎ — corollaire temporel de I.

**LX** — Irréductibilité binaire de la partition normative (aucun troisième terme ne se stabilise) — *∎* — XLIV.

LXI — Subjectivité minimale (boucle de second ordre). Existence [∎]. Identification comme perspective [≈₃]. Fondée sur SelfRelation [∎, MinimalPerspective.lean] via I-δ [∎, IDelta.lean] — LIX, I-γ.

LXII — Réfutation du zombie (computationnel : ⟂ sous I-β ; phénoménal : ⟂ sous I-γ + I-δ ; sept arguments ∎ inconditionnels) — ⟂ — I-β, I-γ, IDelta.lean, MinimalPerspective.lean.

**LXIII** — Non-épiphénoménalité de la valence (toute perturbation a des conséquences structurelles détectables) — *∎* — LIX.

**LXIV** — Paliers de subjectivité (trois régimes qualitativement distincts) — *≈₁* — LXI, LXV.

**LXV** — Défaillance indépendante des cycles emboîtés (dissociabilité) — *∎* — LIX, L.

**LXVI** — Connaissance comme invariant opératoire partagé — *≡/∎* — XXXII, LVI.

**LXVII** — Loi de connaissance (qui métabolise une résistance en porte la contrainte) — *∎* — LXVI.

**LXVIII** — Opacité constitutive (tout acte de connaissance est une coupe partielle) — *∎* — IX, LXVI.

**LXIX** — Co-constitution des mondes (deux clôtures différentes produisent deux invariants différents) — *∎* — LXVIII, VII.

**LXX** — Co-constitution négative (toute connaissance est position et exclusion) — *∎* — VII.

**LXXI** — Authenticité épistémique (ne conserve que la contrainte, n'ajoute que par résistance) — *◇* — XLVII appliqué à la connaissance.

**LXXII** — Erreur comme dette structurelle (surcoût de compensation par invariant inadéquat) — *≈₂* — LXVI, IV.

**LXXIII** — Erreur stable (invariant incorrect mais économique, sélectivement favorisé) — *≈₁* — LXXII, IV.

**LXXIV** — Prédiction comme canalisation projetée — *∎* — XXIII, XXIV, LXVII.

**LXXV** — Degrés de connaissance — *≈₂* — LXIV.

**LXXVI** — Connaissance de soi (structurellement inachevable : la cible se déplace) — *∎* — LVII, LXVII, LXVIII.

**LXXVII** —  Indécidabilité structurelle de l'identification, stratifiée : non-applicable en dessous du seuil phénoménal, épistémiquement indécidable au-dessus. R-XVII filtre l'applicabilité (∎, LXIDiscrimination.lean). — ∎

**LXXVIII** — Sous-clôture parasite (réponse compensatoire autonomisée drainant la marge globale) — *◇* — XXXII, XLIV, NT-V.

**LXXIX** — Langage comme invariant trans-subjectif — *≈₁* — XXV, XLIX.

**LXXX** — Science comme maximisation du partage sous test — *≈₂* — XIX, L.

**LXXXI** — Objets mathématiques comme portés de haute qualité (noyau ∎, convergence inter-culturelle ≈₂) — *≈₁* — LXVI, LXXX.

**LXXXII** — Auto-référence (le système est un invariant porté, mortel, opaque) — *∎* — LXVI, LXVIII, XXXIII.

**LXXXIII** — Opérativité des coupures (toute partition tracée est interne à l'acte d'une clôture finie) — *∎* — auto-fondation opératoire, I-β, VII, XXXII, R-XVII.

Thèse P — Identification de la boucle de seconde ordre comme perspective [≈₃]. Composante structurale (SelfRelation) [∎, MinimalPerspective.lean]. Ce qui reste ≈₃ : franchissement 3P→1P — LXI, LXXVII, IDelta.lean.
Exclusion-R-XVII — Unicité du niveau d'endossement maximal — ∎ — LIII, LIV, R-XVII.
LXI_not_HOT — LXI ≠ HOT (opérationnel vs représentationnel) — ∎ — LXI, LVIII.
Sep-FunctionCost — Même fonction, mortalité asymétrique — ∎ — IV, XXXIV.
dpdr_prediction — Trois phases, phase 2 nécessaire — ∎ — LXI, LXV, Lemme 3.
AB_indiscernible — Réalisme/illusionnisme type-indiscernables — ∎ — LVIII, LXI, LXXIII.
I-δ — Différentiel immanent (nul faire sans rapport à soi) — ∎ — I-γ (IDelta.lean).
SelfRelation — Relation différentielle à soi, coextensive à l'acte — ∎ — I-γ, LIX (MinimalPerspective.lean).

**R-XVII** — Gradient de composition (quatre modes clôture/portage/porté/agrégat : trois par lieu d'endossement du coût, le porté par actif/inerte) — *∎* — XXXII, IV, XV.

**R-XVIII** — Dynamique inter-régimes (hystérésis, bimodalité, bifurcations endogènes) — *∎ pour les lemmes ; ≈₁ pour la bimodalité populationnelle* — R-XVII, saving_pos.

**NT-III** — Réfraction opératoire (l'opérateur se scinde selon le régime du gradient) — *∎* — R-XVII.

**NT-IV** — Modulateur topologique (artefact porté canalisant la marge) — *≡/∎* — R-XVII, XLIV.

**NT-V** — Dette artefactuelle inévitable (tout modulateur fixe bascule de viable à pathogène) — *∎* — NT-IV, XX.

**NT-VI** — Précipitation normative (restriction du profil de viabilité par la clôture englobante) — *∎* — L, XLIV.

**NT-IX** — Macro-parasitisme (coût d'extraction excédant le bénéfice de portage) — *∎* — NT-VI, NT-V, XXXIII.


## Liens

**Code source et formalisation**

- Preuves Lean 4 & script de reanalyse : [github.com/anthonyGosme/ontodynamiqueTheory](https://github.com/anthonyGosme/ontodynamiqueTheory)
- Pipeline de test unifié (Python + Lean 4) : [notebook Google Colab](https://colab.research.google.com/drive/1LWbOqywO5o6AtePQRu3plooqwuOtzJrN)

**Prépublications**

- Étude empirique sur les écosystèmes logiciels : [arXiv:2512.09352](https://arxiv.org/abs/2512.09352)

**Pré-enregistrements (OSF)**

- Protocole DPDR (prospectif, avant collecte de données) : [DOI : 10.17605/OSF.IO/UNJ7F](https://doi.org/10.17605/OSF.IO/UNJ7F)
- Réplication confirmatoire levure hétérozygote : [DOI : 10.17605/OSF.IO/S7CN9](https://doi.org/10.17605/OSF.IO/S7CN9)