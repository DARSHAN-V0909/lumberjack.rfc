let form=document.getElementById("registerForm");
form.addEventListener('submit',async function(event){
    event.preventDefault();
    let formData=new FormData(form);
    let username=formData.get('username');
    let password=formData.get('password');
    let response = await fetch("/register", {
         method: "POST",
         headers: {                     
            'Content-Type': 'application/json'
        },
         body: JSON.stringify({ "username": username, "password":password })
    });
    let result=await response.json();
    console.log(result);
    if(response.ok){
        let goOn=confirm("Registration Successful.Continue to login page?");
        if(goOn){
            window.location.href='/login';
        }
    }else{
        alert('Error: ' + result.error || result.message||"Unknown error");//fallback pattern
    }
});