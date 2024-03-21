const urlApi = "https://187e-77-238-135-243.ngrok-free.app";

document.addEventListener('DOMContentLoaded', () => {

    const authForm = document.getElementById('login-form');
    authForm.addEventListener('submit', (event) => {
        event.preventDefault();
        
        const email = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        const url = `${urlApi}/api/v1/user/auth/sign-in?email=${email}&password=${password}`;

        fetch(url, {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Обработка успешного ответа
            console.log('Успешный ответ:', data);
            if (data.status === false) 
            {
                console.log("Ошибка");
            } else {
                localStorage.setItem('token', data.token);
                window.location.replace('/lk');
            }
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Ошибка валидации:', error);
        });
    })

    const registerForm = document.getElementById('register_form');
    registerForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const username = document.getElementById('name0').value;
        const firstName = document.getElementById('name1').value;
        const lastName = document.getElementById('name2').value;
        const email = document.getElementById('email1').value;
        const password = document.getElementById('password1').value;
        
        const url = `${urlApi}/api/v1/user/auth/sign-up?username=${username}&first_name=${firstName}&last_name=${lastName}&email=${email}&password=${password}`;

        fetch(url, {
            method: 'POST'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            // Обработка успешного ответа
            console.log('Успешный ответ:', data);
            location.reload();
        })
        .catch(error => {
            // Обработка ошибки
            console.error('Ошибка валидации:', error);
        });
    })

})
