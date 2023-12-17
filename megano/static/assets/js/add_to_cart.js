function addProduct_1 () {

    document.getElementById(".add-form-item").addEventListener("submit", function (event) {
        event.preventDefault(); // Предотвращает отправку формы по умолчанию
        var input = document.getElementById("amount").value; // Получаем значение из поля ввода
// Создаем новый объект XMLHttpRequest
        var xhr = new XMLHttpRequest();
// Открываем соединение к серверу Django
        xhr.open("GET", ".", true);
// Устанавливаем заголовок для отправки данных формы
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
// Отправляем данные формы на сервер Django
        xhr.send("Count=" + input);
// Обрабатываем ответ сервера
        xhr.onload = function () {
// Ваш код обработки ответа
            alert(`Отправлено ${input}`);
        };
    });
}


function addProduct () {

    const add = async (event) => {
        event.preventDefault();
        const count = event.target.amount.value
        const item = {
            count: count
        }
        const xhr = new XMLHttpRequest();
        xhr.open('GET', '.', true);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.send('Count='+ count);
        xhr.onload = () => {alert(`Отправлено ${count}`);};
    }

    const addFormItem = document.querySelector('.add-form-item');
    // const countItem = document.querySelector('.Amount-input');
    addFormItem.addEventListener('submit', add);

}

async function makeRequest(url, method, count) {

    let headers = {
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/json'
    }

    let response = await fetch(url, {
        method: method,
        headers: headers,
        count: count,
    })

    return response.json()
}


// async function addNumber(event) {
//
//     let counter = event.target.innerText
//     const data = await makeRequest('.', 'get', {numbers: counter})
//
//     let input_count = document.getElementById('count')
//     let input = document.createElement('input')
//     input.addEventListener('click', addNumber);
//     input.innerHtml = data['numbers']
//     input_count.appendChild(input)
//     console.log(data)
// }



async function addNumber_1() {
    const buttons = document.querySelectorAll('.btn')

    const add = (event) => {
        console.log(parseInt(event.target.dataset.act))
    }
    buttons.forEach(button => {
      button.addEventListener('click', add)
    })
    return
}


async function takeNumber_1() {
}

async function getCounter(add, take) {
    const counter = 1 + 1;
    return counter;
}
