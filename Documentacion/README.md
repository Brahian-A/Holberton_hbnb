Diagrama de secuencia listar lugares
    este diagrama representa el listado de lugares especificados por filtros,
    en este caso se muestra primero el caso exitoso.
    después de que el cliente envía los criterios de filtro, el sistema intenta obtener los lugares que coincidan. Los posibles resultados incluyen una lista exitosa de lugares (200 ok), una lista vacía si no se encuentran coincidencias (200 ok), o un error interno del servidor
    (500 internal server error) si la base de datos presenta un problema.

Diagrama de secuencia Crear un lugar
    Este diagrama representa la creacion de un lugar.
    El flujo principal implica que el cliente envía los datos del lugar a la API, que los valida y, si son correctos, los guarda en la base de datos, retornando un 201 created. Se manejan dos escenarios de error: problemas de validación (400 bad request) y errores internos del servidor durante el guardado (500 internal server error)

Diagrama de secuencia crear una reseña
    este diagrama esta ilustra el posteo de una reseña, el flujo de este diagrama primero muestra los errores y por ultimo el caso exitoso.
    El cliente envía los datos a la API, que los valida con la Lógica de Negocio. Los posibles resultados son: un problema de validación (400 bad request), un error interno del servidor al guardar (500 internal server error) y por ultimo el éxito al guardar la reseña (200 ok)

Diagrama de secuencia crear un Usuario
    este diagrama ilustra el flujo completo para el registro de un usuario detallando la interaccion de las capas del sistema con el usuario.
    el proceso inicia con el cliente enviando los datos a la API, para luego verificar esos datos een la capa businesslogic.
    [it's ok]: si los datos son válidos, el usuario se guarda correctamente devuelve 201 create
    [validate error]: si los datos no cumplen los requisitos devuelve 400 bad request
    [internal server error]: en caso de un problema inesperado al intentar guardar el usuario en la base de datos, devuelve un 500 internal server error