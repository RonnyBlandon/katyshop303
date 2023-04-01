/* increase and decrease the quantity of a product in the cart */
const amountProduct = document.querySelectorAll(".amount-product");
const increaseProduct = document.querySelectorAll(".increase-product");
const decreaseProduct = document.querySelectorAll(".decrease-product");

function increase(amount_product) {
	// If you do not specify the maximum number of units available, we will assign 10 by default.
	if (amount_product.max == "None") {
		amount_product.max = 10;
	}
	if (parseInt(amount_product.value) < amount_product.max) {
		amount_product.value = parseInt(amount_product.value) + 1;
	}
}

function decrease(amount_product) {
	if (parseInt(amount_product.value) > amount_product.min) {
		amount_product.value = parseInt(amount_product.value) - 1;
	}
}

increaseProduct.forEach((element) => {
	element.addEventListener("click", function() {
	  increase(element.previousElementSibling);
	});
  });
  
  decreaseProduct.forEach((element) => {
	element.addEventListener("click", function() {
	  decrease(element.nextElementSibling);
	});
  });
