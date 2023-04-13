function showMenu() {
    let menu = document.getElementById('menu');
    let navSpans = Array.from(document.getElementById('menu-button').children);

    menu.classList.toggle('show-menu');
    navSpans.forEach(element => element.classList.toggle('open'));
}

function subscribe(event) {
    let subscribeForm = document.getElementById('subscribe');
    let validationMessage = !subscribeForm.checkValidity() ? 'Некоректна email адреса!' : 'Успішно підписано!';
    document.getElementById('subscribe-message').innerHTML = validationMessage;
}

function showSorting(blockId) {
    let block = document.getElementById(blockId);
    if (block.style.display === "block") {
        block.style.display = "none"
    }
    else {
        let blocks = Array.from(document.getElementById("sorting-blocks").children);
        blocks.forEach(element => element.style.display = "none");
        document.getElementById(blockId).style.display = "block";
    }
}