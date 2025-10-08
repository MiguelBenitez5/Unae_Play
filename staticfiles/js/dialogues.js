const dialogueTextGlobal = document.getElementById('dialogue-text')
const charImg = document.querySelector('.char-img')
let reset_time_out = null

/**
 * Muestra un dialogo aleatorio de la categoria y juego seleccionados
 * @param {string} category La categoria del juego (inicio, final, victoria, derrota, empate)
 * @param {string} game El juego especifico
 */
async function show_dialogue(category, game, game_data = null){
    if (random_dialogue_interval || reset_time_out){
        stop_random_dialogues()
        stop_reset_time_out()
    }
    if (category === 'final' && (game === 'wordle' || game === 'ahorcado')){
        dialogueTextGlobal.style.animation = 'myDialogueAnim 0.7s ease-in 0s 1 normal forwards'
        dialogueTextGlobal.textContent = game_data.data_info
        charImg.src = get_char_img().talk_pose
        return
    }
    try{
        if (category === 'final') return
        const response = await fetch(`/getdialogue/${category}/${game}`)
        if (!response.ok) throw new Error('No se pudo obtener dialogo del servidor'+response.status)
        const data = await response.json()
        dialogueTextGlobal.style.animation = 'myDialogueAnim 0.7s ease-in 0s 1 normal forwards'
        dialogueTextGlobal.textContent = data.dialogue
        charImg.src = get_char_img().talk_pose
        // el dialogo permanece en pantalla si termina la partida
        if (category === 'victoria' || (category === 'derrota' && (game === 'wordle' || game === 'ahorcado'))){
            setTimeout(()=>show_dialogue('final',game, game_data),10000)
            return
        } 

        random_dialogue()
        if (reset_time_out) stop_reset_time_out()
        reset_time_out = setTimeout(()=>{
                reset_dialogue()
            }, 10000)

    }catch(err){
        console.log(err)
    }
    return
}


function reset_dialogue(){
    dialogueTextGlobal.style.animation = 'none'
    void dialogueTextGlobal.offsetWidth
    dialogueTextGlobal.style.animation = 'myDialogueExitAnim 0.7s ease-in 0s 1 normal forwards'
    
    dialogueTextGlobal.addEventListener('animationend', function handler(e){
        if (e.animationName === 'myDialogueExitAnim'){ 
            dialogueTextGlobal.textContent = '...'
            charImg.src = get_char_img().normal_pose
            dialogueTextGlobal.style.animation = 'myDialogueEnterAnim 0.3s ease-out forwards';
            dialogueTextGlobal.removeEventListener('animationend', handler)
        }
        
    })
    
}

// funcion exclusiva para questions
function show_dialogue_for_questions(data){
    if (random_dialogue_interval || reset_time_out){
        clearInterval(random_dialogue_interval)
        clearTimeout(reset_time_out)
    }
    dialogueTextGlobal.style.animation = 'none'
    void dialogueTextGlobal.offsetWidth
    dialogueTextGlobal.style.animation = 'myDialogueAnim 0.7s ease-in 0s 1 normal forwards'
    dialogueTextGlobal.textContent = data.question_info
    charImg.src = get_char_img().talk_pose
}

// funcion para detener los dialogos aleatorios

function stop_random_dialogues(){
    clearInterval(random_dialogue_interval)
    random_dialogue_interval = null
}
// intervalo de dialogos aleatorios
random_dialogue_interval = null

function stop_reset_time_out(){
    clearTimeout(reset_time_out)
    reset_time_out = null
}

function random_dialogue(){
    if (random_dialogue_interval){
        stop_random_dialogues()
    }
    random_dialogue_interval = setInterval(()=>{
        show_dialogue('general','general')
        .catch(error=>console.error("Error: ", error))
    }, 30000)
}

// leer el localstorage para designar
function get_char_img(){
    const userpet = localStorage.getItem('theme')
    if (userpet){
        switch(userpet){
            case "LASI":
                return {
                    normal_pose : '/static/img/carpincho-1.png',
                    talk_pose   : '/static/img/LASI_TALK.png'
                }
            case "COLONIAS":
                return {
                    normal_pose : '/static/img/leopardo.png',
                    talk_pose   : '/static/img/COLONIAS_TALK.png'
                }
            case "FACAT":
                return {
                    normal_pose : '/static/img/camaleon.png',
                    talk_pose   : '/static/img/FACAT_TALK.png'
                }
            case "FACEM":
                return {
                    normal_pose : '/static/img/tucan.png',
                    talk_pose   : '/static/img/FACEM_TALK.png'
                }
            case "FACQUF":
                return {
                    normal_pose : '/static/img/serpiente.png',
                    talk_pose   : '/static/img/FACQUF_TALK.png'
                }
            case "FACVA":
                return {
                    normal_pose : '/static/img/caballo.png',
                    talk_pose   : '/static/img/FACVA_TALK.png'
                }
            case "FCJHS":
                return {
                    normal_pose : '/static/img/buho.png',
                    talk_pose   : '/static/img/FCJHS_TALK.png'
                }
            case "ISEDE":
                return {
                    normal_pose : '/static/img/conejo.png',
                    talk_pose   : '/static/img/ISEDE_TALK.png'
                }
            default :
                return {
                    normal_pose : '/static/img/carpincho-1.png',
                    talk_pose   : '/static/img/LASI_TALK.png'
                }
        }
    }else{
        return {
            normal_pose : '/static/img/carpincho-1.png',
            talk_pose   : '/static/img/LASI_TALK.png'
        }
    }
} 