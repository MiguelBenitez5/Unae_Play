const hour = document.getElementById('timer-h')
const min = document.getElementById('timer-min')
const dec = document.getElementById('timer-dec')
const sec = document.getElementById('timer-sec')

let h=0, m=0, d=0, s = 0

setInterval(()=>{
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