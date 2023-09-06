let map;

function initMap() {
    // Initialize the map
    map = new google.maps.Map(document.getElementById('map'), {
        center: { lat: 43.7473503, lng: -79.6617062 }, // Default center
        zoom: 12, // Default zoom level
    });

    // Listen for a click event on the map
    map.addListener('click', function(event) {
    const lat = event.latLng.lat();
    const lng = event.latLng.lng();
    console.log('Selected Location:', lat, lng);

    // Populate the hidden form fields with the selected location
    document.getElementById('latInput').value = lat;
    document.getElementById('lngInput').value = lng;


    });
}