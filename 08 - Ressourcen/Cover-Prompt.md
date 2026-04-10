---
beschreibung: Referenz-Prompt für Cover-Illustrationen der Ashworth-Serie
---

# Cover-Prompt — Die Ashworth Drei

## Workflow

1. Illustration ohne Text generieren (Prompt unten)
2. Titel, Serienname, Bandnummer und Autorenname manuell hinzufügen
3. Fertiges Cover nach `08 - Ressourcen/ashworth-book{n}.png` kopieren

## Text-Elemente (manuell)

- **Serientitel:** DIE ASHWORTH DREI (oben, klein, elegant golden)
- **Buchtitel:** variiert pro Band (groß, ornamental, golden mit Glow)
- **Bandnummer:** Band {n} (klein)
- **Autor:** C. J. Whitmore (unten, saubere Serifenschrift)
- **Schriftstil:** Elegante ornamentale goldene Fantasy-Schrift mit warmem Glow-Effekt

## Illustrations-Prompt (ohne Text)

Diesen Prompt als Basis verwenden und pro Band die **SZENE** und **GEBÄUDE**-Beschreibung anpassen:

```
Book cover ILLUSTRATION ONLY - NO TEXT whatsoever on the image. No title,
no author name, no text of any kind. Portrait format, book cover proportions
6:9. Style: atmospheric British childrens book illustration, slightly dark
but child-friendly, classic mystery genre like Lemony Snicket.

BUILDING: [Pro Band anpassen — Beschreibung des zentralen Schauplatzes.
Wichtig: Verfall, Atmosphäre, unregelmäßige/seltsame Architektur, ein
einzelnes mysteriöses Licht als Fokuspunkt.]

CANAL/SETTING: Dark still water in foreground reflecting golden light.
Worn stone towpath between viewer and building. Fog creeps low over water.
[Pro Band anpassen falls anderer Schauplatz.]

THREE CHILDREN on towpath, seen from behind, positioned in lower third.
Left: JUDE, 13, tall lanky, oversized wax jacket with taped elbow patches,
messy dark-blond hair, leaning forward peering at building.
Center: PRIYA, 13, compact build, long black hair in practical braid,
big overstuffed backpack, standing steady and alert.
Right: ARCHIE, 12, noticeably smaller and thinner, straight light-brown
hair over ears, dark clothes, black Chuck Taylor sneakers, hangs back
a half-step, sketchbook under arm, observing quietly.

COMPOSITION: Building fills upper two-thirds. Children small in lower
third on towpath. Leave clear space at top and bottom edges for text
to be added later. NO TEXT ON THE IMAGE.

COLOR: Dark navy deep purple sky, warm gold amber light, muted greens
browns on decay, dark water with golden reflections.
```

## Buch 1 — Das Licht im Badehaus

Gebäude-Beschreibung die zum besten Ergebnis geführt hat:

```
BUILDING: An abandoned Victorian-era PUBLIC BATHHOUSE - a squat, heavy,
ASYMMETRIC industrial civic building. Old British municipal architecture:
thick brick walls, a low flat roof with a stubby ventilation chimney,
wide arched entrances now sealed shut. The facade is IRREGULAR - different
sections added at different times, parts dont match. Some walls older dark
brick, others patched with lighter stone. Several large arched windows
BRICKED UP with mismatched brick. One small window on an upper floor has
mysterious warm golden light glowing from inside. Remnants of old ceramic
tiles or faded signage on exterior. Heavy decay: collapsed section on one
side, missing roof slates, thick ivy, water damage stains, rusted iron
railings. Building sits RIGHT ON the canal edge.
```

## Hinweise

- `/generate` verwenden, NICHT `/edit` (Edit hat bei nanobanana Timeout-Probleme)
- Charakter-Referenzbilder (wenn vorhanden) in `08 - Ressourcen/` mitgeben
- Farbpalette über alle Bände konsistent halten: dunkles Navyblau/Violett + warmes Gold/Bernstein
- Gebäude soll NICHT wie Wohnhaus/Schloss/Herrenhaus aussehen — immer Zweckbau/Funktionsbau betonen
