const cards = document.querySelectorAll('.card')
const giveUpBtn = document.querySelector('.giveup')
const restart = document.querySelector('.reset-btn')
const pairs = document.querySelector('.score')
// seguir trabajando para mostrar en la ventana modal al rendirse
const scoreIconMemoryGame = document.querySelector('.score-icon')
const scoreTitleMemoryGame = document.querySelector('.score-title')


const questionMark = '<i class="fa-solid fa-question fa-small question" style="color: #FFD43B;"></i>'

window.onload = ()=>{
    addEventsForCells()
    show_dialogue('inicio', 'memorygame')
}

async function play_game(id){
    startCountingTimer()
    try{
        const response = await fetch(`/memorygame/${id}`)
        if (!response.ok) throw new Error(`Error del servidor: ${response.status}`)
        const data = await response.json()
        console.log(data)
        const card = document.getElementById(id)
        card.style.cursor = 'auto'
        card.onclick = null
        pairs.textContent = `Pares: ${data.pairs}`


        if (data.user_choose_1 && !data.user_choose_2){
            insert_img(data.user_choose_1, card)
            return
        }
        
        const prev_card = document.getElementById(data.position_1)

        insert_img(data.user_choice_2, card)

        if (data.result === 'not_pair'){
            not_pair(data.position_1, id)
            return
        }

        if (data.game_status !== undefined){
            if (data.game_status === 'win'){
                showModalScreen('memorygame',data)
                show_dialogue('victoria', 'memorygame')
                stopCountingTimer()
                giveUpBtn.style.display = 'none'
            }
        }
        
        
        

    }catch(err){
        console.error(err)
    }
    
}

function addEventsForCells(){
    cards.forEach(card =>{
        card.onclick = () => play_game(card.id)
    })
}



function select_img(char){
    switch(char){
        case 'a':   return '/static/memorygame/img/COLONIAS.png'
        case 'b':   return '/static/memorygame/img/FACAT.png'
        case 'c':   return '/static/memorygame/img/FACEM.png'
        case 'd':   return '/static/memorygame/img/FACQUF.png'
        case 'e':   return '/static/memorygame/img/FACVA.png'
        case 'f':   return '/static/memorygame/img/FCJHS.png'
        case 'g':   return '/static/memorygame/img/ISEDE.png'
        case 'h':   return '/static/memorygame/img/LASI.png'
    }
}

function insert_img(char, card){
    const img_url = select_img(char)
    card.style.transform = 'rotateY(360deg) scale(1.05)'
    card.innerHTML = `<img class='img' src="${img_url}">`
}

function delete_img(card){
    card.style.transform = 'rotateY(-360deg) scale(1)'
    card.innerHTML = questionMark
}

function not_pair(id_card_1, id_card_2){
    const card_1 = document.getElementById(id_card_1)
    const card_2 = document.getElementById(id_card_2)

    setTimeout(()=>{
        delete_img(card_1)
        delete_img(card_2)
        card_1.onclick = () => play_game(card_1.id)
        card_2.onclick = () => play_game(card_2.id)
        card_1.style.cursor = 'pointer'
        card_2.style.cursor = 'pointer'
    },1500)
}

// evento para en boton de rendicion

giveUpBtn.addEventListener('click', giveUp)

async function giveUp(){
    try{
        const response = await fetch('/memorygame/action/giveup')
        if (!response.ok) throw new Error("Ha ocurrido un error con la conexion al servidor"+response.status)
        const data = await response.json()
        console.log(data)

        scoreIconMemoryGame.innerHTML = '<i class="fa-solid fa-flag" style="color: #eaecf0;"></i>'
        scoreTitleMemoryGame.textContent = 'Una rendicion a tiempo es mejor que una derrota'
        showModalScreen('memorygame', data)
        giveUpBtn.style.display = 'none'
        stopCountingTimer()
        removeEventsFromCards()
    }catch(err){
        console.log(err)
    }
}

// boton de reinicio
restart.addEventListener('click', ()=>{
    addEventsForCells()
    fetch('/memorygame/action/restart')
    show_dialogue('inicio', 'memorygame')
    resetCountingTimer()
    pairs.textContent = 'Pares: 0'
    cards.forEach((card, i)=>{
        const {scaleX, scaleY} = getScale(card)
        console.log(`Indice: ${i}\nEscala x: ${scaleX}\nEscala en y: ${scaleY}`)
        if(scaleX !== '1' && scaleY !== '1'){
            setTimeout(delete_img(card), 200*i)
        }
    })
    giveUpBtn.style.display = 'block'
})

// remover eventos
function removeEventsFromCards(){
    cards.forEach(card =>{
        card.onclick = null
    })
}

// funcion auxiliar para obtener escala de elemento
function getScale(element) {
    const style = window.getComputedStyle(element);
    const transform = style.transform; 

    if (transform === "none") {
        return { scaleX: 1, scaleY: 1 };
    }

    const values = transform.match(/matrix\(([^)]+)\)/)[1].split(', ').map(parseFloat);
    const scaleX = values[0]; 
    const scaleY = values[3]; 

    return { scaleX, scaleY };
}