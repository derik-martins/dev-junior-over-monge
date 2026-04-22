const taskForm = document.querySelector("#task-form");
const taskList = document.querySelector("#task-list");
const summaryCards = document.querySelector("#summary-cards");
const reloadButton = document.querySelector("#reload-button");
const errorBox = document.querySelector("#error-box");

document.addEventListener("DOMContentLoaded", () => {
    bindEvents();
    loadDashboard();
});

function bindEvents() {
    taskForm.addEventListener("submit", handleCreateTask);
    reloadButton.addEventListener("click", loadDashboard);
    taskList.addEventListener("click", handleTaskClick);
    taskList.addEventListener("change", handleTaskChange);
}

async function loadDashboard() {
    try {
        setError("");
        renderLoadingState();

        const [tasksResponse, summaryResponse] = await Promise.all([
            request("/api/tasks"),
            request("/api/tasks/summary"),
        ]);

        renderSummary(summaryResponse);
        renderTasks(tasksResponse.items);
    } catch (error) {
        renderTasks([]);
        renderSummary();
        setError(error.message);
    }
}

async function handleCreateTask(event) {
    event.preventDefault();
    const formData = new FormData(taskForm);
    const payload = {
        title: formData.get("title"),
        description: formData.get("description"),
        priority: formData.get("priority"),
    };

    try {
        setError("");
        await request("/api/tasks", {
            method: "POST",
            body: JSON.stringify(payload),
        });
        taskForm.reset();
        taskForm.priority.value = "medium";
        await loadDashboard();
    } catch (error) {
        setError(error.message);
    }
}

async function handleTaskClick(event) {
    const button = event.target.closest("[data-action='delete']");
    if (!button) {
        return;
    }

    try {
        setError("");
        await request(`/api/tasks/${button.dataset.taskId}`, {
            method: "DELETE",
        });
        await loadDashboard();
    } catch (error) {
        setError(error.message);
    }
}

async function handleTaskChange(event) {
    const select = event.target.closest("[data-action='status']");
    if (!select) {
        return;
    }

    try {
        setError("");
        await request(`/api/tasks/${select.dataset.taskId}/status`, {
            method: "PATCH",
            body: JSON.stringify({ status: select.value }),
        });
        await loadDashboard();
    } catch (error) {
        setError(error.message);
    }
}

function renderSummary(summary = defaultSummary()) {
    const cards = [
        { label: "Total", value: summary.total },
        { label: "A fazer", value: summary.by_status.todo },
        { label: "Em andamento", value: summary.by_status.doing },
        { label: "Concluidas", value: summary.by_status.done },
    ];

    summaryCards.innerHTML = cards
        .map(
            (card) => `
                <div class="col-sm-6 col-xl-3">
                    <div class="summary-card h-100">
                        <span class="label">${card.label}</span>
                        <strong class="value">${card.value}</strong>
                    </div>
                </div>
            `
        )
        .join("");
}

function renderTasks(tasks) {
    if (!tasks.length) {
        taskList.innerHTML = `
            <div class="col-12">
                <div class="empty-state">
                    Nenhuma tarefa cadastrada ate o momento.
                </div>
            </div>
        `;
        return;
    }

    taskList.innerHTML = tasks
        .map(
            (task) => `
                <div class="col-md-6 col-xl-4">
                    <article class="task-card p-4">
                        <div class="d-flex justify-content-between gap-3 mb-3">
                            <div>
                                <h3 class="h5 mb-1">${escapeHtml(task.title)}</h3>
                                <span class="badge badge-priority rounded-pill text-uppercase">${task.priority}</span>
                            </div>
                            <button
                                class="btn btn-sm btn-outline-danger"
                                data-action="delete"
                                data-task-id="${task.id}"
                                type="button"
                            >
                                Remover
                            </button>
                        </div>
                        <p class="mb-3">${escapeHtml(task.description || "Sem descricao.")}</p>
                        <label class="form-label" for="status-${task.id}">Status</label>
                        <select
                            class="form-select mb-3"
                            id="status-${task.id}"
                            data-action="status"
                            data-task-id="${task.id}"
                        >
                            ${renderStatusOptions(task.status)}
                        </select>
                        <div class="task-meta">
                            Atualizada em ${formatDate(task.updated_at)}
                        </div>
                    </article>
                </div>
            `
        )
        .join("");
}

function renderLoadingState() {
    taskList.innerHTML = `
        <div class="col-12">
            <div class="empty-state">Carregando painel...</div>
        </div>
    `;
}

function renderStatusOptions(currentStatus) {
    const options = [
        { value: "todo", label: "A fazer" },
        { value: "doing", label: "Em andamento" },
        { value: "done", label: "Concluida" },
    ];

    return options
        .map((option) => {
            const selected = option.value === currentStatus ? "selected" : "";
            return `<option value="${option.value}" ${selected}>${option.label}</option>`;
        })
        .join("");
}

async function request(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });
    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Falha ao processar a requisicao.");
    }

    return data;
}

function setError(message) {
    if (!message) {
        errorBox.textContent = "";
        errorBox.classList.add("d-none");
        return;
    }

    errorBox.textContent = message;
    errorBox.classList.remove("d-none");
}

function defaultSummary() {
    return {
        total: 0,
        by_status: {
            todo: 0,
            doing: 0,
            done: 0,
        },
    };
}

function formatDate(dateValue) {
    const date = new Date(dateValue);
    if (Number.isNaN(date.getTime())) {
        return dateValue;
    }
    return date.toLocaleString("pt-BR");
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}
