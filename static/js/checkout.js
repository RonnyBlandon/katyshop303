import { showHideInputState } from './my-account.js';
/* Change the fields depending on the selected country */
const selectedCountry = document.getElementById('select-country');
const selectedState = document.getElementById('select-state');
const divSelectState = document.querySelector('.div-select-state');
const labelCity = document.getElementById('label-city');

if (selectedCountry) {
	selectedCountry.addEventListener('change', showHideInputState);
}