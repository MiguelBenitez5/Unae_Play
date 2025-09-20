// tablero
const board = document.querySelector('.board')
//variable global para controlar la fila
let row_board = 1
let maxChars = 0;

function paintBoard(){
    fetch('https://unae-play.onrender.com/wordle/action/getdata')
        .then(response => response.json())
            .then(data =>{
                //comprobar error
                if (data.basic_data.word_len === 0){
                    console.log('Error, no hay palabra nueva')
                    return
                }

                console.log(data)

                if (data.basic_data.tries) row_board = data.basic_data.tries
                if (data.basic_data.word_len) maxChars = data.basic_data.word_len 
                
                for (let i = 1; i< 7; i++){
                    const row = document.createElement('div')
                    row.classList.add('row-board')
                    for(let j = 0; j< data.basic_data.word_len ; j++){
                        const cell = document.createElement('div')
                        cell.classList.add('cell')
                        cell.id = `${i}-${j}`
                        if(data.history){
                            if(data.history.game_data.tries > i){
                                cell.textContent = data.history[`${i}`]['result'][`${j}`].char
                                if (data.history[`${i}`]['result'][`${j}`].color === 'green') cell.classList.add('correct')
                                else if (data.history[`${i}`]['result'][`${j}`].color === 'yellow') cell.classList.add('present')
                                else cell.classList.add('absent')
                            }
                        }
                        row.appendChild(cell)
                    }
                    board.appendChild(row)
                }

            }).catch(error => console.log('Ocurrio un error ', error)) 
}

window.onload = paintBoard

function send_word(){
    const startTime = Date.now()
    fetch(`https://unae-play.onrender.com/wordle/${input.value}`)
        .then(response => response.json())
            .then(data =>{
                const resposeTime = Date.now()
                const elapsedTime = resposeTime - startTime
                console.log('Tiempo transcurrido: ',elapsedTime)
                if (data.status === 'error'){
                    console.log('Detalle del error: ',data.message)
                    return
                }

                console.log(data)
            }).catch(error => console.error("Ha ocurrido un error ", error))
}

// //plantear un get_all_data para recibir los datos necesarios para dibujar el tablero
// for (let i = 1; i< 7; i++){
//     const row = document.createElement('div')
//     row.classList.add('row-board')
//     for(let j = 0; j< 5; j++){
//         const cell = document.createElement('div')
//         cell.classList.add('cell')
//         cell.id = `${i}-${j}`
//         row.appendChild(cell)
//     }
//     board.appendChild(row)
// }

const cells = document.querySelectorAll('.cell')


// teclado
const input = document.querySelector(".my-input");
const keys = document.querySelectorAll('.key')
input.focus()

//comportamiento y limitaciones al input para que cumpla con su onjetivo
input.addEventListener("input", () => {
    if (input.value.length > maxChars) {
        input.value = input.value.slice(0, maxChars); // recorta el exceso
    }
    else{
        for (let i = 0; i < input.value.length; i++) {
            const cell = document.getElementById(`${row_board}-${i}`)
            cell.textContent = input.value.charAt(i)
        }
    }
});

//evento para la tecla de borrar
input.addEventListener('keydown', (e)=>{
    if (e.key === 'Backspace'){
        const cell = document.getElementById(`${row_board}-${input.value.length-1}`)
        console.log('Borrar')
        cell.textContent = ''
    }
})

//agregar eventos a todas la teclas del teclado en pantalla
keys.forEach(key =>{
    if (key.textContent == 'Enter'){
        key.addEventListener('click', send_word)
    }
    else if (key.textContent == '⌫'){
        key.addEventListener('click', ()=>{
            input.value = input.value.slice(0,-1)
            input.focus() 
            console.log(input.value)
            const cell = document.getElementById(`${row_board}-${input.value.length}`)
            cell.textContent = ''
        })
    }
    else{
        key.addEventListener('click', ()=>{
            input.value += key.textContent
            if (input.value.length > maxChars) {
                input.value = input.value.slice(0, maxChars); // recorta el exceso
            }
            for (let i = 0; i < input.value.length; i++) {
                const cell = document.getElementById(`${row_board}-${i}`)
                cell.textContent = input.value.charAt(i)
            }
        })
    }
})

//recuperar el foco en el input
input.addEventListener("blur", () => {
    setTimeout(() => input.focus(), 0);
});

//evento de envio presionando la tecla enter
input.addEventListener("keydown",(e)=>{
    if (e.key === 'Enter') send_word
})


