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
            option.value = `${country.alpha2Code}`
            dropDown.add(option);
        })
    })
    .catch(err => console.log(err) );
}


function getTravelRestrictions() {
    let countryCodeArrival = getArrivalCountryCode();
    let countryCodeDeparture = getDepartureCountryCode();
    let url = `https://test.api.amadeus.com/v1/duty-of-care/diseases/covid19-area-report?countryCode=${countryCodeArrival}`
    fetch(url, {
        method: "GET",
        headers: {
            "Authorization": "Bearer h6ougBmpHCdGKN3GUDiWLpCo8Gc2",
        },
        mode:"cors",
        catch:"default"
    }).then(function(response){
        if(response.ok){
            return response.json();
        }else{
            throw new Error(error);
        }
    }).then(function(data){

        // Check travel ban
        let travelBan = document.querySelector("#travel-ban");
        for (let i = 0; i < data['data']['areaAccessRestriction']['entry']['bannedArea'].length; i++ ) {
            if (countryCodeDeparture == data['data']['areaAccessRestriction']['entry']['bannedArea'][i]['iataCode']) {
                travelBan.innerHTML = 'Travel is currently banned';
                break
            } else {
                travelBan.innerHTML = 'Travel is currently not banned';
            }
        }
        
        // Get last update date for travel ban
        let travelBanUpdateDate = document.querySelector("#travel-ban-update-date");
        let getTravelBanUpdateDate = data['data']['areaAccessRestriction']['entry']['date'];
        travelBanUpdateDate.innerHTML = getTravelBanUpdateDate;

        // Set documentation required
        let documentRequired = document.querySelector("#documentation-required");
        let getDocumentRequired = data['data']['areaAccessRestriction']['declarationDocuments']['documentRequired'];
        if (typeof getDocumentRequired == 'undefined') {
            documentRequired.innerHTML = 'N/A'
        } else {
            documentRequired.innerHTML = getDocumentRequired;
        }

        // Set text summary
        let textSummary = document.querySelector("#summary");
        let getTextSummary = data['data']['areaAccessRestriction']['declarationDocuments']['text'];
        textSummary.innerHTML=getTextSummary;

        // Set travel documentation link
        let travelDocumentationLink = document.querySelector("#documentation-link");
        let getTravelDocumentationLink = data['data']['areaAccessRestriction']['declarationDocuments']['travelDocumentationLink'];
        if (typeof getTravelDocumentationLink == 'undefined') {
            travelDocumentationLink.innerHTML = 'N/A'
        } else {
            travelDocumentationLink.innerHTML = getTravelDocumentationLink;
        }

        // Set last update
        let textLastUpdateDate = document.querySelector("#last-updated");
        let getLastUpdateDate = data['data']['areaAccessRestriction']['declarationDocuments']['date'];
        textLastUpdateDate.innerHTML = getLastUpdateDate;

    }).catch(function(error){
        console.log(error);
    })
}

function getArrivalCountryCode() {
    var selectedCountry = document.querySelector("#countries-travelling-to");
    return selectedCountry.value;
}

function getDepartureCountryCode() {
    var selectedCountry = document.querySelector("#countries-departing");
    return selectedCountry.value;
}