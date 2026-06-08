const btnMayor = document.getElementById("btn-mayor")
const btnMenor = document.getElementById("btn-menor")
const contenedor = document.getElementsByClassName("cards-resenas-full")[0]

if (btnMayor && btnMenor && contenedor) {

    btnMayor.addEventListener("click", function() {
        ordenar("mayor")
        btnMayor.classList.add("activo")
        btnMenor.classList.remove("activo")
    })

    btnMenor.addEventListener("click", function() {
        ordenar("menor")
        btnMenor.classList.add("activo")
        btnMayor.classList.remove("activo")
    })
}

function ordenar(criterio) {
    const cards = Array.from(contenedor.getElementsByClassName("card-resena"))

    cards.sort(function(a, b) {
        const estrellasA = a.getElementsByClassName("resena-estrellas")[0].innerText.split("★").length - 1
        const estrellasB = b.getElementsByClassName("resena-estrellas")[0].innerText.split("★").length - 1

        if (criterio === "mayor") {
            return estrellasB - estrellasA
        } else {
            return estrellasA - estrellasB
        }
    })

    cards.forEach(card => contenedor.appendChild(card))
}