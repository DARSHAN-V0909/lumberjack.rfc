let table=document.getElementById("renderTable");
let materialsRS,transactionRS;
document.addEventListener('DOMContentLoaded',async function () {
    let response=await fetch('/materials',{
        method:'GET',
        headers:{
            'Content-type':'application/json'
        }
    }); 
    let resultSet=await response.json();
    materialsRS=resultSet;
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
        alert('Unrecognized error occured while fetching materials, check console');
    }
    let response2=await fetch('/transactions',{
        method:'GET',
        headers:{
            'Content-type':'application/json'
        },
    });
    let resultSet2=await response2.json();
    transactionRS=resultSet2;
    console.log(response2);
    if(!response2.ok)alert('Unrecognized error occured while fetching transactions,check console');
});
document.getElementById("view").addEventListener('change',function(){
    let table=document.getElementById('renderTable');
    if(this.value=='materials'){
        // let headRow=document.getElementById('headRow');
        // let innerInfo=document.getElementById('innerInfo');
        table.innerHTML=`
            <th>Material</th>
            <th>Unit</th>
            <th>Current Stock</th>
            <th>Threshold</td>
        `;
        materialsRS.forEach(element=>{
            table.innerHTML+=
            `<tr>
                <td>${element['name']}</td>
                <td>${element['unit']}</td>
                <td>${element['current_stock']}</td>
                <td>${element['threshold']}</td>
            </tr>`;
        });
    }else{
        // let headRow=document.getElementById('headRow');
        // let innerInfo=document.getElementById('innerInfo');
        table.innerHTML=`
            <th>Material</th>
            <th>Quantity</th>
            <th>Operation Type</th>
            <th>Time Stamp</td>
        `;
        transactionRS.forEach(element=>{
            table.innerHTML+=
            `<tr>
                <td>${element['name']}</td>
                <td>${element['quantity']}</td>
                <td>${element['type'].toUpperCase()}</td>
                <td>${element['timestamp']}</td>
            </tr>`;
        });
    }
});