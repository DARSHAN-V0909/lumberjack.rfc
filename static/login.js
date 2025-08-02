//this JS file handles the request sending to backend to verify login details please read login.html first if you are unfamiliar
let form=document.getElementById("loginForm");//gets the form instance from the HTML page
form.addEventListener('submit',async function(event){//async function to allow us to raise a fetch request
    event.preventDefault();//prevents auto refresh feature of the submit button
    const formData=new FormData(form);//gets the form instance with its data as dictionary of sorts
    const username=formData.get('username');//get the username field data
    const password=formData.get('password');//password field data
    let response = await fetch("/login", {
         method: "POST",
         headers: {                     
            'Content-Type': 'application/json'
        },
         body: JSON.stringify({ "username": username, "password":password })
    });//this is the main json object, it contains a POST request sent to backend with a body containing login details
    let result=await response.json();//waits for confirmation response from backend
    console.log(result);//logs the response
    if(response.ok){//sends an inscreen alert to user, BETTER THIS USING redirect pages and a proper login validation/rejection
        alert("Login Successful");
        window.location.href='/home';
    }else{
        alert('Error: ' + result.error || result.message||"Unknown error");//fallback pattern
    }
})