---
description: Komplette Kapitel-Pipeline — Szenenplan erstellen, reviewen, Szenen schreiben, reviewen, überarbeiten, Chapter Summary anlegen und Glossar aktualisieren.
---

Du orchestrierst die komplette Pipeline zum Schreiben eines einzelnen Kapitels. Du führst die Orchestrierung selbst durch (Schritte 0, 1, 7, 8, 10) und delegierst die kreativen und analytischen Aufgaben an Subagents über das **Task-Tool** (mit `@agent-name` als Ziel-Agent).

**Eingabe:** $ARGUMENTS (z.B. "buch 1 kapitel 3", "b1 k3", "b1 k03")

---

## Schritt 0 — Initialisierung (du selbst)

1. Parse Buch- und Kapitelnummer aus `$ARGUMENTS`. Akzeptiere Formate wie "buch 1 kapitel 3", "b1 k3", "b1 k03". Falls nicht parsebar: frage den User.
2. Setze Variablen:
   - `BUCH` = Buchnummer (z.B. 1)
   - `KAP` = Kapitelnummer zweistellig (z.B. 03)
   - `PLOT_DIR` = `02 - Plot/Buch {BUCH}`
   - `MANUSKRIPT_DIR` = `03 - Manuskript/Buch {BUCH}/K{KAP}`
   - `CONTEXT_DIR` = `.agent-context/buch-{BUCH}/k{KAP}`
   - `SUMMARY_DIR` = `.agent-context/buch-{BUCH}/summaries`
3. Prüfe ob `{PLOT_DIR}/Kapitelplan.md` existiert. Falls nicht: **Abbruch** mit Hinweis, zuerst `/plan-book` auszuführen.
4. Prüfe ob `{PLOT_DIR}/Kapitel/K{KAP}.md` existiert. Falls nicht: **Warnung**, dass keine Kapitelnotiz vorhanden ist.
5. Prüfe ob vorherige Kapitel-Summaries vorhanden sind (`{SUMMARY_DIR}/K*-Summary.md`). Falls Lücken: **Warnung** an den User (z.B. "K01-Summary fehlt, Kontinuität könnte leiden").
6. Erstelle Ordner und `{CONTEXT_DIR}/task-state.md`:
   ```yaml
   buch: {BUCH}
   kapitel: {KAP}
   status: gestartet
   aktuelle_szene: 0
   szenen_gesamt: 0
   letzte_aktion: "Initialisierung"
   naechste_aktion: "Context laden"
   ```
7. Erstelle `{MANUSKRIPT_DIR}/` falls nicht vorhanden.

---

## Schritt 1 — Context laden (du selbst)

Lies folgende Dateien und halte ihren Inhalt für die Subagent-Prompts bereit:
- `{PLOT_DIR}/Buchplot.md`
- `{PLOT_DIR}/Kapitelplan.md`
- `{PLOT_DIR}/Kapitel/K{KAP}.md` (falls vorhanden)
- Alle vorhandenen Chapter-Summaries: `{SUMMARY_DIR}/K*-Summary.md`
- `06 - Regeln/Stilregeln.md`
- `06 - Regeln/Szene-Regeln.md`
- `06 - Regeln/Schreibregeln.md`
- `06 - Regeln/Kritik-Regeln.md`

Identifiziere aus dem Kapitelplan und der Kapitelnotiz, welche Charaktere und Orte in diesem Kapitel vorkommen. Lies deren Glossar-Einträge aus `01 - Glossar/`.

Update `task-state.md`: status → "context-geladen"

---

## Schritt 2 — Szenen planen (@scene-planner)

Rufe das **Task-Tool** auf mit dem `scene-planner` Subagent:

