/* Submit the form by selecting a language. */
const languageSelect = document.getElementById('languageSelect');

languageSelect.addEventListener('change', function() {
    const languageForm = document.getElementById('languageForm');
    languageForm.submit();
});