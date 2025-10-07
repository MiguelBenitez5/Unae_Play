const gameScreen = document.querySelector('.game-all-content')
const loadingScreen = document.querySelector('.loading-screen')
const loadingBtn = document.querySelector('.loading-button')
const selectGame = document.querySelector('#juegos')
const loadingIcon = document.querySelector('.loading-icon')
const loadingText = document.querySelector('.loading-text')
const gameMusic = document.querySelector('audio')

const successIcon = '<i class="fa-solid fa-check" style="color: #e6e9f0;"></i>'
const loadIcon = '<i class="fa-solid fa-spinner fa-spin-pulse" style="color: #e6e9f0;">'
const preloadedImages = {}
const preloadedAudios = {}

// precargar imagenes
function preloadImage(path){
    return new Promise((resolve)=>{
        if (preloadedImages[path]){
            return resolve(preloadedImages[path])
        }

        const img = new Image()
        img.src = path
        img.onload = ()=>{
            preloadedImages[path] = img
            resolve(img)
        }
    })
}

// precargar musica
function preloadAudio(path){
    return new Promise((resolve)=>{
        if (preloadedAudios[path]){
            return resolve(preloadedAudios[path])
        }

        const audio = new Audio()
        audio.src = path
        audio.oncanplaythrough = ()=>{
            preloadedAudios[path] = audio
            resolve(audio)
        }
    })
}


// carga de archivos
async function preloadAll() {
  const imagePaths = ['/static/img/buho.png', '/static/img/caballo.png',
                      '/static/img/camaleon.png', '/static/img/carpincho-1.png', 
                       '/static/img/COLONIAS_TALK.png','/static/img/conejo.png',
                       '/static/img/FACAT_TALK.png','/static/img/FACEM_TALK.png',
                       '/static/img/FACQUF_TALK.png','/static/img/FACVA_TALK.png',
                       '/static/img/FCJHS_TALK.png','/static/img/ISEDE_TALK.png',
                       '/static/img/LASI_TALK.png','/static/img/leopardo.png',
                       '/static/img/serpiente.png','/static/img/tucan.png',
                       '/static/img/imagenEjemplo1.jpg'
                    ]
  const audioPaths = ['/static/music/adivinarnumero.mp3', '/static/music/ahorcado.wav',
                      '/static/music/buscaminas.wav', '/static/music/landing_page.wav',
                      '/static/music/memorygame.wav', '/static/music/piedrapapeltijera.wav',
                      '/static/music/questions.mp3', '/static/music/tateti.wav',
                      '/static/music/wordle.wav',
                    ]

  const promises = [
    ...imagePaths.map(preloadImage),
    ...audioPaths.map(preloadAudio)
  ]

  await Promise.all(promises)
  console.log('✅ Todos los recursos cargados')
}

preloadAll()

// se muestra la pantalla de carga por 5 segundos
function showLoadingScreen(){
    loadingScreen.style.display = 'block'
    gameScreen.style.display = 'none'
    loadingText.textContent = 'Cargando juego'
    loadingIcon.innerHTML = loadIcon
    loadingBtn.style.display = 'none'
    setTimeout(()=>{
        loadingText.textContent = 'Juego completamente cargado'
        loadingIcon.innerHTML = successIcon
        loadingBtn.style.display = 'inline'
    }, 5000)
}

window.onload = showLoadingScreen

// evento para el boton de juego cargado
loadingBtn.addEventListener('click', ()=>{
    // aqui se debe verificar desde el localhost para comprobar si reproducir musica y que volumen
    loadingScreen.style.display = 'none'
    gameScreen.style.display = 'block'
})