Prompt:
```
DEINE AUFGABE: Erstelle einen detaillierten Szenenplan für Kapitel K{KAP} von Buch {BUCH}.

KONTEXT (lies diese Dateien):
- Buchplot: {PLOT_DIR}/Buchplot.md
- Kapitelplan: {PLOT_DIR}/Kapitelplan.md
- Kapitelnotiz: {PLOT_DIR}/Kapitel/K{KAP}.md
- Alle Chapter-Summaries in: {SUMMARY_DIR}/
- Relevante Glossar-Einträge in: 01 - Glossar/Charaktere/ und 01 - Glossar/Orte/
- Szene-Regeln: 06 - Regeln/Szene-Regeln.md
- Stilregeln: 06 - Regeln/Stilregeln.md

OUTPUT: Schreibe den fertigen Szenenplan nach {CONTEXT_DIR}/scene-plan.md
```

Update `task-state.md`: status → "szenen-geplant", szenen_gesamt → Anzahl

---

## Schritt 3 — Szenenplan reviewen (@plan-reviewer)

Rufe das **Task-Tool** auf mit dem `plan-reviewer` Subagent:

Prompt:
```
DEINE AUFGABE: Überprüfe und verbessere den Szenenplan für Kapitel K{KAP} von Buch {BUCH}.

LIES DIESE DATEIEN:
- Szenenplan: {CONTEXT_DIR}/scene-plan.md
- Buchplot: {PLOT_DIR}/Buchplot.md
- Kapitelplan: {PLOT_DIR}/Kapitelplan.md
- Alle Chapter-Summaries in: {SUMMARY_DIR}/
- Relevante Glossar-Einträge in: 01 - Glossar/
- Szene-Regeln: 06 - Regeln/Szene-Regeln.md

FALLS PROBLEME GEFUNDEN: Überarbeite den Szenenplan direkt in {CONTEXT_DIR}/scene-plan.md
FALLS ALLES OK: Ergänze am Ende '## Review: Freigegeben' mit kurzer Bestätigung.
```

Update `task-state.md`: status → "szenen-reviewed"

---

## Schritt 4 — Szenen schreiben (@scene-writer, sequenziell)

Lies den finalen Szenenplan aus `{CONTEXT_DIR}/scene-plan.md`.

Für **jede Szene** (S01, S02, ...) **sequenziell** — rufe jeweils das **Task-Tool** mit dem `scene-writer` Subagent auf:

Prompt pro Szene:
```
DEINE AUFGABE: Schreibe Szene S{nn} von Kapitel K{KAP}, Buch {BUCH}.

LIES DIESE DATEIEN:
- Szenenplan (nur den Abschnitt für S{nn}): {CONTEXT_DIR}/scene-plan.md
- Vorherige Szene (für Übergang): {MANUSKRIPT_DIR}/K{KAP}-S{nn-1}*.md (falls vorhanden)
- Schreibregeln: 06 - Regeln/Schreibregeln.md
- Stilregeln: 06 - Regeln/Stilregeln.md
- Vorlage: 05 - Vorlagen/Vorlage - Szene.md (für das Frontmatter-Format)
- Glossar-Einträge für: [Liste der Charaktere/Orte dieser Szene]

FRONTMATTER: Verwende das Format aus der Vorlage. Fülle aus:
- tags: [plot, szene]
- kapitel: K{KAP}
- pov: [POV-Charakter aus Szenenplan]
- ort: [Ort aus Szenenplan]
- status: entwurf
- was_passiert: [Kurzbeschreibung aus Szenenplan]
- ziel: [Was die Szene erreichen soll]

DANN: Ersetze '# {{title}}' durch '# {Szenentitel}'.
Behalte die Planungs-Abschnitte aus der Vorlage NICHT — schreibe stattdessen unter der Überschrift die eigentliche PROSA.

REGELN:
- Szene beginnt in medias res oder mit sensorischem Detail
- Show don't Tell
- Dialoge: knapp, figurenspezifisch, deutsche Anführungszeichen „..."
- Absatzlänge: max 5-6 Sätze
- Dialog: max 3-4 Zeilen am Stück, dann Action Beat
- Keine Info-Dumps
- Ziel-Wortanzahl: {Wortanzahl aus Szenenplan} (±15%)

OUTPUT: Schreibe die fertige Szene nach {MANUSKRIPT_DIR}/K{KAP}-S{nn} {Szenentitel}.md
```

