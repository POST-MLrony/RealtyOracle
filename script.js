function init() {
    let map = new ymaps.Map('map-test', {
        center: [55.753994, 37.622093],
        zoom: 9
    })
    map.events.add('click', function (e) {
        var coords = e.get('coords');

        console.log(coords);
        var myPlacemark = new ymaps.Placemark(coords);
        map.geoObjects.add(myPlacemark);
    });
}

ymaps.ready(init);