# Introducció

En aquest document veurem el desenvolupament del joc número u, *Flux de Paraules*. Mencionarem els arxius que en formen l'estructura principal, com es comuniquen amb les parts compartides del servidor web i, finalment, explicarem com funciona el mecanisme de teclejar i puntuar.

Cal destacar que aquest codi es va revisar per estar reduït al darrer terme (simplificat). Tot funciona de forma extremadament directa només mitjançant funcions essencials, un únic cronòmetre actiu i evitant codi sobrant o textos innecessaris afegits a la pàgina.


# 1. Funció del joc  
  
L'objectiu principal és posar a prova la velocitat i precisió mecànica del jugador en el teclat de l'ordinador. Al mig de la pantalla anirà apareixent una paraula aleatòria que s'ha de teclejar completament igual (el joc s'encarrega d'ignorar les lletres majúscules que puguis posar accidentalment o espais al darrere). Aquest es troba governat per un simple compte enrere:
  
- **Inici i encerts:** Els jugadors comencen sempre amb 45 segons. Cada vegada que el jugador xifra correctament la totalitat sencera de la paraula exigida, se sumarà un punt complet al seu marcador. Per ajudar al jugador a persistir, el cronòmetre el recompensa afegint **2,5 segons** extres de vida.
- **Penalitzacions (Errors):** De manera oposada, si escrius malament ni que sigui l'inici d'una paraula equivocada (el joc comprova si el teu intent segueix l'ordre lineal establert per la màquina), rebràs una falta anotada: se't resten **2 segons complets** i es pinta la teva paraula a la pantalla en **vermell fosc**. Això inclou que l'animació pausa forçosament l'activitat durant **1 segon complet** com càstig visual on no s'hi pot interactuar.
- La partida es dona per acabada en situar el cronòmetre intern a un resultat igual o per sota a zero i, a conseqüència d'això, es transmet l'historial del rànquing.


# 2. Arxius involucrats  
  
La gran essència del programa funciona gràcies als propis recursos destinats per a ell independentment. Aquests vendrien originats als següents:  
  
- `templates/joc1.html`  
- `static/js/joc1.js`  
- `static/css/joc1.css`  
  
Dins `joc1.html` comptem amb la base gràfica global on recau tot l'entrellat: s'estructura el títol, es configuren en grid les caselles pel menú del comptador i és allí precisament on obrim, en una variable de javascript pròpia (`window.JOC1_WORDS_URL`), quin arxiu concret ens descarregarem com a llista.  
  
Dins a `joc1.js` viuria tota l'adrenalina o el funcionament mental rere càmeres. A través de conceptes com "l'estat actual", nosaltres decidim i vigilem constantment per cada lletra si val la pena seguir endavant, suspendre per temps parat, i finalment és qui utilitza la petició asincrònica `fetch` on informa d'aquest valor guardant els registres en acabar i rebotant aquest contingut al servidor global de manera completament enllaçada.  
  
Per acabar estèticament el projecte, des del subdirectori pertinent dins `joc1.css` donem la maquetació en aspecte fosc i estètica semi transparent per generar un clima cibernètic com és previst a IC Games.
  
## Arxius compartits  
  
Exactament de la mateixa manera que el joc posterior "Neon Drift" o "Selecció en ordre", requerim del suport comú general en Python conegut principalment com `app.py`. Des dels propis budells s'encarrega que s'obri d'una manera pràctica `@app.route('/joc1')` filtrant de manera segura obligatòriament a aquells que es troben ja connectats mitjançant el mode d'inici de sessió.
Convé subratllar que utilitzem completament el mode d'emmagatzemar els registres a través del famós `/finalitzar_joc` programat de forma que totes tres pàgines comparteixin i recaiguin en aquest final en comú de tots els jugadors!

Les lletres on recau l'exercici les pots observar com a un fitxer simple .TXT (de caràcter general) anomenat `joc1-paraules.txt`.


# 3. Homogeneïtzació de Plantilles de Jocs  
  
L'objectiu principal tractava en unificar tota estructura general estalviant grans trossos repetitius i copiant elements amb tecnologies anomenades 'herència de plantilles de *Jinja*'.  Això resol problemes duplicats on l'aparença general de dades (La UI) fos un tòpic compartit perfectament idèntiques en la família dels tres aplicatius.

La matriu la trobaríem encavallada directament dins `templates/base.html` de manera que en el nostre arxiu en qüestió calia definir per lliure aquestes excepcions singularitzades:  
- `title`: Aquí fariem referència en que es digui explícitament "IC Games - Flux de Paraules" obrint títol web informatiu de la sessió. 
- `head`: Es permet enxarxar individualitzadament exclusivament pel "Joc 1" com podrien ser fitxers extra exclusius estètics i fonts externes concretes (Google Fonts).
- `content`: Aquí col·loquem definitivament les caixes HTML en que transcorreria d'arrel tota l'activitat com les taules o el quadre introductori prenen control sobre la web central.  
  
A banda com qualsevol joc es conserva estretament elements comuns que no desapareixen pas d'aquesta finestra compartida de la web original des del "main".

## Contracte d'Implementació per a cada Joc  
Com amb el respectat minijoc de número tres, s'ordena des d'inici aplicar que hereta tota visual en comú predeterminada a priori `{% extends "base.html" %}`, la construcció es llegeix i munta internament pel Flask de l'ordinador de la següent organització seqüencial temporal:

1. L'ordinador amb Flask adrecça la direcció oberta en resoldre la via (`/joc1`) de `app.py`.  
2. El model del *Jinja* uneix totes aquestes capes prèviament assignades i dissenya per complet d'aquest bloc construent la llançadera total finalment visual.  
3. Absorbeix per la vista sense interacció ni còpia l'àrea del `topbar` indicant sessió constant activa gràcies a aquest enxarxament unificat de l'invent!

Gràcies només d'aquesta regla tenim un salt qualitativament visible ja que es requereix moltes menys codificacions, s'estandaritza un "Llibre d'estil" idèntic en qualsevol nova activitat a afegir en paral·lel pel centre on es conserva una consistència altament acceptable d'imatge central corporativa!
