
function reset_pressed() {
    console.log("Reset pressed");
    fetch("/reset", {
        method: "POST",
    });
}

function key_entered(event) {
    console.log(event.key);
    fetch("/key", {
        method: "POST",
        body: event.key,
        headers: {
            "Content-type": "text/plain"
        }
    });
    document.getElementById("entry").value = event.key;
}
