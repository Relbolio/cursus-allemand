"""Construit les paquets Anki (.apkg) et le manifeste anki/index.json
à partir des fichiers texte anki/leconNN-*.txt.

Usage :  python build_anki.py        (depuis la racine du workspace)

- Aucune dépendance : sqlite3, zipfile, json, hashlib (bibliothèque standard).
- Format .apkg « legacy » (schéma 11), importé par Anki Desktop 2.1+, AnkiDroid et AnkiMobile.
- Identifiants stables (deck, modèle, GUID des notes) dérivés des noms : réimporter un paquet
  mis à jour ajoute seulement les nouvelles cartes et conserve la progression.

Format des fichiers .txt (séparateur point-virgule, UTF-8) :
    # titre: Leçon 02 · nombres, alphabet, haben
    # deck: Allemand A1::L02 nombres alphabet haben
    # niveau: A1
    # lecon: 2
    # type: general | it
    recto;verso
Les lignes commençant par # sont ignorées par Anki et servent de métadonnées ici.
"""
from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANKI_DIR = ROOT / "anki"

MODEL_NAME = "Allemand (recto-verso)"
CSS = """.card { font-family: Georgia, "Palatino Linotype", serif; font-size: 24px; text-align: center;
 color: #111; background: #fffff8; padding: 12px; }
.small { font-size: 14px; color: #666; margin-top: 18px; }
hr#answer { border: 0; border-top: 1px solid #ddd; margin: 18px 0; }"""

SCHEMA = """
CREATE TABLE col (id integer primary key, crt integer not null, mod integer not null, scm integer not null,
 ver integer not null, dty integer not null, usn integer not null, ls integer not null, conf text not null,
 models text not null, decks text not null, dconf text not null, tags text not null);
CREATE TABLE notes (id integer primary key, guid text not null, mid integer not null, mod integer not null,
 usn integer not null, tags text not null, flds text not null, sfld integer not null, csum integer not null,
 flags integer not null, data text not null);
CREATE TABLE cards (id integer primary key, nid integer not null, did integer not null, ord integer not null,
 mod integer not null, usn integer not null, type integer not null, queue integer not null, due integer not null,
 ivl integer not null, factor integer not null, reps integer not null, lapses integer not null, left integer not null,
 odue integer not null, odid integer not null, flags integer not null, data text not null);
CREATE TABLE revlog (id integer primary key, cid integer not null, usn integer not null, ease integer not null,
 ivl integer not null, lastIvl integer not null, factor integer not null, time integer not null, type integer not null);
CREATE TABLE graves (usn integer not null, oid integer not null, type integer not null);
CREATE INDEX ix_notes_usn ON notes (usn);
CREATE INDEX ix_cards_usn ON cards (usn);
CREATE INDEX ix_revlog_usn ON revlog (usn);
CREATE INDEX ix_cards_nid ON cards (nid);
CREATE INDEX ix_cards_sched ON cards (did, queue, due);
CREATE INDEX ix_revlog_cid ON revlog (cid);
CREATE INDEX ix_notes_csum ON notes (csum);
"""


def stable_id(text: str) -> int:
    """Entier 31 bits stable, dérivé d'un nom (pour deck id / model id)."""
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest()[:8], 16) & 0x7FFFFFFF | 0x10000000


def guid_for(deck: str, recto: str) -> str:
    return hashlib.sha1(f"{deck}\x1f{recto}".encode("utf-8")).hexdigest()[:10]


def csum(text: str) -> int:
    return int(hashlib.sha1(text.encode("utf-8")).hexdigest()[:8], 16)


