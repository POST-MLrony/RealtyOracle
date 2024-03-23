document.getElementById('sendData').addEventListener('click', function() {
    const square = document.getElementById('square').value; // Получаем значение площади
    let rooms = document.getElementById('rooms').value; 
    const floors = document.getElementById('floors').value; 
    const type = document.getElementById('type').value; 
    const floor = document.getElementById('floor').value; 
    const wall_id = document.getElementById('wall_id').value;
    const class_ = document.getElementById('class').value;
    var meta_district = document.getElementById('districtSelector');
    var selectedText = meta_district.options[meta_district.selectedIndex].text;

    // Здесь URL, на который вы отправляете запрос. Замените его на актуальный URL вашего API
    const url = "https://151b-77-238-135-243.ngrok-free.app/api/v1/msk/";

    // Подготавливаем данные для отправки
    let studio = false; // Исходно предполагаем, что это не студия
    if (rooms == "0") { // Проверяем строковое значение, так как .value возвращает строку
        studio = true;
        rooms = "1"; // Изменяем на строку, чтобы сохранить консистентность типов данных
    }

    const data = {
        square: Number(square),
        rooms: Number(rooms),
        floors: Number(floors),
        type: String(type),
        floor: Number(floor),
        building_class: String(class_),
        lo: Number(window.GlobCoords[1]),
        la: Number(window.GlobCoords[0]),
        wall_id: String(wall_id),
        district: String(selectedText)
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
        // Здесь обрабатываем полученные данные и выводим на страницу
        console.log('Success:', data);
        updateUI(data); // Функция для обновления UI, которую вам нужно реализовать
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function updateUI(data) {
    const container = document.querySelector('.container');
    
    // Удаляем предыдущие результаты, если они есть
    const oldResults = document.getElementById('results');
    if (oldResults) {
        oldResults.remove();
    }
    
    // Создаем новый div для результатов
    const resultsDiv = document.createElement('div');
    resultsDiv.id = 'results';
    resultsDiv.innerHTML = `
        <div class="result-item"><strong>Предсказанная стоимость квартиры:</strong> <span id="predictedPrice">${data.predict ? `${parseFloat(data.predict).toFixed(1)} рублей` : "Недоступно"}</span></div>
        <div class="result-item"><strong>Ближайшее метро:</strong> <span id="nearestMetro">${data.nearest_metro ? data.nearest_metro : "Недоступно"}</span></div>
        <div class="result-item"><strong>Расстояние до ближайшего метро:</strong> <span id="metroDistance">${data.dist_to_metro ? `${parseFloat(data.dist_to_metro).toFixed(1)} км` : "Недоступно"}</span></div>
        <div class="result-item"><strong>Расстояние до центра города:</strong> <span id="cityCenterDistance">${data.dist_to_centre ? `${parseFloat(data.dist_to_centre).toFixed(1)} км` : "Недоступно"}</span></div>
        <div class="result-item"><strong>Влияние различных факторов на стоимость квартиры:</strong> <div id="imagePlaceholder"></div></div>
    `;
    container.appendChild(resultsDiv);

    // Если сервер предоставил изображение, отображаем его
    if (data.shap_waterfall_image) {
        const imageElement = document.getElementById('imagePlaceholder');
        imageElement.innerHTML = ''; // Очистить предыдущее содержимое, если оно есть
        const img = new Image();
        img.src = `data:image/png;base64,${data.shap_waterfall_image}`;
        imageElement.appendChild(img); // Добавляем изображение
    }
}