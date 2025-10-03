// 1. Initialize the map and set its view to our area of interest
const map = L.map('map').setView([35.15, -119.75], 10);

// 2. Add a background map from OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

// 3. Add the citizen science points from our points.js file
citizenPoints.forEach(point => {
  L.marker([point.lat, point.lng])
    .addTo(map)
    .bindPopup(`<b>Observer:</b> ${point.observer}<br><b>Notes:</b> ${point.notes}`);
});

// 4. Fetch the satellite bloom data and add it to the map
fetch('./bloom_areas.geojson')
  .then(response => response.json())
  .then(data => {
    L.geoJSON(data, {
      style: { color: "#00FF00", weight: 1, fillOpacity: 0.5 }
    }).bindPopup("Satellite Detected Bloom Area").addTo(map);
  })
  .catch(error => console.error('Error loading GeoJSON:', error));
