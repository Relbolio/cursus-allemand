"""Build du workspace : découvre les leçons, fiches et learning-records depuis les fichiers,
synchronise status.json (lu par le site) et régénère les paquets Anki.

Usage :  python build.py          (depuis la racine du workspace)

Ce qui est GÉNÉRÉ dans status.json (écrasé à chaque build) :
    lecons[], references[], records[], compteurs, anki, misAJour
Ce qui est PRÉSERVÉ (édité à la main par le professeur) :
    niveau, semaine, positionActuelle, prochaineEtape, gates,
    et pour chaque leçon déjà connue : etat ("a-faire" | "faite") et faiteLe.

Métadonnées lues dans les fichiers :
    lessons/NNNN-slug.html  : <title>, kicker « Leçon N · Niveau A1 · ≈ 35 minutes », « Leçon créée le 21 septembre 2026 »
    reference/*.html        : <title>, <meta name="niveau" content="A1"> (sinon « Transversal »), première date française
    learning-records/*.md   : première ligne « # titre »
Aucune dépendance hors bibliothèque standard.
"""
from __future__ import annotations

import json
import re
import time
from datetime import date
from pathlib import Path

import build_anki

ROOT = Path(__file__).resolve().parent
MOIS = {m: i + 1 for i, m in enumerate(
    ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"])}
RE_DATE_FR = re.compile(r"(\d{1,2})(?:er)?\s+(" + "|".join(MOIS) + r")\s+(\d{4})", re.I)


def date_fr(text: str, fallback: Path | None = None) -> str:
    m = RE_DATE_FR.search(text)
    if m:
        return f"{int(m.group(3)):04d}-{MOIS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}"
    if fallback is not None:
        return date.fromtimestamp(fallback.stat().st_mtime).isoformat()
    return ""


def title_of(html: str, default: str) -> str:
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else default


def scan_lessons() -> list[dict]:
    out = []
    for p in sorted((ROOT / "lessons").glob("[0-9][0-9][0-9][0-9]-*.html")):
        html = p.read_text(encoding="utf-8")
        numero = int(p.name[:4])
        titre = re.sub(r"^Leçon\s+\d+\s*[—–-]\s*", "", title_of(html, p.stem))
        kick = re.search(r'class="kicker">(.*?)</div>', html, re.S)
        kick_txt = kick.group(1) if kick else ""
        niveau = (re.search(r"Niveau\s+([ABC][12])", kick_txt) or [None, ""])[1]
        duree = (re.search(r"≈\s*(\d+)\s*min", kick_txt) or [None, ""])[1]
        cree = re.search(r"Leçon créée le ([^<.]+)", html)
        out.append({
            "numero": numero, "titre": titre, "fichier": f"lessons/{p.name}", "niveau": niveau or "A1",
            "duree": int(duree) if duree else None, "date": date_fr(cree.group(1) if cree else "", p),
        })
    return out


def scan_references() -> list[dict]:
    out = []
    for p in sorted((ROOT / "reference").glob("*.html")):
        html = p.read_text(encoding="utf-8")
        meta = re.search(r'<meta\s+name="niveau"\s+content="([^"]+)"', html)
        footer = re.search(r"<footer>(.*?)</footer>", html, re.S)
        sub = re.search(r'class="sub">(.*?)</p>', html, re.S)
        out.append({
            "titre": title_of(html, p.stem), "fichier": f"reference/{p.name}",
            "niveau": meta.group(1) if meta else "Transversal",
            "date": date_fr((footer.group(1) if footer else "") + " " + (sub.group(1) if sub else ""), p),
        })
    return out


def scan_records() -> list[dict]:
    out = []
    for p in sorted((ROOT / "learning-records").glob("[0-9][0-9][0-9][0-9]-*.md")):
        txt = p.read_text(encoding="utf-8")
        first = next((l for l in txt.splitlines() if l.startswith("# ")), "# " + p.stem)
        out.append({"numero": int(p.name[:4]), "titre": first[2:].strip(), "fichier": f"learning-records/{p.name}",
                    "date": date_fr(txt, p)})
    return out


def main() -> None:
    build_anki.main()
    manifest = json.loads((ROOT / "anki" / "index.json").read_text(encoding="utf-8"))

    sp = ROOT / "status.json"
    status = json.loads(sp.read_text(encoding="utf-8")) if sp.exists() else {"version": 1}
    old = {l["numero"]: l for l in status.get("lecons", [])}

    lecons = []
    for l in scan_lessons():
        prev = old.get(l["numero"], {})
        l["etat"] = prev.get("etat", "a-faire")
        if prev.get("faiteLe"):
            l["faiteLe"] = prev["faiteLe"]
        elif l["etat"] == "faite" and prev.get("date"):
            l["faiteLe"] = prev["date"]          # migration : l'ancien champ date valait « validée le »
        lecons.append(l)

    status["lecons"] = lecons
    status["references"] = scan_references()
    status["records"] = scan_records()
    status["anki"] = {"cartes": manifest["tout"]["cartes"], "decks": manifest["tout"]["decks"],
                      "manifeste": "anki/index.json", "tout": manifest["tout"]["fichierApkg"]}
    status["compteurs"] = {"leconsFaites": sum(1 for l in lecons if l["etat"] == "faite"),
                           "leconsGenerees": len(lecons), "references": len(status["references"]),
                           "records": len(status["records"])}
    status["misAJour"] = time.strftime("%Y-%m-%d")
    sp.write_text(json.dumps(status, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"status.json : {len(lecons)} leçons ({status['compteurs']['leconsFaites']} faites), "
          f"{len(status['references'])} fiches, {len(status['records'])} records, {status['anki']['cartes']} cartes")
    for l in lecons:
        print(f"  {l['numero']:04d} [{l['niveau']}] {l['titre']}  ({l['etat']}, créée {l['date']}"
              + (f", faite {l['faiteLe']}" if l.get("faiteLe") else "") + ")")


if __name__ == "__main__":
    main()
