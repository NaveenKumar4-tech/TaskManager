async function signin(){

    let username = document.getElementById("username").value;


    let password = document.getElementById("loginpassword").value;


    let response = await fetch(
        "http://127.0.0.1:8000/signin",
        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                username,
                password

            })

        }
    );


    let data = await response.json();


    if(data.access_token){

        localStorage.setItem(
            "token",
            data.access_token
        );

        window.location.href =
        "/taskmanager";
    }

    else{
        console.log("error")
        // alert("Login failed");
    }

    console.log(data)
}