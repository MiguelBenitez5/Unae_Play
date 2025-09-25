const modalWindow = document.querySelector('.modal')
const cards = document.querySelectorAll('.card')

const questionMark = '<i class="fa-solid fa-question" style="color: #FFD43B;"></i>'

async function play_game(id){
    try{
        const response = await fetch(`/memorygame/${id}`)
        if (!response.ok) throw new Error(`Error del servidor: ${response.status}`)
        const data = await response.json()
        console.log(data)
        const card = document.getElementById(id)
        card.style.cursor = 'auto'
        card.onclick = null

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
                // mostrar ventana modal al finalizar
                setTimeout(()=>modalWindow.style.display = 'flex', 1500)
            }
        }
        
        
        

    }catch(err){
        console.error(err)
    }
    
}

cards.forEach(card =>{
    card.onclick = () => play_game(card.id)
})



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