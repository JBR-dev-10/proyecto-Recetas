from app.services import llm_service

def register_and_login(client, email="chef@ejemplo.com", password="Password123!"):
    reg_res = client.post("/auth/register", json={"email": email, "password": password})
    assert reg_res.status_code == 201

    login_res = client.post(
        "/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_health_and_panel_routes(client):
    assert client.get("/health").status_code == 200
    assert client.get("/").status_code == 200
    assert client.get("/panel").status_code == 200

def test_auth_and_ingredients_crud(client):
    headers = register_and_login(client)

    # Crear ingrediente
    create_res = client.post(
        "/ingredients/",
        json={"nombre": "Arroz", "cantidad": 2.0, "unidad": "tazas"},
        headers=headers,
    )
    assert create_res.status_code == 201
    ing_id = create_res.json()["id"]

    # Listar ingredientes
    list_res = client.get("/ingredients/", headers=headers)
    assert list_res.status_code == 200
    assert len(list_res.json()) == 1

    # Actualizar ingrediente
    upd_res = client.put(
        f"/ingredients/{ing_id}",
        json={"cantidad": 3.5},
        headers=headers,
    )
    assert upd_res.status_code == 200
    assert upd_res.json()["cantidad"] == 3.5

    # Eliminar ingrediente
    del_res = client.delete(f"/ingredients/{ing_id}", headers=headers)
    assert del_res.status_code == 204

def test_recipe_generation_and_rating(client, monkeypatch):
    headers = register_and_login(client, email="cocinero@ejemplo.com")

    client.post(
        "/ingredients/",
        json={"nombre": "Huevo", "cantidad": 3, "unidad": "unidades"},
        headers=headers,
    )

    def fake_generate(ingredients, preferences=None):
        return {
            "nombre_plato": "Tortilla rápida",
            "ingredientes_json": [{"nombre": "Huevo", "cantidad": "3 unidades"}],
            "pasos_json": ["Batir los huevos", "Cocinar en sartén"],
            "tiempo_estimado": "10 minutos",
            "dificultad": "Fácil",
        }

    monkeypatch.setattr("app.routers.recipes.generate_recipe_from_ingredients", fake_generate)

    gen_res = client.post(
        "/recipes/generate",
        json={"preferencias": "rápida", "usar_inventario": True},
        headers=headers,
    )
    assert gen_res.status_code == 201
    recipe_id = gen_res.json()["id"]
    assert gen_res.json()["nombre_plato"] == "Tortilla rápida"

    # Calificar receta
    rate_res = client.post(
        f"/recipes/{recipe_id}/ratings/",
        json={"puntuacion": 5, "comentario": "Muy buena"},
        headers=headers,
    )
    assert rate_res.status_code == 201
    assert rate_res.json()["puntuacion"] == 5