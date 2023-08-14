document.addEventListener('DOMContentLoaded', fetchProviders);
// document.addEventListener('DOMContentLoaded', fetchModels);
  
async function fetchProviders() {
    try {
        var provider = document.getElementById('provider').value || localStorage.getItem("provider");
        var model = document.getElementById('model').value || localStorage.getItem("model"); 
        debugger
        if (model == '' || model == null) {
            model = 'gpt-3.5-turbo'
        }
        
        const [providersResponse, bestProviderResponse] = await Promise.all([  
            fetch(`${url_prefix}/get-providers_by_model`,{
                method: "POST",
                headers: {  
                    "Content-Type": "application/json",  
                },  
                body: JSON.stringify({ model: model })
            }),
            fetch(`${url_prefix}/get-best_provider_by_model`,{
                method: "POST",
                headers: {  
                    "Content-Type": "application/json",  
                },  
                body: JSON.stringify({ model: model })
            })
        ]);
        
        
  
        const providers = await providersResponse.json();
        const best      = await bestProviderResponse.text();

        const providersSelect =  document.getElementById('provider');
        var exist = false
        providersSelect.innerHTML = "";
        const option = document.createElement('option');
        option.value = "BEST";  
        option.textContent = "BEST";
        providersSelect.appendChild(option);  
        providers.forEach(prov => {
            if (prov == provider){
                exist = true;
            }
            const option = document.createElement('option');  
            option.value = prov;  
            option.textContent = prov;  
            providersSelect.appendChild(option);
        });

        if(exist == true || best == 'None'){
            setProviderOnPageLoad(provider);
            localStorage.setItem("provider", provider);
        }else{
            setProviderOnPageLoad(best);
            localStorage.setItem("provider", best);
        }
        localStorage.setItem("model", model);
        
        await fetchModels()
    } catch (error) {  
        console.error("Failed to fetch languages or current language");  
    }
}

function setProviderOnPageLoad(best) {  
    document.getElementById("provider").value = best;  
}

async function fetchModels() {
    try {
        var provider = document.getElementById('provider').value || localStorage.getItem("provider");
        var current_model = document.getElementById('model').value || localStorage.getItem("model");
        // const all_models = document.getElementById('all-models').value;

        if (current_model == ''){
            current_model = 'gpt-3.5-turbo'
        }
        var [modelsResponse] = await Promise.all([  
            fetch(`${url_prefix}/get-models_by_provider`,{
                method: "POST",
                headers: {  
                    "Content-Type": "application/json",  
                },
                body: JSON.stringify({ provider: provider })
            })
        ]);

        debugger
        // if(all_models != 'off'){
        //     var [modelsResponse] = await Promise.all([  
        //         fetch(`${url_prefix}/get-models_by_provider`,{
        //             method: "POST",
        //             headers: {  
        //                 "Content-Type": "application/json",  
        //             },
        //             body: JSON.stringify({ provider: provider })
        //         })
        //     ]);
        // }else{
        //     var [modelsResponse] = await Promise.all([  
        //         fetch(`${url_prefix}/get-all_models`,{
        //             method: "GET"
        //         })
        //     ]);
        // }
        // debugger
        // localStorage.setItem("model", current_model);
        localStorage.setItem("provider", provider);
        const models = await modelsResponse.json();
        if(models.length == 0){
            setModelOnPageLoad(current_model);
            return
        }

        const modelsSelect = document.getElementById('model');
        modelsSelect.innerHTML = "";
        models.forEach(model => {  
            const option = document.createElement('option');  
            option.value = model;  
            option.textContent = model;  
            modelsSelect.appendChild(option);  
        });
        
        setModelOnPageLoad(current_model);
    } catch (error) {  
        console.error("Failed to fetch languages or current language");  
    }
}

function setModelOnPageLoad(current_model) {  
    document.getElementById("model").value = current_model;  
}


// function changeProvider(model) {  
//     fetch(`${url_prefix}/change-language`, {  
//         method: "POST",  
//         headers: {  
//             "Content-Type": "application/json",  
//         },  
//         body: JSON.stringify({ language: lang }),  
//     }).then((response) => {  
//         if (response.ok) {  
//             localStorage.setItem("language", lang);  
//             location.reload();  
//         } else {  
//             console.error("Failed to change language");  
//         }  
//     });  
// }
