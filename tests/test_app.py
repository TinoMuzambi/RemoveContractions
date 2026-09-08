from app import MAX_TEXT_LENGTH, app, expand_contractions


def test_expands_contractions_and_preserves_layout():
    result, count = expand_contractions("I’m ready.\nYou can't stop us!")

    assert result == "I am ready.\nYou cannot stop us!"
    assert count == 2


def test_preserves_possessives_and_unknown_apostrophes():
    result, count = expand_contractions("Tino's laptop and the developers' notes")

    assert result == "Tino's laptop and the developers' notes"
    assert count == 0


def test_preserves_case():
    result, count = expand_contractions("IT'S DONE, but That's fine.")

    assert result == "IT IS DONE, but That is fine."
    assert count == 2


def test_longest_contractions_are_matched_first():
    result, count = expand_contractions("I couldn't've known.")

    assert result == "I could not have known."
    assert count == 1


def test_home_page_and_security_headers():
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert "Say it in full" in response.text
    assert "frame-ancestors 'none'" in response.headers["Content-Security-Policy"]
    assert response.headers["X-Content-Type-Options"] == "nosniff"


def test_valid_submission():
    response = app.test_client().post("/", data={"uncontracted": "We're ready."})

    assert response.status_code == 200
    assert "We are ready." in response.text
    assert "1 replacement" in response.text


def test_empty_submission_is_rejected():
    response = app.test_client().post("/", data={"uncontracted": ""})

    assert response.status_code == 200
    assert "Enter some text to expand." in response.text


def test_oversized_submission_is_rejected():
    response = app.test_client().post(
        "/", data={"uncontracted": "a" * (MAX_TEXT_LENGTH + 1)}
    )

    assert response.status_code == 200
    assert "Keep the text under 50,000 characters." in response.text


def test_health_endpoint():
    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.json == {"status": "ok"}