Nach jeder Szene: Update `task-state.md` (aktuelle_szene, letzte_aktion).

---

## Schritt 5 — Szenen reviewen (@scene-reviewer, parallel)

Für **jede geschriebene Szene** — rufe das **Task-Tool** mit dem `scene-reviewer` Subagent auf. Alle Reviews können **parallel** gestartet werden:

Prompt pro Szene:
```
DEINE AUFGABE: Bewerte Szene K{KAP}-S{nn} von Buch {BUCH}.

LIES DIESE DATEIEN:
- Die Szene: {MANUSKRIPT_DIR}/K{KAP}-S{nn} {Titel}.md
- Kritik-Regeln: 06 - Regeln/Kritik-Regeln.md
- Buchplot: {PLOT_DIR}/Buchplot.md
- Szenenplan: {CONTEXT_DIR}/scene-plan.md
- Alle Chapter-Summaries in: {SUMMARY_DIR}/
- Relevante Glossar-Einträge für die vorkommenden Charaktere und Orte

BEWERTE (1-5 Skala):
1. Klarheit — Ist die Szene verständlich?
2. Pacing — Stimmt das Tempo?
3. Charakterstimme — Klingt der POV-Charakter authentisch?
4. Spannung — Gibt es einen Grund weiterzulesen?
5. Regelkonformität — Werden Schreib- und Stilregeln eingehalten?

GESAMTURTEIL:
- 'Akzeptiert' wenn alle Kategorien ≥ 3 UND Durchschnitt ≥ 3.5
- 'Überarbeitung empfohlen' sonst — die 3 wichtigsten Änderungen priorisiert auflisten

OUTPUT: Schreibe das Review nach {CONTEXT_DIR}/s{nn}-review.md
```

Update `task-state.md`: status → "am-reviewen"

---

## Schritt 6 — Überarbeiten (@reviser, nur falls "Überarbeitung empfohlen")

Lies die Review-Ergebnisse. Für jede Szene mit "Überarbeitung empfohlen":

Rufe das **Task-Tool** mit dem `reviser` Subagent auf:

Prompt:
```
DEINE AUFGABE: Überarbeite Szene K{KAP}-S{nn} basierend auf dem Review.

LIES DIESE DATEIEN:
- Die Szene: {MANUSKRIPT_DIR}/K{KAP}-S{nn} {Titel}.md
- Das Review: {CONTEXT_DIR}/s{nn}-review.md
- Schreibregeln: 06 - Regeln/Schreibregeln.md
- Stilregeln: 06 - Regeln/Stilregeln.md

ANWEISUNGEN:
- Setze die konkreten Verbesserungsvorschläge aus dem Review um
- Ändere NUR die bemängelten Stellen — NICHT die gesamte Szene umschreiben
- Aktualisiere 'status' im Frontmatter auf 'überarbeitet'
- Bewahre den Ton und Stil der Szene

OUTPUT: Überschreibe die Szene direkt: {MANUSKRIPT_DIR}/K{KAP}-S{nn} {Titel}.md
```

Nach der Überarbeitung: führe ein **Mini-Review** durch (nur die vorher bemängelten Kategorien). Maximal **2 Überarbeitungs-Durchläufe**, dann akzeptieren und weitermachen.

Update `task-state.md`: status → "am-überarbeiten"

---

## Schritt 7 — Kapitel zusammenführen (du selbst)

Erstelle oder aktualisiere `{MANUSKRIPT_DIR}/_Kapitel.md` basierend auf der Vorlage `05 - Vorlagen/Vorlage - Kapitel.md`:

