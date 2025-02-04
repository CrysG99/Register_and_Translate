function showPopup(title, description) {
    // Fikser tittelen og beskrivelsen
    document.getElementById('popup-title').textContent = title;
    document.getElementById('popup-body').textContent = description;

    // Viser popuppen og overlayen
    document.getElementById('popup').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
}

function closePopup() {
    // Skjuler popupen og overlayen
    document.getElementById('popup').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

function checkChooseLanguage() {
    var languageSelect = document.getElementById("language");
    var submitBook = document.getElementById("submitBook");
    var otherLanguageInput = document.getElementById("otherLanguage")

    if (languageSelect.value === "" || languageSelect.value === "Choose") {
        submitBook.style.display = "none";
        otherLanguageInput.style.display = "none";
    } else {
        submitBook.style.display = "block";
        if (languageSelect.value === "Other") {
            otherLanguageInput.style.display = "block";
        } else {
            otherLanguageInput.style.display = "none";
        }
    }
}