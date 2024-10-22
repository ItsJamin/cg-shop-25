# Projekt Workflow aufsetzen

## VSCode und Git aufsetzen
Installiere [VSCode](https://code.visualstudio.com/download) und öffne es.

Öffne "Source Control", das dritte Symbbol links in VSCode.
Sollte hier "git installieren" stehen folge den Anweisungen um git auf deinen Computer zu installieren. Starte danach VSCode neu.


Hier solltest du nun den Button "Clone Repository" sehen. Klicke ihn und gebe folgenden Link ein:
```
https://github.com/ItsJamin/cg-shop-25.git
```

Wähle das Verzeichnis wo du das Projekt haben willst.

Öffne das Verzeichnis im Dateimanager und öffne dort eine Kommandozeile.

Gebe folgende Befehle ein mit den richtigen Werten:
```
git config --global user.email "deineemail@gmail.com"
git config --global user.name "BeliebigerName"
```

Wenn du nun was im Projekt in VSCode änderst und einen Commit machst (Source Control -> Commit) solltest du beim ersten mal aufgefordert werden, dich auf GitHub zu verifizieren. Folge den Anweisungen.

### Hinweise zu Version Control
- Statt dem Source Control in VSCode kann auch z.B. GitHub Desktop benutzt werden

- Änderungen die du am Projekt machst, uploadest du durch einen Commit. Commits brauchen immer Commit Messages

## Python und Virtual Environment in VSCode nutzen

Lade dir [Python](https://www.python.org/downloads/) runter und starte VSCode. Es ist wichtig bei der Installation von Python die Option "Add Python To Environment Variables" zu aktivieren!

Installiere in VSCode die Erweiterung "Python". Erweiterungen kannst du im fünften Symbol in der linken Leiste installieren.

Drücke Strg+Shift+P und wähle "Python: Create Environment" -> "Venv" -> "Python... (Global)" -> "requirement.txt"

### Hinweise zu Pip und Bibliotheken in Python
Durch dieses Setup werden einmal alle Libraries aus der "requirements.txt" installiert. Während des Projekts werden immer wieder Libraries hinzukommen.

Libraries können mit pip installiert werden, z.B. `pip install numpy`.

Wenn du eine Library erstellst, update die "requirements.txt" mit diesem Befehl in der Kommandozeile von VSCode:
```
pip freeze > requirement.txt
```

Wenn du nicht alle Libraries installiert hast, kannst du folgenden Befehl benutzen:
```
pip install -r requirement.txt
```

