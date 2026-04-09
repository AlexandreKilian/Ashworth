# Roman-Template

Dieses Template bietet eine vollständige Projektstruktur für Romane und Buchserien.

## Schnellstart

1. **Repo klonen/kopieren** und umbenennen
2. `AGENTS.md` anpassen (Projekttitel, Beschreibung, Arbeitsweise)
3. Prämisse ausfüllen: `00 - Übersicht/Prämisse.md`
4. Erste Charaktere und Orte im Glossar anlegen (Vorlagen in `05 - Vorlagen/`)
5. Kapitelplan erstellen: `02 - Plot/Buch 1/Kapitelplan.md`
6. Szenen schreiben unter `03 - Manuskript/`

## Struktur

```
00 - Übersicht/     Prämisse, Themen, Zeitstrahl
01 - Glossar/       Charaktere, Orte, Begriffe
02 - Plot/          Serienplot + pro Buch: Buchplot, Kapitelplan, Kapitelnotizen
03 - Manuskript/    Fertige Prosa (bei Serien: Buch 1/, Buch 2/, ...)
04 - Recherche/     Notizen und Referenzmaterial
05 - Vorlagen/      Templates für alle Glossar- und Plot-Typen
06 - Regeln/        Schreib-, Szene- und Kritik-Regeln
07 - Kritik/        Feedback und Probelese-Ergebnisse
```

## Einzelwerk vs. Serie

**Einzelwerk:** Kapitelordner (K01, K02, ...) direkt unter `03 - Manuskript/`.

**Serie:** Unter `03 - Manuskript/` ein Ordner pro Buch:
```
03 - Manuskript/
  Buch 1/
    K01/
      _Kapitel.md
      K01-S01 Szenenname.md
      K01-S02 Szenenname.md
    K02/
      ...
  Buch 2/
    ...
```

Das Build-Script erkennt beide Varianten automatisch.

## PDF bauen

```bash
pip install fpdf2           # einmalig
python3 build-pdf.py                          # alle Bücher
python3 build-pdf.py -b "Buch 1"              # nur Buch 1
python3 build-pdf.py -t "Mein Roman" -a "Name"  # mit Titel & Autor
```

## Obsidian

Das Template ist Obsidian-kompatibel. Die `_Index.md`-Dateien nutzen Dataview-Queries.
