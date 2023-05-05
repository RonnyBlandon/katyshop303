/* Product image carousel logic */
const listImageProduct = document.querySelectorAll(".img-secondary");
const btnPrev = document.querySelector(".btn-prev");
const btnNext = document.querySelector(".btn-next");
const imageMain = document.querySelector(".img-main");
const points = document.getElementById("points");

//points image indicator
function positionCarousel(indexImage) {
    points.innerHTML = "";
    for (let i = 0; i < listImageProduct.length; i++) {
        if (indexImage == i) {
            points.innerHTML += '<p class="bold">.</p>';
        }
        else {
            points.innerHTML += '<p>.</p>';
        }
    }
}
//back and forward buttons
function moveInCarousel(button) {
    const currentImage = Array.from(listImageProduct).findIndex((img) => img.src === imageMain.src);

    if (button === "Next") {
        if (currentImage < listImageProduct.length - 1) {
            imageMain.src = listImageProduct[currentImage + 1].src;
            positionCarousel(currentImage + 1);
        }
    } else if (button === "Previous") {
        if (currentImage > 0) {
            imageMain.src = listImageProduct[currentImage - 1].src;
            positionCarousel(currentImage - 1);
        }
    }
}
btnNext.addEventListener("click", () => {
    moveInCarousel("Next");
});
btnPrev.addEventListener("click", () => {
    moveInCarousel("Previous");
});

// Get the modal
const modal = document.getElementById("modal");
// Get the image and insert it inside the modal
const imgMain = document.querySelector(".img-main");
const modalImg = document.getElementById("img01");
imgMain.addEventListener("click", function(){
  modal.classList.add("open-modal")
  modalImg.src = this.src;
});
// Get the <span> element that closes the modal
const modalClose = document.getElementsByClassName("close")[0];
// When the user clicks on <span> (x), close the modal
modalClose.addEventListener("click", function() { 
    modal.classList.remove("open-modal")
});
const thumbnails = document.querySelectorAll(".thumbnail");

thumbnails.forEach((thumbnail) => {
    thumbnail.addEventListener("click", (event) => {
        const selectedImage = event.target.src;
        modalImg.src = selectedImage;
    });
});


/* increase and decrease the quantity of a product in the cart */
const amountProduct = document.querySelectorAll(".amount-product");
const increaseProduct = document.querySelectorAll(".increase-product");
const decreaseProduct = document.querySelectorAll(".decrease-product");

function increase(amount_product, url) {
	// If you do not specify the maximum number of units available, we will assign 10 by default.
	if (amount_product.max == "None") {
		amount_product.max = 10;
	};
	if (parseInt(amount_product.value) < amount_product.max) {
		amount_product.value = parseInt(amount_product.value) + 1;
	};
};

function decrease(amount_product, url) {
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

  
/* After 2.7 seconds we remove the added product message */
const messageSuccessAddCart = document.querySelector(".success-add-cart");
if (messageSuccessAddCart) {
    setTimeout(function(){
        messageSuccessAddCart.remove()
    }, 2700);
};
/* After 2.7 seconds we remove the alert product message */
const messageAlertAddCart = document.querySelector(".alert-add-cart");
if (messageAlertAddCart) {
    setTimeout(function(){
        messageAlertAddCart.remove()
    }, 2700);
};