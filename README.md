# Practicas Simulacion

Repositorio para la práctica de simulación de un sistema de selección natural.





Universidad De Jaén
Escuela Politécnica Superior de Jaén

	

Grado en Ingeniería Informática -
Modelos de Simulación


***Autores: Alejandro de la Cruz López y Jesús Enrique Cartas Rascón***

## Índice 
- Simulador de selección natural
    - Formulación del problema
    - Motivación de la Simulación
- Definición del sistema
- Definición del modelo
- Cadena alimenticia
- Terreno
- Comportamientos
- Generación espontánea de Recursos
- Atributos
    - Fuerza
    - Velocidad
    - Factores de reproducción
    - Campo de visión
    - Aversión al riesgo
    - Emocional / Racional
    - Tiempo de vida natural
- Clasificación del Modelo
- Monitorización y Contadores estadísticos
- Eventos


## Simulador de selección natural
### Formulación del problema
El problema a resolver es encontrar la configuración genética del mejor individuo en el entorno a desarrollar, de forma que le permita sobrevivir y dejar un legado competente para que su especie no se extinga. Las reglas de dicho entorno se verán en la definición del modelo.

A su vez, también se busca recabar información acerca de cuáles son las distribuciones de la población, y qué genética tiene ésta en media, para arrojar luz acerca de cuáles son los individuos que más sobreviven, qué recursos tienen para ello y por qué.

### Motivación de la Simulación
Son numerosos los motivos que pueden llevar a la decisión de crear un modelo de simulación frente a un modelo matemático. En este apartado abordaremos estos motivos y su explicación adaptados a nuestra propuesta.

Nuestro problema se basa en el fenómeno de la selección natural. Éste es un fenómeno que se presta bien a ser simulado ya que la definición formal de éste problema es altamente compleja y depende de una gran cantidad de factores.

A pesar de lo comentado en el párrafo anterior, sería posible la creación de un modelo matemático adaptado a nuestro problema ya que el modelo que planteamos carece de una gran parte de la complejidad.

Pese a ser posible, hay diferentes motivos por los cuales no sería recomendable abordar este problema a través de un modelo matemático. El primero de estos motivos es la simplicidad. Sin duda, un modelo de simulación ofrecería una abstracción a los modelos formales que necesitan de mucho conocimiento experto y tiempo de estudio. 

Otro motivo es la incapacidad de observar la historia a través de un modelo matemático. Esto impediría la obtención de estadísticas que nos permiten tener una mayor comprensión del modelo y ser capaces de dar una mejor explicación a los resultados.


## Definición del sistema
El sistema propuesto consistirá en un entorno en el que varios tipos de entidades desarrollen su vida y reaccionen a las diferentes adversidades que se interpongan en ella.  Estas entidades serán Conejos y Linces.

Las variables de estado que van a definir nuestro sistema serán:

- Tiempo transcurrido.
- Generación media de las entidades.
- Número de Conejos.
- Atributos de cada una de estas entidades.
- Número de Linces.
- Atributos de cada una de estas entidades.


## Definición del modelo
El objetivo es crear un sistema similar a un algoritmo genético basado en selección natural que nos dé información acerca de cuál es la mejor combinación de genes para cada individuo de forma que le permita sobrevivir lo máximo posible.

Para simular este modelo, debemos crear la estructura lógica, que definirá los comportamientos que todos los individuos presentes en el sistema tendrán.

Esta estructura lógica será la siguiente:

### Cadena alimenticia

Los conejos se alimentan de zanahorias. 
Los linces se alimentan de conejos.


## Terreno
<img src='media/mapa definitivo 800x800.png'>

El terreno se ha generado proceduralmente como un mapa de alturas, de acuerdo al modelo de ruido de Perlin (mucho más conocido como Perlin Noise), que nos permite crear una matriz de valores y asociarles una altura en función del valor para generar los biomas necesarios, como praderas o montañas.

Los conejos aparecerán y vivirán en el bioma de la pradera, donde también crecen las zanahorias.

Los linces aparecerán y vivirán en el bioma montañoso. Este es un bioma frío en el que el lince se desenvuelve bien, pero para poder comer debe bajar al bioma de la pradera a por conejos. 

