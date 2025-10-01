const modal = document.getElementById('rankingModal');
const rankingFilter = document.getElementById('rankingFilter');
const rankingTable = document.getElementById('rankingTable').querySelector('tbody');
const closeBtn = document.querySelector('.close-btn')
const modalContent = document.querySelector('.modal-content')


// Cerrar modal
closeBtn.addEventListener('click', () => {
    modal.style.animation = 'none'
    void modal.offsetWidth
    modal.style.animation = 'myModalCloseAnim 1s ease-out 0s 1 normal forwards'                                                                                                                               
    modal.addEventListener('animationend', function handler(e){
        if(e.animationName === 'myModalCloseAnim'){
            modal.style.display = 'none';
            modal.removeEventListener('animationend', handler)
        }
    })
    
});

// Cerrar modal haciendo click fuera del contenido
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});

function showModalScreen(){
    
    modal.style.display = 'flex'
}

