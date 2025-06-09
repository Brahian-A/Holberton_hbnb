Diagrama de secuencia listar lugares
este diagrama representa el listado de lugares especificados por filtros,
en este caso se muestra primero el caso exitoso.
después de que el cliente envía los criterios de filtro, el sistema intenta obtener los lugares que coincidan. Los posibles resultados incluyen una lista exitosa de lugares (200 ok), una lista vacía si no se encuentran coincidencias (200 ok), o un error interno del servidor
(500 internal server error) si la base de datos presenta un problema.