Para equilibrar la cadena y que el conejo no sufra de una desventaja por la definición del modelo, si el lince pasa demasiado tiempo fuera de su bioma, morirá de asfixia debido al calor que no está acostumbrado a soportar.

Ambas entidades están localizadas por su posición en el plano (x, y) para que puedan interactuar con las entidades cercanas y para monitorizar su ciclo de vida y datos interesantes, como el punto en el que mueren, entre otros.

Más concretamente, el terreno se compone de dos matrices. La primera matriz, denominada world, alberga vectores de 3 elementos que corresponden al color de ese píxel (R,G,B). Esta estructura de datos se encarga únicamente de gestionar los colores. Los colores usados son los pertenecientes al terreno (darkSand, lightSand, lightGreen, green, darkGreen, mountain y snow).

La segunda matriz la denominamos manipulable_world. Esta matriz es la que recibirá todas las actualizaciones que las entidades hagan durante la simulación. Su contenido es una tupla de dos enteros [int, int]:

- el primero indica cuál es el nivel del terreno del mapa original (valores de 1 a 6, siendo 1 darkSand y 6 snow)

- el segundo indica si el terreno está vacío o tiene algo:

```
- NADA = 0
- CONEJO = 1
- ZANAHORIA_CONEJO = 2
- ZANAHORIA = 3
- CONEJO_REPRODUCCION = 4
- CONEJO_CONEJO = 5
- PELEA_CONEJO = 6
- LINCE = 7
- PELEA_LINCE = 8
- ZANAHORIA_LINCE = 9
- CONEJO_LINCE = 10
- LINCE_LINCE = 11
- LINCE_REPRODUCCION = 12
```

La idea es que las entidades, al interactuar modifiquen la matriz manipulable_world simplemente poniendo el valor que corresponda en función de su situación y posición, y ya se encargará el gestor del terreno de actualizar esa información y traducirla a colores que posteriormente formará la imagen que se rasterizará y presentará en pantalla. 


### Comportamientos
Destacar que todos los atributos que serán mencionados posteriormente son genes. Las primeras entidades se generarán con estos atributos definidos por funciones de probabilidad. Las entidades de las de las generaciones posteriores tendrán como genes el producto del cruce de los genes de sus progenitores. Para añadir diversidad a la población, introduciremos un factor de mutación, que puede modificar el gen de un recién nacido aleatoriamente.

Para la apropiada manipulación y comprensión de los atributos, éstos estarán normalizados entre [0, 1]. Esto nos permite que cada atributo tenga infinitos valores posibles, además de ser inteligibles para facilitar así la obtención de conclusiones.

### Generación espontánea de Recursos
Las zanahorias aparecerán en puntos aleatorios del mapa siempre que sea dentro del bioma que les corresponde. La frecuencia de aparición y el lugar vendrán definidos por funciones de distribución aleatoria.
Existirá una variable tiempo = {sol, lluvia}, de forma que si llueve, la función de distribución que define la frecuencia de aparición de zanahorias aumentará. La frecuencia de cambio de la variable tiempo entre sus estados vendrá definida por otra función de distribución. 

### Atributos
#### Fuerza
Determina la probabilidad de que esta entidad gane contra otra de la misma clase por un recurso. Se creará una función probabilística que calcule qué entidad gana en función de su fuerza. Este atributo será siempre inverso a la velocidad.

#### Velocidad
Determina cuántas unidades de terreno recorre por unidad de tiempo. Útil para huir o cazar. Este atributo será siempre inverso a la fuerza.

#### Factores de reproducción
- Necesidad reproductiva
- Se activará a un determinado tiempo de vida

#### Campo de visión
Determina qué porción de terreno puede la entidad ver dada su posición. Ya que es un recurso muy valioso, se compensará de forma que aquellas entidades con visión muy aguda tendrán hambre más frecuentemente.

#### Hambre
Necesidad de comida que presenta una entidad en un momento dado.
Factor hambre
Determina cuánto se saciará el medidor de hambre por unidad de alimento.


