function confirmar_reintegracion(){
    let respuesta = confirm("¿Esta seguro de reintegrar esta instancia?")
    if(respuesta){
        return true;
    }else{
        event.preventDefault();
        return false;
    }
}