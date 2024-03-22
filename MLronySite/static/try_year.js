
// Получаем элемент по его ID

const numberInput = document.getElementById('building_year');

// Добавляем слушатель события для валидации при вводе
numberInput.addEventListener('input', function() {
    if (this.value.length === 4) {
        const min = numberInput.getAttribute('min');
        const max = numberInput.getAttribute('max');
        let value = parseInt(this.value, 10); // Преобразуем введенное значение в число
        
        // Проверяем, выходит ли число за пределы диапазона
        if (value < min) {
            this.value = min; // Устанавливаем минимальное значение
        } else if (value > max) {
            this.value = max; // Устанавливаем максимальное значение
        }
    }
});
