# Examination

Individuell examinationsuppgift i kursen Programmering med Python.

Börja läs igenom game.py - det är där projektet startas.

## Starta projektet

```commandline
python -m src.game
```

Perfekt! Här är en snygg och detaljerad version av din README-text för Fruit Loop, med rubriker, punktlistor och tydlig struktur:

Fruit Loop – Terminalbaserat spel

Fruit Loop är ett terminalbaserat spel där spelaren navigerar i en rutnätsbaserad spelvärld. Målet är att samla upp alla ursprungliga ätbara föremål, undvika fällor, använda verktyg och eventuellt placera och detonera bomber för att röja väggar eller hinder. När alla ätbara föremål är upplockade kan spelaren gå till utgången (E) för att vinna.

Spelets mål

Samla alla ursprungliga ätbara föremål som finns på spelplanen.

Undvik att få minuspoäng genom fällor.

Använd verktyg, nycklar och eventuellt bomber för att röja vägar och låsa upp kistor.

När alla ursprungliga ätbara föremål är upplockade, nå utgången (E) för att vinna spelet.

Spelarens handlingar
Rörelse

Gå: W (upp), A (vänster), S (ned), D (höger)

Hoppa: JW, JA, JS, JD – hoppa över två rutor i angiven riktning

Samla föremål till inventory

Ätbart (t.ex. morot, äpple) – ger poäng och 5 steg grace-period

Verktyg (shovel/spade) – kan riva innerväggar

Nycklar – kan låsa upp kistor

Bomb – kan placeras på spelplanen och explodera i ett 3×3-område

Interagera med objekt

Ätbart: ökar poäng, ger grace-period

Verktyg: används för att riva innerväggar

Nyckel + kista: låser upp kistor som ger poäng

Bomb: placera med B och explodera efter tre steg

Fälla: ger minuspoäng; kan desarmeras med T

Exit (E): spelaren kan gå ut när alla ursprungliga ätbara föremål är upplockade

Poäng och mekanik

Spelaren startar med 10 poäng.

Varje steg minskar poängen med 1, men grace-perioden efter att ha plockat upp ett ätbart föremål stoppar poängavdrag i 5 steg.

Fertile soil: varje steg ökar värdet; efter 25 steg genereras ett nytt slumpmässigt ätbart föremål på spelplanen.

Bomb-timer: startar när bomb placeras ut; exploderar efter att spelaren tagit 3 steg.

Tips

Planera dina steg och inventory-användning för att maximera poäng och effektivitet.

Håll koll på fällor och använd verktyg smart för att nå svåråtkomliga områden.

När alla ätbara föremål är samlade, gå till E för att avsluta spelet och vinna.
