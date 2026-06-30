function mostrar_lista(){
    let lista = document.querySelectorAll("[name=lista]");
    event.stopPropagation();
    lista.forEach((objeto) => {
        objeto.style.display = "block";
    });
}

function ocultar_lista(){
    let lista = document.querySelectorAll("[name=lista]");
    lista.forEach((objeto) => {
        objeto.style.display = "none";
    });
}