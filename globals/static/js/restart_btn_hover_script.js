const restartBtnGlobal = document.querySelector('.reset')

const resetBtn = '<i class="fa-solid fa-rotate-right" style="color: #fff; font-size: 26px;"></i>'
const resetBtnHover = '<i class="fa-solid fa-rotate-right fa-spin" style="color: #ffffff; font-size: 26px;"></i>'

// eventos para animacion del boton de reinicio
restartBtnGlobal.addEventListener('mouseenter', ()=>{
    restartBtnGlobal.innerHTML = resetBtnHover
})

restartBtnGlobal.addEventListener('mouseleave', ()=>{
    restartBtnGlobal.innerHTML = resetBtn
})