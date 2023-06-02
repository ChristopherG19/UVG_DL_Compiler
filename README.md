# Generador de analizadores sintácticos

Este proyecto fue utilizado para la clase de diseño de lenguajes. En este primer curso se buscó la creación de un generador de analizadores sintáticos capaz de leer archivos yal, yalp y cualquier archivo de texto para comprobar que estaban bien definidos y retornar una respuesta positiva en caso de que todo esté definido y en caso contrario retornar los errores sintáticos y/o gramaticales que se presenten.

- Funciones disponibles:
  - Generador de autómatas determinísticos y no-determinísticos
    - Método directo
    - Construcción por Thompson
    - AFN -> AFD
  - Simulación de cadenas de texto en dichos autómatas
  - Generación gráfica de los autómatas
  - Generador de scanners por medio de autómatas y lectura de archivos yal
  - Lectura de tokens a partir de los scanners
  - Lector de archivos yalp para construcción de autómata LR(0)
  - Creación de tabla de parseo LR(1)
  - Simulación de tabla de parseo y lectura de tokens
  - Verificación de errores sintácticos y gramaticales

- Resultados:
  - Tablas de parseo: Directorio tables
  - Autómatas: Directorio results
  - Objetos serializados: Directorios: tokens y scanners_dfa
  - Árboles (archivos Yal): Directorio: resultsYalex
