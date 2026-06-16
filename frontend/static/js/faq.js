const items = document.getElementsByClassName("faq-item")
for(let i = 0; i < items.length; i++) {
    const boton = items[i].getElementsByClassName("faq-pregunta")[0]
    const respuesta = items[i].getElementsByClassName("faq-respuesta")[0]
    const icono = items[i].getElementsByClassName("faq-icono")[0]
    boton.addEventListener("click", function() {
        const estaAbierto = respuesta.style.display === "block"

        for(let j = 0; j < items.length; j++) {
            items[j].getElementsByClassName("faq-respuesta")[0].style.display = "none"
            items[j].getElementsByClassName("faq-icono")[0].innerText = "+"
        }
        if(!estaAbierto) {
            respuesta.style.display = "block"
            icono.innerText = "-"
        }
    })
}