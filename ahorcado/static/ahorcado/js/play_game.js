const cells = document.querySelectorAll('.cell');
const hearts = document.querySelector('.hearts');
const input = document.querySelector('.my-input');
const keys = document.querySelectorAll('.key');
const gameWordContainer = document.querySelector('.game-word-container')
const modalScore = document.querySelector('.modal')
const newWordBtn = document.querySelector('.new-word-btn')

let word_length = 0
let tries = 0
let time_out = null

const emptyHeart = "fa-regular fa-heart"
const fullHeart = "fa-solid fa-heart fa-beat"
const fadedHeart = "fa-solid fa-heart fa-fade"


// evento para el boton de inicio de partida posterior a la pantalla de carga
loadingBtn.addEventListener('click', restartGame)

function play_game(char){
    fetch(`/ahorcado/${char.toLowerCase()}`)
    .then(response => response.json())
    .then(data =>{
        console.log(data)
        if(data.status){
            if(data.status == 'error'){
                console.log(data.message)
                return
            }
        }
        if(data.key_error){
            console.log('Ya jugaste esta letra')
            return
        }

        if(data.game_data.tries !== undefined){
            tries = data.game_data.tries
        }
        if(data.game_data.word_len) word_length = data.game_data.word_len

        if(data.not_found){
            console.log("Letra no encontrada, pierdes vida")
            delete_heart()
            if (data.game_status !== 'defeat')
                return
        }

        // mostrar pantalla modal si finaliza la partida

        if(data.game_data.result){
            paint_board(data)
        }

        // comprobar victoria o derrota
        if(data.game_status === 'win' ){
            showModalScreen('ahorcado', data)
            show_dialogue('victoria', 'ahorcado',data)
            return
        }

        if (data.game_status === 'defeat'){
            showModalScreen('ahorcado', data)
            show_dialogue('derrota', 'ahorcado',data)
            return
        }
              
    }).catch(error=> console.log(error))
}

function get_data(){
    fetch(`/ahorcado/action/getdata`)
    .then(response => response.json())
    .then(data =>{

        console.log(data)
        if(data.status === 'error'){
            console.log(data.message)
            return
        }

        if(data.game_data.tries) tries = data.game_data.tries
        if(data.game_data.tries) word_length = data.game_data.word_len
        
        paint_hearts()
        paint_board(data)

    }).catch(error => console.error("Error criminal: ",error))
}

function paint_board(data){
    gameWordContainer.innerHTML = ''
    gameWordContainer.style.gridTemplateColumns = `repeat(${data.game_data.word_len}, 1fr)`
    for(let i = 0; i < data.game_data.word_len; i++){
        const cell = document.createElement('div')
        cell.id = `cell-${i}`
        cell.className = 'cell'
        
        if(data.game_data.result[i]){
            cell.textContent = data.game_data.result[i]
        }
        
        gameWordContainer.appendChild(cell)
    }
}

function delete_heart(){
    console.log("Intentos al borrar: ",tries)
    const heart = document.getElementById(`heart-${tries}`)
    heart.className = fadedHeart
    setTimeout(()=>{
        heart.className = emptyHeart
    }, 1500)

}

function paint_hearts(){
    hearts.innerHTML = ''
    for(let i = 0; i < 5; i++){
        const heart = document.createElement('i')
        heart.id = `heart-${i}`
        heart.style.color = '#ba0808'  
        if ( i< tries){
            heart.className = fullHeart
        }else{
            heart.className = emptyHeart 
        }
        hearts.appendChild(heart) 
    }
}

function play_game_handler(event){
    play_game(this.textContent)
    // lugar para desabilitar la tecla visualmente
    this.style.backgroundColor =  '#424242'

    this.removeEventListener('click', play_game_handler)
}

function addEventsForKeys(){
    keys.forEach(key =>{
        if (key.textContent !== 'Enter' && key.textContent !== '⌫'){
            key.addEventListener('click', play_game_handler)
            key.style.backgroundColor = '#d3d6da'
        }
    })
}

document.addEventListener('keydown', (e)=>{
    const allowedChars = /^[a-zA-ZñÑ]$/
    if (allowedChars.test(e.key)){
        play_game(e.key)
    }
})

async function restartGame() {
    newWordBtn.removeEventListener('click', restartGame)
    setTimeout(()=> newWordBtn.addEventListener('click', restartGame),500)
    try{
        const response = await fetch('/ahorcado/action/restart')
        if (!response.ok) throw new Error("Ocurrio un error en la consulta en el servidor "+response.status)
        const data = response.json()
        console.log(data)
        // se reinicia la partida y se vuelve a repintar el tablero y los corazones
        addEventsForKeys()
        get_data()
        show_dialogue('inicio', 'ahorcado')
    }catch(err){
        console.log(err)
    }
}

newWordBtn.addEventListener('click', restartGame)