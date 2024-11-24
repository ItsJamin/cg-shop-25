# Greedy Top-Down Algorithmus

Der Algorithmus `greedy_top_down` dient der Konstruktion einer Triangulation, die anschließend angepasst wird, um ungewünschte Eigenschaften (wie stumpfe Winkel) zu entfernen.

#### Funktionsweise

1. **Initialisierung**  
   Der Algorithmus startet mit einer Liste von Kanten, bestehend aus den harten Einschränkungen (`g_constraints`) und den Randkanten der Region (`g_region_boundary`).

2. **Sortierung der Punkte**  
   Alle Punkte der Region werden entlang der y-Achse sortiert (von oben nach unten).

3. **Iterative Kantenkonstruktion**  
   - Für jeden Punkt wird geprüft, ob eine Kante zu einem bereits besuchten Punkt erstellt werden kann.
   - Eine Kante wird hinzugefügt, wenn:
     - Sie keine bestehende Kante schneidet.
     - Sie innerhalb der definierten Region liegt.
   - Nach dem Hinzufügen der Kante:
     - Die zugehörigen Flächen (Dreiecke) werden überprüft.
     - Nicht-stumpfe Dreiecke werden markiert.
     - Stumpfe Dreiecke werden für eine spätere Nachbearbeitung gespeichert.

4. **Nachbearbeitung: Entfernung von stumpfen Winkeln**  
   Um stumpfe Dreiecke zu entfernen, wird folgender Ansatz verfolgt:
   - **Kantentausch:**  
     Für jeden stumpfen Winkel wird überprüft, ob ein benachbartes Dreieck existiert, mit dem ein Kantentausch (Edge Flip) möglich ist, um die stumpfen Winkel zu eliminieren.  
   - **Hinzufügen eines Steinerpunkts:**  
     Falls kein Kantentausch möglich ist, wird ein Steinerpunkt hinzugefügt, der den stumpfen Winkel in zwei rechte Winkel unterteilt. Dieser Punkt wird so platziert, dass er orthogonal zu der längsten Kante des stumpfen Dreiecks liegt.Das Nachbardreieck muss dementsprechend auch aktualisiert werden da es nun einen unverbundenen Punkt hat.
