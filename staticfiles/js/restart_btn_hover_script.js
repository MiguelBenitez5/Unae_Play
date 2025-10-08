const restartBtnGlobal = document.querySelector('.reset')

const resetBtn = '<i class="fa-solid fa-rotate-right game-reset-icon" style="color: #fff;"></i>'
const resetBtnHover = '<i class="fa-solid fa-rotate-right fa-spin game-reset-icon" style="color: #ffffff;"></i>'

// eventos para animacion del boton de reinicio
if(restartBtnGlobal){
    restartBtnGlobal.addEventListener('mouseenter', ()=>{
        restartBtnGlobal.innerHTML = resetBtnHover
    })

    restartBtnGlobal.addEventListener('mouseleave', ()=>{
        restartBtnGlobal.innerHTML = resetBtn
    })
}