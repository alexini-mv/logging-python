# Tutorial para crear logs con la libreria Logging de Python
Breve tutorial para aprender a implementar logs en Python. Este lenguaje provee una biblioteca para construir e ir guardando logs básicos: logging.

## Introducción básica
Cuando manejamos logs, existen diferentes niveles de logs según su importancia:
* NOSET = 0
* DEBUG = 10
* INFO = 20
* WARN = 30
* ERROR = 40
* CRITICAL = 50

Para implementar un manejador de logs, son necesarios tres cosas, principalmente:

1. El objeto que se encargará de orquestar los logs: **logger**. El logger tiene tres campos: *la propagación* que le dirá si el log se debe propagar al logger padre; *nivel* que filtrará los logs de menor importancia; *handler*, que es el objeto que muestra los logs.
2. El objeto **handler** que muestra y escribe los logs. Este puede ser un handler para escribir en la consola *StreamHandler*, o un manejador que guarda los logs en un archivo *FileHandler*, o que lo enviará por correo electrónico *SMTPHander*. Estos tres son los más comunes, pero hay varios más. Para declarar un handler se requiere dos objetos: el formateador y el nivel de logs. Con el nivel declarado se filtrarán los logs menos importantes.
3. El objeto **formatter** que le dará formato al *mensaje* que imprimiremos y además de que le dará contexto sobre lo que está sucediendo, por ejemplo, archivo, fecha, methodo, hilo, proceso, etc.

## Implementación
Importamos la librería para manejar logs:
```python
import logging
```
Instanciamos nuestro logger. En principio puede llevar cualquier nombre pero es convención ponerle el nombre de `__name__`.
```python
logger = logging.getLogger(name=__name__)
```
Establecemos el nivel del cual imprimirá los logs:
```python
logger.setLevel(level=logging.INFO)
```
Establecemos un objeto que nos construira el mensaje con formato (ver [nombres de los elementos](https://docs.python.org/3/library/logging.html#logrecord-attributes) ):
```python
formatter = logging.Formatter(
    fmt="{asctime} {filename} [{levelname}] {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{"
)
```
Instanciamos un handler para que escriba los logs. En este caso será un handler que imprimirá en consola. Se puede tener más de un handler:
```python
handler_consola = logging.StreamHandler()
handler_consola.setFormatter(formatter)
logger.addHandler(handler_consola)

handler_file = logging.FileHandler(filename="test.log")
handler_file.setFormatter(formatter)
logger.addHandler(handler_file)
```
Enviamos nuestros primeros logs haciendo uso del logger, según los niveles:
```python
logger.info("Iniciamos la prueba.")
logger.warning("Houston, tenemos un problema.")
logger.error("Tuvimos un error.")
logger.critical("¡Estoy muerto!")
```
Como declaramos un nivel INFO, no se imprimirán logs de nivel inferior, por ejemplo, debugs:
```python
logger.debug("Este mensaje no se imprimirá por ser nivel DEBUG.")
```
Podemos usar el logger para reportar los traceback que ocurran dentro de un bloque `try-except`.
```python
try:
    a, b = 7, 0
    division = a/b
    print(division)
except:
    logger.exception("Ocurrio un gravisimo error.")

logger.info("No pasa nada, seguimos trabajando!!!")
```

Y la salida en la consola o en el archivo que guarda los logs se verá así:

```console
2022-10-24 04:19:40 main.py [INFO] Iniciamos la prueba.
2022-10-24 04:19:40 main.py [WARNING] Houston, tenemos un problema.
2022-10-24 04:19:40 main.py [ERROR] Tuvimos un error.
2022-10-24 04:19:40 main.py [CRITICAL] ¡Estoy muerto!
2022-10-24 04:19:40 main.py [ERROR] Ocurrio un gravisimo error.
Traceback (most recent call last):
  File "/home/alejandro/Documentos/logging-python/main.py", line 43, in <module>
    division = a/b
ZeroDivisionError: division by zero
2022-10-24 04:19:40 main.py [INFO] No pasa nada, seguimos trabajando!!!
```

### Cargar configuración a partir de un archivo.
Podemos declarar un configuración desde un archivo externo y después será leido por python para aplicarlo.

Para eso, declaramos la configuración en un archivo .yaml (un formato más legible para declarar diccionarios), con la siguiente estructura:

```yaml
version: 1
disable_existing_loggers: true

# Declaramos el formateador y sus parámetros
formatters:
  standard:
    format: "{asctime} [{levelname}] {message}"
    datefmt: "%Y-%m-%d %H:%M:%S"
    style: "{"

# Declaramos los handlers, tanto para la salida en consola, como para la salida a archivo
handlers:
  console:
    class: logging.StreamHandler
    formatter: standard
    stream  : ext://sys.stdout

  file:
    filename: log_app.log
    class: logging.FileHandler
    formatter: standard  

# Declaramos finalmente el logger
loggers:
  nombre:
    level: INFO
    handlers: [console, file]
```
Y dentro del código de python leemos la configuración, usando la libreria `pyyaml`, convirtiendo el archivo yaml en un diccionario y usando la función `logging.config.dictConfig`

```python
import logging
import logging.config
from pathlib import Path
import yaml

def setup_logger(config_path='configLog.yaml', default_level=logging.INFO):
    """Cargamos la configuración para el logger"""
    if Path(config_path).exists():
        with open(config_path, 'r') as f:
            try:
                # Cargamos los datos desde el archivo yaml a un diccionario
                config = yaml.safe_load(f.read())

                # Seteamos la configuración al logging
                logging.config.dictConfig(config)
            except Exception as e:
                print(e)
                print('Error in Logging Configuration. Using default configs')
                logging.basicConfig(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        print('Failed to load configuration file. Using default configs')

    # Retornamos un logger con la configuración cargada.
    return logging.getLogger("nombre")
```

Finalmente, llamamos la función para instanciar el logger que utilizaremos dentro de nuestro código de trabajo.

## Referencias
* Documentación oficial de [logging](https://docs.python.org/3/library/logging.html).
* Videos en español con [conceptos](https://www.youtube.com/watch?v=Qqjbe_bbz1k) y [práctica](https://www.youtube.com/watch?v=ZwXc-niL-AQ).
* Videos tutoriales en inglés, con la teoría [básica](https://www.youtube.com/watch?v=-ARI4Cz-awo) y [práctica](https://www.youtube.com/watch?v=jxmzY9soFXg).

