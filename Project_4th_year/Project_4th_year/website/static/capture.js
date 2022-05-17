
function button_press(){
    console.log("button pressed");
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
        var response = xhttp.responseText;
        console.log("ok"+response);
    }
};
xhttp.open("GET", local_ip+":5000/api/test", true);

xhttp.send();
}

function myFunc(vars) {
    return vars
}