1. Lies die Vorlage `05 - Vorlagen/Vorlage - Kapitel.md`
2. Fülle das Frontmatter: `status: entwurf`
3. Ersetze `# {{title}}` durch `# Kapitel {KAP} — {Titel aus Kapitelplan}`
4. Trage unter `## Szenen` die Tabelle mit allen Szenen:
   | Nr. | Szene | POV | Ort | Status |
   Verwende Obsidian-Links: `[[K{KAP}-S{nn} {Titel}]]`
5. Fülle `## Zusammenfassung` basierend auf dem Kapitelplan
6. Fülle `## Ziel des Kapitels` basierend auf dem Kapitelplan

Update `task-state.md`: status → "am-zusammenführen"

---

## Schritt 8 — Chapter Summary erstellen (du selbst)

Lies alle fertigen Szenen des Kapitels. Erstelle `{SUMMARY_DIR}/K{KAP}-Summary.md`:

```markdown
---
buch: {BUCH}
kapitel: {KAP}
szenen: {Anzahl}
status: fertig
---

# Kapitel {KAP} — Summary

## Handlung
<!-- Kompakte Nacherzählung der Ereignisse -->

## Charakter-Entwicklung
<!-- Wie haben sich die Figuren verändert? -->

## Plot-Threads
### Geöffnet
-
### Geschlossen/Vorangetrieben
-

## Emotionaler Zustand am Ende
<!-- Stimmung, Gefühlslage der Hauptfiguren -->

## Wichtige Reveals / Neue Informationen
-
```

Ziel: 300-500 Wörter. Diese Summary ist **persistenter Kontext** — sie wird von allen folgenden Kapiteln gelesen.

**WICHTIG:** Der `summaries/`-Ordner wird NIEMALS gelöscht.

---

## Schritt 9 — Glossar updaten (@glossarist)

Rufe das **Task-Tool** mit dem `glossarist` Subagent auf:

Prompt:
```
DEINE AUFGABE: Prüfe ob im fertigen Kapitel K{KAP} neue oder geänderte Glossar-Einträge nötig sind.

LIES:
- Alle Szenen in: {MANUSKRIPT_DIR}/ (alle K{KAP}-S*.md Dateien)
- Bestehende Glossar-Einträge: 01 - Glossar/Charaktere/, 01 - Glossar/Orte/, 01 - Glossar/Begriffe/
- Vorlagen: 05 - Vorlagen/Vorlage - Charakter.md, 05 - Vorlagen/Vorlage - Ort.md, 05 - Vorlagen/Vorlage - Begriff.md

FÜR NEUE EINTRÄGE: Verwende EXAKT die Vorlage, fülle alle Felder mit Informationen aus den Szenen.
FÜR BESTEHENDE EINTRÄGE: NICHT überschreiben — nur ergänzen (neue Infos unter '## Notizen').

AKTUALISIERE die _Index.md Dateien in den jeweiligen Glossar-Ordnern.
BERICHTE am Ende: welche Einträge neu erstellt, welche ergänzt wurden.
```

---

## Schritt 10 — Abschluss (du selbst)

1. **Reviews archivieren:** Verschiebe alle `s{nn}-review.md` aus `{CONTEXT_DIR}/` nach `07 - Kritik/Buch {BUCH}/K{KAP}/` (erstelle den Ordner falls nötig).
2. **Aufräumen:** Lösche den temporären Ordner `{CONTEXT_DIR}/` (task-state.md, scene-plan.md, revision-notes.md).
3. **NICHT löschen:** `{SUMMARY_DIR}/` — die Summaries sind persistenter Kontext.
4. **Zusammenfassung an den User:**
   - Wortanzahl gesamt und pro Szene
   - Szenenanzahl
   - Review-Ergebnisse (Durchschnittsbewertungen pro Kategorie)
   - Überarbeitungen (welche Szenen, wie viele Durchläufe)
   - Glossar-Änderungen (neu erstellt / ergänzt)
   - Nächster Schritt: `/write-chapter b{BUCH} k{nächstes Kapitel}`
