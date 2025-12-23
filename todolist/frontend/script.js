const API_URL = "http://127.0.0.1:8000/todos";

const form = document.getElementById("todoForm");
const todoList = document.getElementById("todoList");

// Fetch Todos
async function fetchTodos() {
    const response = await fetch(API_URL);
    const todos = await response.json();

    todoList.innerHTML = "";
    todos.forEach(todo => {
        const div = document.createElement("div");
        div.className = "todo-item";

        div.innerHTML = `
            <h3>${todo.title}</h3>
            <p>${todo.description}</p>
            <button class="complete" onclick="toggleComplete(${todo.id}, ${todo.completed})">
                ${todo.completed ? "Completed" : "Mark Complete"}
            </button>
            <button class="delete" onclick="deleteTodo(${todo.id})">Delete</button>
        `;

        todoList.appendChild(div);
    });
}

// Create Todo
form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const title = document.getElementById("title").value;
    const description = document.getElementById("description").value;

    await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title, description })
    });

    form.reset();
    fetchTodos();
});

// Delete Todo
async function deleteTodo(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });
    fetchTodos();
}

// Update Todo (Complete)
async function toggleComplete(id, completed) {
    const response = await fetch(`${API_URL}/${id}`);
    const todo = await response.json();

    await fetch(`${API_URL}/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: todo.title,
            description: todo.description,
            completed: !completed
        })
    });

    fetchTodos();
}

// Initial Load
fetchTodos();
