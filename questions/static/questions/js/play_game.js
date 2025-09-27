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

const timer_default_color = '#333'
const timer_warning_color = '#f20'


let difficulty = 'easy'
let timer_count = 60
let level_display = 'Fácil'
let percent_display = '0 %'
let questions_count = 1
let question_count_display = `${questions_count}/15`
let timer_interval = null

let tries = 1


window.onload =  first_events_for_answers

async function new_question(){
    repaint_answers()
    startCounting(difficulty)
    add_events_for_answers()
    show_give_up_button()
    question_count.textContent = question_count_display
    level.textContent = level_display
    percent.textContent = percent_display
    try{
        const response = await fetch('/questions/action/request')
        if (!response.ok) throw new Error("Error en la respuesta del servidor: "+response.status)
        const data = await response.json()
        console.log(data)
        question.textContent = data.question
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
    try{
        const response = await fetch(`/questions/${answer}`)
        if (!response.ok) throw new Error("Error en la respuesta del servidor: "+response.status)
        const data = await response.json()
        console.log(data)
        tries = data.tries+1
        difficulty = data.level
        level_display = get_level()
        questions_count++
        percent_display = `${data.percent} %`

        if (data.game_status){
            if (data.game_status == 'end'){
                show_modal()
                // lugar para dialogos
            }
        }

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
            // lugar para dialogo
            remove_events_from_answers()
            if (tries >= 15){ 
                show_restart_button()
                show_modal()
            }
            else show_next_button()
            return
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

async function answer_question_handler(event){
    const response = await answer_question(event.currentTarget.children[1].textContent)
    if (response.status === 'correct'){
        event.target.classList.add('correct')
    }else{
        event.target.classList.add('incorrect')
        answers.forEach(answer=>{
            if(answer.children[1].textContent === response.correct_option){
                answer.classList.add('correct')
            }
        })
    }
    remove_events_from_answers()
    show_next_button()
}

function get_level(){
    switch(difficulty){
        case "easy":
            level_display = 'Fácil'
            break
        case "medium":
            level_display = 'Normal'
            break
        case "hard":
            level_display = 'Difícil'
            break
    }
}

// eventos
function add_events_for_answers(){
    answers.forEach(answer=>{
        answer.removeEventListener('click', new_question)
        answer.onclick = async () => {
            stopCounting()
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
            remove_events_from_answers()
            show_next_button()
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
