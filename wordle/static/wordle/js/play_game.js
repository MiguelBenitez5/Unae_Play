// tablero
const board = document.querySelector('.board')
//variable global para controlar la fila
let row_board = 1
let maxChars = 0;
// nivel de dificultad
const wordLevel = document.querySelector('.level')
const restartButton = document.querySelector('.new-word') 

function paintBoard(){
    board.innerHTML = ''
    fetch('/wordle/action/getdata')
        .then(response => response.json())
            .then(data =>{
                //comprobar error
                if (data.basic_data.word_len === 0){
                    console.log('Error, no hay palabra nueva')
                    return
                }

                if (data.basic_data.word_len <= 4) wordLevel.textContent = 'Facil'
                else if (data.basic_data.word_len <= 9) wordLevel.textContent = 'Normal'
                else wordLevel.textContent = 'Dificil'

                console.log(data)

                if (data.basic_data.tries) row_board = data.basic_data.tries + 1
                if (data.basic_data.word_len) maxChars = data.basic_data.word_len 

                for (let i = 1; i< 7; i++){
                    for(let j = 0; j< data.basic_data.word_len ; j++){
                        const cell = document.createElement('div')
                        cell.classList.add('cell')
                        cell.id = `${i}-${j}`
                        board.appendChild(cell)
                        if(data.history){
                            console.log("Historial: ",data.history)
                            if(data.basic_data.tries >= i){
                                console.log(data.history[i]['result'][j].char)
                                cell.textContent = data.history[`${i}`]['result'][`${j}`].char
                                if (data.history[`${i}`]['result'][`${j}`].color === 'green') cell.classList.add('correct')
                                    else if (data.history[`${i}`]['result'][`${j}`].color === 'yellow') cell.classList.add('present')
                                else cell.classList.add('absent')
                        }
                    }

                    board.appendChild(cell)

                }
            }
            board.style.gridTemplateColumns = `repeat(${data.basic_data.word_len}, minmax(20px,45px))`

            }).catch(error => console.log('Ocurrio un error ', error)) 
}

// evento para el boton de inicio de partida al finalizar la pantalla de carga
loadingBtn.addEventListener('click', ()=>{
    show_dialogue('inicio', 'wordle')
    addEventsForKeys()
    paintBoard()
    resetCountingTimer()
    startCountingTimer()
})

// animacion de error para las casillas de esa fila
function errorAnimation(){
    for (let i = 0; i < maxChars; i++){
        const cell = document.getElementById(`${row_board}-${i}`)
        cell.style.animation = 'none'
        void cell.offsetWidth
        cell.style.animation = 'myErrorAnim 0.5s ease 0s 1 reverse forwards'                                                                                                                               
        cell.addEventListener('animationend', function handler(e){
        if(e.animationName === 'myErrorAnim'){
            cell.style.animation = 'none';
            cell.removeEventListener('animationend', handler)
        }
    }) 
    }
}

// funcion personalizada de dialogo solo para wordle 

function send_word(){
    fetch(`/wordle/${input.value.toLowerCase()}`)
        .then(response => response.json())
            .then(data =>{
                console.log(data)

                switch(data.status){
                    case 'error': 
                        console.log('Detalle del error: ',data.message)
                        errorAnimation()
                        return
    
                    case 'not_found': 
                        console.log("Palabra incorrecta")
                        errorAnimation()
                        return

                }
                // pintar letras
                paintRow(data)

                switch(data.game_status){
                    //mostrar la pantalla modal con los puntajes
                    case 'win': 
                        show_dialogue('final', 'wordle', data)
                        fetch('/wordle/action/restart/')
                        removeEventsFromKeys()
                        showModalScreen('wordle', data)
                        stopCountingTimer()
                        return
                    case 'defeat': 
                        console.log('Perdiste')
                        show_dialogue('final', 'wordle', data.game_data)
                        fetch('/wordle/action/restart/')
                        removeEventsFromKeys()
                        showModalScreen('wordle', data)
                        stopCountingTimer()
                        return
                }


                console.log(data)
                row_board++
                input.value = ''
            }).catch(error => console.error("Ha ocurrido un error ", error))
}

function paintRow(data){
    for (let i = 0; i< maxChars; i++){
        const cell = document.getElementById(`${row_board}-${i}`)
        // las letras se pintan con un pequeño delay por tecla
        setTimeout(()=>setColor(data,cell,i),135*i)
    }
}

function resetGame(){
    fetch('/wordle/action/restart/')
        .then(response => response.json())
            .then(data => {
                console.log(data.message)
                paintBoard()
                input.value = ''
                row_board = 1
            })
                .catch(error => console.error('No se pudo establecer la conexion', error))
}

function setColor(data,cell, index){
    if (data.result[index].color === 'green') cell.classList.add('correct')
    else if (data.result[index].color === 'yellow') cell.classList.add('present')
    else cell.classList.add('absent') 
}

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


//agregar eventos a todas la teclas del teclado en pantalla
function handler_screen_keyboard(){
    input.value += this.textContent
    if (input.value.length > maxChars) {
        input.value = input.value.slice(0, maxChars); // recorta el exceso
    }
    for (let i = 0; i < input.value.length; i++) {
        const cell = document.getElementById(`${row_board}-${i}`)
        cell.textContent = input.value.charAt(i)
    }
}

function handler_keyboard(e){
    if (e.key === 'Backspace'){
        const cell = document.getElementById(`${row_board}-${input.value.length-1}`)
        console.log('Borrar')
        cell.textContent = ''
    }
    if (e.key === 'Enter'){ 
        send_word()
        input.focus()
    }
}

function delete_handler(){
    input.value = input.value.slice(0,-1)
    input.focus() 
    console.log(input.value)
    const cell = document.getElementById(`${row_board}-${input.value.length}`)
    cell.textContent = ''
}

function addEventsForKeys(){
    // eventos para el teclado en pantalla
    keys.forEach(key =>{
        if (key.textContent == 'Enter'){
            key.addEventListener('click', send_word)
        }
        else if (key.textContent == '⌫'){
            key.addEventListener('click', delete_handler)
        }
        else{
            key.addEventListener('click', handler_screen_keyboard)
        }
    })
    // eventos para el teclado fisico
    input.addEventListener('keydown', handler_keyboard)
    input.value = ''
    input.disabled = false
    input.focus()
}

// remover los eventos de las teclas
function removeEventsFromKeys(){
    keys.forEach(key =>{
        key.removeEventListener('click', send_word)
        key.removeEventListener('click', handler_screen_keyboard)
        input.removeEventListener('keydonw', handler_keyboard)
        key.removeEventListener('click', delete_handler)
        input.value = ''
        input.disabled = true
    })
}

//recuperar el foco en el input
let focusInterval = null
input.addEventListener('blur', () => {
  // Comienza a comprobar cada cierto tiempo
  focusInterval = setInterval(() => {
    const active = document.activeElement;
    // Si el usuario no está en el select, vuelve a enfocar
    if (
      active === document.body ||
      active === null ||
      !["SELECT", "INPUT", "TEXTAREA", "BUTTON"].includes(active.tagName)
    ) {
      input.focus();
    }
  }, 200);
});

input.addEventListener('focus', () => {
  // Cuando el input recupera el foco, detenemos el intervalo
  clearInterval(focusInterval);
});


restartButton.addEventListener('click', ()=>{
    resetGame()
    addEventsForKeys()
    show_dialogue('inicio', 'wordle')
    resetCountingTimer()
})
