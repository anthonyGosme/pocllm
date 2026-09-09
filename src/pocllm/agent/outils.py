"""Outils de l'agent — les mêmes fonctions que servent les serveurs MCP.

Le jalon 5 a prouvé le transport MCP sur stdio ; le jalon 4 porte sur la boucle,
pas sur le transport. On appelle donc les fonctions en direct, sans payer un
sous-processus et une reconstruction d'index par appel. Ce sont littéralement
les mêmes fonctions : `pocllm.mcp._commun.chercher` et `resultat_formel`.
"""
from __future__ import annotations
import re

from pocllm.mcp._commun import chercher, envelopper
from pocllm.mcp.systeme_maison import resultat_formel as _resultat_formel

# Les chiffres romains sont partout dans le canon (propositions, livres,
# chapitres) : y envoyer un code maison ramène PROPOSITION XXXI. On le retire.
_CODE = re.compile(r"^\s*(?:[IVXLC]{1,7}(?:-bis|-ter)?|R-[IVXLC]+|NT-[IVXLC]+)\s*[—–-]\s*")


def chercher_canon(question: str, k: int = 6, lexical_seul: bool = False) -> str:
    return envelopper(chercher("canon", _CODE.sub("", question), k=k, dense=not lexical_seul))


def chercher_maison(question: str, k: int = 6) -> str:
    return envelopper(chercher("maison", question, k=k))


def resultat_formel(code: str) -> str:
    return _resultat_formel(code)


SCHEMAS = [
    {"name": "chercher_canon",
     "description": "Cherche dans le canon philosophique français (23 œuvres du domaine "
                    "public, 21 600 passages : Spinoza, Kant, Descartes, Rousseau, Pascal, "
                    "Locke, Malebranche, Leibniz, Nietzsche, Montesquieu, Schopenhauer, "
                    "Platon, Bergson, Montaigne, Hume). Formule la requête en langue "
                    "naturelle : n'y mets JAMAIS un code du système maison, les chiffres "
                    "romains y désignent des propositions et pollueraient la recherche.",
     "input_schema": {"type": "object", "properties": {
         "question": {"type": "string", "description": "requête en langue naturelle"},
         "k": {"type": "integer", "description": "nombre de passages (défaut 6)"},
         "lexical_seul": {"type": "boolean",
                          "description": "true pour une référence exacte — auteur, numéro de "
                                         "proposition, pagination — où le lexical fait mieux"}},
         "required": ["question"]}},
    {"name": "chercher_maison",
     "description": "Cherche dans le système Ontodynamique : prose (manuscrit, résumé) et "
                    "preuves Lean 4. Utilise-le pour retrouver une thèse, un passage, ou un "
                    "identifiant de théorème.",
     "input_schema": {"type": "object", "properties": {
         "question": {"type": "string"},
         "k": {"type": "integer", "description": "nombre de passages (défaut 6)"}},
         "required": ["question"]}},
    {"name": "resultat_formel",
     "description": "Fiche structurée d'un résultat formel du système par son code (I, IV, "
                    "XXXII, XVII-bis, R-XVII, NT-IX, LXVIII…) : intitulé, MARQUEUR DE FORCE "
                    "et dépendances minimales. Le marqueur borne ce qu'on peut conclure : "
                    "∎ démontré, ◇ constructible mais NON démontré, ≈ conditionnel. "
                    "Consulte-le avant de t'appuyer sur un résultat.",
     "input_schema": {"type": "object", "properties": {
         "code": {"type": "string", "description": "ex. XXXII, VI, XVII-bis, R-XVII"}},
         "required": ["code"]}},
]

IMPLEMENTATIONS = {"chercher_canon": chercher_canon,
                   "chercher_maison": chercher_maison,
                   "resultat_formel": resultat_formel}
