//this js file handles the registration validation, it is recommended you read login.js,login.html before continuing to edit to understand
//core app functionality
let form=document.getElementById("registerForm");
form.addEventListener('submit',async function(event){
    event.preventDefault();//prevents default submission nature of submit button
    let formData=new FormData(form);
    let username=formData.get('username');
    let password=formData.get('password');
    let response = await fetch("/register", {
         method: "POST",
         headers: {                     
            'Content-Type': 'application/json'
        },
         body: JSON.stringify({ "username": username, "password":password })
    });//again this json post object contains username password attribute to be sent to backend similar to the login.js page
    let result=await response.json();
    console.log(result);
    if(response.ok){//this page asks user if they want to go to login page after, would recommend that we show this in a neater way 
        //or directly redirct to login page if no error
        let goOn=confirm("Registration Successful.Continue to login page?");
        if(goOn){
            window.location.href='/login';
        }
    }else{//handles any 400-like error response from backend, alerts user with this, would recommend that user is given a cleaner error message
        alert('Error: ' + result.error || result.message||"Unknown error");//fallback pattern
    }
});