/* increase and decrease the quantity of a product in the cart */
const amountProduct = document.querySelectorAll(".amount-product");
const increaseProduct = document.querySelectorAll(".increase-product");
const decreaseProduct = document.querySelectorAll(".decrease-product");

// function to increase the quantity of a product in the cart
function updateCart(url, subtotal_product) {
	fetch(url).then(response => response.json()).then(function (data) {
		if (data.success) {
			const quantityItemsMiniCart = document.querySelector(".quantity-items");
			const quantityItemsCart = document.querySelector(".proceed-to-pay-quantity");
			const subtotal = document.querySelector(".proceed-to-pay-subtotal");
			quantityItemsMiniCart.innerHTML = data.quantity_items;
			quantityItemsCart.innerHTML = data.quantity_items;
			subtotal.innerHTML = "$" + data.cart_subtotal;
			subtotal_product.innerHTML = "$" + data.item_subtotal;
		};
	});
};

function increase(amount_product, url) {
	// If you do not specify the maximum number of units available, we will assign 10 by default.
	if (amount_product.max == "None") {
		amount_product.max = 10;
	};
	if (parseInt(amount_product.value) < amount_product.max) {
		const subtotal_product = amount_product.parentNode.parentNode.parentNode.querySelector(".subtotal-product");
		//We add the value of the input to the url as a parameter
		full_url = url+"?quantity="+amount_product.value;
		console.log("Esto contiene value: ", amount_product.value);
		//We make the request and update the data
		updateCart(full_url, subtotal_product);
		amount_product.value = parseInt(amount_product.value) + 1;
	};
};

function decrease(amount_product, url) {
	if (parseInt(amount_product.value) > amount_product.min) {
		const subtotal_product = amount_product.parentNode.parentNode.parentNode.querySelector(".subtotal-product");
		//We add the value of the input to the url as a parameter
		full_url = url+"?quantity="+amount_product.value;
		//We make the request and update the data
		updateCart(full_url, subtotal_product);
		amount_product.value = parseInt(amount_product.value) - 1;
	}
}

increaseProduct.forEach((element) => {
	element.addEventListener("click", function() {
	  increase(element.previousElementSibling, element.dataset.urlIncrease);
	});
  });
  
  decreaseProduct.forEach((element) => {
	element.addEventListener("click", function() {
	  decrease(element.nextElementSibling, element.dataset.urlDecrease);
	});
  });

  
/* After 2.7 seconds we remove the added product message */
const messageSuccessAddCart = document.querySelector(".success-add-cart");
if (messageSuccessAddCart) {
    setTimeout(function(){
        messageSuccessAddCart.remove()
    }, 2700);
};