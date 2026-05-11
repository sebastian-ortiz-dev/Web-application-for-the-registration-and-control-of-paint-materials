function editar(){
    let respuesta = confirm("¿Esta seguro de modificar esta instancia?")
    if(respuesta){
        return true;
    }else{
        event.preventDefault();
        return false;
    }
}