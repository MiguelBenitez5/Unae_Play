const tosModal = document.querySelector('.modal-tos')
const tosAcceptBtn = document.querySelector('.tos-btn')
const tosCloseBtn = document.querySelector('.tos-close-btn')
const tosActivator = document.querySelector('.form-link')
const checkbox = document.getElementById('checkbox') 

tosActivator.addEventListener('click', ()=>{
    tosModal.style.display = 'flex'
})

tosCloseBtn.addEventListener('click', ()=>{
    tosModal.style.display = 'none'
})

tosAcceptBtn.addEventListener('click', ()=>{
    tosModal.style.display = 'none'
    checkbox.checked = true
})


