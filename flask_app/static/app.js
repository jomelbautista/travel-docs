document.addEventListener('DOMContentLoaded', () => {
    getCountryNames('#countries-departing');
    getCountryNames('#countries-travelling-to');
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
            option.value = `${country.name}`;
            dropDown.add(option);
        })
    })
    .catch(err => console.log(err) );
}

// API call to populate country names into select dropdown
function getCountryCodeDeparture(countryName) {
    let countryCodeSrc = document.querySelector("#country-code-departing");
    fetch(`https://restcountries.com/v2/name/${countryName}?fullText=true`)
    .then(response => response.json() )
    .then(coderData => {
        countryCodeSrc.value = coderData[0]['alpha2Code'];
    })
    .catch(err => console.log(err) );
}

function getCountryCodeArrival(countryName) {
    let countryCodeSrc = document.querySelector("#country-code-arriving");
    fetch(`https://restcountries.com/v2/name/${countryName}?fullText=true`)
    .then(response => response.json() )
    .then(coderData => {
        countryCodeSrc.value = coderData[0]['alpha2Code'];
    })
    .catch(err => console.log(err) );
}