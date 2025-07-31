let form=document.getElementById("loginForm");
form.addEventListener('submit',async function(event){
    event.preventDefault();
    const formData=new FormData(form);
    const username=formData.get('username');
    const password=formData.get('password');
    let response = await fetch("/login", {
         method: "POST",
         headers: {                     
            'Content-Type': 'application/json'
        },
         body: JSON.stringify({ "username": username, "password":password })
    });
    let result=await response.json();
    console.log(result);
    if(response.ok){
        alert("Login Successful");
    }else{
        alert('Error: ' + result.error || result.message||"Unknown error");//fallback pattern
    }
})