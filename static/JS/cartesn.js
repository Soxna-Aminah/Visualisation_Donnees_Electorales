let uses = document.querySelectorAll(".carteSn .use")
let divRegionInf = document.querySelector(".carteSn .divRegionInf")
let carteSn = document.querySelector(".carteSn")


function generate_content(data){

    divRegionInf.innerHTML = `
        <h2>${data.region}</h2>
        <p class="departement">
            <strong class="label-strong">Departement :</strong>
            ${
                data.departement.map((dep) => "<span> "+ dep +"</span>")
            }
        </p>
        <p>${data.commune} <strong class="label-strong">communes</strong></p>
        <p>${data.electeur} <strong class="label-strong">Electeurs</strong></p>
    `
}


for(let use of uses){

    use.addEventListener("mouseenter", async(e) => {
        e.stopPropagation()

        divRegionInf.style.visibility = 'visible'


        let element = e.target
        let elementTitle = element.getAttribute('title')

        let response = await fetch('/api/info')
        let data = await response.json()

        data = data.filter(region => region.region === elementTitle)

        generate_content(data[0])

        
    })
    
    use.addEventListener('mouseout', ()=>{
        divRegionInf.style.visibility = 'hidden'
        divRegionInf.innerText = ''
    })
    
}















// for(let use of uses){

//     use.addEventListener("mouseenter", (e) => {
//         let element = e.target
//         let elementTitle = element.getAttribute('title')

//         for(let div of divRegionInf){
//             console.log(elementTitle)
//             console.log(div.classList.contains(`${elementTitle}`))
//             if(div.classList.contains(`${elementTitle}`)){
//                 console.log("samba ndiaye")
//                 div.style.display = 'block'
//             }
//         }

//     }).addEventListener('mouseout', (e) => {

//         for(let div of divRegionInf){
//             console.log(elementTitle)
//             console.log(div.classList.contains(`${elementTitle}`))
//             if(div.classList.contains(`${elementTitle}`)){
//                 console.log("samba ndiaye")
//                 div.style.display = 'none'
//             }
//         }
//     })
    
    
// }
