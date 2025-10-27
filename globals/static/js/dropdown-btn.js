const menuBtn = document.querySelector(".menu-btn");
const dropdownContent = document.querySelector(".dropdown-content");
const audio = document.getElementById("bg-music");
const toggle = document.getElementById("music-toggle");
const volumeSlider = document.getElementById("volume-slider");
const msg = document.getElementById("msg");

let isPlaying = true; 


menuBtn.addEventListener("click", () => {
    dropdownContent.style.display = dropdownContent.style.display === "flex" ? "none" : "flex";
});

function toggleSubmenu(id) {
    const submenus = document.querySelectorAll(".submenu");
    submenus.forEach(sub => {
        if (sub.id !== id) {
            sub.style.display = "none"; 
        }
    });
    const submenu = document.getElementById(id);
    submenu.style.display = submenu.style.display === "flex" ? "none" : "flex";
}

document.addEventListener("click", (e) => {
    if (!dropdownContent.contains(e.target) && e.target !== menuBtn) {
        dropdownContent.style.display = "none";
        document.querySelectorAll(".submenu").forEach(sub => sub.style.display = "none");
    }
});

toggle.addEventListener("click", () => {
    const music_option = localStorage.getItem('music_state')
    if (music_option == 'on') {
        audio.pause();
        msg.textContent = "Off";
        localStorage.setItem('music_state', 'off')
    } else {
        audio.play()
        .then(() => {
            audio.muted = false;
            msg.textContent = "On";
            localStorage.setItem('music_state', 'on')
        }).catch(err => {
            console.log("Autoplay bloqueado:", err);
        });
    }
});

volumeSlider.addEventListener("input", () => {
    if (volumeSlider <= 50) {
        audio.volume = volumeSlider.value / 200;
    } else {
        audio.volume = volumeSlider.value / 100;
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const music_option = localStorage.getItem('music_state')
    if (!music_option){
        localStorage.setItem('music_state', 'on')
    }
    else if (music_option === 'off'){
        msg.textContent = 'Off'
        return
    }

    audio.volume = 0.5; 
    document.addEventListener("click", () => {
        audio.play()
        .then(()=>{
            audio.muted = false
            }
        )
    }, { once: true });
    document.addEventListener('touchstart', () => {
        audio.play()
        .then(()=>{
            audio.muted = false
            }
        )
    }, { once: true });
    document.addEventListener('keydown', () => {
        audio.play()
        .then(()=>{
            audio.muted = false
            }
        )
    }, { once: true });
});

const pets = document.getElementById('mascotas')

pets.addEventListener('click', (e)=>{
    const petbox = e.target.closest('.submenu-item')
    if (petbox){
        localStorage.setItem('theme', petbox.id)
        toggleSubmenu('mascotas')
    }
})