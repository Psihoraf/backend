async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2024-08-01",
            "date_to": "2024-08-10",
        }
    )
    print(f"{response.json()}")

    assert response.status_code == 200

async def test_get_facilities(ac):
    response = await ac.get(
        "/facilities",
        params=None
    )

    print(f"{response.json()}")

    assert response.status_code == 200

async def test_add_facilities(ac):
    facility_title = "Интернет"
    response = await ac.post(
        "/facilities",
        json={
            "title": facility_title
        }
    )
    assert response.status_code == 200
    result = response.json()
    print(f"{result }")

    assert isinstance(result, dict)
    assert result["data"]["title"] == facility_title
    assert "data" in result