var idtimeout = '';
var lista_string = document.getElementById('json').textContent; 
var lista = JSON.parse(lista_string);

function llamada(number){
    clearTimeout(idtimeout);
    var cabezero = 0

    if(number == 1){
        objetive = document.getElementById('cabezero').value;
        cabezero = 1
    }else if(number == 2){
        objetive = document.getElementById('cabezero-2').value;
        cabezero = 2
    }else if(number == 3){
        objetive = document.getElementById('cabezero-3').value;
        cabezero = 3
    }else{
        objetive = document.getElementById('cabezero-4').value;
        cabezero = 4
    }
    
    idtimeout = setTimeout(() => {
        objetivo(objetive.toLowerCase(), cabezero)
    }, 500);
}

function objetivo(puntero, cabezero){
    var resultado = lista.filter(value => value[1].toLowerCase().includes(puntero));
    var index = 0;
    var size = resultado.length;
    for(i = 0; i<lista.length; i++){
        if(cabezero == 1){
            var element = document.getElementById(lista[i][0]);
            var no_found = document.getElementById("no_found");
        }else if(cabezero == 2){
            var element = document.getElementById("2" + lista[i][0]);
            var no_found = document.getElementById("2no_found");
        }else if(cabezero == 3){
            var element = document.getElementById("3" + lista[i][0]);
            var no_found = document.getElementById("3no_found");
        }else{
            var element = document.getElementById("4" + lista[i][0]);
            var no_found = document.getElementById("4no_found");
        }

        if(size > 0){
            
            if(no_found.classList[3] == 'flex'){
                no_found.classList.remove('flex');
                no_found.classList.add('hidden');
            }
            
            if(index < size && resultado[index][0] == lista[i][0]){
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

function ponerTexto(id, cual){
    if(cual == 1){
        var select = '[id="' + id + '"]';
        var place = document.getElementById('cabezero');
        var result_hidden = document.getElementById('valor_id');
    }else if(cual == 2){
        var select = '[id="' + id + '"]';
        var place = document.getElementById('cabezero-2');
        var result_hidden = document.getElementById('2valor_id');
    }else if(cual == 3){
        var select = '[id="' + id + '"]';
        var place = document.getElementById('cabezero-3');
        var result_hidden = document.getElementById('3valor_id');
    }else{
        var select = '[id="' + id + '"]';
        var place = document.getElementById('cabezero-4');
        var result_hidden = document.getElementById('4valor_id');
    }
    var father = document.querySelector(select)
    var sons = father.querySelectorAll('p')
    place.value = sons[1].textContent;
    result_hidden.value = parseInt(sons[0].textContent);
}
