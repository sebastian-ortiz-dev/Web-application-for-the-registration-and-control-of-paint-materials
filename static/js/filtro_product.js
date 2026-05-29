var idtimeout = '';
var lista_string = document.getElementById('json').textContent; 
var lista = JSON.parse(lista_string);

function llamada(){
    clearTimeout(idtimeout);
    objetive = document.getElementById('cabezero').value
    idtimeout = setTimeout(() => {
        objetivo(objetive.toLowerCase())
    }, 500);
}

function objetivo(puntero){
    var resultado = lista.filter(value => value[1].toLowerCase().includes(puntero));
    var index = 0;
    var size = resultado.length;
    var no_found = document.getElementById("no_found");
    for(i = 0; i<lista.length; i++){
        var element = document.getElementById(lista[i][0]);
        if(size > 0){
            console.log(no_found.classList == 'flex')
            
            if(no_found.classList == 'flex'){
                no_found.classList.remove('flex');
                no_found.classList.add('hidden');
            }

            if(resultado[index][0] == lista[i][0] &&  index < size){
                element.classList.remove('hidden');
                element.classList.add('flex');
                index++;
            }else{
                element.classList.remove('flex');
                element.classList.add('hidden');
            }
        }else{
            element.classList.remove('flex');
            element.classList.add('hidden');
            no_found.classList.remove('hidden');
            no_found.classList.add('flex');
        }
    }
}

function ponerTexto(id){
    var select = '[id="' + id + '"]';
    var place = document.getElementById('cabezero');
    var result_hidden = document.getElementById('valor_id');
    var father = document.querySelector(select)
    var sons = father.querySelectorAll('p')
    place.value = sons[1].textContent;
    result_hidden.value = id;
}
