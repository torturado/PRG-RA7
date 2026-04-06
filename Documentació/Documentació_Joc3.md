___  
# Introducció

En aquest document veurem el desenvolupament del joc número tres, *Selecció en ordre*. Veurem els arxius que ho conformes enterament, els que són compartits amb els altres membres de l'equip i finalment algunes solucions o formes diferents de resoldre punts específics.

Cal ressaltar que per al principi del projecte creï un gestor d'usuaris molt primerenc i provisional fins que Arnau va poder implementar la seva versió que era moltíssim més completa i resolia millor la gestió d'usuaris.

---
# 1. Funció del joc  
  
El jugador haurà de clicar en ordre en els números que apareixen en pantalla, aquestes caixes apareixen en un ordre aleatori. Es comença amb tres caixes i gràcies a la variable `currentLevel` i la funció `startLevel()` en l'arxiu `static/js/joc3.js` es podrà anar augmentant la dificultat afegint una caixa per nivell.  
  
En pantalla veurem en el nivell que estem amb `currentLevel - 2` i en cada encert se'ns sumaran deu punts a la nostra puntuació fins que ens equivoquem i el navegador torni un `alert` que activarà la condició que anomena a la funció `finalitzarPartida()`.

---
# 2. Arxius involucrats  
  
En essència els arxius que conformen el tercer joc són els que porten la seva etiqueta específicament. Aquests serien:  
  
- `templates/joc3.HTML`  
- `static/js/joc3.js`  
- `static/css/joc3.css`  
  
En `joc3.HTML` tenim la vista general del joc; el títol, instruccions, el contenidor de la puntuació; la injecció de `window.joc3Username`, CSS i JS.  
  
En `joc3.js` tenim la lògica del joc com a tal, aquí estan els nivells, les caixes enumerades, la puntuació; el fetch a `finalitzar_joc` i la redirecció a `home`.  
  
Finalment, en `joc3.css` està tot el que seria la part estètica de la pàgina, amb els estils del tauler i les caixes  
  
## Arxius compartits  
  
Primer en el `app.py` vaig posar la ruta `@app.route('/joc3')` perquè el joc la pàgina principal redirigís al meu joc amb una sessió obligatòria; també està un `render_template("joc3.HTML", ...)` perquè l'HTML quedés més simplificat i s'utilitzessin els mateixos arxius. Finalment el endpoint `/finalitzar_joc` és **comú** a tots els jocs.  
  
En l'HTML trobarem les targetes que enllacen amb `url_for('joc3')`, el nom és visible en la interfície d'usuari.

---
# 3. Homogeneïtzació de Plantilles de Jocs  
  
L'objectiu d'això era unificar l'estructura de les vistes dels jocs (`joc1`, `joc2`, `joc3`) mitjançant herència de plantilles *Jinja*, per a reduir duplicació d'HTML i garantir una UI consistent.  
  
El disseny base el trobem en `templates/base.HTML` i aquí tenim els blocs definits:  
- `title`: títol de pestanya per vista.  
- `head`: injecció de recursos específics (CSS, metadades, fonts).  
- `content`: contingut principal de cada joc.  
  
I també hi ha elements comuns centralitzats:  
- `topbar` d'aplicació en cas que hi hagi una sessió activa.  
- Estructura semàntica general `<main class="page-content">`.  
- Estil global de barra superior (`static/css/topbar.css`).

## Contracte d'Implementació per a cada Joc  
Totes les plantilles de joc segueixen un contracte, primer, hereten de `base.HTML` amb `{% extends "base.HTML" %}` i sobreescriuen `title` amb el nom del minijoc; després, sobreescriuen `head` per a carregar el seu CSS/recursos propis. Igual que `content` amb el seu propi *layout* i script de joc.  
  
En el flux de Renderitzat tindríem aquest ordre:  
1. Flask resol la ruta (`/joc1`, `/joc2`, `/joc3`) en `app.py`.  
2. Jinja renderitza la plantilla de joc.  
3. La plantilla hereta automàticament l'estructura comuna des de `base.HTML`.  
4. S'injecta `usuari` des de `context_processor`, habilitant topbar i dades de sessió en vistes.  
  
Això ens ofereix uns certs avantatges tècnics, com el poden ser:  
- Menys duplicació de codi entre jocs.  
- Canvis globals més ràpids.  
- Major coherència visual i de navegació.  
- Menor risc de divergències entre pàgines.  
- Escalabilitat: afegir un nou joc requereix només crear la seva plantilla filla i respectar blocs.

> [!IMPORTANT]
> - Evitar duplicar metadades globals en `head` si ja existeixen en `base.HTML`.  
> - Mantenir scripts i estils específics dins del bloc `head/*content` de cada joc.  
> - Conservar noms de blocs (`title`, `head`, `content`) per a no trencar l'herència.

---

