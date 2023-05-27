function showMenu() {
    let menu = document.getElementById('menu');
    let navSpans = Array.from(document.getElementById('menu-button').children);

    menu.classList.toggle('open');
    navSpans.forEach(element => element.classList.toggle('open'));
}

function subscribe(event) {
    let subscribeForm = document.getElementById('subscribe');
    let validationMessage = !subscribeForm.checkValidity() ? 'Некоректна email адреса!' : 'Успішно підписано!';
    document.getElementById('subscribe-message').innerHTML = validationMessage;
}

function showSorting(blockId) {
    let block = document.getElementById(blockId);
    let form = document.getElementById('sorting-form');

    if (block.classList.contains('open')) {
        block.classList.remove('open');
        form.classList.remove('open');
    }
    else {
        let blocks = Array.from(document.getElementsByClassName('sort-category'));
        blocks.forEach(element => element.classList.remove('open'));
        block.classList.add('open');
        form.classList.add('open')
    }
}

function orderPopup() {
     document.getElementById('order-popup').classList.add('open');
}