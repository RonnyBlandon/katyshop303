/* Show and hide the mobile menu */
const userMenuShow = document.querySelector(".nav-user-show");
const userMenuClose = document.querySelector(".nav-user-close");

userMenuShow.addEventListener("click", () => {
	const boxNavUser = document.querySelector(".box-nav-user");
	boxNavUser.style.right = "0";
});

userMenuClose.addEventListener("click", () => {
	const boxNavUser = document.querySelector(".box-nav-user");
	boxNavUser.style.right = "100%";
});


/* Change the fields depending on the selected country */
const selectedCountry = document.getElementById('select-country');
// 
const selectedState = document.getElementById('select-state');
const divSelectState = document.querySelector('.div-select-state');
const labelCity = document.getElementById('label-city');
console.log(selectedState);

selectedCountry.addEventListener('change', function () {
	//
	let selectedOption = selectedCountry.options[selectedCountry.selectedIndex];
	if (selectedOption.value == "Puerto Rico") {
		selectedState.required = false
		divSelectState.hidden = true;
		labelCity.innerHTML = 'Municipalidad';
	};

	if (selectedOption.value == "Estados Unidos") {
		divSelectState.hidden = false;
		selectedState.required = true;
		labelCity.innerHTML = 'Ciudad';
	};
});




const re = /^\d{5}(\-\d{4})?/;
const text = "12345";

if (re.test(text)) {
   console.log("Es correcto");
}
else {
   console.log("Es incorrecto");
}