/* Show and hide the mobile menu */
const userMenuShow = document.querySelector(".user-menu-show");
const userMenuClose = document.querySelector(".nav-user-close");
const boxNavUser = document.querySelector(".box-nav-user");

if (userMenuShow) {
	userMenuShow.addEventListener("click", () => {
		boxNavUser.style.right = "0";
	});
}
if (userMenuClose) {
	userMenuClose.addEventListener("click", () => {
		boxNavUser.style.right = "100%";
	});
}

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
	selectedCountry.addEventListener('change', showHideInputState);
}
