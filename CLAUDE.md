# Roman-Projekt — Claude Code Konfiguration

Dies ist ein Roman-/Buchserien-Projekt. Alle Arbeit geschieht in Markdown (Obsidian-kompatibel).
Alle Outputs auf Deutsch, es sei denn explizit anders gewünscht.

## Projektstruktur

| Ordner | Inhalt | Anmerkung |
|--------|--------|-----------|
| `00 - Übersicht/` | Prämisse, Themen, Zeitstrahl | Serienübergreifend |
| `01 - Glossar/` | Charaktere, Orte, Länder, Begriffe | Je mit `_Index.md` (Dataview). Serienübergreifend |
| `02 - Plot/` | `Serienplot.md` + pro Buch: `Buchplot.md`, `Kapitelplan.md`, `Kapitel/` | Spiegelt Manuskript-Struktur |
| `03 - Manuskript/` | Fertige Prosa: `Buch {n}/K{nn}/K{nn}-S{nn} Titel.md` | Szenen als einzelne Dateien |
| `04 - Recherche/` | Notizen & Referenzmaterial | |
| `05 - Vorlagen/` | Templates: `Vorlage - Charakter.md`, `Vorlage - Ort.md`, etc. | Beim Anlegen neuer Einträge verwenden |
| `06 - Regeln/` | Schreibregeln, Szene-Regeln, Kritik-Regeln, Stilregeln | **Verbindlich** — vor jeder Aufgabe lesen |
| `07 - Kritik/` | Probelese-Ergebnisse, archivierte Reviews | Pro Buch/Kapitel strukturiert |

## Globale Regeln

- Markdown-Dateien verwenden YAML-Frontmatter.
- **Keine bestehenden Dateien überschreiben** ohne Rückfrage an den User.
- Neue Glossar-Einträge MÜSSEN die Vorlagen aus `05 - Vorlagen/` verwenden (`Vorlage - Charakter.md`, `Vorlage - Ort.md`, `Vorlage - Land.md`, `Vorlage - Begriff.md`).
- Neue Glossar-Einträge MÜSSEN als eigene Datei im jeweiligen Unterordner von `01 - Glossar/` angelegt werden.
- Szenen verwenden `05 - Vorlagen/Vorlage - Szene.md`, Kapitel-Übersichten verwenden `05 - Vorlagen/Vorlage - Kapitel.md`.
- Regelwerke in `06 - Regeln/` sind verbindlich — lies die jeweils relevante Datei, bevor du eine Aufgabe ausführst.
- Nutze `AskUserQuestion` wenn du unsicher bist, statt Annahmen zu treffen.

## Agent-Kontext-Ordner (`.agent-context/`)

Dieser Ordner speichert Arbeitsstatus und persistenten Agent-Kontext. Fertige Outputs (Szenen, Glossar) wandern in die Hauptstruktur. **Chapter Summaries bleiben hier** — sie sind reiner Agent-Kontext und gehören nicht ins Manuskript/PDF.

```
.agent-context/
└── buch-{n}/
    ├── summaries/                 # PERSISTENT — wird NICHT gelöscht
    │   ├── K01-Summary.md
    │   ├── K02-Summary.md
    │   └── ...
    └── k{nn}/                     # TEMPORÄR — wird nach Kapitel-Abschluss aufgeräumt
        ├── task-state.md
        ├── scene-plan.md
        ├── s{nn}-review.md
        └── revision-notes.md
```

## Context-Loading nach Agent-Typ

### Planner (Buchplanung, Szenenplanung)
- `02 - Plot/Serienplot.md`
- `02 - Plot/Buch {n}/Buchplot.md`
- `02 - Plot/Buch {n}/Kapitelplan.md`
- Alle Chapter-Summaries: `.agent-context/buch-{n}/summaries/K*-Summary.md`
- `06 - Regeln/Szene-Regeln.md`
- `06 - Regeln/Stilregeln.md`

### Writer (Szenen schreiben)
- Aktueller Szenenplan (`.agent-context/buch-{n}/k{nn}/scene-plan.md`)
- Letzte fertige Szene (für Übergänge)
- Relevante Glossar-Einträge (Charaktere/Orte die in der Szene vorkommen)
- `06 - Regeln/Schreibregeln.md`
- `06 - Regeln/Stilregeln.md`

### Reviewer (Szenen bewerten)
- Draft-Szene
- `02 - Plot/Buch {n}/Buchplot.md`
- Kapitelnotiz aus `02 - Plot/Buch {n}/Kapitel/`
- Relevante Glossar-Einträge
- `06 - Regeln/Kritik-Regeln.md`
- Alle Chapter-Summaries: `.agent-context/buch-{n}/summaries/`

### Glossarist (Glossar pflegen)
- Fertige Szene/Kapitel
- Bestehende Glossar-Dateien in `01 - Glossar/`
- Vorlagen aus `05 - Vorlagen/`

## Subagents (`.claude/agents/`)

Die Kapitel-Pipeline nutzt spezialisierte Subagents. Jeder hat eine eigene Definitionsdatei:

| Agent | Datei | Aufgabe |
|-------|-------|---------|
| Scene Planner | `scene-planner.md` | Kapitel in Szenen aufteilen, Szenenplan erstellen |
| Plan Reviewer | `plan-reviewer.md` | Szenenplan gegen Buchplot und Kontinuität prüfen |
| Scene Writer | `scene-writer.md` | Einzelne Szenen als Prosa schreiben |
| Scene Reviewer | `scene-reviewer.md` | Geschriebene Szenen bewerten (1-5 Skala) |
| Reviser | `reviser.md` | Szenen basierend auf Review-Feedback überarbeiten |
| Glossarist | `glossarist.md` | Glossar-Einträge erstellen und aktualisieren |

## Verfügbare Slash-Commands

| Command | Zweck |
|---------|-------|
| `/plan-book` | Neues Buch interaktiv planen: Prämisse, Beats, Kapitelplan, Ordnerstruktur |
| `/write-chapter` | Komplette Kapitel-Pipeline: Szenenplan → Schreiben → Review → Überarbeitung → Summary |
