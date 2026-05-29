function mostrar_lista(){
    let lista = document.getElementById("lista");
    
    event.stopPropagation();
    lista.style.display = "block";
}

function ocultar_lista(){
    let lista = document.getElementById("lista");
    lista.style.display = "none";
}