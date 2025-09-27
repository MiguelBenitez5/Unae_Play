//el juego se reinicia cada vez que carga la pagina
window.onload = restart_game

const cells = document.querySelectorAll(".cell")
const level = document.querySelector('.level')
const nextLevel = document.querySelector('.next-level')
const giveup = document.querySelector('.giveup')
const reset = document.querySelector('.reset')
const score = document.querySelector('.score')
const tryAgain = document.querySelector('.try-again')

const circle = '<i class="fa-regular fa-circle" style="color: #cb151e;"></i>'
const xmark = '<i class="fa-solid fa-xmark" style="color: #0c7b0a;"></i>'

function cleanBoard(){
    cells.forEach(cell =>{
        cell.innerHTML = ''
        cell.classList.add('empty')
        cell.addEventListener('click', clientPlay)
    })
}

function paintBoard(board){
    for (let row = 0; row < 3; row++ ){
        for (let col = 0; col < 3; col++ ){
            if(board[row][col] == 'X' || board[row][col] == '0'){
                let content
                switch (board[row][col]){
                    case 'X': content = xmark; break
                    case '0': content = circle; break
                }
                const cell = document.getElementById(`${row}-${col}`)
                cell.innerHTML = content
                cell.removeEventListener('click', clientPlay)
                cell.classList.remove('empty')
            }
        }
    }
}

function removeEvents(){
    cells.removeEventListener('click', clientPlay)
    cells.classList.remove('empty')
}

async function restart_game(){
    try{
        const response = await fetch('/tateti/action/restart')
        if(!response.ok) throw new Error('Ocurrio un error al consultar al servidor: '+response.status)
        const data = await response.json()
        
        console.log(data)
        cleanBoard()
        level.textContent = 'Nivel: Facil'
        nextLevel.classList.add('hidden')
        score.textContent = 'Puntaje: 0'
    }
    catch(err){
        console.log(err)
    }
}

async function next_level() {
    try{
        const response = await fetch('/tateti/action/nextlevel')
        if (!response.ok) throw new Error('Ocurrio un error al consultar al servidor: '+response.status)
        const data = await response.json()
        
        console.log(data)

        level.textContent = data.level == 'easy'? 'Nivel: Facil' : data.level == 'medium'? 'Nivel: Normal' : 'Nivel: Dificil'
        cleanBoard()
        if(data.hard_machine_move.board){
            paintBoard(data.hard_machine_move.board)
            console.log('hey')
        }

    }catch(err){
        console.log(err)
    }
}

async function give_up() {
    try{
        const response = await fetch('/tateti/giveup/')
        if (!response.ok) throw new Error('Ocurrio un error al consultar al servidor: '+response.status)
        const data = await response.json()
        
        console.log(data)
    }catch(err){
        console.log(err)
    }
}

//evento para el boton de siguiente nivel
nextLevel.addEventListener('click', function(){
    fetch('/tateti/action/nextlevel')
        .then(response => response.json())
            .then(data =>{

                console.log(data)

                level.textContent = data.level == 'easy'? 'Nivel: Facil' : data.level == 'medium'? 'Nivel: Normal' : 'Nivel: Dificil'
                cleanBoard()
                if(data.hard_machine_move.board){
                    // deberia haber dialogo
                    paintBoard(data.hard_machine_move.board)
                }
            }).catch(error => console.error('Ha ocurrido un error al consultar la url ',error))
})

//evento para el boton de reiniciar partida
reset.addEventListener('click', restart_game)

//evento para el boton de rendirse
giveup.addEventListener('click', function(){
    fetch('/tateti/giveup/')
        .then(response => response.json())
            .then(data =>{
                // dialogo de rendicion y mostrar puntaje
            }).catch(error => console.error('Ha ocurrido un error al consultar la url ',error))
})

async function clientPlay(){
    const starTime = Math.floor(Date.now()/1000)
    try{
        const response = await fetch(`/tateti/${this.id}`)
        if (!response.ok) throw new Error('Error en la consulta con el servidor: '+ response.status)
        const data = await response.json()

        let timeNow = Math.floor(Date.now()/1000)
        const elapsedTime = timeNow - starTime
        console.log('Primero: ', elapsedTime)
        console.log('Respuesta del servidor: ',data)
        
        
        if (data.status == 'error') {
            console.log(data.status)
            return
        }
        //se pinta el tablero en cada jugada
        paintBoard(data.board)
        level.textContent = (data.level == 'easy')? 'Nivel: Facil' : (data.level == 'medium')? 'Nivel: Normal' : 'Nivel: Dificil'
        // posible dialogo
        if(data.game_status == 'win'){
            // dialogo de victoria 
            nextLevel.classList.remove('hidden')
        }else{
            nextLevel.classList.add('hidden')
        }
        if(data.game_status == 'draw'){
            //posible dialogo
            tryAgain.classList.remove('hidden')
            return
        }
        if(data.game_status == 'defeat'){
            //posible dialogo
            giveup.classList.add('hidden')
        }else{
            giveup.classList.remove('hidden')
        }
        tryAgain.classList.add('hidden')
        //se muestra el score
        score.textContent = 'Puntaje: ' + data.score
        //aqui la logica para mostrar pantalla de puntaje
    }catch(err){
        console.log(err)
    }   
    
}

//eventos para cada celda del tablero
cells.forEach(cell =>{
    cell.addEventListener("click", clientPlay )
})