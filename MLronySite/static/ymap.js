function init() {
    var myMap = new ymaps.Map('map', {
        center: [59.9386, 30.3141],
        zoom: 12
    });
    myMap.controls.remove('searchControl');
    myMap.controls.remove('rulerControl');
    myMap.controls.remove('trafficControl');
    myMap.controls.remove('typeSelector');
    myMap.controls.remove('fullscreenControl');
    let currentPlacemark = null;

    function setPlacemark(coords) {
        if (currentPlacemark) {
            myMap.geoObjects.remove(currentPlacemark);
        }
        currentPlacemark = new ymaps.Placemark(coords);
        myMap.geoObjects.add(currentPlacemark);
    }

    myMap.events.add('click', function (e) {
        var coords = e.get('coords');
        setPlacemark(coords);
        ymaps.geocode(coords).then(function (res) {
            var firstGeoObject = res.geoObjects.get(0);
            var address = firstGeoObject.getAddressLine();
            document.getElementById('selectedLocation').value = address;
        });
    });

    var searchControl = new ymaps.control.SearchControl({
        options: {
            provider: 'yandex#search',
            noPlacemark: true,
            resultsPerPage: 5, // Количество результатов на странице
            boundedBy: myMap.getBounds(), // Ограничение области поиска текущими границами карты
            strictBounds: true, // Запрещаем выход за границы при поиске
            kind: 'house' // Ограничение поиска только адресами (включает улицы и дома)
        }
    });

    myMap.controls.add(searchControl);

    searchControl.events.add('resultselect', function (e) {
        e.get('index');
        searchControl.getResult(e.get('index')).then(function (res) {
            var coords = res.geometry.getCoordinates();
            setPlacemark(coords);
            ymaps.geocode(coords).then(function (res) {
                var firstGeoObject = res.geoObjects.get(0);
                var address = firstGeoObject.getAddressLine();
                document.getElementById('selectedLocation').value = address;
            });
        });
    });
}

ymaps.ready(init);
