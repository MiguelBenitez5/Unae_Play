//el juego se reinicia cada vez que carga la pagina
window.onload = function(){
    fetch('http://127.0.0.1:8000/tateti/action/restart')
    .then(response => response.json())
    .then(data =>{
        console.log(data)
    })
}

const cells = document.querySelectorAll(".cell")
//parrafo de prueba, borrar luego
const parrafo = document.querySelector('.dialog-text')
//parrafo de prueba, borrar luego
const level = document.querySelector('.level')

const circle = '<i class="fa-regular fa-circle" style="color: #cb151e;"></i>'
const xmark = '<i class="fa-solid fa-xmark" style="color: #0c7b0a;"></i>'

function cleanBoard(){
    cells.forEach(cell =>{
        cell.innerHTML = ''
        cell.classList.add('activo')
    })
}

cells.forEach(cell =>{
    cell.addEventListener("click", function(){
        fetch(`http://127.0.0.1:8000/tateti/${this.id}`)
        .then(response => response.json())
        .then(data =>{
            if (data.status == 'error') {
                console.log(data.status)
                return
            }
            level.textContent = data.level
            this.innerHTML = circle
            this.classList.remove('activo')
            
            if (data.hard_machine_move){
                cleanBoard()
                parrafo.textContent = 'Ahora empiezo yo'
                cells.forEach(c =>{
                    if (c.id == data.hard_machine_move){
                        c.innerHTML = xmark
                        return
                    }
                })
            }

            if(data.game_status == 'win_game'){
                parrafo.textContent = 'Felicidades, ganaste la partida'
                setTimeout(2000)
                parrafo.textContent = 'Tu puntaje es: '+data.score
                cleanBoard()
                return
            }
            if(data.game_status == 'win'){
                cleanBoard()
                if(data.level == 'medium'){
                    parrafo.textContent = 'Me ganaste, pero eso solo fue el prinicipio. Ganame ahora'
                }else{
                    parrafo.textContent = 'Esta vez juego yo primero'
                    
                }
                return
            }
            if(data.game_status == 'draw'){
                cleanBoard()
                parrafo.textContent = 'Guau, nadie gano, sigue intentandolo.'
                setTimeout(2000)
                parrafo.textContent = 'Tu puntaje es '+ response.score
                return                
            }
            if(data.game_status == 'defeat'){
                cleanBoard()
                parrafo.textContent = 'Gane esta vez, nadie puede conmigo'
                setTimeout(2000)
                parrafo.textContent = 'Tu puntaje es '+ response.score
                return
            }

            //turno de la maquina
            machineCell = data.machine_move
            cells.forEach(c =>{
                if(c.id == data.machine_move){
                    c.innerHTML = '<i class="fa-solid fa-xmark" style="color: #3f2;"></i>'
                    c.classList.remove('activo')
                    return
                }
            })
            
        })
    })
})