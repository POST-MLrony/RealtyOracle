document.getElementById('sendData').addEventListener('click', function() {
    const square = document.getElementById('square').value; // Получаем значение площади
    let rooms = document.getElementById('rooms').value; 
    const building_year = document.getElementById('building_year').value; 
    const keep = document.getElementById('keep').value; 
    const floors = document.getElementById('floors').value; 
    const type = document.getElementById('type').value; 
    const floor = document.getElementById('floor').value; 
    const balcon = document.getElementById('balcon').value; 
    const bedrooms_cnt = document.getElementById('bedrooms_cnt').value; 
    const mortgage = document.getElementById('mortgage').value;
    const wall_id = document.getElementById('wall_id').value;
    const euro = document.getElementById('euro').value;
    var meta_district = document.getElementById('districtSelector');
    var selectedText = meta_district.options[meta_district.selectedIndex].text;


    const path = window.location.pathname;
    // Извлекаем имя файла (страницы) из пути
    const pageName = path.split('/').pop().replace('.html', '');

    // Используем полученное имя страницы в URL
    const url = `https://151b-77-238-135-243.ngrok-free.app/api/v1/${pageName}/`;
    // Подготавливаем данные для отправки
    let studio = false; // Исходно предполагаем, что это не студия
    if (rooms == "0") { // Проверяем строковое значение, так как .value возвращает строку
        studio = true;
        rooms = "1"; // Изменяем на строку, чтобы сохранить консистентность типов данных
    }

  

    const data = {
        square: Number(square),
        rooms: Number(rooms),
        building_year: Number(building_year),
        keep: String(keep),
        floors: Number(floors),
        type: String(type),
        floor: Number(floor),
        balcon: String(balcon),
        bedrooms_cnt: Number(bedrooms_cnt),
        studio: Boolean(studio),
        mortgage: Boolean(mortgage),
        lo: Number(window.GlobCoords[1]),
        la: Number(window.GlobCoords[0]),
        wall_id: String(wall_id),
        euro: Boolean(euro),
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
        <div class="result-item"><strong>Предсказанная стоимость квартиры:</strong> <span id="predictedPrice">${data.predict ? `${parseFloat(data.predict).toFixed(0)} руб.` : "Недоступно"}</span></div>
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