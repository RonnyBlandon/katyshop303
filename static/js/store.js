/* Logic to add product to cart */
const products = document.querySelectorAll(".btn-add-cart");
products.forEach(function (element, index) {
    element.addEventListener("click", function(event) {
        event.preventDefault;
        //We add a loader while the request is executed
        const loaderAddCart = element.parentNode.nextElementSibling;
        loaderAddCart.style.display = "block";
    });
});
// After 2.7 seconds we remove the added product message
const messageSuccessAddCart = document.querySelector(".success-add-cart");
const messageAlertAddCart = document.querySelector(".alert-add-cart");
if (messageSuccessAddCart) {
    setTimeout(function(){
        messageSuccessAddCart.remove()
    }, 2700);
};
if (messageAlertAddCart) {
    setTimeout(function(){
        messageAlertAddCart.remove()
    }, 2700);
};