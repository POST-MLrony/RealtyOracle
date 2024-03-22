function init() {
    let map = new ymaps.Map('map', {
        center: [55.753994, 37.622093],
        zoom: 13
    });

    // Переменная для хранения текущей метки на карте
    let currentPlacemark = null;

    map.events.add('click', function (e) {
        var coords = e.get('coords');

        // Если метка уже существует, удаляем ее
        if (currentPlacemark) {
            map.geoObjects.remove(currentPlacemark);
        }

        // Создаем новую метку
        currentPlacemark = new ymaps.Placemark(coords);
        map.geoObjects.add(currentPlacemark);

        console.log(coords);
    });
}

ymaps.ready(init);
