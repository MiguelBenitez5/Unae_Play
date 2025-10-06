const timer = document.querySelector('.timer')
const level = document.querySelector('.level')
const question_count = document.querySelector('.question-count')
const percent = document.querySelector('.percent')
const answers = document.querySelectorAll('.answer')
const next_btn = document.querySelector('.next-btn')
const giveup_btn = document.querySelector('.giveup-btn')
const reload_btn = document.querySelector('.reload-btn')
const question = document.querySelector('.question')
const modal_window = document.querySelector('.modal')
const dialogText = document.querySelector('.dialogue-text')

timer_interval = null

const timer_default_color = '#333'
const timer_warning_color = '#f20'

/***
 * Obtener el CSFR token para enviar datos por post
 */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie("csrftoken");

window.onload =  ()=>{
    first_events_for_answers()
    show_dialogue('inicio', 'questions')
}

// se obtiene una nueva pregunta y se muestra en pantalla
async function new_question(){ 
    show_dialogue('siguiente', 'questions')
    repaint_answers()
    add_events_for_answers()
    show_give_up_button()
    try{
        const response = await fetch('/questions/action/request')
        if (!response.ok) throw new Error("Error en la respuesta del servidor: "+response.status)
        const data = await response.json()
        console.log(data)
        // comenzar el temporizador
        startCounting(data.level)
        // mostrar nivel actual
        level.textContent = get_level(data.level)
        // mostrar cantidad de preguntas respondidas
        question_count.textContent = `${(data.tries)+1}/15`
        // mostrar la pregunta
        question.textContent = data.question
        // mostrar opciones de respuesta
        paint_answers(data.answers)
    }catch(err){
        console.log(err)
    }

}

function paint_answers(data){
    for(let i =0; i < 4; i++){
        const answer = document.getElementById(i)
        answer.textContent = data[i]
    }
}

function repaint_answers(){
    answers.forEach(answer=> answer.className = 'answer active')
}

async function answer_question(answer) {
    // se envia la respuesta del jugador por metodo POST
    const formData = new FormData()
    formData.append('answer',answer)
    try{
        const response = await fetch(`/questions/answer`, {
            method : 'POST',
            headers : {
                "X-CSRFToken" : csrftoken
            },
            body   : formData
        })
        if (!response.ok) throw new Error("Error en la respuesta del servidor: "+response.status)
        const data = await response.json()
        console.log(data)
        if (data.percent){
            percent.textContent = `${data.percent} %`
            if (data.percent >= 60){
                percent.style.color = '#4e2'
            }
        }
        if (data.game_status){
            if (data.game_status == 'win'){
                // lugar para dialogo final de victoria
                showModalScreen('questions',data)
                show_restart_button()
                return data
            }else{
                // dialogos de derrota
                showModalScreen('questions', data)
                show_restart_button()
                return data
            }
        }
        // mostrar dialogo de la descripcion de la pregunta
        show_dialogue_for_questions(data)
        show_next_button()
        return data

    }catch(err){
        console.log(err)
    }
}

async function restart_game() {
    try {
        const response = await fetch('/questions/action/restart')
        if (!response.ok) throw new Error("Error en la respuesta del servidor: "+response.status)
        const data = await response.json()
        console.log(data)
    } catch (error) {
        
    }
}

function run_timer(start_time){
    timer.style.color = timer_default_color
    timer_count = start_time
    timer_interval = setInterval(()=>{
        timer_count--
        timer.textContent = timer_count

        timer.style.animation = 'none';
        timer.offsetHeight; // fuerza reflow
        timer.style.animation = 'timerAnim 0.6s ease 0s 1 normal forwards';
        if (timer_count <= 0){
            clearInterval(timer_interval)
            answer_question('out_of_time')
            remove_events_from_answers()
        }
        if (timer_count <= 5){
            timer.style.color = timer_warning_color
        }

    },1000)
}


function startCounting(level){
    switch(level){
        case 'easy':
            run_timer(60)
            break
        case 'medium':
            run_timer(30)
            break
        case 'hard':
            run_timer(15)
            break
    }
}

function stopCounting(){
    clearInterval(timer_interval)
}

function show_next_button(){
    next_btn.classList.remove('hidden')
    giveup_btn.classList.add('hidden')
    reload_btn.classList.add('hidden')
}

function show_give_up_button(){
    next_btn.classList.add('hidden')
    giveup_btn.classList.remove('hidden')
    reload_btn.classList.add('hidden')
}

function show_restart_button(){
    next_btn.classList.add('hidden')
    giveup_btn.classList.add('hidden')
    reload_btn.classList.remove('hidden')
}

function show_modal(){
    setTimeout(()=>{
        modal_window.style.display = 'flex'
    }, 1500)
}

function get_level(level){
    switch(level){
        case "easy":
            return 'Fácil'
        case "medium":
            return 'Normal'
        case "hard":
            return 'Difícil'
    }
}

// eventos
function add_events_for_answers(){
    answers.forEach(answer=>{
        answer.removeEventListener('click', new_question)
        answer.onclick = async () => {
            stopCounting()
            remove_events_from_answers()
            show_next_button()
            const response = await answer_question(answer.children[1].textContent)
            if (response.status === 'correct'){
                answer.classList.add('correct')
            }else{
                answer.classList.add('incorrect')
                answers.forEach(answer=>{
                    if(answer.children[1].textContent === response.correct_option){
                        answer.classList.add('correct')
                    }
                })
            }
            if (response.game_status){
                if (response.game_status === 'end'){
                    show_restart_button()
                    return
                }
            }
        }
        answer.classList.add('active')
    })
}

function remove_events_from_answers(){
    answers.forEach(answer=>{
        answer.onclick = null
        answer.classList.remove('active')
    })
}

function first_events_for_answers(){
    answers.forEach(answer=>{
        answer.addEventListener('click', new_question)
    })
}

next_btn.addEventListener('click', new_question)

reload_btn.addEventListener('click', ()=> location.reload())
