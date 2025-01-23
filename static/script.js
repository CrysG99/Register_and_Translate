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