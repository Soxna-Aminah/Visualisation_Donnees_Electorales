let uses = document.querySelectorAll(".carteSn .use")
let carteSn = document.querySelector(".carteSn")


for(let use of uses){

    let div = document.createElement('div')
    let p = document.createElement('p')

    div.setAttribute('class', 'divInfos')

    use.addEventListener("mouseenter", (e) => {

        p.innerText = 'mafé'

        div.append(p)
        carteSn.prepend(div)

    })
    
    
}
