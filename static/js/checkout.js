import { showHideInputState } from './my-account.js';
/* Change the fields depending on the selected country */
const selectedCountry = document.getElementById('select-country');
const selectedState = document.getElementById('select-state');
const divSelectState = document.querySelector('.div-select-state');
const labelCity = document.getElementById('label-city');

function showHideInputState() {
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
}

if (selectedCountry) {
	selectedCountry.addEventListener('change', showHideInputState);
}