# Práctica Sistemas Multiagente
## Master universitario en ingeniería del software e inteligencia artificial

Alumno: Juan Carlos Recio Abad

Todo el código, documentación y comentarios están en inglés para que puedan publicarse y sea accesible a más gente después de su uso en la asignatura siempre y cuando el profesor de permiso.

Las clases, métodos y en general todo el código intentan ser autoexplicativos de lo que se hace.

Para preparar el entorno:
1. Crear entorno virtual con venv
2. Instalar las dependencias en el entorno: python install -r requirements.txt

Para ejecutar el sistema tan solo hace falta ejecutar el comando:
> main.py <parámetros de entrada>

Explicación de la simulación.

### Inicialización
- Se generan aleatoriamente todas las casillas con direcciones de movimiento aleatorias.
- Al mismo tiempo, se generan obstaculos (casillas no transitables) con el rate indicado en los parámetros.
- Después se intentan ajustar las direcciones de las casillas para evitar bucles muy evidentes, y que las casillas
  de los bordes no apunten hacia fuera.
- Se añaden semáforos en los cruces.
- Se genera un punto de entrada para los vehículos
- Se especifican todos los vehícles disponibles con el rate indicado en los parámetros.

### Comportamiento
Agente Townhall:
- Es un agente que permite a los vehículos conocer el entorno, descubrir que hay en las casillas por las que circulan,
  descubrir si hay otros vehículos o semáforos. Es como una especie de gps/agente omnisciente para guiar a los vehículos
  Es una forma de desacoplar los vehículos directamente del modelo.

Agentes vehículo:
- Se mueven 1 casilla por tiempo/segundo. Siguen la dirección especificada por las casillas.
- En detalle, se moverán por la casilla dictada por la casilla actual, o por las casillas laterales/ortogonales
  si tienen definido el movimiento en esa dirección (como en una carretera normal con sus cruces izq y dcho.)
- Si se encuentran bloqueados sin espacio durante X segundos, se considera que aparcan y se introducen un nuevo vehículo
  al sistema.
- Si se encuentran bloqueados pero con espacio libre que puedan tomar, realizan una "infracción" y se van por otro lado. 
  Esto permite que las reglas estrictas de la simulación no dejen el sistema bloqueado fácilmente.

Agentes semáforo:
- Se sitúan en los cruces, cada X segundos cambian la dirección en la que admiten la circulación.
  Cada semáforo va a su propio ritmo. Admiten las direcciones que generaron el cruce.
