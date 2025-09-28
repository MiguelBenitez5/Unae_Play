const dialogueTextGlobal = document.getElementById('dialogue-text')

/**
 * Muestra un dialogo aleatorio de la categoria y juego seleccionados
 * @param {string} category La categoria del juego (Inicio, Final, Victoria, Derrota)
 * @param {string} game El juego especifico
 */
async function show_dialog(category, game){
    return
}


function reset_dialogue(){
    return
}

// intervalo de dialogos aleatorios
random_dialog_interval = null

function random_dialog(){
    random_dialog_interval = setInterval(()=>{
        fetch('/getdialogue/general/general')
        .then(response => response.json())
        .then(data =>{
            console.log(data)
            dialogueTextGlobal.textContent = data.dialogue
        })
        .catch(error=>console.error("Error: ", error))
    }, 10000)
}

random_dialog()

// leer el localstorage para designar
function get_char_img(){
    const ussersettings = localStorage.getItem('usersettings')
    if (ussersettings){
        userpet = JSON.parse(ussersettings)
        switch(userpet.pet){
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
        }
    }else{
        return {
            normal_pose : '/static/img/carpincho-1.png',
            talk_pose   : '/static/img/LASI_TALK.png'
        }
    }
} 