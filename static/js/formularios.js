function cambio(){
    let tamanio = document.getElementsByClassName('formulario-movimiento')

    for(i = 1; i<=tamanio.length ; i++){
        formularios = document.getElementById(i);
        formularios.style.display = 'none';
    }

    let eleccion = document.getElementById('movimiento');
    let valor = eleccion.value;

    if(valor != ""){
        formulario = document.getElementById(valor);
        formulario.style.display = 'block';
    }
}

function formu(){
    let formulario = document.getElementById('existente_producto');
    formulario.style.display = 'none';
    let formulario_nuevo = document.getElementById('nuevo_producto');
    formulario_nuevo.style.display = 'none';
    let eleccion = document.getElementById('tipo');
    let resultado = eleccion.value;

    if(resultado == "Existente"){
        let cambiar = document.getElementById('existente_producto')
        cambiar.style.display = 'block';
    } else if(resultado == "Nuevo"){
        let cambiar = document.getElementById('nuevo_producto')
        cambiar.style.display = 'block';
    }
}