#### Aversión al riesgo
Este factor define cómo de mucho defenderá una entidad el recurso a consumir cuando otra entidad de la misma clase quiere acceder al mismo. Por ejemplo, si dos conejos quieren comerse la misma zanahoria, deberán luchar por ella. Su factor de aversión al riesgo definirá si el conejo huye o luchará con el otro conejo por el recurso, con el factor de riesgo de morir en el intento. De la misma forma funcionará con linces que buscan el mismo conejo.

#### Tiempo de vida natural
Define el tiempo que una entidad permanecerá en la simulación como máximo (en caso de que ninguna otra entidad la matase o muriese de hambre).

#### Asfixia (sólo linces)
Este parámetro determinará cuál es el tiempo máximo que un lince podrá permanecer en la pradera buscando conejos antes de morir asfixiado por el calor. Al borde de la asfixia, el lince volverá rápidamente a la montaña y ahí, este valor se restaurará lentamente a su valor mínimo.


#### Clasificación del Modelo
Con la lógica del modelo expuesta anteriormente, procedemos a hacer una clasificación del modelo:
Se va a tratar de un modelo dinámico. Las entidades evolucionan a lo largo del tiempo (hambre, necesidad reproductiva), además, generan nuevas entidades con diferentes atributos que “sustituyen” a la generación anterior.

El modelo será de naturaleza probabilística ya que contará con factores aleatorios para muchos de los eventos que ocurran, como la reproducción, la caza o la generación de zanahorias entre muchos otros.

El espacio del modelo será continuo dado que los atributos, acotados en el dominio [0, 1] tienen infinitos valores posibles.

El objetivo final del modelo de simulación será la obtención de la combinación de genes adecuada que garantice la supervivencia de cada especie. Por lo tanto, la finalidad del modelo será prescriptiva. Añadir que, pese a que este es el objetivo final, la obtención de estadísticas y el estudio de éstas serán de suma importancia para la explicación de los resultados, por lo que se podría añadir una finalidad descriptiva.

El modelo será de ciclo cerrado ya que cada ejecución de la simulación será independiente de las anteriores y las posteriores. Aclarar que éstas sólo dependerán de la semilla aleatoria que se haya establecido al inicio de la misma.

## Monitorización y Contadores estadísticos

Durante la ejecución de la simulación se guardarán diferentes métricas que nos ayudarán a sacar conclusiones de la solución final obtenida. Además, éstas nos aportarán información sobre cómo se está desarrollando el modelo para así poder hacer correcciones adecuadas que lo mejoren.

Las métricas estadísticas que vamos a utilizar se aplicarán a cada uno de los atributos de las entidades, y serán tales como:

- Media
- Desviación típica
- Varianza
- Tiempo de vida
- Relaciones entre atributos
 
A su vez, se generarán tablas y gráficas a partir de estos datos, para poder representarlos pertinentemente y obtener una visión global del funcionamiento del sistema para cada uno de los diferentes ámbitos, y poder relacionarlos para sacar conclusiones y abordar la respuesta a nuestro problema inicial.

## Eventos
### Inicio de la simulación
Se genera un número determinado de entidades. Se generarán más conejos que linces. Las entidades se generarán en el espacio al que pertenecen (conejos en praderas y linces en montañas)

### Conejo come zanahoria
Si una zanahoria entra en el campo de visión de un conejo y éste tiene hambre, el conejo irá hacia la zanahoria. Hasta que no esté suficientemente cerca, no podrá comérsela. Si varios conejos tratan de acceder a la zanahoria, el último conejo retará al primero. El que pierda el reto morirá y el otro podrá comerse la zanahoria. Se establecerá una cola para las peleas entre entidades, ya que no se pueden pelear dos entidades a la vez.

### Lince come conejo
El funcionamiento será exactamente igual, pero en la relación lince-conejo.

### Reproducción
Cuando dos entidades se quieran aparear, se acercarán y tras un pequeño lapso de tiempo, generarán una nueva entidad de esa especie.

### Fin de la simulación
Se establecerá una condición de parada para finalizar la simulación y se publicarán las estadísticas que nos ayudarán a inferir el conocimiento sobre el modelo.
