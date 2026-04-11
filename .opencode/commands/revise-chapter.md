---
description: Kritik aus Reviews einarbeiten — textliche Änderungen automatisch per Subagent umsetzen, inhaltliche Änderungen mit dem User besprechen und freigeben lassen.
---

Du arbeitest die Verbesserungsvorschläge aus den Reviews eines Kapitels in die Szenen ein. Du unterscheidest dabei zwischen **textlichen** und **inhaltlichen** Änderungen.

**Eingabe:** $ARGUMENTS (z.B. "buch 2 kapitel 5", "b2 k5", "b2 k05")

---

## Schritt 0 — Initialisierung

1. Parse Buch- und Kapitelnummer aus `$ARGUMENTS`. Akzeptiere Formate wie "buch 2 kapitel 5", "b2 k5", "b2 k05". Falls nicht parsebar: frage den User.
2. Setze Variablen:
   - `BUCH` = Buchnummer
   - `KAP` = Kapitelnummer zweistellig (z.B. 05)
   - `MANUSKRIPT_DIR` = `03 - Manuskript/Buch {BUCH}/K{KAP}`
   - `KRITIK_DIR` = `07 - Kritik/Buch {BUCH}/K{KAP}`
3. Prüfe ob `{MANUSKRIPT_DIR}` existiert und Szenen enthält (`K{KAP}-S*.md`). Falls nicht: **Abbruch** — es gibt nichts zu überarbeiten.
4. Prüfe ob `{KRITIK_DIR}` existiert und Reviews enthält (`s*-review.md`). Falls nicht: **Abbruch** — es gibt keine Kritik zum Einarbeiten.

---

## Schritt 1 — Szenen und Reviews laden

Für jede Szene des Kapitels:
1. Lies die Szene aus `{MANUSKRIPT_DIR}/K{KAP}-S{nn} *.md`
2. Lies das zugehörige Review aus `{KRITIK_DIR}/s{nn}-review.md`
3. Lies die Regeldateien:
   - `06 - Regeln/Schreibregeln.md`
   - `06 - Regeln/Stilregeln.md`

Erstelle eine Übersicht: welche Szenen haben Reviews, welche nicht.

---

## Schritt 2 — Verbesserungsvorschläge kategorisieren

Gehe jeden Verbesserungsvorschlag aus jedem Review durch. Jeder Vorschlag fällt in **eine** von zwei Kategorien:

### Textlich (automatisch einarbeiten)
Änderungen an Formulierung, Stil, Rhythmus, Regelkonformität — alles, was den **Text** verbessert, ohne die **Handlung** zu verändern:
- Leitmotiv-Häufigkeit reduzieren (z.B. Bleistift-Erwähnungen streichen)
- Wiederholungen kürzen oder streichen
- Beschreibungen komprimieren
- Sätze straffen oder umbauen
- Verbotene Wörter/Muster ersetzen
- Sensorik anpassen
- Dialog-Attribution verbessern
- Regelkonformität herstellen

### Inhaltlich (nur nach Rückfrage)
Änderungen, die die **Handlung, Charakterisierung oder Dramaturgie** betreffen:
- Neue Reaktionen oder Emotionen hinzufügen
- Szenen-Dynamik verändern (z.B. "emotionale Schärfung")
- Neue Handlungselemente oder Beats einfügen
- Charakter-Verhalten ändern
- Dialog-Inhalte ändern (nicht Stil, sondern *was* gesagt wird)

---

## Schritt 3 — Textliche Änderungen einarbeiten (@reviser, parallel)

Für jede Szene, die textliche Verbesserungsvorschläge hat, rufe das **Task-Tool** mit dem `reviser` Subagent auf. Die Szenen können **parallel** bearbeitet werden:

Prompt pro Szene:
```
DEINE AUFGABE: Arbeite die folgenden TEXTLICHEN Verbesserungsvorschläge in die Szene ein.

LIES DIESE DATEIEN:
- Die Szene: {MANUSKRIPT_DIR}/K{KAP}-S{nn} {Titel}.md
- Schreibregeln: 06 - Regeln/Schreibregeln.md
- Stilregeln: 06 - Regeln/Stilregeln.md

EINZUARBEITENDE VORSCHLÄGE:
{Liste der textlichen Vorschläge für diese Szene, mit Zeilenbezug aus dem Review}

REGELN:
- Ändere NUR die Stellen, die von den Vorschlägen betroffen sind
- Schreibe NICHT die gesamte Szene um
- Bewahre Ton, Rhythmus und Stil
- Wortanzahl-Änderung maximal ±10%
- Keine neuen Handlungselemente einführen
- Keine Charaktere anders darstellen als im Glossar
- Aktualisiere 'status' im Frontmatter auf 'überarbeitet'

OUTPUT: Überschreibe die Szene direkt: {MANUSKRIPT_DIR}/K{KAP}-S{nn} {Titel}.md
```

---

## Schritt 4 — Inhaltliche Änderungen mit User besprechen

Für jede Szene, die inhaltliche Verbesserungsvorschläge hat:

1. Stelle dem User den Vorschlag vor — mit:
   - Welche Szene betroffen ist
   - Was das Review vorschlägt (Originaltext aus dem Review zitieren)
   - Warum das eine inhaltliche Änderung ist
   - Was sich in der Szene konkret ändern würde
2. Frage den User: "Soll ich diesen Vorschlag einarbeiten? (ja/nein/anpassen)"
3. Falls **ja**: Arbeite den Vorschlag per Task-Tool mit dem `reviser` Subagent ein (gleiche Regeln wie Schritt 3, aber mit dem inhaltlichen Vorschlag).
4. Falls **anpassen**: Frage nach, wie der User die Änderung haben möchte, und setze das um.
5. Falls **nein**: Überspringe den Vorschlag.

Fasse alle inhaltlichen Vorschläge einer Szene in **einer** Frage zusammen, wenn es mehrere gibt — nicht einzeln fragen.

---

## Schritt 5 — Abschluss

1. Berichte dem User:
   - Welche Szenen überarbeitet wurden
   - Welche textlichen Änderungen automatisch eingearbeitet wurden (kurze Auflistung)
   - Welche inhaltlichen Änderungen eingearbeitet oder übersprungen wurden
   - Ob es Szenen ohne Reviews gab
2. Setze im Frontmatter jeder überarbeiteten Szene `status: überarbeitet`.
