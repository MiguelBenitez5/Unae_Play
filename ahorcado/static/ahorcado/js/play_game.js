const cells = document.querySelectorAll('.cell');
const hearts = document.querySelector('.hearts');
const input = document.querySelector('.my-input');
const keys = document.querySelectorAll('.key');
const wordContainer = document.querySelector('.word-container')
const modalScore = document.querySelector('.modal')
let word_length = 0
let tries = 0

const emptyHeart = "fa-regular fa-heart"
const fullHeart = "fa-solid fa-heart fa-beat"
const fadedHeart = "fa-solid fa-heart fa-fade"

window.onload = get_data

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
            return
        }

        // mostrar pantalla modal si finaliza la partida

        if(data.game_data.result){
            paint_board(data)
        }

        // comprobar victoria o derrota
        if(data.game_status === 'win' || data.game_status === 'defeat'){
            setTimeout(()=>{
                modalScore.style.display = 'flex'
            },1500)
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
    wordContainer.innerHTML = ''
    wordContainer.style.gridTemplateColumns = `repeat(${word_length}, 1fr)`
    for(let i = 0; i < word_length; i++){
        const cell = document.createElement('div')
        cell.id = `cell-${i}`
        cell.className = 'cell'
        
        if(data.game_data.result[i]){
            cell.textContent = data.game_data.result[i]
        }
        
        wordContainer.appendChild(cell)
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

    this.removeEventListener('click', play_game_handler)
}

keys.forEach(key =>{
    if (key.textContent !== 'Enter' && key.textContent !== '⌫'){
        key.addEventListener('click', play_game_handler)
    }
})

document.addEventListener('keydown', (e)=>{
    const allowedChars = /^[a-zA-ZñÑ]$/
    if (allowedChars.test(e.key)){
        play_game(e.key)
    }
})