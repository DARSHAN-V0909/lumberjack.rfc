//made to handle logout request
document.addEventListener('DOMContentLoaded',async function(){
    let response = await fetch('/stockStatus',{
        method:'GET',
        headers:{
            'content-type':'application/json'
        }
    });
    let resultSet=await response.json();
    console.log(resultSet);
    if (!response.ok) {
        alert('Failed to fetch stock status');
        return;
    }
    console.log(response);
    if(resultSet.length!=0){
        resultSet.forEach(element => {//default bootstrap toast template
            let string=element['threshold']>element['current_stock']?`Critical Stock Alert: Only ${element['current_stock']} ${element['unit']} of minimum ${element['threshold']} ${element['unit']} present for ${element['name']}.`:`Stock Alert: Current stock at threshold level of ${element['threshold']} ${element['unit']} for ${element['name']}.`;
            const toastHTML = `
            <div class="toast align-items-center ${element['threshold']>element['current_stock']?'text-bg-danger':'text-bg-warning'} text-dark border-0 mb-5 p-2 fw-bolder" role="alert" aria-live="assertive " aria-atomic="true">
                <div class="d-flex">
                    <div class="toast-body">
                    ${string} <a href="/materialAdd" class="text-decoration-none">Click here to update stock now</a>
                    </div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
            </div>
            `;
            document.getElementById("toast-container").insertAdjacentHTML('beforeend', toastHTML);
            const toastEl = document.querySelector('#toast-container .toast:last-child');
            const bsToast = new bootstrap.Toast(toastEl);
            bsToast.show();
        });
    }
});