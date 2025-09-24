const modal = document.getElementById('rankingModal');
const rankingFilter = document.getElementById('rankingFilter');
const rankingTable = document.getElementById('rankingTable').querySelector('tbody');
const closeBtn = document.querySelector('.close-btn')


// Cerrar modal
closeBtn.addEventListener('click', () => {
    modal.style.display = 'none';
});

// Cerrar modal haciendo click fuera del contenido
window.addEventListener('click', (e) => {
    if (e.target === modal) {
        modal.style.display = 'none';
    }
});