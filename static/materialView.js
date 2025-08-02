let table=document.getElementById("renderTable");
document.addEventListener('DOMContentLoaded',async function () {
    let response=await fetch('/materials',{
        method:'GET',
        headers:{
            'Content-type':'application/json'
        }
    });
    let resultSet=await response.json();
    console.log(response)
    if(response.ok){
        if(resultSet.length==0){
            table.innerHTML+="<tr><td colspan='4'>No Content Found</td></tr>"
        }
        resultSet.forEach(element => {
            table.innerHTML+=`
            <tr>
                <td>${element['name']}</td>
                <td>${element['unit']}</td>
                <td>${element['current_stock']}</td>
                <td>${element['threshold']}</td>
            </tr>
            `
        });
    }else{
        alert('Unrecognized error occured, check console');
    }

});