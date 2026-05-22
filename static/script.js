let btn = document.getElementById("btn")

let updatebtn = document.getElementById("updatebtn")

let viewtask = document.querySelector(".view-task")

let currentid = null

// STORE TASKS TEMPORARILY
let tasks = []

// ---------------- GET TOKEN ----------------

let token = localStorage.getItem("token")

console.log("TOKEN :", token)

// IF TOKEN DOESN'T EXIST
if (!token) {

    alert("Please login first")

    window.location.href = "/signin"
}


// ---------------- ADD TASK ----------------
btn.addEventListener("click", async () => {

    let title = document.getElementById("title").value

    let note = document.getElementById("note").value

    // ALWAYS FALSE FOR NEW TASK
    let status = false

    if (title.trim() === "") {

        alert("Title is required")

        return
    }

    try {

        let response = await fetch("/addtask", {

            method: "POST",

            headers: {

                "Content-Type": "application/json",

                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({

                title,

                note,

                status
            })
        })

        let data = await response.json()


        document.getElementById("title").value = ""

        document.getElementById("note").value = ""

        GetTasks()

    }

    catch (error) {


    }

})

// ---------------- GET TASKS ----------------

async function GetTasks() {

    try {

        let response = await fetch("/tasks", {

            method: "GET",

            headers: {

                "Authorization": `Bearer ${token}`
            }

        })

        // UNAUTHORIZED
        if (response.status === 401) {

            alert("Please login again")

            localStorage.removeItem("token")

            window.location.href = "/signin"

            return
        }

        tasks = await response.json()


        // SAFETY CHECK
        if (!Array.isArray(tasks)) {


            return
        }

        viewtask.innerHTML = ""

       tasks.forEach((task) => {

    viewtask.innerHTML += `

    <div class="task">

        <div class="top-section">

            <input
                type="checkbox"
                ${task.status ? "checked" : ""}
                onchange="toggleStatus(${task.id}, this)"
            >

            <div class="task-p">
                <p class="${task.status ? 'completed' : ''}">
                    ${task.title}
                </p>
            </div>

            <div>

                <button
                    class="editbtn"
                    onclick="edittask(${task.id})">
                    Edit
                </button>

                <button
                    class="delbtn"
                    onclick="deletetask(${task.id})">
                    Delete
                </button>

            </div>

        </div>

        <div class="notes"></div>

    </div>
    `
})


// SELECT ALL TASKS
let allTasks = document.querySelectorAll(".task")

allTasks.forEach((taskBox, index) => {

    let taskword = taskBox.querySelector(".task-p")

    let notes = taskBox.querySelector(".notes")

    taskword.addEventListener("click", () => {

        if (taskBox.classList.contains("expand")) {

            taskBox.classList.remove("expand")

            notes.innerHTML = ""

        }

        else {

            taskBox.classList.add("expand")

            notes.innerHTML = `

            <div class="note-content">

                Notes:

                <p style="margin:10px 0">
                    ${tasks[index].note}
                </p>

            </div>
            `
        }

    })

})
 

    }

    catch (error) {


    }
}

GetTasks()


// ---------------- EDIT TASK ----------------
function edittask(id) {

    let task = tasks.find(t => t.id === id)

    if (!task) return

    document.getElementById("title").value = task.title

    document.getElementById("note").value = task.note

    currentid = id

    btn.style.display = "none"

    updatebtn.style.display = "inline-block"
}


// ---------------- UPDATE BUTTON ----------------

updatebtn.addEventListener("click", () => {

    updatetask()
})


// ---------------- UPDATE TASK ----------------
async function updatetask() {

    let title = document.getElementById("title").value

    let note = document.getElementById("note").value

    let task = tasks.find(t => t.id === currentid)

    let status = task.status

    await fetch(`/tasks/${currentid}`, {

        method: "PUT",

        headers: {

            "Content-Type": "application/json",

            "Authorization": `Bearer ${token}`
        },

        body: JSON.stringify({

            title,

            note,

            status
        })

    })

    document.getElementById("title").value = ""

    document.getElementById("note").value = ""

    btn.style.display = "inline-block"

    updatebtn.style.display = "none"

    GetTasks()
}

// ---------------- DELETE TASK ----------------

async function deletetask(id) {

    try {

        let response = await fetch(`/tasks/${id}`, {

            method: "DELETE",

            headers: {

                "Authorization": `Bearer ${token}`
            }

        })

        let data = await response.json()


        GetTasks()

    }

    catch (error) {


    }
}


// ---------------- TOGGLE STATUS ----------------

async function toggleStatus(id, checkbox) {

    let task = tasks.find(t => t.id === id)

    if (!task) return

    let newStatus = checkbox.checked

    try {

        await fetch(`/tasks/${id}`, {

            method: "PUT",

            headers: {

                "Content-Type": "application/json",

                "Authorization": `Bearer ${token}`
            },

            body: JSON.stringify({

                title: task.title,

                note: task.note,

                status: newStatus
            })

        })

        GetTasks()

    }

    catch (error) {


    }
}

// ------------view task ------------