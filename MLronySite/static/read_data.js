document.getElementById('sendData').addEventListener('click', function() {
    const square = document.getElementById('square').value; // Получаем значение площади
    const rooms = document.getElementById('rooms').value; 
    const building_year = document.getElementById('building_year').value; 
    const keep = document.getElementById('keep').value; 
    const floors = document.getElementById('floors').value; 
    const type = document.getElementById('type').value; 
    const floor = document.getElementById('floor').value; 
    const balcon = document.getElementById('balcon').value; 
    const bedrooms_cnt = document.getElementById('bedrooms_cnt').value; 

    // Здесь URL, на который вы отправляете запрос. Замените его на актуальный URL вашего API
    const url = "https://eogg0zzl24nxi01.m.pipedream.net";

    // Подготавливаем данные для отправки
    const data = {
        square: square,
        rooms: rooms,
        building_year: building_year,
        keep: keep,
        floors: floors,
        type: type,
        floor: floor,
        rooms: rooms,
        balcon: balcon,
        bedrooms_cnt: bedrooms_cnt,
    };

    // Отправляем данные
    fetch(url, {
        method: 'POST', // Или другой метод, который ожидается сервером
        headers: {
            'Content-Type': 'application/json',
            // Добавьте другие необходимые заголовки
        },
        body: JSON.stringify(data) // Преобразуем данные в строку JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Или обрабатываем ответ как нужно
    })
    .then(data => {
        console.log('Success:', data); // Обработка успешного ответа
    })
    .catch((error) => {
        console.error('Error:', error); // Обработка ошибки запроса
    });
});