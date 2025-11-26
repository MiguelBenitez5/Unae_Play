const modalInfo = document.querySelector('#info_modal')
const infoCloseBtn = document.querySelector('.tos-close-btn')
const infoAcceptBtn = document.querySelector('.tos-btn')

modalInfo.addEventListener('click', (event)=>{
    if (event.target === infoCloseBtn || 
        event.target === infoAcceptBtn || 
        event.target === modalInfo){
            modalInfo.style.display = 'none'
    }
})