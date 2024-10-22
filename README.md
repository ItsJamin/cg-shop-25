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

### Hinweise
- Statt dem Source Control in VSCode kann auch z.B. GitHub Desktop benutzt werden

- Änderungen die du am Projekt machst, uploadest du durch einen Commit. Commits brauchen immer Commit Messages