def test_healthcheck_returns_api_identity(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {
        "service": "junior-challenge-api",
        "status": "ok",
    }


def test_create_and_list_tasks(client):
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Criar o fluxo principal",
            "description": "Implementar tela inicial e cadastro.",
            "priority": "medium",
        },
    )

    list_response = client.get("/api/tasks")
    created_task = create_response.get_json()
    items = list_response.get_json()["items"]

    assert create_response.status_code == 201
    assert created_task["title"] == "Criar o fluxo principal"
    assert len(items) == 1
    assert items[0]["id"] == created_task["id"]


def test_get_missing_task_returns_404(client):
    response = client.get("/api/tasks/nao-existe")

    assert response.status_code == 404
    assert response.get_json()["error"] == "Tarefa nao encontrada."


def test_update_status_and_summary(client):
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Fechar checklist",
            "priority": "high",
        },
    )
    task_id = create_response.get_json()["id"]

    patch_response = client.patch(
        f"/api/tasks/{task_id}/status",
        json={"status": "done"},
    )
    summary_response = client.get("/api/tasks/summary")

    assert patch_response.status_code == 200
    assert patch_response.get_json()["status"] == "done"
    assert summary_response.get_json()["by_status"]["done"] == 1


def test_delete_task_returns_success_message(client):
    create_response = client.post(
        "/api/tasks",
        json={
            "title": "Excluir tarefa temporaria",
            "priority": "low",
        },
    )
    task_id = create_response.get_json()["id"]

    delete_response = client.delete(f"/api/tasks/{task_id}")
    list_response = client.get("/api/tasks")

    assert delete_response.status_code == 200
    assert delete_response.get_json()["message"] == "Tarefa removida com sucesso."
    assert list_response.get_json()["items"] == []
