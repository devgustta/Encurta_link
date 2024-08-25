document.getElementById("encurta-btn").onclick = function(){
    var texto = document.getElementById("input-text").value;
    
    if(texto == ""){
        return
    }

    console.log(texto)
    encurta_url(texto)
}

function encurta_url(texto){        
    
        fetch('http://127.0.0.1:5000/enc/',{
           method: 'POST',
           headers: {
            'Content-Type': 'application/json',
           },
           body: JSON.stringify({ data: texto}),
        })
        .then(response => response.text())
        .then(data => {
            console.log("Success:", data)

            var novoLink = "http://127.0.0.1:5000/redi/" + data;
            var shortLinkElement = document.getElementById("shortLink");
            shortLinkElement.href = novoLink;
            shortLinkElement.textContent = novoLink;
            console.log(shortLinkElement)

        })
        .catch((error) => {
            console.log("Error:", error)
        });
    }



