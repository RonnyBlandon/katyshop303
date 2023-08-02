/* LOGIC OF THE ORDER ADDRESS FORM */
/* Change the fields depending on the selected country */
const selectedCountry = document.getElementById('select-country');
const selectedState = document.getElementById('select-state');
const divSelectState = document.querySelector('.div-select-state');
const labelCity = document.getElementById('label-city');
const langValue = document.documentElement.lang;

function showHideInputState() {
	let selectedOption = selectedCountry.options[selectedCountry.selectedIndex];
	if (selectedOption.value == "Puerto Rico") {
		selectedState.required = false
		divSelectState.hidden = true;
		if (langValue === "en") {
			labelCity.innerHTML = 'Municipality';
		} else {
			labelCity.innerHTML = 'Municipalidad';
		}
	};
	if (selectedOption.value == "United States") {
		divSelectState.hidden = false;
		selectedState.required = true;
		if (langValue === "en") {
			labelCity.innerHTML = 'City';
		} else {
			labelCity.innerHTML = 'Ciudad';
		}
	};
}

if (selectedCountry) {
	showHideInputState();
	selectedCountry.addEventListener('change', showHideInputState);
};


/* POINTS FORM LOGIC */
// logic to apply points button
const boxDiscountElement = document.querySelector('.box-discount');
const discountElement = document.querySelector('.discount');
const divApplyPoints = document.querySelector('.apply-points');
const orderPoints = document.querySelector('.order-points');
const userPoints = document.getElementById('user-points');
const formPoints = document.getElementById('form-points');
const btnApplyPoints = document.getElementById('btn-apply-points');
const btnCancelPoints = document.querySelector('.btn-cancel-points');
// We hide the div to apply the discount if one has been applied
if (discountElement.innerHTML == '$0.00') {
	boxDiscountElement.style.display = 'none';
	divApplyPoints.style.display = 'flex';
} else {
	boxDiscountElement.style.display = 'flex';
	divApplyPoints.style.display = 'none';
}

btnApplyPoints.addEventListener('click', function() {
    formPoints.style.display = 'block';
});

btnCancelPoints.addEventListener('click', function() {
	formPoints.style.display = 'none';
});

// We send the request with the number of points to be redeemed as a parameter in the url
const btnMakeDiscount = document.querySelector(".btn-make-discount");
btnMakeDiscount.addEventListener('click', function () {
	//We add a loader while the request is executed
	const loaderDiscount = document.querySelector(".loader-discount");
	//
	const totalElement = document.querySelector(".total");
	const pointsElement = document.getElementById("redemption-points");
	const points = parseInt(pointsElement.value);
	const user_points = parseInt(pointsElement.dataset.user_points);
	const point_redemption_rate = parseInt(pointsElement.dataset.point_redemption_rate);

	if (points >= point_redemption_rate && points <= user_points) {
		if (pointsElement.nextElementSibling.classList.contains("message-points")) {
			pointsElement.nextElementSibling.remove();
		};
		loaderDiscount.style.display = "flex";
		let url = window.location.origin + '/redeem-points/' + points + '/';
		fetch(url).then(response => response.json()).then(function (data) {
			userPoints.innerHTML = parseInt(data["user_points"]);
			discountElement.innerHTML = '$'+data["discount"];
			totalElement.innerHTML = '$'+parseFloat(data["total"]).toFixed(2);
			// We updated the interface of the checkout page
			boxDiscountElement.style.display = 'flex';
			divApplyPoints.style.display = 'none';
			formPoints.style.display = 'none';
			orderPoints.innerHTML = parseInt(Math.round(data["total"] * orderPoints.dataset.earning_points_rate));
			setTimeout(function() {
				loaderDiscount.style.display = "none";
			}, 500); // 0.5 second pause
		});
	};

	if (points < point_redemption_rate) {
		// Create message reporting the error
		const message = document.createElement('p');
		message.classList.add('message-points');
		const langValue = document.documentElement.lang;
		if (langValue === "en") {
			message.innerHTML = "The minimum you can redeem is " + point_redemption_rate + " points.";
		} else {
			message.innerHTML = "Lo mínimo que puedes canjear son " + point_redemption_rate + " puntos.";
		}
		// Insert the message after the input
		const messagePointsClass = pointsElement.nextElementSibling.classList.contains("message-points");
		if (messagePointsClass) {
			if (pointsElement.nextSibling.innerHTML != message.innerHTML) {
				pointsElement.nextSibling.remove();
				pointsElement.parentNode.insertBefore(message, pointsElement.nextSibling);
			};
		} else {
			pointsElement.parentNode.insertBefore(message, pointsElement.nextSibling);
		};
	};

	if (points > user_points) {
		// Create message reporting the error
		const message = document.createElement('p');
		message.classList.add('message-points');
		const langValue = document.documentElement.lang;
		if (langValue === "en") {
			message.innerHTML = "You cannot redeem more points than you have accumulated. ";
		} else {
			message.innerHTML = "No puedes canjear más puntos de los que tienes acumulados. ";
		}
		// Insert the message after the input
		const messagePointsClass = pointsElement.nextElementSibling.classList.contains("message-points");
		if (messagePointsClass) {
			if (pointsElement.nextSibling.innerHTML != message.innerHTML) {
				pointsElement.nextSibling.remove();
				pointsElement.parentNode.insertBefore(message, pointsElement.nextSibling);
			};
		} else {
			pointsElement.parentNode.insertBefore(message, pointsElement.nextSibling);
		};
	};
});

// We send the request to remove the discount from the cart.
const removeDiscount = document.getElementById("remove-discount");
if (removeDiscount) {
	removeDiscount.addEventListener('click', function () {
		//We add a loader while the request is executed
		const loaderDiscount = document.querySelector(".loader-discount");
		// we send a request to remove the discount from the cart
		const totalElement = document.querySelector('.total');
		loaderDiscount.style.display = "flex";
		let url = window.location.origin + '/remove-discount-checkout/';
		fetch(url).then(response => response.json()).then(function (data) {
			userPoints.innerHTML = parseInt(data["user_points"]);
			totalElement.innerHTML = '$'+data["total"];
			// We updated the interface of the checkout page
			divApplyPoints.style.display = "flex";
			boxDiscountElement.style.display = "none";
			orderPoints.innerHTML = parseInt(Math.round(data["total"] * orderPoints.dataset.earning_points_rate));
			setTimeout(function() {
				loaderDiscount.style.display = "none";
			}, 500); // 0.5 second pause
		});
	});
}
