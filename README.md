## 1. Running the model
To set up the environment:
1. Create a virtual environment with venv.
2. Install the dependencies in the environment using `pip install -r requirements.txt`.

To run the system, simply execute the following command:
> main.py <input parameters>

The parameters are:
```- rows = number of rows in the grid
- columns = number of columns in the grid
- duration = duration in seconds (simulation time)
- ratio_obstacles = float, ratio of obstacles with respect to the total number of cells, e.g., 0.15
- ratio_vehicles = float, ratio of vehicles with respect to the total number of cells, e.g., 0.2
- wait_before_remove = seconds it takes to remove a vehicle that cannot move anymore
- seed = seed for simulation reproduction, e.g., 1111
- display = 1 to show graphics, 0 to not show
```

Ejemplo: `main.py 20 20 3600 0.15 0.2 10 1113 0`
<br />
<br />

(20 rows, 20 columnas, 3600s de duración, 15% de obstáculos, 20% de vehículos, 10 s antes de aparcar, seed de 1113 y no mostrar gráficamente)
o también se puede usar el fichero adjunto launch.json para ejecutar con vscode y depurar el código

Explicación de la simulación.

## 2. Inicialización
- Se generan direcciones en las casillas de la siguiente forma: se genera una dirección inicial, y con un 70% se mantiene estable
  hasta que el 30% restante genera un cambio ortogonal de dirección.
- Al mismo tiempo, se generan obstaculos (casillas no transitables) con el rate indicado en los parámetros.
- Después se intentan ajustar las direcciones de las casillas para evitar bucles muy evidentes, y que las casillas
  de los bordes no apunten hacia fuera.
- Se añaden semáforos en los cruces.
- Se genera un punto de entrada para los vehículos
- Se especifican todos los vehículos disponibles con el rate indicado en los parámetros.

## 3. Comportamiento
Agente Townhall:
- Es un agente que permite a los vehículos conocer el entorno, descubrir que hay en las casillas por las que circulan,
  descubrir si hay otros vehículos o semáforos. Es como una especie de gps/agente omnisciente para guiar a los vehículos
  
  Es una forma de desacoplar los vehículos directamente del modelo.

Agentes vehículo:
- Se mueven 1 casilla por tiempo/segundo. Siguen la dirección especificada por las casillas.
- En detalle, se moverán por la casilla dictada por la casilla actual, o por las casillas laterales/ortogonales
  si tienen definido el movimiento en esa dirección (como en una carretera normal con sus cruces izq y dcho.)
- Si se encuentran bloqueados sin espacio durante X segundos, se considera que aparcan y se introduce un nuevo vehículo
  al sistema.
- Si se encuentran bloqueados pero con espacio libre que puedan tomar, realizan una "infracción" y se van por otro lado. 
  Esto permite que las reglas estrictas de la simulación no dejen el sistema bloqueado fácilmente.

Agentes semáforo:
- Se sitúan en los cruces, cada X segundos cambian la dirección en la que admiten la circulación.
  Cada semáforo va a su propio ritmo (uno puede cambiar hacia donde está en verde cada 5 segundos mientras que otro puede hacerlo cada 8s). Admiten solo las direcciones que generaron el cruce para ponerse en verde.

## 4. Resultados
Cuando la simulación acabe mostrará el tiempo consumido por cada vehículo esperando por otros vehículos y esperando por semáforos.
También se mostrará la media y el total de tiempo acumulado.
Aparte se mostrará cuales son las posiciones del sistema por las cuales los vehículo aparcaron al no poder desplazarse más.

## 5. Representación gráfica
- Agentes se muestran como bolitas de colores
- Semáforos se muestran como flechas verdes que apuntarán cada vez a la dirección a la que permiten el acceso
- Townhall no tiene representación

- Agentes artificiales de representación: (he usado agentes porque usar javascript era bastante enrevesado solo para eso
  y quería dedicar tiempo al proyecto como tal y no con javascript y pintar gráficos.)
    - Casillas normales muestran una flecha con la dirección del tráfico
    - Obstáculos o casillas no transitables muestran un cuadrado negro
    - Punto de entrada es rojo
## 6. Siguientes pasos:
- Comunicación entre vehículos para optimizar rutas.
