function addProduct_1 () {

    document.getElementById(".add-form-item").addEventListener("submit", function (event) {
        event.preventDefault(); // Предотвращает отправку формы по умолчанию
        var input = document.getElementById("amount").value; // Получаем значение из поля ввода
        var xhr = new XMLHttpRequest(); // Создаем новый объект XMLHttpRequest и открываем соединение к серверу Django
        xhr.open("GET", ".", true);   // Устанавливаем заголовок для отправки данных формы
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");  // Отправляем данные формы на сервер Django
        xhr.send("Count=" + input); // Обрабатываем ответ сервера
        xhr.onload = function () {  // Ваш код обработки ответа
            alert(`Отправлено ${input}`);
        };
    });
}

async function addProduct() {

    const add = async (event) => {
        event.preventDefault();
        const count = event.target.amount.value
        const item = {
            count: count,
        }
        const product = new XMLHttpRequest();
        product.open('GET', '.', true);
        product.setRequestHeader("Content-Type", "application/json");
        product.send('count' + item)
        console.log(item)
    }
    const addFormItem = document.querySelector('.add-form-item');
    addFormItem.addEventListener('submit', add);

}
//
// async function makeRequest(url, method, count) {
//
//     let headers = {
//         'X-Requested-With': 'XMLHttpRequest',
//         'Content-Type': 'application/json'
//     }
//
//     let response = await fetch(url, {
//         method: method,
//         headers: headers,
//         count: count,
//     })
//
//     return response.json()
// }
//
//
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
//
//
//
// async function addNumber_1() {
//     const buttons = document.querySelectorAll('.btn')
//
//     const add = (event) => {
//         console.log(parseInt(event.target.dataset.act))
//     }
//     buttons.forEach(button => {
//       button.addEventListener('click', add)
//     })
//     return
// }
