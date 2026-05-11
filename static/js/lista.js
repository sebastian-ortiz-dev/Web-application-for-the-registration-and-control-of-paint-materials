function mostrar_lista(){
    let lista = document.getElementById("lista");
    let flecha = document.getElementById("flecha");

    event.stopPropagation()
    if(lista.style.display == "none"){
        flecha.classList.add('-rotate-92');
        lista.style.display = "block";
    }else{
        flecha.classList.remove("-rotate-92");
        lista.style.display = "none";
    }
}

function ocultar_lista(){
    let lista = document.getElementById("lista");

    if(lista.style.display == "block"){
        flecha.classList.remove("-rotate-92");
        lista.style.display = "none";
    }
}