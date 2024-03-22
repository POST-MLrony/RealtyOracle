document.getElementById('sendData').addEventListener('click', function() {
    const square = document.getElementById('square').value; // Получаем значение площади
    let rooms = document.getElementById('rooms').value; 
    const floors = document.getElementById('floors').value; 
    const type = document.getElementById('type').value; 
    const floor = document.getElementById('floor').value; 
    const wall_id = document.getElementById('wall_id').value;
    const class_ = document.getElementById('class').value;

    // Здесь URL, на который вы отправляете запрос. Замените его на актуальный URL вашего API
    const url = "https://eoqzc7r8qiy6u3p.m.pipedream.net";

    // Подготавливаем данные для отправки
    let studio = false; // Исходно предполагаем, что это не студия
    if (rooms == "0") { // Проверяем строковое значение, так как .value возвращает строку
        studio = true;
        rooms = "1"; // Изменяем на строку, чтобы сохранить консистентность типов данных
    }

  

    const data = {
        square: square,
        rooms: rooms,
        floors: floors,
        type: type,
        floor: floor,
        lo: window.GlobCoords[1],
        la: window.GlobCoords[0],
        wall_id: wall_id,
        class_: class_
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