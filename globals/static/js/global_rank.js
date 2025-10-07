const sponsorLink1 = document.getElementById('sponsor-link-1')
const sponsorLink2 = document.getElementById('sponsor-link-2')

async function clickCampaign(){
    try{
        const response = await fetch('asdasda')
        if(!response.ok) throw new Error('Error en la respuesta del servidor: '+response.status)
        const data = await response.json()
            if (data){
                if(data.status === 'success'){
                    setTimeout(()=>{
                        location.reload()
                    },3000)
                }
            }
    }catch(err){
        console.log(err)
    }
}

sponsorLink1.addEventListener('click', clickCampaign)
sponsorLink2.addEventListener('click', clickCampaign)