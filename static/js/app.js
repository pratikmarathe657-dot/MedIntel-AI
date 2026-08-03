let currentChatId = null;

console.log("app.js loaded");
// ======================================
// ELEMENTS
// ======================================

const uploadBtn = document.getElementById("uploadBtn");
const pdfFile = document.getElementById("pdfFile");

const sendBtn = document.getElementById("sendBtn");
const questionInput = document.getElementById("questionInput");
const chatBox = document.getElementById("chatBox");

const historyList = document.getElementById("historyList");
const newChatBtn = document.getElementById("newChatBtn");
const exportBtn = document.getElementById("exportBtn");
const logoutBtn = document.getElementById("logoutBtn");



// ======================================
// PAGE LOAD
// ======================================

window.onload = async function(){

    await loadHistory();


    const savedChat =
    localStorage.getItem("currentChatId");


    if(savedChat){

        openChat(savedChat);

    }

};






// ======================================
// UPLOAD BUTTON
// ======================================


uploadBtn.onclick = ()=>{

    pdfFile.click();

};






// ======================================
// UPLOAD PDF
// ======================================


pdfFile.addEventListener(
"change",
async()=>{


    if(pdfFile.files.length===0)
        return;



    const formData =
    new FormData();



    formData.append(
        "file",
        pdfFile.files[0]
    );



    try{


        uploadBtn.innerText = "Uploading...";
        uploadBtn.disabled = true;



        const response =
        await fetch(
            "/upload",
            {

                method:"POST",

                body:formData

            }
        );



        const data =
        await response.json();

        if (!response.ok) {

    throw new Error(data.detail || "Upload failed");

}



        currentChatId =
        data.chat_id;



        localStorage.setItem(
            "currentChatId",
            currentChatId
        );



       uploadBtn.innerText = "Upload Report";
       uploadBtn.disabled = false;
       pdfFile.value = "";



        clearChat();


    addMessage(

`✅ Report uploaded

📄 ${data.pages} ${data.pages === 1 ? "page" : "pages"} processed

Start asking questions.`,

"bot"

);



        await loadHistory();


    }



    catch(error){


        console.log(error);


        uploadBtn.innerText = "Upload Report";
        uploadBtn.disabled = false;


        addMessage(

            "❌ Upload failed",

            "bot"

        );


    }


});









// ======================================
// ADD MESSAGE
// ======================================


function addMessage(message, sender) {

    const welcome = document.querySelector(".welcome");

    if (welcome)
        welcome.remove();

    const div = document.createElement("div");

    div.className = "message " + sender;

    // Message text
    const text = document.createElement("div");
    text.className = "message-text";
    text.innerText = message;

    div.appendChild(text);

    // Copy button only for AI messages
    if (sender === "bot") {

        const copyBtn = document.createElement("button");

        copyBtn.className = "copy-btn";

        copyBtn.innerText = "📋 Copy";

        copyBtn.onclick = () => {

            navigator.clipboard.writeText(message);

            copyBtn.innerText = "✅ Copied";

            setTimeout(() => {

                copyBtn.innerText = "📋 Copy";

            }, 1500);

        };

        div.appendChild(copyBtn);
    }

    chatBox.appendChild(div);

    chatBox.scrollTop = chatBox.scrollHeight;
}









// ======================================
// ASK AI
// ======================================


sendBtn.onclick =
askQuestion;



questionInput.addEventListener(
"keypress",
(e)=>{


    if(e.key==="Enter")
        askQuestion();


});