def parse_txt(path: Path) -> dict:
    meta = {"titre": path.stem, "deck": f"Allemand::{path.stem}", "niveau": "", "lecon": None, "type": ""}
    cards: list[tuple[str, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        if line.startswith("#"):
            m = re.match(r"#\s*([a-z]+)\s*:\s*(.*)", line.strip())
            if m and m.group(1) in meta:
                meta[m.group(1)] = m.group(2).strip()
            continue
        if ";" not in line:
            raise SystemExit(f"{path.name}: ligne sans point-virgule : {line!r}")
        recto, verso = line.split(";", 1)
        cards.append((recto.strip(), verso.strip()))
    if meta["lecon"] is not None and str(meta["lecon"]).isdigit():
        meta["lecon"] = int(meta["lecon"])
    return {"id": path.stem, "fichierTxt": f"anki/{path.name}", "cartes": cards, **meta}


def model_json(mid: int, now: int) -> dict:
    tmpl = lambda name, ord_, q, a: {
        "name": name, "ord": ord_, "qfmt": q, "afmt": a, "bqfmt": "", "bafmt": "", "did": None, "bfont": "", "bsize": 0,
    }
    return {
        "id": mid, "name": MODEL_NAME, "type": 0, "mod": now, "usn": -1, "sortf": 0, "did": 1,
        "tmpls": [
            tmpl("Français → Allemand", 0, "{{Verso}}<div class=small>dis-le en allemand</div>",
                 "{{FrontSide}}<hr id=answer>{{Recto}}"),
            tmpl("Allemand → Français", 1, "{{Recto}}", "{{FrontSide}}<hr id=answer>{{Verso}}"),
        ],
        "flds": [
            {"name": "Recto", "ord": 0, "sticky": False, "rtl": False, "font": "Arial", "size": 20, "media": []},
            {"name": "Verso", "ord": 1, "sticky": False, "rtl": False, "font": "Arial", "size": 20, "media": []},
        ],
        "css": CSS,
        "latexPre": "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage[utf8]{inputenc}\n"
                    "\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n",
        "latexPost": "\\end{document}", "latexsvg": False,
        "req": [[0, "all", [1]], [1, "all", [0]]], "tags": [], "vers": [],
    }


def deck_json(did: int, name: str, now: int) -> dict:
    return {
        "id": did, "name": name, "desc": "", "mod": now, "usn": -1, "collapsed": False, "browserCollapsed": False,
        "newToday": [0, 0], "revToday": [0, 0], "lrnToday": [0, 0], "timeToday": [0, 0],
        "dyn": 0, "extendNew": 0, "extendRev": 0, "conf": 1,
    }


DCONF = {"1": {
    "id": 1, "name": "Default", "replayq": True, "timer": 0, "maxTaken": 60, "autoplay": True, "mod": 0, "usn": 0,
    "lapse": {"leechFails": 8, "minInt": 1, "delays": [10], "leechAction": 0, "mult": 0},
    "rev": {"perDay": 200, "fuzz": 0.05, "ivlFct": 1, "maxIvl": 36500, "ease4": 1.3, "bury": True, "minSpace": 1},
    "new": {"perDay": 20, "delays": [1, 10], "separate": True, "ints": [1, 4, 7], "initialFactor": 2500,
            "bury": True, "order": 1},
}}


def write_apkg(out: Path, decks: list[dict]) -> int:
    """Écrit un .apkg contenant les decks donnés. Retourne le nombre de notes."""
    now = int(time.time())
    now_ms = now * 1000
    mid = stable_id(MODEL_NAME)
    db_path = out.with_suffix(".anki2.tmp")
    if db_path.exists():
        db_path.unlink()
    con = sqlite3.connect(db_path)
    con.executescript(SCHEMA)

    deck_map = {"1": deck_json(1, "Default", now)}
    for d in decks:
        # crée aussi les decks parents (« Allemand A1 » pour « Allemand A1::L02 … »)
        parts = d["deck"].split("::")
        for i in range(1, len(parts) + 1):
            name = "::".join(parts[:i])
            did = stable_id(name)
            deck_map.setdefault(str(did), deck_json(did, name, now))

    conf = {"activeDecks": [1], "curDeck": 1, "newSpread": 0, "collapseTime": 1200, "timeLim": 0, "estTimes": True,
            "dueCounts": True, "curModel": mid, "nextPos": 1, "sortType": "noteFld", "sortBackwards": False,
            "addToCur": True, "dayLearnFirst": False, "newBury": True}
    con.execute("INSERT INTO col VALUES (1,?,?,?,11,0,0,0,?,?,?,?,?)",
                (now, now_ms, now_ms, json.dumps(conf), json.dumps({str(mid): model_json(mid, now)}),
                 json.dumps(deck_map), json.dumps(DCONF), "{}"))

    n = 0
    nid = now_ms
    cid = now_ms + 10_000_000
    for d in decks:
        did = stable_id(d["deck"])
        tag = f"lecon{int(d['lecon']):02d}" if isinstance(d["lecon"], int) else d["id"]
        tags = f" {tag} {d['type'] or 'general'} {d['niveau'] or ''} ".replace("  ", " ")
        for recto, verso in d["cartes"]:
            n += 1
            nid += 1
            con.execute("INSERT INTO notes VALUES (?,?,?,?,-1,?,?,?,?,0,'')",
                        (nid, guid_for(d["deck"], recto), mid, now, tags, f"{recto}\x1f{verso}", recto, csum(recto)))
            for ord_ in (0, 1):
                cid += 1
                con.execute("INSERT INTO cards VALUES (?,?,?,?,?,-1,0,0,?,0,0,0,0,0,0,0,0,'')",
                            (cid, nid, did, ord_, now, n))
    con.commit()
    con.close()

    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(db_path, "collection.anki2")
        z.writestr("media", "{}")
    db_path.unlink()
    return n


def main() -> None:
    txts = sorted(ANKI_DIR.glob("lecon*.txt"))
    if not txts:
        raise SystemExit("aucun fichier anki/lecon*.txt")
    decks = [parse_txt(p) for p in txts]
    manifest = {"version": 1, "genere": time.strftime("%Y-%m-%d"), "decks": [], "tout": {}}
    total = 0
    for d in decks:
        apkg = ANKI_DIR / f"{d['id']}.apkg"
        n = write_apkg(apkg, [d])
        total += n
        manifest["decks"].append({
            "id": d["id"], "titre": d["titre"], "deck": d["deck"], "niveau": d["niveau"], "lecon": d["lecon"],
            "type": d["type"] or "general", "cartes": n,
            "fichierTxt": d["fichierTxt"], "fichierApkg": f"anki/{apkg.name}",
        })
        print(f"{apkg.name:32} {n:4} notes  ({d['deck']})")
    tout = ANKI_DIR / "allemand-tout.apkg"
    write_apkg(tout, decks)
    manifest["tout"] = {"fichierApkg": f"anki/{tout.name}", "cartes": total, "decks": len(decks)}
    (ANKI_DIR / "index.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{tout.name:32} {total:4} notes  (tous les decks)")
    print(f"manifeste : anki/index.json ({len(decks)} decks, {total} cartes)")


if __name__ == "__main__":
    main()
