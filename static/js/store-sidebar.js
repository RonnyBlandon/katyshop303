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

/* search engine by category */
const searchInputs = document.querySelectorAll('.search-category-movil, .search-category-desktop');
const categoryLists = document.querySelectorAll('.dropdown-categories li, .list-category li');

searchInputs.forEach(function (searchInput) {
	searchInput.addEventListener('keyup', function (event) {
		const searchTerm = event.target.value.toLowerCase();

		categoryLists.forEach(function (category) {
			const categoryName = category.textContent.toLowerCase();

			if (categoryName.includes(searchTerm)) {
				category.style.display = 'block';
			} else {
				category.style.display = 'none';
			}
		});
	});
});

