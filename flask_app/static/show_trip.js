document.addEventListener('DOMContentLoaded', () => {
    let countryCodeDeparture = document.querySelector("#countries-departing-code").innerHTML;
    let countryCodeArrival = document.querySelector("#countries-travelling-to-code").innerHTML;
    getTravelRestrictions(countryCodeDeparture, countryCodeArrival);
})

function getTravelRestrictions(countryCodeDeparture, countryCodeArrival) {
    let url = `https://test.api.amadeus.com/v1/duty-of-care/diseases/covid19-area-report?countryCode=${countryCodeArrival}`
    fetch(url, {
        method: "GET",
        headers: {
            "Authorization": "Bearer yAZyqHRq3cCPPDlJT3bCAOHnHQcd",
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
        let depatureCountry = document.querySelector("#countries-departing").innerHTML;
        let arrivalCountry = document.querySelector("#countries-travelling-to").innerHTML;
        for (let i = 0; i < data['data']['areaAccessRestriction']['entry']['bannedArea'].length; i++ ) {
            if (countryCodeDeparture == data['data']['areaAccessRestriction']['entry']['bannedArea'][i]['iataCode']) {
                travelBan.innerHTML = 'Travel from ' + depatureCountry + ' to ' + arrivalCountry + ' is currently banned.';
                document.querySelector("#travel-ban").style.color = "red";
                document.querySelector("#travel-ban").style.fontWeight = "bolder";
                break
            } else {
                travelBan.innerHTML = 'Travel from ' + depatureCountry + ' to ' + arrivalCountry + ' is currently allowed.';
                document.querySelector("#travel-ban").style.color = "green";
                document.querySelector("#travel-ban").style.fontWeight = "bolder";
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
            documentRequired.innerHTML = 'Information cannot be found at this time.'
        } else {
            documentRequired.innerHTML = getDocumentRequired;
        }

        // Set text summary
        let textSummary = document.querySelector("#summary");
        let getTextSummary = data['data']['areaAccessRestriction']['declarationDocuments']['text'];
        if (typeof getTextSummary == 'undefined') {
            textSummary.innerHTML = 'Information cannot be found at this time.'
        } else {        
            textSummary.innerHTML=getTextSummary;
        }


        // Set travel documentation link
        let travelDocumentationLink = document.querySelector("#documentation-link");
        let getTravelDocumentationLink = data['data']['areaAccessRestriction']['declarationDocuments']['travelDocumentationLink'];
        if (typeof getTravelDocumentationLink == 'undefined') {
            travelDocumentationLink.innerHTML = 'Information cannot be found at this time.'
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