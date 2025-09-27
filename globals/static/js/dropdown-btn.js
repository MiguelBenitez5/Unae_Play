const menuBtn = document.querySelector(".menu-btn");
const dropdownContent = document.querySelector(".dropdown-content");

// Abrir/cerrar menú principal
menuBtn.addEventListener("click", () => {
    dropdownContent.style.display = dropdownContent.style.display === "flex" ? "none" : "flex";
});

// Función para mostrar/ocultar submenús, cerrando los demás
function toggleSubmenu(id) {
    const submenus = document.querySelectorAll(".submenu");
    submenus.forEach(sub => {
        if (sub.id !== id) {
            sub.style.display = "none"; // cerrar los demás
        }
    });

    const submenu = document.getElementById(id);
    submenu.style.display = submenu.style.display === "flex" ? "none" : "flex";
}

// Opcional: cerrar dropdown si se hace clic fuera
document.addEventListener("click", (e) => {
    if (!dropdownContent.contains(e.target) && e.target !== menuBtn) {
        dropdownContent.style.display = "none";
        document.querySelectorAll(".submenu").forEach(sub => sub.style.display = "none");
    }
});



const audio = document.getElementById("bg-music");
const toggle = document.getElementById("music-toggle");
const volumeSlider = document.getElementById("volume-slider");
const msg = document.getElementById("msg");

let isPlaying = true; // empieza apagado

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
    audio.volume = volumeSlider.value / 100;
});

document.addEventListener("DOMContentLoaded", () => {
  const audio = document.getElementById("bg-music");
  audio.volume = 0.5; // volumen inicial
  // lo dejamos muteado hasta que el usuario haga una acción
  document.addEventListener("click", () => {
    if (audio.muted) {
      audio.muted = false; // 🔊 se desmutea al primer clic
    }
  }, { once: true });
});