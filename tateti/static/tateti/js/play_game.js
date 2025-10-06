//el juego se reinicia cada vez que carga la pagina
window.onload = ()=>{
    restart_game()
    random_dialogue()
}

const cells = document.querySelectorAll(".cell")
const level = document.querySelector('.level')
const nextLevel = document.querySelector('.next-level')
const giveup = document.querySelector('.giveup')
const reset = document.querySelector('.reset')
const score = document.querySelector('.score')
const tryAgain = document.querySelector('.try-again')
const scoreTitleTateti = document.querySelector('.score-title')
const scoreIconTateti = document.querySelector('.score-icon')
const dialogueText = document.getElementById("dialogue-text")

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
                let content;
                switch (board[row][col]){
                    case 'X': content = xmark; break;
                    case '0': content = circle; break;
                }
                const cell = document.getElementById(`${row}-${col}`);
                cell.innerHTML = content;

                // Animación: agrega clase appear
                const icon = cell.querySelector('i');
                if(icon){
                    icon.classList.remove('appear');   // reinicia animación si es necesario
                    void icon.offsetWidth;             // fuerza reflow
                    icon.classList.add('appear');      // aplica animación
                }

                cell.removeEventListener('click', clientPlay);
                cell.classList.remove('empty');
            }
        }
    }
}

async function restart_game(){
    try{
        const response = await fetch('/tateti/action/restart')
        if(!response.ok) throw new Error('Ocurrio un error al consultar al servidor: '+response.status)
        const data = await response.json()
        show_dialogue('inicio', 'tateti')
        resetCountingTimer()
        console.log(data)
        cleanBoard()
        level.textContent = 'Facil'
        nextLevel.classList.add('hidden')
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

        level.textContent = data.level == 'easy'? 'Facil' : data.level == 'medium'? 'Normal' : 'Dificil'
        cleanBoard()
        nextLevel.classList.add('hidden')
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
        const response = await fetch('/tateti/action/giveup/')
        if (!response.ok) throw new Error('Ocurrio un error al consultar al servidor: '+response.status)
        const data = await response.json()
        //configurar y mostrar ventana modal 
        scoreIconTateti.innerHTML = '<i class="fa-solid fa-flag" style="color: #eaecf0;"></i>'
        scoreTitleTateti.textContent = 'Una rendicion a tiempo es mejor que una derrota'
        showModalScreen('tateti', data)
        giveup.classList.add('hidden')
        nextLevel.classList.add('hidden')
        tryAgain.classList.add('hidden')
        removeEvents()
        stopCountingTimer()
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
                nextLevel.classList.add('hidden')

                level.textContent = data.level == 'easy'? 'Facil' : data.level == 'medium'? 'Normal' : 'Dificil'
                cleanBoard()
                if(data.hard_machine_move.board){
                    paintBoard(data.hard_machine_move.board)
                }
            }).catch(error => console.error('Ha ocurrido un error al consultar la url ',error))
})

async function try_again(){
    try{
        const response = await fetch('/tateti/action/tryagain')
        if(!response.ok) throw new Error("Error en la conexion con el servidor"+response.status)
        const data = await response.json()
        cleanBoard()
        paintBoard(data.board)

    }catch(err){
        console.log(err)
    }
}

//evento para el boton de reiniciar partida
reset.addEventListener('click', restart_game)

//evento para el boton de rendirse
giveup.addEventListener('click', give_up)

// evento para el boton de reintentar
tryAgain.addEventListener('click', try_again)

async function clientPlay(){
    startCountingTimer()
    try{
        const response = await fetch(`/tateti/${this.id}`)
        if (!response.ok) throw new Error('Error en la consulta con el servidor: '+ response.status)
        const data = await response.json()

        console.log('Respuesta del servidor: ',data)
        
        if (data.status == 'error') {
            console.log(data.status)
            return
        }
        //se pinta el tablero en cada jugada
        paintBoard(data.board)

        level.textContent = (data.level == 'easy')? 'Facil' : (data.level == 'medium')? 'Normal' : 'Dificil'

        if(data.game_status === 'win' && data.level === 'medium'){
            nextLevel.classList.remove('hidden')
            tryAgain.classList.add('hidden')
            giveup.classList.remove('hidden')
            show_dialogue('tatetidificil', 'tateti')
            removeEvents()
            return
        }
        
        if(data.game_status == 'win' && data.level === 'hard'){
            nextLevel.classList.add('hidden')
            giveup.classList.add('hidden')
            tryAgain.classList.add('hidden')
            show_dialogue('victoria','tateti')
            removeEvents()
            showModalScreen('tateti',data)
            stopCountingTimer()
            return
        }

        if(data.game_status === 'win'){
            nextLevel.classList.remove('hidden')
            giveup.classList.remove('hidden')
            show_dialogue('siguiente','general')
            removeEvents()
            return
        }

        if(data.game_status == 'draw'){
            show_dialogue('empate','tateti')
            tryAgain.classList.remove('hidden')
            nextLevel.classList.add('hidden')
            giveup.classList.remove('hidden')
            return
        }

        if(data.game_status == 'defeat'){
            show_dialogue('derrota','tateti')
            giveup.classList.add('hidden')
            nextLevel.classList.add('hidden')
            showModalScreen('tateti',data)
            stopCountingTimer()
            removeEvents()
            return
        }

        giveup.classList.remove('hidden')
        nextLevel.classList.add('hidden')
        tryAgain.classList.add('hidden')
        
    }catch(err){
        console.log(err)
    }   
    
}

//eventos para cada celda del tablero
cells.forEach(cell =>{
    cell.addEventListener("click", clientPlay )
})

// remover eventos de celdas
function removeEvents(){
    cells.forEach(cell =>{
        cell.removeEventListener('click', clientPlay)
        cell.classList.remove('empty')
    })   
}