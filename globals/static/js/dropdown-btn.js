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
    if (isPlaying) {
        audio.pause();
        msg.textContent = "Off";
    } else {
        audio.play()
        .then(() => {
            audio.muted = false;
            msg.textContent = "On";
        }).catch(err => {
            console.log("Autoplay bloqueado:", err);
        });
    }
    isPlaying = !isPlaying;
});

volumeSlider.addEventListener("input", () => {
    if (volumeSlider <= 50) {
        audio.volume = volumeSlider.value / 200;
    } else {
        audio.volume = volumeSlider.value / 100;
    }
});

document.addEventListener("DOMContentLoaded", () => {
    const audio = document.getElementById("bg-music");
    audio.volume = 0.5; 
    document.addEventListener("click", () => {
        if (audio.muted) {
        audio.muted = false; 
        }
    }, { once: true });
});