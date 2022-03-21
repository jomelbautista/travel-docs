document.addEventListener('DOMContentLoaded', () => {
    getCountryNamesA('#countries-departing');
    getCountryNamesA('#countries-travelling-to');
})


// API call to populate country names into select dropdown
function getCountryNames(id) {
    var dropDown = document.querySelector(id);
    fetch("https://restcountries.com/v2/all")
    .then(response => response.json() )
    .then(coderData => {
            let option;
        coderData.forEach(country => {
            option = document.createElement('option');
            option.text = `${country.name}`;
            option.value = `${country.alpha2Code}`;
            dropDown.add(option);
        })
    })
    .catch(err => console.log(err) );
}