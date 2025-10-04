const modal = document.getElementById('rankingModal');
const rankingFilter = document.getElementById('rankingFilter');
const rankingTable = document.querySelector('.ranking-table');
const closeBtn = document.querySelector('.close-btn')
const modalContent = document.querySelector('.modal-content')
const gameOption = document.querySelector("#game")
const wordTitle = document.querySelector('.word-title')
const wordContainer = document.querySelector('.word')
const scoreIcon = document.querySelector('.score-icon')
const scoreTitle = document.querySelector('.score-title')
const playerScore = document.querySelector('.player-score')
const scoreScreen = document.querySelector('.score-screen')
const auxInput = document.querySelector("#aux-input")



// Cerrar modal
closeBtn.addEventListener('click', () => {
    modal.style.animation = 'none'
    void modal.offsetWidth
    modal.style.animation = 'myModalCloseAnim 1s ease-out 0s 1 normal forwards'                                                                                                                               
    modal.addEventListener('animationend', function handler(e){
        if(e.animationName === 'myModalCloseAnim'){
            modal.style.display = 'none';
            modal.removeEventListener('animationend', handler)
        }
    })
    
});

function openAnimModal(){
    modal.style.animation = 'none'
    void modal.offsetWidth
}

// Cerrar modal haciendo click fuera del contenido
window.addEventListener('click', (e) => {
    console.log("Click target:", e.target)
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

// asegurar que el select no cierre la ventana modal por accidente
rankingFilter.addEventListener('click', (e) => {
    e.stopPropagation();
});

/**
 * Muestra la pantalla modal con el puntaje del jugador, el ranking del juego y global
 * @param {string} game El juego actual en minuscula, ejemplo: 'tateti'
 * @param {object} game_data Los datos de la partida    
 */
async function showModalScreen(game, game_data){
    auxInput.value = game
    try{
        // mostrar la ventana modal con un pequeño delay
        openAnimModal()
        setTimeout(()=> modal.style.display = 'flex', 1500)

        const response = await fetch(`/getscores/${game}`)
        if(!response.ok) throw new Error("No se pudo realizar la conexion con el servidor "+response.status)
        const data = await response.json()
        console.log(data)

        
        // se actualiza la tabla de ranking
        for(let i=0; i<10; i++){
            const player = document.getElementById(`player-${i+1}`)
            const score = document.getElementById(`score-${i+1}`)
            if(rankingFilter.value === 'game'){
                if (i < data.game_ranking.length){
                    player.textContent = data.game_ranking[i].user__username || ''
                    score.textContent = data.game_ranking[i].score || ''
                    continue
                }
                
            }else if(rankingFilter.value === 'global'){
                if(i < data.global_ranking.length){
                    player.textContent = data.global_ranking[i].user__username || '' 
                    score.textContent = data.global_ranking[i].score || ''
                    continue
                }
            }

            player.textContent = ''
            score.textContent = ''
        }
            
        
    
        // nombre para el option del ranking del juego
        const capitalizedGameName = capitalizeText(game)
        gameOption.textContent = `Top ${capitalizedGameName}`

        if (game_data.game_status && game_data.game_status == 'win'){
            scoreIcon.innerHTML = `<i class="fa-solid fa-crown fa-bounce" style="color: #edca1d;"></i>`
            scoreTitle.textContent = `Felicidades ${data.username}, ganaste esta partida`
            setTimeout(() => {
                scoreIcon.innerHTML = `<i class="fa-solid fa-crown fa-bounce" style="color: #edca1d;"></i>`
            }, 2000);
        }

        // si el juego es de palabras, se muestra la palabra correcta al final
        if ( game === 'wordle' || game === 'ahorcado'){
            wordTitle.style.display = 'block'
            wordContainer.style.display = 'block'
            if (game === 'wordle'){
                wordContainer.textContent = "La palabra es: "+ game_data.game_data.word
            }else{
                wordContainer.textContent = "La palabra es: "+ game_data.word
            }
            
        }

        if (game_data.game_status && game_data.game_status == 'defeat'){
            scoreIcon.innerHTML = `<i class="fa-solid fa-face-anxious-sweat fa-beat" style="color: #9c0202;"></i>`
            scoreTitle.textContent = `${data.username}, a veces se gana y otras se aprende`
            setTimeout(() => {
                scoreIcon.innerHTML = `<i class="fa-solid fa-face-anxious-sweat" style="color: #9c0202;"></i>`
            }, 2000);
        }
        
        playerScore.textContent = `Tu puntaje: ${data.player_score}` 
        
    }catch(err){
        console.log(err)
    }
    
}

// funcion auxiliar para texto capitalizado (simple estetica)
function capitalizeText(text){
    return text.charAt(0).toUpperCase() + text.slice(1)
}


// eventos para los cambios del select
rankingFilter.addEventListener('change', ()=>{
    const value = rankingFilter.value
    modal.style.display = 'flex'
    switch(value){
        case 'score':
            scoreScreen.style.display = 'block'
            rankingTable.style.display = 'none'
            break
        case 'game':
            scoreScreen.style.display = 'none'
            rankingTable.style.display = 'block'
            showModalScreen(auxInput.value, null, 'game_ranking')
            break
        case 'global':
            scoreScreen.style.display = 'none'
            rankingTable.style.display = 'block'
            showModalScreen(auxInput.value, null, 'global_ranking')
            break
    }
})

