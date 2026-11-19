#!/usr/bin/env python3
"""Claude-Code-Stop-Hook: findet nackte IDs in Claudes Chat-Antwort.

Gemeint sind Kürzel aus PRDs, Konzepten und Doku wie R-10, F13, H3, N1, AC-3,
P4.1 oder Q-07, die ohne Klartext dastehen. Erlaubt ist die ID in Klammern hinter
dem Klartext („Irrelevant-Markierung über neue Crawls (R-10)“), in Code, in URLs,
und in Markdown-Überschriften.

Findet der Hook etwas, blockiert er das Turn-Ende einmal. Claude schiebt dann
eine Tabelle „ID | Bedeutung“ nach, ein Satz je ID. Kein zweiter Block (stop_hook_active), keine Schleife.

  stop-pure-ids              Hook-Modus (JSON auf stdin)
  stop-pure-ids --test DATEI  prüft den Text einer Datei und gibt die Treffer aus
"""
import json
import re
import sys

ID = re.compile(
    r"(?<![\w/.-])"
    r"("
    r"[A-Z]{1,3}-\d{1,3}[a-z]?"          # R-10, AC-3, M-012, Q-07
    r"|[A-Z]{1,2}\d{1,2}(?:\.\d{1,2})*"  # F13, H3, N1, P4.1
    r")"
    r"(?![\w-]|\.\d)"
)

# Kürzel, die keine Doku-IDs sind
ERLAUBT = re.compile(
    r"^(UTF-8|ISO-\d+|MP3|MP4|S3|EC2|G2|A4|A3|A5|H\.264|Q[1-4]|KW\d+|IPV[46]|PHP\d+|ES\d+|CO2|K8)$",
    re.I,
)



def bereinigen(text):
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"`[^`\n]*`", " ", text)
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", text)  # Markdown-Links samt Ziel
    # Klammerinhalte entfernen, innen nach außen
    vorher = None
    while vorher != text:
        vorher = text
        text = re.sub(r"\([^()]*\)", " ", text)
    zeilen = [z for z in text.splitlines() if not z.lstrip().startswith("#")]
    text = "\n".join(zeilen)
    return text


def treffer(text):
    gesehen = []
    for m in ID.finditer(bereinigen(text)):
        tok = m.group(1)
        if ERLAUBT.match(tok) or tok in gesehen:
            continue
        gesehen.append(tok)
    return gesehen


def ist_echte_nutzernachricht(eintrag):
    if eintrag.get("type") != "user" or eintrag.get("isSidechain"):
        return False
    inhalt = (eintrag.get("message") or {}).get("content")
    if isinstance(inhalt, str):
        return True
    if isinstance(inhalt, list):
        return any(b.get("type") == "text" for b in inhalt if isinstance(b, dict))
    return False


def texte_des_turns(pfad):
    try:
        zeilen = open(pfad, encoding="utf-8").read().splitlines()
    except Exception:
        return []
    eintraege = []
    for z in zeilen:
        try:
            eintraege.append(json.loads(z))
        except Exception:
            pass
    start = 0
    for i, e in enumerate(eintraege):
        if ist_echte_nutzernachricht(e):
            start = i + 1
    texte = []
    for e in eintraege[start:]:
        if e.get("type") != "assistant" or e.get("isSidechain"):
            continue
        inhalt = (e.get("message") or {}).get("content")
        if isinstance(inhalt, list):
            for b in inhalt:
                if isinstance(b, dict) and b.get("type") == "text":
                    texte.append(b.get("text", ""))
    return texte


def main():
    if "--test" in sys.argv:
        datei = sys.argv[sys.argv.index("--test") + 1]
        print(", ".join(treffer(open(datei, encoding="utf-8").read())) or "keine")
        return
    try:
        data = json.load(sys.stdin)
    except Exception:
        return
    if data.get("stop_hook_active"):
        return
    texte = texte_des_turns(data.get("transcript_path", ""))
    letzte = data.get("last_assistant_message")
    if isinstance(letzte, str) and letzte not in texte:
        texte.append(letzte)
    ids = treffer("\n\n".join(texte))
    if not ids:
        return
    grund = (
        "Nackte IDs in deiner Antwort: " + ", ".join(ids) + ". "
        "Der Nutzer hat die Zuordnung nicht im Kopf. Schieb jetzt eine Auflösung nach, "
        "ausschließlich als Markdown-Tabelle mit zwei Spalten „ID“ und „Bedeutung“, "
        "je ID eine Zeile, in der Bedeutung genau ein kurzer Satz. "
        "Kein Text davor oder danach, keine Wiederholung der Antwort, keine Entschuldigung."
    )
    print(json.dumps({"decision": "block", "reason": grund}, ensure_ascii=False))


if __name__ == "__main__":
    main()
