# single-question-mode

Ein Skill für Claude Code, der offene Fragen oder Entscheidungen einzeln mit dir durchgeht. Pro Runde zeigt Claude genau eine Frage mit dem nötigen Kontext, einer klaren Empfehlung, der Zahl der noch offenen Fragen und einem Fortschrittsbalken. Die nächste Frage kommt erst, wenn die aktuelle entschieden ist.

Aufruf mit `/single-question-mode` oder Sätzen wie „eine Frage nach der anderen“, „geh die offenen Fragen mit mir durch“. Als Quelle taugt eine Notion-Seite, eine Datei, ein PR oder eine eingefügte Liste.

## Installation durch den Agenten

Sag Claude: „Installiere den Skill von dieser URL: https://github.com/joerncodes/claude/tree/main/skills/single-question-mode“

Anweisung für den Agenten:

1. Skill herunterladen:
   ```sh
   mkdir -p ~/.claude/skills/single-question-mode
   curl -fsSL https://raw.githubusercontent.com/joerncodes/claude/main/skills/single-question-mode/SKILL.md -o ~/.claude/skills/single-question-mode/SKILL.md
   ```
2. Prüfen, dass die Datei mit einem YAML-Frontmatter (`---`, `name: single-question-mode`) beginnt.
3. Dem Nutzer sagen, dass der Skill ab der nächsten Claude-Code-Session als `/single-question-mode` verfügbar ist.
