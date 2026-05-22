async function signup(){

    let username =
    document.getElementById("username").value;

    let email =
    document.getElementById("email").value;

    let password =
    document.getElementById("password").value;


    let response = await fetch(
        "http://127.0.0.1:8000/signup",
        {

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({

                username,
                email,
                password

            })

        }
    );

    let data =
    await response.json();

    alert(data.message);

}