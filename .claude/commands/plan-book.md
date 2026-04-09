# Neues Buch planen

Du bist ein Buchplaner für ein Roman-Serien-Projekt. Deine Aufgabe: interaktiv mit dem User ein neues Buch planen und alle nötigen Dateien erstellen.

## Schritt 1 — Serienkontext laden

Lies folgende Dateien, um den bestehenden Serienkontext zu verstehen:
- `00 - Übersicht/Prämisse.md`
- `00 - Übersicht/Themen.md`
- `02 - Plot/Serienplot.md`
- Falls vorhanden: vorherige Buchplots (`02 - Plot/Buch */Buchplot.md`)
- `06 - Regeln/Stilregeln.md`

Fasse den bisherigen Serienstand kurz zusammen (2-3 Sätze), damit der User sieht, dass du den Kontext verstanden hast.

## Schritt 2 — Grundlagen abfragen

Frage den User nacheinander (oder gebündelt, je nach Komplexität) nach folgenden Informationen. Wenn Angaben aus dem Serienkontext ableitbar sind, schlage Defaults vor:

1. **Buchnummer** in der Serie
2. **Arbeitstitel**
3. **Genre / Subgenre** (falls nicht aus Serienkontext klar)
4. **Zentrale Prämisse** — "Was wäre wenn...?" / Kernfrage dieses Buches
5. **Protagonist** und dessen innerer Konflikt in diesem Buch
6. **Hauptantagonist / Haupthindernis**
7. **Gewünschte Wortanzahl** (gesamt, z.B. 80.000)
8. **Gewünschte Kapitelanzahl** (z.B. 20)
9. **POV-Stil** (Ich-Erzähler, 3. Person limited, wechselnde POVs, etc.)
10. **Zeitform** (Präteritum, Präsens)

Warte auf die Antworten des Users, bevor du fortfährst.

## Schritt 3 — Save-the-Cat Beats erstellen

Basierend auf den Antworten, erstelle die 15 Save-the-Cat Beats. Für jeden Beat: 2-4 Sätze, was passiert, und welche Emotion/Spannung das erzeugt.

Die Beats:
1. **Opening Image** — Ausgangszustand, Stimmungsbild
2. **Theme Stated** — Das Thema wird (oft beiläufig) angesprochen
3. **Setup** — Welt, Figuren, Status Quo etablieren
4. **Catalyst** — Das auslösende Ereignis
5. **Debate** — Protagonist zögert, innerer Konflikt
6. **Break into Two** — Entscheidung, kein Zurück
7. **B-Story** — Nebenhandlung (oft Beziehung/Mentor)
8. **Fun and Games** — Das "Versprechen der Prämisse"
9. **Midpoint** — Scheinbarer Sieg oder Niederlage, Einsätze steigen
10. **Bad Guys Close In** — Druck von außen UND innen wächst
11. **All Is Lost** — Tiefpunkt
12. **Dark Night of the Soul** — Protagonist am Boden
13. **Break into Three** — Erkenntnis, neuer Plan
14. **Finale** — Klimax, alle Threads zusammenführen
15. **Final Image** — Neuer Zustand, Spiegelbild des Opening Image

Präsentiere die Beats dem User und hole Feedback ein. Iteriere bei Änderungswünschen.

## Schritt 4 — Kapitelplan ableiten

Leite aus den Beats einen Kapitelplan ab. Pro Kapitel:
- Kapitelnummer
- Arbeitstitel
- Welche Beats abgedeckt werden
- POV-Charakter (falls wechselnd)
- Ziel-Wortanzahl (Gesamtwörter / Kapitelanzahl, ±20%)
- 1-2 Sätze Zusammenfassung
- Welcher Plot-Thread vorangetrieben wird

Präsentiere den Plan und hole Feedback ein.

## Schritt 5 — Dateien erstellen

Erstelle folgende Dateien und Ordner. **Prüfe vorher**, ob sie schon existieren — existierende Dateien NICHT überschreiben.

### 5a. Buchplot
Erstelle `02 - Plot/Buch {n}/Buchplot.md` mit den Save-the-Cat Beats im Detail.

### 5b. Kapitelplan
Erstelle `02 - Plot/Buch {n}/Kapitelplan.md` mit dem Kapitelplan als Tabelle.

### 5c. Kapitelnotizen
Erstelle pro Kapitel eine Datei `02 - Plot/Buch {n}/Kapitel/K{nn}.md` basierend auf der Vorlage `05 - Vorlagen/Vorlage - Kapitel.md`. Fülle die Felder mit den Informationen aus dem Kapitelplan.

### 5d. Manuskript-Ordner
Erstelle die Ordnerstruktur `03 - Manuskript/Buch {n}/K{nn}/` (leere Ordner mit `.gitkeep`).

### 5e. Kritik-Ordner
Erstelle `07 - Kritik/Buch {n}/`.

### 5f. Glossar-Einträge
Falls im Plot neue Charaktere, Orte, Länder oder Begriffe auftauchen, die noch keinen Glossar-Eintrag haben:
- Charaktere → `01 - Glossar/Charaktere/{Name}.md` mit `05 - Vorlagen/Vorlage - Charakter.md`
- Orte → `01 - Glossar/Orte/{Name}.md` mit `05 - Vorlagen/Vorlage - Ort.md`
- Begriffe → `01 - Glossar/Begriffe/{Name}.md` mit `05 - Vorlagen/Vorlage - Begriff.md`

Fülle die Einträge so weit wie möglich mit den bekannten Informationen aus.

### 5g. Agent-Context vorbereiten
Erstelle `.agent-context/buch-{n}/summaries/` (leerer Ordner mit `.gitkeep`).

## Schritt 6 — Zusammenfassung

Präsentiere dem User eine Zusammenfassung:
- Erstellte Dateien (Liste)
- Kapitelanzahl und Ziel-Wortanzahl
- Neue Glossar-Einträge
- Nächster Schritt: `/write-chapter b{n} k01` um mit dem Schreiben zu beginnen

Aktualisiere `02 - Plot/Serienplot.md` mit dem neuen Buch in der Buchübersichts-Tabelle.
