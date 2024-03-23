    const buttons = document.querySelectorAll('.button');

    // Добавляем каждой кнопке обработчик события клика
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            const href = this.getAttribute('data-href'); // Получаем URL из атрибута data-href
            if(href) {
                window.location.href = href; // Перенаправляем на указанный URL
            }
        });
    });