//el juego se reinicia cada vez que carga la pagina
window.onload = function(){
    fetch('localhost:8000/tateti/restart')
    .then(response => response.json())
    .then(data =>{
        console.log(data)
    })
}

const cells = document.querySelectorAll(".celda")
//parrafo de prueba, borrar luego
const parrafo = document.querySelector('.borrar-despues')
//parrafo de prueba, borrar luego
const level = document.querySelector('.level')

function cleanBoard(){
    cells.forEach(cell =>{
        cell.innerHTML = ''
        cell.classList.add('activo')
    })
}

cells.forEach(cell =>{
    cell.addEventListener("click", function(){
        fetch(`localhost:8000/tateti/${this.id}`)
        .then(response => response.json())
        .then(data =>{
            if (data.status == 'error') {
                console.log(data.status)
                return
            }
            level.textContent = data.level
            this.innerHTML = '<i class="fa-solid fa-xmark" style="color: #c60c0c;"></i>'
            this.classList.remove('activo')
            if(data.game_status == 'win_game'){
                parrafo.textContent = 'Felicidades, ganaste la partida'
                cleanBoard()
                return
            }
            if(data.game_status == 'win'){
                cleanBoard()
                if(data.level == 'medium'){
                    parrafo.textContent = 'Me ganaste, pero eso solo fue el prinicipio. Ganame ahora'
                }else {
                    parrafo.textContent = 'No me esperaba que me ganes, ahora te mostratre mi verdadero poder'
                }
                return
            }
            if(data.game_status == 'draw'){
                cleanBoard()
                parrafo.textContent = 'Guau, nadie gano, sigue intentandolo.'
                return                
            }
            if(data.game_status == 'defeat'){
                cleanBoard()
                parrafo.textContent = 'Gane esta vez, nadie puede conmigo'
                return
            }
            
        })
    })
})