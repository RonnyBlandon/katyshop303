/* switch For menu buttons */
// We use regular expressions to compare the pathnames
const start = /^\/$/;
const store = /^\/store\/$/;
const category = /^(\/category\/)([\s\S]*\/)$/;
const product = /^(\/product\/)([\s\S]*\/)$/;
const contact = /^\/contact\/$/;
const myAccount = /^(\/my-account\/)([\s\S]*\/)$/;
const pointsRules = /^\/points-rules\/$/;

let pathname = window.location.pathname;
let linkMenuPage = "";
switch (true) {
    case start.test(pathname):
        linkMenuPage = document.getElementById("start")
        linkMenuPage.classList.add("active");
        break;
    case store.test(pathname):
    case category.test(pathname):
    case product.test(pathname):
        linkMenuPage = document.getElementById("store")
        linkMenuPage.classList.add("active");
        break;
    case contact.test(pathname):
        linkMenuPage = document.getElementById("contact")
        linkMenuPage.classList.add("active");
        break;
    case myAccount.test(pathname):
        linkMenuPage = document.getElementById("my-account")
        linkMenuPage.classList.add("active");
        break;
    case pointsRules.test(pathname):
        linkMenuPage = document.getElementById("points-rules")
        linkMenuPage.classList.add("active");
        break;
};


/* We show and hide the mini cart */
const miniCart = document.querySelector('.container-mini-cart');
const buttonCart = document.querySelector('.cart');
const boxCart = document.querySelector('.box-cart');
const buttonCartClose = document.querySelector('.mini-cart-close');
// Mobile devices
buttonCart.addEventListener('touchend', (event) => {
    if (window.location.pathname != '/cart/') {
        event.preventDefault()
        miniCart.classList.add('mini-cart-show');
    };
});
buttonCartClose.addEventListener('click', () => {
    miniCart.classList.remove('mini-cart-show');
});
/* desktops and laptops */
buttonCart.addEventListener('mouseover', () => {
    // We check if the mobile close button of the mini cart is present with offsetParent to know if we are 
    // on a desktop screen
    if (!buttonCartClose.offsetParent && window.location.pathname != '/cart/') {
        miniCart.classList.add('mini-cart-show');
    }
});
miniCart.addEventListener('mouseover', () => {
    // We check if the mobile close button of the mini cart is present with offsetParent to know if we are 
    // on a desktop screen
    if (!miniCart.offsetParent && window.location.pathname != '/cart/') {
        miniCart.classList.add('mini-cart-show');
    }
});
buttonCart.addEventListener('mouseout', () => {
    miniCart.classList.remove('mini-cart-show');
});
miniCart.addEventListener('mouseout', () => {
    miniCart.classList.remove('mini-cart-show');
});