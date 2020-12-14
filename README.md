# integrador-programacion-concurrente
## Escenario
Tenemos una cocina en la que los platos son un recurso escaso (en realidad serian recipientes, pero por fines practicos vamos a decirles platos directamente), tenemos una cantidad fija de platos a usar, que van a ser manipulados, lavados y ordenados para poder volver a usarlos nuevamente.

Como estamos obligados a mantener el order vamos a tener que asignar a distintos empleados de la cocina a realizar una función en particular respecto a los platos:

*  Ayudantes: van a sacar los platos usados y los van a mandar a lavar.
*  Bacheros: están encargados de lavar los platos y a gurdarlos con los platos limpios. Tenemos un espacio de trabajo que esta sufiendo mantenimiento, por lo que solo pueden trabajar uno a la vez.
  
Ambos trabajan con un plato a la vez.

Desde la cocina va a importar muy poco como se este dando la organización. Lo importante es que, mientras los platos sean usados, este alguien lavandolos. 

## Solución

### Involucrando a la concurrencia 
La concurrencia nos sirve en esta situación para simular el comportamiento de varios encargados interactuando minimamente pero manteniendo una sincronización para mantener el orden.
Tenemos una situación en la que existen varios actores con la función de mantener la circulación de los 'productos'. Los platos pueden estar en tres estados distintos (limpios, en uso y sucios) y solo van a dejar de circular si la cocina deja de usarlos. 

Es necesario que mantengamos la sincronización para evitar las inconcistencias que, dado que tenemos una cantidad fija de recursos, se van a notar facilmente.
Las dos situaciones planteadas a continuación tienen en común el uso de los siguientes semáforos:
* semaforoSucios: bacheros y ayundantes la usan con la variable platosSucios. 
  
* semaforoLibres: cocina y ayudantes la usan con la variable platosEnUso.

* semaforoBacheros: limita la cantidad de bacheros que pueden estar trabajando a la vez.
  
### Caso 1: de un plato a la vez
En la cocina se usa un plato cada cierta cantidad de tiempo. 
En este caso es muy difícil que se genere un interbloqueo si mantenemos la circulación constante.

### Caso 2: de a varios platos a la vez

Acá se nos pueden generar problemas con el monitor, en estos casos tenemos que cuidarnos de los potenciales deadlocks(esta situación es más grave teniendo un solo bachero, no tengo seguridad de como se genera pero creo que tiene que ver con varias noficaciones realizadas antes de que el bachero termine su tarea). Por lo que vamos a usar un semáforo.
Podemos tener la situación de que no queden platos limpios y que la cocina quede esperando mientras que los hilos siguen con sus tareas.