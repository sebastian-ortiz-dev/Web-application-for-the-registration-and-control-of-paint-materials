
var input_password = document.getElementById("contraseña")
var confirm_password = document.getElementById("confirmar")
var send_form = document.getElementById("send")

confirm_password.addEventListener("input", setTimeout(() => {
    var password = input_password.value
    var confirm_p = confirm_password.value
    if(password != confirm_p){
        send_form.style.display = "none";
    }else{
        send_form.style.display = "block";
    }
}), 5000);