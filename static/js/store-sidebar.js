/* We show and hide the dropdown menu of categories */

const dropdownMenu = document.querySelector('.dropdown-categories');
const dropdownToggle = document.querySelector('.dropdown-toggle');

dropdownToggle.addEventListener('click', () => {
	dropdownMenu.classList.toggle('show');
});

window.addEventListener('click', (event) => {
	if (!dropdownToggle.contains(event.target) && !dropdownMenu.contains(event.target)) {
		dropdownMenu.classList.remove('show');
	}
});
