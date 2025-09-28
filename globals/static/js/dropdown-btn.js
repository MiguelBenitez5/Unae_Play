// ========================
// ELEMENTOS DEL DOM
// ========================
const menuBtn = document.querySelector(".menu-btn");
const dropdownContent = document.querySelector(".dropdown-content");
const audio = document.getElementById("bg-music");
const toggle = document.getElementById("music-toggle");
const volumeSlider = document.getElementById("volume-slider");
const msg = document.getElementById("msg");

// ========================
// ESTADOS
// ========================
let isPlaying = true;
let audioUnlocked = false;

// ========================
// FUNCIONES
// ========================

// Desbloqueo de audio (evento trampa)
function unlockAudio() {
    if (audioUnlocked) return;
    audio.muted = false;
    audio.play().then(() => {
        console.log("Audio desbloqueado");
        audioUnlocked = true;
        if (!isPlaying) audio.pause();
    }).catch(err => console.log("Error al desbloquear audio:", err));
}

// Resalta la mascota activa
function setActivePet(petName) {
    const items = document.querySelectorAll(".submenu-item");
    items.forEach(item => {
        const span = item.querySelector("span");
        if (span && span.textContent.trim() === petName) {
            item.classList.add("active-pet");
        } else {
            item.classList.remove("active-pet");
        }
    });
}

// Toggle submenú
function toggleSubmenu(id) {
    unlockAudio();
    const submenus = document.querySelectorAll(".submenu");
    submenus.forEach(sub => {
        if (sub.id !== id) sub.style.display = "none";
    });
    const submenu = document.getElementById(id);
    submenu.style.display = submenu.style.display === "flex" ? "none" : "flex";
}

// ========================
// INICIALIZACIÓN AL CARGAR
// ========================
document.addEventListener("DOMContentLoaded", () => {

    // --- Música ON/OFF ---
    const savedState = localStorage.getItem("musicState");
    if (savedState === "off") {
        audio.pause();
        msg.textContent = "Off";
        isPlaying = false;
    } else {
        audio.play().catch(err => console.log("Autoplay bloqueado:", err));
        msg.textContent = "On";
        isPlaying = true;
    }

    // --- Volumen ---
    const savedVolume = localStorage.getItem("musicVolume");
    if (savedVolume !== null) {
        audio.volume = parseFloat(savedVolume);
        volumeSlider.value = audio.volume * 100;
    } else {
        audio.volume = 0.5;
        volumeSlider.value = 50;
    }

    // --- Mascota ---
    let savedPet = localStorage.getItem("selectedPet");
    if (!savedPet) {
        savedPet = "LASI";
        localStorage.setItem("selectedPet", savedPet);
    }
    setActivePet(savedPet);

    // --- Eventos trampa para desbloqueo de audio ---
    const events = ["mousemove", "wheel", "keydown", "touchstart", "click"];
    events.forEach(ev => document.addEventListener(ev, unlockAudio, { once: true }));

    const interactiveElements = document.querySelectorAll('a, button, .nav-link, .game-card, .menu-btn');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', unlockAudio, { once: true });
        el.addEventListener('focus', unlockAudio, { once: true });
    });

    window.addEventListener('focus', unlockAudio, { once: true });
});

// ========================
// INTERACCIONES DE USUARIO
// ========================

// Menú principal
menuBtn.addEventListener("click", () => {
    unlockAudio();
    dropdownContent.style.display = dropdownContent.style.display === "flex" ? "none" : "flex";
});

// Toggle música
toggle.addEventListener("click", () => {
    unlockAudio();
    if (isPlaying) {
        audio.pause();
        msg.textContent = "Off";
        localStorage.setItem("musicState", "off");
    } else {
        audio.play().then(() => {
            audio.muted = false;
            msg.textContent = "On";
            localStorage.setItem("musicState", "on");
        }).catch(err => console.log("Autoplay bloqueado:", err));
    }
    isPlaying = !isPlaying;
});

// Control de volumen
volumeSlider.addEventListener("input", () => {
    unlockAudio();
    const volume = volumeSlider.value <= 50 ? volumeSlider.value / 200 : volumeSlider.value / 100;
    audio.volume = volume;
    localStorage.setItem("musicVolume", volume);
});

// Cerrar submenús al hacer click fuera
document.addEventListener("click", (e) => {
    unlockAudio();
    if (!dropdownContent.contains(e.target) && e.target !== menuBtn) {
        dropdownContent.style.display = "none";
        document.querySelectorAll(".submenu").forEach(sub => sub.style.display = "none");
    }
});

// ========================
// ELECCIÓN DE MASCOTA
// ========================
document.querySelectorAll(".submenu-item").forEach(item => {
    item.addEventListener("click", () => {
        const span = item.querySelector("span");
        if (!span) return; // Ignora items que no sean mascotas
        const petName = span.textContent.trim();
        localStorage.setItem("selectedPet", petName);
        setActivePet(petName);
        const submenu = item.closest(".submenu");
        if (submenu) submenu.style.display = "none"; // cerrar submenú
        console.log("Mascota elegida:", petName);
    });
});

// ========================
// HOVER y Scroll
// ========================
document.querySelectorAll('.nav-link, .game-card, .link').forEach(el => {
    el.addEventListener('mouseenter', unlockAudio, { once: true });
});

let scrollAttempts = 0;
window.addEventListener('scroll', () => {
    if (scrollAttempts < 3) {
        unlockAudio();
        scrollAttempts++;
    }
});

// Timeout seguridad
setTimeout(() => {
    if (!audioUnlocked) unlockAudio();
}, 5000);

// Formularios y arrastre
document.querySelectorAll('input, select, textarea').forEach(el => {
    el.addEventListener('focus', unlockAudio, { once: true });
    el.addEventListener('input', unlockAudio, { once: true });
});
document.addEventListener('dragstart', unlockAudio, { once: true });
window.addEventListener('load', unlockAudio, { once: true });
window.addEventListener('resize', unlockAudio, { once: true });