async function askQuestion(){


    const question =
    questionInput.value.trim();



    if(!question)
        return;




    if(!currentChatId){


        alert(
            "Please upload medical report first"
        );


        return;

    }





    addMessage(

        question,

        "user"

    );



    questionInput.value="";



    const loading = document.createElement("div");
loading.className = "message loading";
loading.innerHTML = "<div class='message-text'>🤖 AI analyzing...</div>";

chatBox.appendChild(loading);
chatBox.scrollTop = chatBox.scrollHeight;


    






    try{


        const response =
        await fetch(

            "/ask",

            {


            method:"POST",


            headers:{


                "Content-Type":
                "application/json"


            },


            body:JSON.stringify({

                question:question,

                chat_id:currentChatId

            })


            }

        );




        const data =
        await response.json();

        if (!response.ok) {
    throw new Error(data.detail || "Request failed");
}




        loading.className = "message bot";

loading.innerHTML = `
    <div class="message-text">${data.answer}</div>
    <button class="copy-btn">📋 Copy</button>
`;

loading.querySelector(".copy-btn").onclick = function () {

    navigator.clipboard.writeText(data.answer);

    this.innerText = "✅ Copied";

    setTimeout(() => {

        this.innerText = "📋 Copy";

    }, 1500);

};



        loadHistory();


    }



    catch(error){

loading.className = "message bot";
loading.innerHTML = `
<div class="message-text">
❌ Something went wrong
</div>
`;


    }


}









// ======================================
// LOAD HISTORY
// ======================================


async function loadHistory(){


    try{


        const response =
        await fetch(
            "/history"
        );



        const data =
        await response.json();



        historyList.innerHTML="";




        if(data.chats.length===0){


            historyList.innerHTML =
            `

            <p>
            No conversations yet
            </p>

            `;


            return;


        }





        data.chats.forEach(chat=>{



            const item =
            document.createElement("div");



            item.className =
            "history-item";



            item.innerHTML =


            `

            <span>
            📄 ${chat.filename}
            </span>


            <button class="delete-btn">
            🗑️
            </button>


            `;



            item.onclick=()=>{

                openChat(chat.id);

            };




            const deleteBtn =
            item.querySelector(".delete-btn");



            deleteBtn.onclick=(e)=>{


                e.stopPropagation();


                deleteChat(chat.id);


            };



            historyList.appendChild(item);



        });



    }


    catch(error){

        console.log(
            "History error",
            error
        );

    }


}









// ======================================
// OPEN CHAT
// ======================================


async function openChat(id){


    const response =
    await fetch(

        `/history/${id}`

    );



    const chat =
    await response.json();




    currentChatId=id;



    localStorage.setItem(

        "currentChatId",

        id

    );




    clearChat();




    chat.messages.forEach(msg=>{


        addMessage(

            msg.content,


            msg.role==="user"

            ?

            "user"

            :

            "bot"


        );


    });



}









// ======================================
// DELETE CHAT
// ======================================


async function deleteChat(id){



    await fetch(

        `/history/${id}`,

        {

            method:"DELETE"

        }

    );




    if(id===currentChatId){


        currentChatId=null;


        localStorage.removeItem(
            "currentChatId"
        );


        clearChat();


    }




    loadHistory();


}









// ======================================
// NEW CHAT
// ======================================


newChatBtn.onclick=function(){



    currentChatId=null;



    localStorage.removeItem(

        "currentChatId"

    );



    pdfFile.value="";



    clearChat();



};


// ======================================
// EXPORT CHAT
// ======================================

exportBtn.onclick = function () {

    if (!currentChatId) {

        alert("Open or upload a report first");

        return;

    }

    // Export as PDF
    window.location.href = `/export/${currentChatId}/pdf`;

    // If you want TXT instead, use:
    // window.location.href = `/export/${currentChatId}/txt`;

};


// ======================================
// LOGOUT
// ======================================
// ======================================
// LOGOUT
// ======================================

logoutBtn.onclick = function () {

    const confirmLogout = confirm("Do you want to logout?");

    if (!confirmLogout) return;


    localStorage.removeItem("username");
    localStorage.removeItem("currentChatId");


    window.location.href = "/logout";

};








// ======================================
// CLEAR CHAT
// ======================================


function clearChat(){



    chatBox.innerHTML =


    `

    <div class="welcome">


        <h2>
        Welcome 👋
        </h2>



        <p>

        Upload a medical report and ask questions about it.

        </p>


    </div>

    `;


}









// ======================================
// QUICK ACTIONS
// ======================================


function askQuick(question){


    questionInput.value =
    question;


    askQuestion();


}