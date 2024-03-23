// Получение элемента модального окна
var modal = document.getElementById("myModal");

// Получение кнопки, которая открывает модальное окно
var btn = document.getElementById("selectAddress");

// Получение элемента <span>, который закрывает модальное окно
var span = document.getElementsByClassName("close")[0];

// Получение элемента body для блокировки прокрутки
var body = document.body;

// Функция для открытия модального окна
function openModal() {
    modal.style.display = "block";
    body.style.overflow = "hidden"; // Блокировка прокрутки
}

// Функция для закрытия модального окна
function closeModal() {
    modal.style.display = "none";
    body.style.overflow = "auto"; // Разблокировка прокрутки
}

// Обработчик клика на кнопку для открытия модального окна
btn.onclick = function() {
    openModal();
}

// Обработчик клика на <span> (x) для закрытия модального окна
span.onclick = function() {
    closeModal();
}

// Обработчик клика в любом месте за пределами модального окна для его закрытия
window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}

