document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('confirmSelection').addEventListener('click', function() {
        var selectedLocationValue = document.getElementById('selectedLocation').value;

        // Исправляем здесь, устанавливаем значение в value, а не в placeholder
        document.getElementById('addressInput').value = selectedLocationValue;
        document.getElementById('myModal').style.display = 'none';
        document.body.style.overflow = ''
    });
});
