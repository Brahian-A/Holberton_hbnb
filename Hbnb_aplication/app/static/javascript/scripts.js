/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const placesListSection = document.getElementById('places-list');

    // Función para obtener los datos de los lugares desde la API
    async function fetchPlaces() {
        try {
            // Asegúrate de que esta URL sea la correcta para tu endpoint de la API
            const response = await fetch('http://localhost:5000/api/v1/places/'); // Cambiá 5000 por el puerto de tu API
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            return data; // Devuelve los datos
        } catch (error) {
            console.error('Error fetching places:', error);
            // Mostrar un mensaje de error en la UI si la API falla
            placesListSection.innerHTML = '<p class="error-message">No se pudieron cargar los lugares. Por favor, inténtelo de nuevo más tarde.</p>';
            return []; // Retorna un array vacío para evitar errores posteriores
        }
    }

    // Función para renderizar los lugares en el HTML
    async function renderPlaces() {
        const places = await fetchPlaces();

        // Limpiar cualquier contenido existente (tus articles de prueba)
        placesListSection.innerHTML = '';

        if (places.length === 0) {
            placesListSection.innerHTML = '<p class="no-places-found">No hay lugares disponibles en este momento.</p>';
            return;
        }

        places.forEach(place => {
            const article = document.createElement('article');
            article.classList.add('place-card'); // Añade la clase CSS

            // Construye el HTML interno del article usando los datos del 'place'
            // Asegurate de que los nombres de las propiedades (place.name, place.price_by_night, etc.)
            // coincidan con los que devuelve tu API.
            article.innerHTML = `
                <h2 class="place-card-title">${place.title}</h2>
                <h5 class="place-card-price">price per night: $${place.price}</h5>
                <a class="details-button" href="/places/${place.id}">View Details</a>
                <div class="place-details">
                </div>
            `;
            // Asegúrate de que los campos como 'max_guests', 'number_rooms', 'number_bathrooms', 'description'
            // existan en los objetos 'place' que devuelve tu API.

            placesListSection.appendChild(article);
        });
    }

    // Llama a la función principal para renderizar los lugares cuando la página esté lista
    renderPlaces();

    // Puedes añadir aquí la lógica para el filtro de precio si quieres implementarlo más adelante
    const priceFilter = document.getElementById('price-filter');
    priceFilter.addEventListener('change', (event) => {
        const filterValue = event.target.value;
        console.log('Filtro de precio seleccionado:', filterValue);
        // Aquí iría la lógica para filtrar los places ya cargados o hacer una nueva llamada a la API
        // renderPlacesWithFilter(filterValue); // Por ejemplo, llamar a una nueva función de renderizado con filtro
    });
  });