# Greedy-Algorithmus

Der Greedy-Algorithmus für das Minimum Non-Obtuse Triangulation (MNOT)-Problem verfolgt eine schrittweise Strategie, um eine Triangulierung zu erzeugen, bei der alle Dreiecke Winkel von höchstens 90 Grad haben. Ziel ist es, eine gültige nicht-stumpfe Triangulierung zu finden, während die Anzahl der hinzugefügten **Steinerpunkte** minimiert wird. Der Algorithmus ist "greedy", weil er bei jedem Schritt versucht, eine lokale Entscheidung zu treffen, die das Problemziel (nicht-stumpfe Winkel) so gut wie möglich erfüllt, ohne dabei Rücksprünge oder globale Optimierungen durchzuführen.

### Detaillierte Schritte des Greedy-Algorithmus

1. **Start mit der Konvexen Hülle**:
   - Der Algorithmus beginnt mit der **konvexen Hülle** des Planar Straight Line Graphs (PSLG). Die konvexe Hülle ist das kleinste konvexe Polygon, das alle Punkte des PSLG einschließt.
   - Die Kanten der konvexen Hülle werden als Ausgangspunkt für die Triangulierung genutzt, da hier zuerst die äußeren Dreiecke erstellt werden.

2. **Initiale Dreiecksbildung entlang der Hülle**:
   - Der Greedy-Algorithmus betrachtet jede Kante der konvexen Hülle nacheinander und versucht, ein Dreieck zu erstellen, das an dieser Kante anliegt und einen Punkt im Inneren des PSLG als dritten Eckpunkt enthält.
   - Er wählt den nächstgelegenen Punkt im Inneren des Graphen, der zusammen mit der Kante ein potenziell nicht-stumpfes Dreieck bildet. Dabei werden die Winkel des entstehenden Dreiecks überprüft.
   - Wenn alle Winkel dieses Dreiecks ≤ 90° sind, wird das Dreieck zur Lösung hinzugefügt und diese Konfiguration wird festgeschrieben.

3. **Überprüfung der Winkel und Hinzufügen von Steinerpunkten**:
   - Falls das neu erzeugte Dreieck einen stumpfen Winkel (d.h. > 90°) enthält, greift der Algorithmus auf einen **Steinerpunkt** zurück. Dieser wird strategisch in der Nähe der Kante oder des stumpfen Winkels platziert, um den Winkel zu verkleinern.
   - Die genaue Platzierung des Steinerpunkts erfolgt so, dass das ursprüngliche stumpfe Dreieck in zwei oder mehrere kleinere Dreiecke zerlegt wird, die nun alle Winkel ≤ 90° aufweisen.
   - Der Greedy-Algorithmus sucht typischerweise nach der Punktposition, die den Winkel so verbessert, dass möglichst wenige Steinerpunkte eingefügt werden.

4. **Fortlaufende Triangulierung der inneren Bereiche**:
   - Sobald die Kanten der konvexen Hülle alle als Teil eines Dreiecks eingebunden sind, verlagert sich der Fokus auf die verbleibenden inneren Bereiche.
   - Der Algorithmus wählt jeweils die nächste Kante an einer bestehenden Grenze (z.B. eine Kante eines bereits vorhandenen Dreiecks) und versucht, ein weiteres Dreieck zu erstellen, das alle Winkelbedingungen erfüllt.
   - Für jede neue Kante wird geprüft, ob sie zusammen mit einem dritten Punkt im Inneren des Polygons ein gültiges Dreieck mit nicht-stumpfen Winkeln bildet. Wenn dies möglich ist, wird das Dreieck hinzugefügt; andernfalls wird wieder ein Steinerpunkt eingefügt.

5. **Iterative Erweiterung bis zur Vollständigkeit**:
   - Der Greedy-Algorithmus setzt diesen Vorgang fort, indem er schrittweise alle inneren Bereiche des PSLG trianguliert und nach Bedarf Steinerpunkte hinzufügt.
   - Er „klettert“ dabei von den äußeren Bereichen des PSLG in die Mitte, trianguliert schrittweise und stellt sicher, dass keine stumpfen Winkel entstehen.
   - Der Prozess endet, sobald alle Bereiche innerhalb der konvexen Hülle trianguliert sind und es keine unberücksichtigten Kanten oder Punkte mehr gibt.

6. **Endbedingung und Validierung**:
   - Der Algorithmus überprüft am Ende, ob alle Dreiecke in der resultierenden Triangulierung die Bedingung der nicht-stumpfen Winkel erfüllen.
   - Falls ein Teil der Lösung dennoch stumpfe Winkel aufweist und keine weiteren Steinerpunkte hinzugefügt werden können, wird die Lösung im Sinne einer Minimierung der stumpfen Winkel angepasst.

### Beispiel für den Greedy-Algorithmus in Aktion

Angenommen, das PSLG bildet ein einfaches Polygon:
1. Der Greedy-Algorithmus startet an einer Kante der konvexen Hülle.
2. Angenommen, die Kante \( AB \) und ein Punkt \( C \) im Inneren des Polygons bilden ein Dreieck \( ABC \).
3. Der Algorithmus prüft die Winkel an \( A \), \( B \), und \( C \):
   - Wenn alle Winkel ≤ 90° sind, wird \( ABC \) als gültiges Dreieck festgelegt.
   - Falls der Winkel bei \( A \) z.B. 110° beträgt, fügt der Algorithmus einen Steinerpunkt \( D \) auf der Kante \( AC \) hinzu, um den Winkel an \( A \) zu verkleinern.
4. Das resultierende Dreieck wird gespeichert, und der Prozess setzt sich fort, indem das nächste gültige Dreieck von einer noch nicht verwendeten Kante aus gebildet wird.

### Vorteile und Grenzen des Greedy-Algorithmus

**Vorteile**:
- **Einfachheit und Effizienz**: Der Greedy-Ansatz ist einfach zu implementieren und arbeitet lokal, was ihn in vielen Fällen schnell macht.
- **Konstruktiv und nachvollziehbar**: Er erlaubt die schrittweise Überprüfung der Lösung und bietet eine gute Heuristik für nicht-stumpfe Triangulierungen.

**Grenzen**:
- **Lokal statt global optimal**: Da der Algorithmus immer nur die beste lokale Entscheidung trifft, kann die Anzahl der Steinerpunkte suboptimal sein, da er die Gesamtstruktur nicht optimiert.
- **Komplexe Strukturen**: In komplexen oder dichten PSLGs kann der Greedy-Algorithmus durch zahlreiche Steinerpunkte ineffizient werden, da viele lokale Entscheidungen das globale Ziel erschweren.

### Zusammenfassung
Der Greedy-Algorithmus ist eine schrittweise und pragmatische Methode, um das MNOT-Problem zu lösen. Er arbeitet auf der Basis lokaler Entscheidungen und erstellt bei Bedarf zusätzliche Punkte, um gültige Dreiecke zu erhalten, die die Bedingung der nicht-stumpfen Winkel erfüllen.
