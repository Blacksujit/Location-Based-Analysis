document.addEventListener('DOMContentLoaded', function() {
    fetch('/static/restaurants_map.html')
        .then(response => response.text())
        .then(html => {
            document.getElementById('map').innerHTML = html;
        });
});
