# stop-pure-ids

Claude schreibt gern „R-10 ist drin, F13 hängt noch“, ohne zu sagen, was das ist. Dieser Stop-Hook für Claude Code merkt nackte Doku-IDs in der Antwort und lässt Claude eine Tabelle „ID | Bedeutung“ nachschieben, ein Satz pro ID.

- Gemeldet: Kürzel wie `R-10`, `AC-3`, `Q-07`, `F13`, `H3`, `P4.1`.
- Erlaubt: die ID in Klammern hinter dem Klartext („CSV-Export (F13)“), in Code, URLs, Links und Überschriften.
- Ausgenommen: UTF-8, MP4, S3, Q1–Q4, KW47 und ähnliche.
- Blockiert höchstens einmal pro Antwort, keine Schleife.

Braucht nur `python3`.

## Installation durch den Agenten

Sag Claude: „Installier den Stop-Hook aus diesem Ordner.“ Der Agent geht so vor:

1. `stop-pure-ids.py` aus diesem Ordner nach `~/.claude/hooks/stop-pure-ids` kopieren und ausführbar machen (`chmod +x`).
2. In `~/.claude/settings.json` unter `hooks.Stop` diesen Eintrag ergänzen. Bestehende Hooks und Einstellungen bleiben unverändert; gibt es `hooks.Stop` schon, kommt der Eintrag dazu:
   ```json
   {
     "hooks": [
       {
         "type": "command",
         "command": "\"$HOME\"/.claude/hooks/stop-pure-ids 2>/dev/null || true",
         "timeout": 10
       }
     ]
   }
   ```
3. Prüfen, dass die settings.json gültiges JSON ist.
4. Testen: `Das löst R-10 und F13 (P4.1).` in eine temporäre Datei schreiben und `~/.claude/hooks/stop-pure-ids --test <datei>` aufrufen. Erwartet: `R-10, F13`.
5. Dem Nutzer sagen, dass der Hook ab der nächsten Claude-Code-Session aktiv ist.

## Anpassen

Kürzel, die nie gemeldet werden sollen, stehen in `ERLAUBT`. Wie die Auflösung aussehen soll, steht im Text hinter `grund`.
