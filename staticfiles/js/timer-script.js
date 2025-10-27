const hour = document.getElementById('timer-h')
const min = document.getElementById('timer-min')
const dec = document.getElementById('timer-dec')
const sec = document.getElementById('timer-sec')

let h=0, m=0, d=0, s = 0
let timer_interval = null

/**
 * Funcion para utilizarla en los juegos que necesiten un contador
 */
function startCountingTimer(){
    if(timer_interval){
        return
    }
    timer_interval = setInterval(()=>{
        s++
        if(s === 10){
            d++
            s=0
        }
        if(d === 6){
            m++
            d=0
        }
        if(m === 6){
            h++
            m=0    
        }

        sec.textContent = s
        dec.textContent = d
        min.textContent = m
        hour.textContent = h
    }, 1000)
}


/**
 * Para el contador
 */
function stopCountingTimer(){
    clearInterval(timer_interval)
    timer_interval = null
}

/**
 * Reinicia en 0 el contador
 */
function resetCountingTimer(){
    clearInterval(timer_interval)
    timer_interval = null
    h = 0, m=0, d=0, s = 0
    sec.textContent = s
    dec.textContent = d
    min.textContent = m
    hour.textContent = h
}