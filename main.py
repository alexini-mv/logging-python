# Importamos la librería para manejar logs
import logging

# Instanciamos nuestro logger. En principio puede llevar cualquier nombre
# pero es convencion ponerle el nombre de: __name__
logger = logging.getLogger(name=__name__)

# Establecemos el nivel del cual imprimirá los logs.
logger.setLevel(level=logging.INFO)

# Establecemos un objeto que nos construira el mensaje con formato.
formatter = logging.Formatter(
    fmt="{asctime} {filename} [{levelname}] {message}",
    datefmt="%Y-%m-%d %H:%M:%S",
    style="{"
)

# Instanciamos un handler para que escriba los logs. En este caso será un
# handler que imprimirá en consola. Se puede tener más de uno.
handler_consola = logging.StreamHandler()
handler_consola.setFormatter(formatter)
logger.addHandler(handler_consola)

handler_file = logging.FileHandler(filename="test.log")
handler_file.setFormatter(formatter)
logger.addHandler(handler_file)

# Enviamos nuestros primeros logs haciendo uso del logger, según los niveles
logger.info("Iniciamos la prueba.")
logger.warning("Houston, tenemos un problema.")
logger.error("Tuvimos un error.")
logger.critical("¡Estoy muerto!")

# Como declaramos un nivel INFO, no se imprimirán logs de nivel inferior,
# por ejemplo, debugs
logger.debug("Este mensaje no se imprimirá por ser nivel DEBUG.")

# Podemos usar el logger para reportar los traceback que ocurran dentro de un 
# bloque try except.

try:
    a, b = 7, 0
    division = a/b
    print(division)
except:
    logger.exception("Ocurrio un gravisimo error.")

logger.info("No pasa nada, seguimos trabajando!!!")