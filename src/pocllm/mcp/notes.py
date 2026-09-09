"""Serveur MCP `notes` — écriture des objections retenues et des révisions.

Seul serveur qui écrit, donc seul serveur soumis au §6 : « human-in-the-loop
avant toute écriture ». La barrière n'est pas une consigne dans le prompt — un
agent peut l'ignorer — mais une **contrainte de protocole** : `proposer` met la
note en attente et rend un identifiant ; `confirmer` seul écrit, et personne
d'autre que l'utilisateur n'est censé l'appeler. Un agent qui voudrait écrire
sans validation ne le peut pas : il n'a que la moitié du chemin.
"""
from __future__ import annotations
import json, time, uuid
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from pocllm.mcp._commun import ROOT

server = MCPServer(
    name="notes",
    instructions="Consigne les objections retenues et les révisions de thèses. "
                 "Toute écriture passe par une validation humaine explicite.")

DIR = ROOT / "data" / "notes"
ATTENTE = DIR / "en_attente.jsonl"
JOURNAL = DIR / "journal.jsonl"


def _ajouter(p: Path, obj: dict) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _lire(p: Path) -> list[dict]:
    return [json.loads(l) for l in p.open(encoding="utf-8")] if p.exists() else []


@server.tool(description="Propose une note. N'écrit RIEN au journal : met en attente de validation.")
def proposer(type: str, these: str, contenu: str, sources: list[str] | None = None) -> str:
    """`type` : objection | revision | tension. `sources` : identifiants de passages
    qui fondent la note — une note sans source est recevable mais signalée."""
    if type not in ("objection", "revision", "tension"):
        return "type invalide : attendu objection, revision ou tension."
    note = {"id": uuid.uuid4().hex[:8], "type": type, "these": these, "contenu": contenu,
            "sources": sources or [], "propose_le": time.strftime("%Y-%m-%dT%H:%M:%S")}
    _ajouter(ATTENTE, note)
    alerte = "" if note["sources"] else "\nATTENTION : aucune source citée."
    return (f"Note {note['id']} EN ATTENTE — rien n'est écrit au journal.{alerte}\n"
            f"Elle ne sera consignée que si l'utilisateur appelle `confirmer('{note['id']}')`. "
            "N'appelle pas cet outil toi-même : la validation lui revient.")


@server.tool(description="RÉSERVÉ À L'UTILISATEUR. Valide une note en attente et l'écrit au journal.")
def confirmer(note_id: str, verdict: str = "retenue") -> str:
    attente = _lire(ATTENTE)
    note = next((n for n in attente if n["id"] == note_id), None)
    if note is None:
        return f"Aucune note en attente sous l'identifiant {note_id}."
    note["verdict"] = verdict
    note["confirme_le"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    _ajouter(JOURNAL, note)
    restantes = [n for n in attente if n["id"] != note_id]
    ATTENTE.write_text("".join(json.dumps(n, ensure_ascii=False) + "\n" for n in restantes),
                       encoding="utf-8")
    return f"Note {note_id} consignée au journal ({verdict})."


@server.tool(description="Liste les notes en attente de validation.")
def en_attente() -> str:
    notes = _lire(ATTENTE)
    if not notes:
        return "Aucune note en attente."
    return "\n".join(f"{n['id']} [{n['type']}] {n['contenu'][:96]}"
                     f"{'  (sans source)' if not n['sources'] else ''}" for n in notes)


@server.resource("notes://journal", description="Journal des notes validées.")
def journal() -> str:
    notes = _lire(JOURNAL)
    if not notes:
        return "Journal vide."
    return "\n\n".join(
        f"[{n['confirme_le']}] {n['id']} · {n['type']} · {n.get('verdict', '')}\n"
        f"Thèse : {n['these']}\n{n['contenu']}\n"
        f"Sources : {', '.join(n['sources']) or 'aucune'}" for n in notes)


@server.prompt(description="Gabarit : réviser une thèse après une objection tenue pour valide.")
def revision(these: str, objection: str) -> str:
    return (f"Thèse actuelle :\n{these}\n\nObjection tenue pour valide :\n{objection}\n\n"
            "Propose une révision minimale : la plus petite modification qui absorbe l'objection "
            "sans changer ce que la thèse n'avait pas à changer. Indique explicitement ce que la "
            "révision fait perdre. Puis appelle `proposer` — et arrête-toi là : la validation "
            "revient à l'utilisateur, pas à toi.")


if __name__ == "__main__":
    server.run()
