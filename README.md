# Práctica Sistemas Multiagente
## Master universitario en ingeniería del software e inteligencia artificial

Alumno: Juan Carlos Recio Abad

Todo el código, documentación y comentarios están en inglés.

Las clases, métodos y en general todo el código intentan ser autoexplicativos de lo que se hace.

## 1. Ejecución del modelo
Para preparar el entorno:
1. Crear entorno virtual con venv
2. Instalar las dependencias en el entorno: pip install -r requirements.txt

Para ejecutar el sistema tan solo hace falta ejecutar el comando:
> main.py <parámetros de entrada>

y los parámetros son:
```- rows = nº de rows del grid
- columns = nº de columnas del grid
- duration = duración en segundos (tiempos de mesa framework)
- ratio_obstacles = float, ratio de obstaculos con respecto del total de casillas, ej: 0.15
- ratio_vehicles = float, ratio de vehículos con respecto del total de casillas, ej 0.2
- wait_before_remove = segundos que tarda en aparcar (eliminarse) un vehículo que no puede moverse más
- seed = seed para la reproducción de la simulación, ej: 1111
- display = 1 para mostrar gráficamente, 0 para no
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
