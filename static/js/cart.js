/* increase and decrease the quantity of a product in the cart */
const amountProduct = document.querySelectorAll(".amount-product");
const increaseProduct = document.querySelectorAll(".increase-product");
const decreaseProduct = document.querySelectorAll(".decrease-product");

function increase(amount_product) {
	if (parseInt(amount_product.value) < 10) {
		amount_product.value = parseInt(amount_product.value) + 1;
	}
}

function decrease(amount_product) {
	if (parseInt(amount_product.value) > 1) {
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
