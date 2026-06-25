# Manual de usuario — RoboMaze

Bienvenido a **RoboMaze**, una aplicación web que muestra cómo un "robot" encuentra el camino para salir de un laberinto. Tú dibujas el laberinto (paredes, punto de partida y punto de llegada), eliges un método de búsqueda y la aplicación te muestra, paso a paso, el camino que encontró.

Este manual está pensado para **cualquier persona**, sin conocimientos técnicos. Explica, una por una, todas las pantallas y todos los botones.

---

## Índice

1. [Qué hace esta aplicación (en palabras simples)](#1-qué-hace-esta-aplicación-en-palabras-simples)
2. [Antes de empezar: abrir la aplicación](#2-antes-de-empezar-abrir-la-aplicación)
3. [La barra superior (presente en todas las pantallas)](#3-la-barra-superior-presente-en-todas-las-pantallas)
4. [Los colores del laberinto (leyenda)](#4-los-colores-del-laberinto-leyenda)
5. [Pantalla "Inicio"](#5-pantalla-inicio)
6. [Pantalla "Laberintos"](#6-pantalla-laberintos)
7. [Pantalla "Buscar ruta" (la principal)](#7-pantalla-buscar-ruta-la-principal)
8. [Pantalla "Comparar"](#8-pantalla-comparar)
9. [Cómo entender los resultados](#9-cómo-entender-los-resultados)
10. [Mensajes y avisos que pueden aparecer](#10-mensajes-y-avisos-que-pueden-aparecer)
11. [Preguntas frecuentes](#11-preguntas-frecuentes)
12. [Glosario](#12-glosario)

---

## 1. Qué hace esta aplicación (en palabras simples)

Imagina un tablero cuadriculado, como un tablero de ajedrez. En ese tablero:

- Hay una casilla de **inicio** (donde está el robot).
- Hay una casilla de **meta** (a donde quiere llegar).
- Hay **paredes** (casillas bloqueadas por las que no se puede pasar).

La aplicación calcula **el camino** que conecta el inicio con la meta sin atravesar paredes, y te lo dibuja. Además te dice cuántos pasos tiene ese camino, cuántas casillas tuvo que revisar y cuánto tardó.

Puedes usar laberintos que ya vienen listos, o dibujar el tuyo propio.

> **Importante:** el cálculo lo hace el "motor" de la aplicación (el backend). Para que todo funcione, ese motor debe estar encendido. En la barra superior verás siempre si está **en línea** o **desconectado** (ver sección 3).

---

## 2. Antes de empezar: abrir la aplicación

La aplicación tiene dos partes que deben estar funcionando a la vez:

1. **El motor (backend).** Es un programa que hace los cálculos. Alguien con conocimientos técnicos lo deja encendido; cuando está activo, queda disponible en una dirección como `http://localhost:8001`.
2. **El sitio web (frontend).** Es lo que tú ves y usas en el navegador.

Para abrir el sitio web, escribe en tu navegador la dirección donde está publicado (por ejemplo `http://localhost:5500`) y pulsa Enter. Se abrirá la pantalla de **Inicio**.

> Si al abrir la aplicación ves en la esquina superior derecha el aviso **"Backend desconectado"** en rojo, significa que el motor no está encendido. En ese caso, los cálculos no funcionarán. Pide a la persona que administra el sistema que lo encienda y luego pulsa ese aviso para volver a comprobar.

---

## 3. La barra superior (presente en todas las pantallas)

En la parte de arriba de **todas** las pantallas hay una barra fija con:

- **RoboMaze** (a la izquierda): es el logo. Si haces clic, te lleva a la pantalla de Inicio.
- **El menú de navegación**, con cuatro opciones:
  - **Inicio** — la página de bienvenida.
  - **Laberintos** — la galería de laberintos listos para usar.
  - **Buscar ruta** — donde dibujas y resuelves un laberinto.
  - **Comparar** — donde enfrentas dos o más métodos sobre el mismo laberinto.
  - La opción en la que te encuentras aparece resaltada.
- **El indicador de conexión** (a la derecha): un puntito de color con un texto. Te dice si el motor está disponible:
  - 🟢 **"Backend en línea"** — todo listo, puedes trabajar.
  - 🔴 **"Backend desconectado"** o **"Backend con problemas"** — el motor no responde.
  - ⚪ **"Conectando…"** — está comprobando en este momento.
  - **Truco:** puedes hacer **clic** sobre este indicador para forzar una nueva comprobación.

Para moverte entre pantallas, simplemente haz clic en las opciones del menú. No se pierde nada al cambiar de pantalla.

---

## 4. Los colores del laberinto (leyenda)

En cada laberinto, los colores significan siempre lo mismo. Debajo de cada tablero hay una **leyenda** que te lo recuerda:

| Color / elemento | Significado |
|------------------|-------------|
| **Inicio** | La casilla de partida (donde arranca el robot). |
| **Meta** | La casilla de destino (a donde debe llegar). |
| **Muro** | Una pared. El camino **no** puede pasar por aquí. |
| **Explorado** | Casillas que el método revisó mientras buscaba el camino. |
| **Ruta** | El camino final encontrado, del inicio a la meta. |

Entender estos cinco colores es suficiente para usar toda la aplicación.

---

## 5. Pantalla "Inicio"

Es la primera pantalla que ves. Sirve de bienvenida y de punto de partida.

Contiene:

- Un **texto de presentación** que explica brevemente qué hace RoboMaze.
- Dos botones grandes:
  - **"Empezar a buscar"** — te lleva directo a la pantalla *Buscar ruta*.
  - **"Ver laberintos"** — te lleva a la galería de *Laberintos*.
- Tres **tarjetas** ("¿Qué quieres hacer?") que son atajos a las secciones principales:
  - **Laberintos predefinidos** → abre la galería.
  - **Buscar una ruta** → abre el editor de búsqueda.
  - **Comparar algoritmos** → abre la comparación.
- Un recuadro **"Estado del backend"** que confirma si el motor está conectado, con un botón **"Volver a comprobar"** por si quieres revisar de nuevo.

**Qué hacer aquí:** si es tu primera vez, lo más sencillo es pulsar **"Ver laberintos"** para usar uno que ya viene listo (ver la siguiente sección).

---

## 6. Pantalla "Laberintos"

Aquí encuentras una **galería de laberintos de ejemplo** que ya vienen incluidos (hay 5). Sirven para practicar sin tener que dibujar nada.

Mientras cargan, verás un mensaje **"Cargando laberintos desde el backend…"**. Después aparecerán como **tarjetas**. Cada tarjeta muestra:

- Una **miniatura** (vista en pequeño del laberinto).
- Un **nombre** y una **descripción** (por ejemplo, "Sin solución: la meta queda encerrada").
- Datos rápidos: **Tamaño** (filas × columnas), número de **Muros** e **ID**.
- Dos botones:
  - **"Buscar ruta"** — carga ese laberinto y te lleva a la pantalla *Buscar ruta* con todo listo para ejecutar.
  - **"Comparar"** — carga ese laberinto y te lleva a la pantalla *Comparar*.

**Cómo usarla, paso a paso:**

1. Espera a que carguen las tarjetas.
2. Mira las descripciones y elige el laberinto que te interese.
3. Pulsa **"Buscar ruta"** (o **"Comparar"**).
4. La aplicación te cambia de pantalla automáticamente con ese laberinto ya cargado. Solo te falta ejecutar.

> Si ves el mensaje **"No se pudieron cargar los laberintos"**, significa que el motor no respondió. Revisa el indicador de conexión y pulsa **"Reintentar"**.

---

## 7. Pantalla "Buscar ruta" (la principal)

Esta es la pantalla más importante. Aquí **dibujas** el laberinto, eliges un método y **ejecutas** la búsqueda. Está dividida en dos zonas: a un lado los **controles**, al otro el **tablero** y los **resultados**.

### 7.1 El tablero

Es la cuadrícula grande. Cada cuadrito es una casilla. Sobre él harás clic para dibujar. Debajo tiene la leyenda de colores (sección 4).

Cuando entras por primera vez sin haber elegido un laberinto, aparece un tablero **vacío de 10×10**, con el inicio en la esquina superior izquierda y la meta en la esquina inferior derecha.

### 7.2 Caja "Herramienta de edición"

Aquí eliges **qué vas a dibujar** al hacer clic en el tablero. Hay tres herramientas; la activa aparece resaltada:

- **Muro** — para poner o quitar paredes.
- **Inicio** — para mover la casilla de partida.
- **Meta** — para mover la casilla de destino.

**Cómo dibujar muros:**

1. Asegúrate de tener seleccionada la herramienta **Muro**.
2. Haz **clic** en una casilla vacía para convertirla en pared.
3. Si **mantienes pulsado y arrastras**, vas pintando varias paredes de una sola vez (muy cómodo).
4. Para **borrar** una pared, vuelve a hacer clic sobre ella (al arrastrar empezando sobre una pared, las vas borrando).

**Cómo mover el inicio o la meta:**

1. Pulsa la herramienta **Inicio** (o **Meta**).
2. Haz clic en la casilla donde quieras colocarlo.
3. No se puede poner el inicio o la meta encima de una pared, ni encima de la otra casilla (inicio y meta no pueden coincidir).

### 7.3 Caja "Algoritmo"

Aquí decides **qué método de búsqueda** usar y cómo ver el resultado:

- **Menú desplegable de algoritmo**, con tres opciones:
  - **BFS — Anchura (ruta más corta):** siempre encuentra el camino **más corto**. Recomendado si quieres la mejor ruta.
  - **DFS — Profundidad:** explora "metiéndose" por un camino hasta el fondo. Es rápido, pero **no** garantiza el camino más corto.
  - **A\* — Heurística (opcional):** método "inteligente" que suele encontrar el camino más corto revisando menos casillas.
- **Casilla "Animar exploración"** (activada por defecto): si está marcada, verás la búsqueda **en cámara lenta**, casilla por casilla. Si la desmarcas, el resultado aparece **al instante**.
- **Barra "Velocidad de animación"**: deslízala hacia **"Rápida"** o **"Lenta"** para ajustar qué tan veloz se ve la animación.
- **Botón "Ejecutar búsqueda"**: pone en marcha el cálculo. Es el botón principal de esta pantalla.

### 7.4 Caja "Tamaño del laberinto"

Sirve para empezar de cero o cambiar las dimensiones:

- **Filas** y **Columnas**: escribe cuántas quieres (entre 2 y 40).
- **"Crear laberinto vacío"**: borra todo y crea un tablero nuevo del tamaño indicado.
- **"Limpiar muros"**: quita todas las paredes pero conserva el inicio y la meta.
- **"Cargar predefinido…"**: un menú para traer uno de los laberintos de ejemplo **sin salir** de esta pantalla. Elige uno y se carga al momento.

### 7.5 Ejecutar una búsqueda, paso a paso

1. Prepara el laberinto: dibuja paredes y coloca inicio y meta (o carga un predefinido).
2. En la caja **Algoritmo**, elige el método (por ejemplo, **BFS**).
3. Si quieres ver la animación, deja marcada **"Animar exploración"** y ajusta la velocidad.
4. Pulsa **"Ejecutar búsqueda"**. El botón cambiará a **"Buscando…"** un instante.
5. Observa el tablero: las casillas **Exploradas** se irán pintando y, al final, se dibujará la **Ruta** del inicio a la meta.
6. Lee los **Resultados** debajo del tablero (ver sección 9).

> **Si olvidas poner inicio o meta**, aparecerá el aviso *"Define el inicio y la meta antes de buscar."* y no se ejecutará nada. Coloca ambos y vuelve a intentar.

### 7.6 La caja "Resultados"

Debajo del tablero. Antes de ejecutar muestra el texto "Ejecuta una búsqueda para ver la ruta y las métricas." Después de ejecutar muestra:

- Un **mensaje** en verde (**"Ruta encontrada…"**) o en rojo (**"No existe ruta…"**).
- Cuatro datos: **Algoritmo**, **Longitud de ruta**, **Nodos explorados** y **Tiempo de ejecución** (explicados en la sección 9).

---

## 8. Pantalla "Comparar"

Esta pantalla sirve para **enfrentar dos o más métodos** sobre el **mismo** laberinto y ver cuál es mejor en cada aspecto. Es ideal para entender las diferencias entre BFS, DFS y A\*.

La parte de **dibujar el laberinto** funciona **igual** que en *Buscar ruta*: tienes el tablero, las herramientas **Muro / Inicio / Meta**, y la caja de **Laberinto** con Filas, Columnas, "Crear vacío", "Limpiar muros" y "Cargar predefinido…".

La diferencia está en la caja **"Algoritmos a comparar"**:

- Hay tres opciones marcables: **BFS**, **DFS** y **A\***.
- Marca las que quieras enfrentar. **Debes elegir al menos dos.**
- Pulsa el botón **"Comparar"**.

**Paso a paso:**

1. Prepara el laberinto (dibújalo o carga un predefinido) y coloca inicio y meta.
2. Marca al menos dos algoritmos (por defecto vienen BFS y DFS).
3. Pulsa **"Comparar"** (cambiará a **"Comparando…"** un momento).
4. Aparecerá la sección **"Resultado de la comparación"** con dos cosas:
   - Una **tabla resumen** que enfrenta los métodos fila por fila (¿encontró ruta?, longitud, nodos explorados, tiempo). En cada fila, el mejor método se marca con la etiqueta **"Mejor"** y la casilla resaltada.
   - Un **tablero por cada método**, mostrando lado a lado la ruta que encontró cada uno, con sus números (Ruta, Nodos, Tiempo) debajo.

> **Avisos posibles:** si seleccionas menos de dos métodos, verás *"Selecciona al menos dos algoritmos para comparar."* Si falta el inicio o la meta, verás *"Define el inicio y la meta antes de comparar."*

> En la comparación los tableros **no** se animan: muestran el resultado completo de inmediato para que puedas verlos en paralelo.

---

## 9. Cómo entender los resultados

Tras ejecutar una búsqueda (o una comparación), verás estos cuatro datos. Así se interpretan:

- **Algoritmo:** el método que se usó (BFS, DFS o A\*).
- **Longitud de ruta:** cuántos **pasos** tiene el camino encontrado, del inicio a la meta. Cuanto **menor**, más corto es el camino. (Si no hubo camino, aparece "—".)
- **Nodos explorados:** cuántas casillas tuvo que **revisar** el método para encontrar (o descartar) el camino. Cuanto **menor**, más eficiente fue la búsqueda. No confundir con la longitud de la ruta: se pueden revisar muchas casillas y que el camino final sea corto.
- **Tiempo de ejecución:** cuánto tardó el cálculo, en milisegundos (milésimas de segundo). Suelen ser cantidades muy pequeñas.

**Dos resultados posibles:**

- ✅ **"Ruta encontrada"** (verde): existe un camino y se dibujó en el tablero.
- ❌ **"No existe ruta"** (rojo): el inicio y la meta están incomunicados (por ejemplo, la meta está totalmente rodeada de paredes). Esto **no** es un error de la aplicación: simplemente no hay forma de llegar. El tablero te mostrará todas las casillas que se exploraron en el intento.

**¿Qué método elegir?**

- Si quieres el **camino más corto**: usa **BFS** o **A\***.
- Si quieres comparar comportamiento o ver cómo explora cada uno: usa la pantalla **Comparar**.
- **DFS** puede encontrar un camino más largo, pero a veces revisa menos casillas; es útil para entender las diferencias.

---

## 10. Mensajes y avisos que pueden aparecer

La aplicación muestra pequeños **avisos** (aparecen unos segundos y desaparecen solos) en la esquina de la pantalla. Estos son los más comunes:

| Mensaje | Qué significa | Qué hacer |
|---------|---------------|-----------|
| *"Backend desconectado"* (indicador arriba) | El motor de cálculo no está encendido. | Pide que enciendan el backend; pulsa el indicador para reintentar. |
| *"Define el inicio y la meta antes de buscar/comparar."* | Falta colocar el inicio o la meta. | Usa las herramientas Inicio y Meta y vuelve a ejecutar. |
| *"Selecciona al menos dos algoritmos para comparar."* | En *Comparar* marcaste menos de dos métodos. | Marca dos o más y pulsa "Comparar". |
| *"… cargado."* / *"… listo."* (verde) | Un laberinto se cargó correctamente. | Nada; puedes continuar. |
| *"No se pudieron cargar los laberintos"* | El motor no respondió al pedir la galería. | Revisa la conexión y pulsa "Reintentar". |
| Aviso en rojo tras ejecutar | Hubo un problema con los datos enviados (por ejemplo, una casilla inválida). | Revisa el inicio, la meta y el laberinto, y vuelve a intentar. |

---

## 11. Preguntas frecuentes

**¿Necesito instalar algo?**
No. Solo un navegador web (Chrome, Edge, Firefox, etc.). El motor de cálculo lo enciende quien administra el sistema.

**¿Se guardan mis laberintos al cerrar?**
La aplicación recuerda el laberinto cuando pasas de una pantalla a otra (por ejemplo, de *Laberintos* a *Buscar ruta*). No está pensada para guardar tus dibujos de forma permanente al cerrar el navegador.

**¿Por qué no aparece ningún camino?**
Probablemente la meta está rodeada de paredes o separada del inicio. Verás el mensaje rojo "No existe ruta". Quita algunas paredes o mueve el inicio/la meta.

**¿Por qué los botones no hacen nada / no calcula?**
Casi siempre es porque el motor (backend) está apagado. Mira el indicador de conexión arriba a la derecha: debe estar **verde, "Backend en línea"**.

**¿Puedo hacer laberintos grandes?**
Sí, hasta 40×40 casillas. Cuanto más grande, más casillas se exploran (y la animación tarda más).

**¿Cuál es la diferencia entre "Buscar ruta" y "Comparar"?**
*Buscar ruta* ejecuta **un** método y te muestra la animación. *Comparar* ejecuta **varios** a la vez sobre el mismo laberinto y te muestra una tabla con el ganador de cada aspecto.

---

## 12. Glosario

- **Algoritmo de búsqueda:** el "método" que usa la aplicación para encontrar el camino.
- **BFS (Anchura):** método que explora por niveles y encuentra el camino más corto.
- **DFS (Profundidad):** método que se mete por un camino hasta el fondo antes de probar otro; no garantiza el más corto.
- **A\*:** método "inteligente" que se guía hacia la meta para revisar menos casillas.
- **Nodo / casilla:** cada cuadrito del tablero.
- **Muro / obstáculo:** casilla bloqueada por la que no se puede pasar.
- **Inicio:** casilla de partida.
- **Meta:** casilla de destino.
- **Ruta:** el camino encontrado entre el inicio y la meta.
- **Nodos explorados:** casillas que el método revisó durante la búsqueda.
- **Backend / motor:** el programa que hace los cálculos; debe estar encendido.
- **Frontend / sitio web:** lo que ves y usas en el navegador.
- **Milisegundo (ms):** una milésima de segundo; la unidad en que se mide el tiempo de cálculo.

---

*RoboMaze · Manual de usuario. Si algo no funciona como se describe aquí, lo primero a revisar siempre es el indicador de conexión en la esquina superior derecha.*
