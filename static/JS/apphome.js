let button=document.getElementById("charger")
let h3=document.querySelector("h3")
let p=document.querySelector(".message")

button.addEventListener("click",e=>{
    fetch("/postall")
    // .then(function (reponse){
    // //    let verif=reponse.statusText
    // //    console.log(verif);
    // //    if(verif=="OK"){
    // //      h3.style.display="none"
    // //      p.style.display="none"
    // //      button.style.display="none"

    //    }

    // })
    
})

