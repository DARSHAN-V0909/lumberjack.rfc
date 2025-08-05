let form = document.getElementById("materialsAdd");
let updateMaterialID="";//will store material_id for update queries
form.addEventListener("submit",async function(event){
    event.preventDefault();
    let operation=document.getElementById("operation").value;
    if(operation=='ADD'){
        const formData=new FormData(form);
        const name=formData.get('name');
        const unit=formData.get('unit');
        const stock=formData.get('current_stock');
        const threshold=formData.get('threshold');
        let response= await fetch("/materials",{
            method: "POST",
            headers:{
                'Content-type':'application/json'
            },
            body:JSON.stringify({'name':name,'unit':unit,'current_stock':stock,'threshold':threshold})
        });
        let result=await response.json();
        console.log(result);
        if(response.ok){
            alert('Items added succesfully');
            window.location.reload();
        }else{
            alert("Error, materials couldn't be added! Check console for more information");
            console.log('Error: ' + result.error || result.message||"Unknown error");
        }       
    }else if(operation=='UPDATE'){
        const formData=new FormData(form);
        const material=document.getElementById('material').value;
        const quantity=document.getElementById('quantity').value
        const dataAvailability = Number(document.getElementById('quantity').min*-1);
        console.log(material,quantity,dataAvailability,updateMaterialID);
        let response= await fetch("/materials",{
            method: "PUT",
            headers:{
                'Content-type':'application/json'
            },
            body:JSON.stringify({'name':material,'quantity':quantity,'current_stock':dataAvailability,'material_id':updateMaterialID})
        });
        let result=await response.json();
        console.log(result);
        if(response.ok){
            alert('Material updated succesfully');
            window.location.reload();
        }else{
            alert("Error, materials couldn't be updated! Check console for more information");
            console.log('Error: ' + result.error || result.message||"Unknown error");
        }  
    }else if(operation=='DELETE'){
        const formData=new FormData(form);
        const material=document.getElementById('material').value;
        console.log(material);
        let response= await fetch("/materials",{
            method: "DELETE",
            headers:{
                'Content-type':'application/json'
            },
            body:JSON.stringify({'name':material,'material_id':updateMaterialID})
        });
        let result=await response.json();
        console.log(result);
        if(response.ok){
            alert('Material deleted succesfully');
            window.location.reload();
            
        }else{
            alert("Error, materials couldn't be deleted! Check console for more information");
            console.log('Error: ' + result.error || result.message||"Unknown error");
        } 
    }

})
//operations on selecting option in select
document.getElementById("operation").addEventListener('change',async function(){
    let value=document.getElementById("operation").value;
    let renderArea=document.getElementById("renderArea");
    if(value=="ADD"){
        renderArea.innerHTML=`Material Name: <input type="text" name="name" id="name" required><br>
        Unit:          <select name="unit" id="unit" required>
                            <option value="kg">kg</option><br>
                            <option value="Liters">Liters</option><br>
                            <option value="g">grams</option>
                            <option value="pieces">pieces</option>
                            <option value="bags">bags</option>
                            <option value="units">units</option>
                         </select><br>
        Current Stock:   <input type="number" name="current_stock" id="current_stock" required min="0"><br>
        Threshold (Minimum stock): <input type="number" name="threshold" id="threshold" required min="0"><br>
        <input type="submit" value="submit">`
        }else if(value=='UPDATE'){
        let htmlString = `Select Material: 
            <select id="material" name="material" required><option value="" disabled selected>Select a material</option>`;
        
        let response = await fetch('/materials', {
            method: 'GET',
            headers: {
                'Content-type': 'application/json'
            }
        });
        let resultSet = await response.json();
        console.log(response);

        if (!response.ok) {
            alert("Error, materials couldn't be fetched! Check console for more information");
            console.log('Error: ' + result.error || result.message || "Unknown error");
            return;
        }

        resultSet.forEach(element => {
            htmlString += `<option value="${element.name}">${element.name}</option>`;
        });

        htmlString += `</select><br>
            <div id="numField"></div><br>
            <input type="submit" value="submit">`;

        renderArea.innerHTML = htmlString;

        // ✅ Corrected to 'change' and added missing #numField container
        document.getElementById('material').addEventListener('change', function () {
            let value = this.value;
            let selectedMaterial = resultSet.find(material => material.name === value);
            let numberField = document.getElementById('numField');
            if (selectedMaterial) {
                let maxValue = selectedMaterial.current_stock;
                updateMaterialID = selectedMaterial.material_id;

                numberField.innerHTML = `
                    Enter Amount to be added or deleted:
                    (Current Stock is ${maxValue} ${selectedMaterial.unit})<br>
                    <input type="number" name="quantity" id="quantity" required min="${-1 * maxValue}">
                `;
            }
        });
    }else if(value=='DELETE'){
        let htmlString=`Select Material: <select id="material" required>
        `;//add event listener for material to give max material to remove
        let response=await fetch('/materials',{
            method:'GET',
            headers:{
                'Content-type':'application/json'
            }
        });
        let resultSet=await response.json();//stores all the db values
        console.log(response);
        if(!response.ok){
            alert("Error, materials couldn't be added! Check console for more information");
            console.log('Error: ' + result.error || result.message||"Unknown error");
        }
        resultSet.forEach(element => {
            htmlString+=`<option value="${element['name']}">${element['name']}</option>`
        });
        renderArea.innerHTML=htmlString+'</select><br>';
        renderArea.innerHTML+='<input type="submit" value="submit">';
        document.getElementById('material').addEventListener('change', function () {
            let value = this.value;
            let selectedMaterial = resultSet.find(material => material.name === value);
            let numberField = document.getElementById('numField');
            if (selectedMaterial) {
                updateMaterialID = selectedMaterial.material_id;
            }
        });
    }
});
