document.getElementById('search_input').onkeypress = function (e) {
    if (!e) e = window.event;
    var keyCode = e.keyCode || e.which;
    if (keyCode == '13') {

        return false;
    }
};

$("#search_input").keyup(function (event) {
    console.log("presion");
    if (event.keyCode === 13) {
        $("#search_button").click();
    }
});

function search() {
    if (document.getElementById('search_input').value.trim()) {
        window.location.href = "/search/" + document.getElementById('search_input').value;
    } else {
        window.location.href = "/"
    }
}