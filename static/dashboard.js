//made to handle logout request
fetch('/logout').then(res=>res.json()).then((res)=>alert(res.message)).then(()=>window.location.href='/');