const number = document.getElementById('number')
const message = document.getElementById('message')

document.getElementById('generate').addEventListener('click', ()=>{
    fetch('http://127.0.0.1:3000/test/generate').
    then(response => response.json()).
    then(data =>{
        number.textContent = data.random_number
        message.textContent = data.title
    })
})