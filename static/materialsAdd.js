let form = document.getElementById("materialsAdd");
form.addEventListener("submit",async function(event){
    event.preventDefault();
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
    }else{
        alert("Error, materials couldn't be added! Check console for more information");
        console.log('Error: ' + result.error || result.message||"Unknown error");
    }
})