/* Product image carousel logic */
const listImageProduct = document.querySelectorAll(".img-secondary");
const btnPrev = document.querySelector(".btn-prev");
const btnNext = document.querySelector(".btn-next");

function moveInCarousel (button) {
	let imageMain = document.querySelector(".img-main");
	for (let i=0; i<listImageProduct.length; i++) {
		if (button === "Next") {
			if (imageMain.src === listImageProduct[i].src) {

				if (listImageProduct.length > i+1) {
					imageMain.src = listImageProduct[i + 1].src;
				};
				break;
			};
		};
		if (button === "Previous") {
			if (imageMain.src === listImageProduct[i].src) {

				if (i > 0) {
					imageMain.src = listImageProduct[i - 1].src;
				};
				break;
			};
		}
	};
};

btnNext.addEventListener("click", () => {
	moveInCarousel("Next");
});
btnPrev.addEventListener("click", ()=> {
	moveInCarousel("Previous");
})
