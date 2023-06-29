/* Submit the form by selecting a language. */
const languageSelect = document.getElementById('languageSelect');

console.log("Esto tiene languageSelect: ", languageSelect);
languageSelect.addEventListener('change', function() {
    const languageForm = document.getElementById('languageForm');
    languageForm.submit();
    console.log("Esto tiene languageForm: ", languageForm);
});