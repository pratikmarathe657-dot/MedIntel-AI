document.addEventListener("DOMContentLoaded", function(){

    const username = document.getElementById("username");
    const password = document.getElementById("password");

    const registerBtn = document.getElementById("registerBtn");
    const message = document.getElementById("message");


    registerBtn.onclick = async function(){


        if(!username.value || !password.value){

            message.innerText = "Please fill all fields";
            return;

        }


        try{


            const response = await fetch("/register", {

                method:"POST",

                headers:{
                    "Content-Type":"application/json"
                },

                body:JSON.stringify({

                    username: username.value,
                    password: password.value

                })

            });



            const data = await response.json();



            if(response.ok && data.success){


                message.innerText = "Account created successfully";


                setTimeout(()=>{

                    window.location.href="/";

                },1000);


            }

            else{

                message.innerText = data.detail || "Registration failed";

            }



        }

        catch(error){

            console.log(error);

            message.innerText="Unable to connect to server";

        }


    };


});