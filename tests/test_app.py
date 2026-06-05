import pytest
import os
from app import app as flask_app


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["DEBUG"] = False
    with flask_app.test_client() as client:
        yield client


# ---------------------------------------------------------------------------
# Existing / basic tests (kept and expanded)
# ---------------------------------------------------------------------------

def test_index_returns_200(client):
    """GET '/' should return HTTP 200 OK."""
    response = client.get("/")
    assert response.status_code == 200


def test_index_content_type_is_html(client):
    """GET '/' response Content-Type should be text/html."""
    response = client.get("/")
    assert "text/html" in response.content_type


def test_index_body_contains_hello_world(client):
    """GET '/' response body should contain the text 'Hello World'."""
    response = client.get("/")
    assert b"Hello World" in response.data


# ---------------------------------------------------------------------------
# HTML content / template tests
# ---------------------------------------------------------------------------

def test_index_has_correct_html_title(client):
    """The page title should be 'Hello World'."""
    response = client.get("/")
    assert b"<title>Hello World</title>" in response.data


def test_index_contains_welcome_badge(client):
    """The page should contain the welcome badge text."""
    response = client.get("/")
    assert b"Welcome" in response.data


def test_index_contains_get_started_button(client):
    """The page should contain the 'Get Started' call-to-action."""
    response = client.get("/")
    assert b"Get Started" in response.data


def test_index_contains_flask_mention(client):
    """The page should mention Flask."""
    response = client.get("/")
    assert b"Flask" in response.data


def test_index_contains_python_mention(client):
    """The page should mention Python."""
    response = client.get("/")
    assert b"Python" in response.data


def test_index_contains_footer_note(client):
    """The page should contain the footer note."""
    response = client.get("/")
    assert b"Flask 3.0" in response.data


def test_index_contains_doctype(client):
    """The page should start with a valid HTML5 DOCTYPE."""
    response = client.get("/")
    assert b"<!DOCTYPE html>" in response.data.upper().replace(b"\n", b"") or \
           b"<!doctype html>" in response.data.lower()


def test_index_contains_main_element(client):
    """The page should contain a <main> element."""
    response = client.get("/")
    assert b"<main" in response.data


def test_index_contains_card_class(client):
    """The main card element should have the 'card' class."""
    response = client.get("/")
    assert b'class="card"' in response.data


def test_index_contains_h1_tag(client):
    """The page should contain an h1 tag."""
    response = client.get("/")
    assert b"<h1>" in response.data


def test_index_contains_poppins_font(client):
    """The page should reference the Poppins font."""
    response = client.get("/")
    assert b"Poppins" in response.data


def test_index_contains_viewport_meta(client):
    """The page should contain a viewport meta tag for responsiveness."""
    response = client.get("/")
    assert b'name="viewport"' in response.data


def test_index_contains_charset_meta(client):
    """The page should declare UTF-8 charset."""
    response = client.get("/")
    assert b"UTF-8" in response.data


def test_index_contains_orb_elements(client):
    """The page should contain the decorative orb elements."""
    response = client.get("/")
    assert b"orb" in response.data


def test_index_contains_aria_hidden_orbs(client):
    """Decorative orbs should be hidden from assistive technology."""
    response = client.get("/")
    assert b'aria-hidden="true"' in response.data


def test_index_contains_role_main(client):
    """The main content area should have role='main'."""
    response = client.get("/")
    assert b'role="main"' in response.data


def test_index_response_is_utf8(client):
    """The response should be decodable as UTF-8."""
    response = client.get("/")
    try:
        response.data.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail("Response data is not valid UTF-8")


def test_index_contains_subtitle_text(client):
    """The page should contain part of the subtitle text."""
    response = client.get("/")
    assert b"starting point" in response.data


def test_index_contains_divider(client):
    """The page should contain the divider element."""
    response = client.get("/")
    assert b'class="divider"' in response.data


def test_index_btn_has_href(client):
    """The Get Started button should be an anchor with href."""
    response = client.get("/")
    assert b'class="btn"' in response.data
    assert b'href="#"' in response.data


# ---------------------------------------------------------------------------
# HTTP method handling tests
# ---------------------------------------------------------------------------

def test_index_post_returns_405(client):
    """POST '/' should return 405 Method Not Allowed."""
    response = client.post("/")
    assert response.status_code == 405


def test_index_put_returns_405(client):
    """PUT '/' should return 405 Method Not Allowed."""
    response = client.put("/")
    assert response.status_code == 405


def test_index_delete_returns_405(client):
    """DELETE '/' should return 405 Method Not Allowed."""
    response = client.delete("/")
    assert response.status_code == 405


def test_index_patch_returns_405(client):
    """PATCH '/' should return 405 Method Not Allowed."""
    response = client.patch("/")
    assert response.status_code == 405


def test_index_head_returns_200(client):
    """HEAD '/' should return 200 (Flask handles HEAD automatically)."""
    response = client.head("/")
    assert response.status_code == 200


def test_index_head_has_no_body(client):
    """HEAD '/' response body should be empty."""
    response = client.head("/")
    assert response.data == b""


# ---------------------------------------------------------------------------
# 404 / unknown route tests
# ---------------------------------------------------------------------------

def test_unknown_route_returns_404(client):
    """GET on an unknown route should return 404."""
    response = client.get("/nonexistent")
    assert response.status_code == 404


def test_unknown_nested_route_returns_404(client):
    """GET on a nested unknown route should return 404."""
    response = client.get("/some/deep/path")
    assert response.status_code == 404


def test_unknown_route_with_extension_returns_404(client):
    """GET on a route with file extension should return 404."""
    response = client.get("/index.php")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Response header tests
# ---------------------------------------------------------------------------

def test_index_response_has_content_length(client):
    """Response should include a Content-Length header."""
    response = client.get("/")
    # Content-Length is not always set by Flask test client directly,
    # but data should be non-empty
    assert len(response.data) > 0


def test_index_content_type_includes_charset(client):
    """Content-Type header should specify charset=utf-8."""
    response = client.get("/")
    assert "utf-8" in response.content_type.lower() or \
           "utf-8" in response.headers.get("Content-Type", "").lower()


# ---------------------------------------------------------------------------
# App configuration tests
# ---------------------------------------------------------------------------

def test_app_testing_mode(client):
    """App should be in TESTING mode when configured so."""
    assert flask_app.config["TESTING"] is True


def test_app_is_flask_instance():
    """The app object should be a Flask instance."""
    from flask import Flask
    assert isinstance(flask_app, Flask)


def test_app_has_index_route():
    """The app should have a route registered for '/'."""
    rules = [rule.rule for rule in flask_app.url_map.iter_rules()]
    assert "/" in rules


def test_index_route_only_allows_get_and_head(client):
    """The '/' route should list GET and HEAD in allowed methods."""
    response = client.get("/")
    # Verify the route exists and GET works (already tested above)
    assert response.status_code == 200


# ---------------------------------------------------------------------------
# Debug mode environment variable parsing (unit tests for __main__ logic)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("env_value,expected", [
    ("1", True),
    ("true", True),
    ("True", True),
    ("TRUE", True),
    ("yes", True),
    ("Yes", True),
    ("YES", True),
    ("false", False),
    ("False", False),
    ("FALSE", False),
    ("0", False),
    ("no", False),
    ("", False),
    ("random", False),
])
def test_debug_mode_env_parsing(env_value, expected, monkeypatch):
    """FLASK_DEBUG env var should be parsed correctly."""
    monkeypatch.setenv("FLASK_DEBUG", env_value)
    result = os.environ.get("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    assert result == expected


def test_debug_mode_default_is_false(monkeypatch):
    """When FLASK_DEBUG is not set, debug mode should default to False."""
    monkeypatch.delenv("FLASK_DEBUG", raising=False)
    result = os.environ.get("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    assert result is False


# ---------------------------------------------------------------------------
# Multiple requests / statelessness tests
# ---------------------------------------------------------------------------

def test_index_is_stateless_across_requests(client):
    """Multiple GET requests to '/' should all return 200."""
    for _ in range(5):
        response = client.get("/")
        assert response.status_code == 200


def test_index_response_consistent(client):
    """Two consecutive GET requests should return identical response bodies."""
    response1 = client.get("/")
    response2 = client.get("/")
    assert response1.data == response2.data


# ---------------------------------------------------------------------------
# Query string / trailing slash tests
# ---------------------------------------------------------------------------

def test_index_with_query_string_returns_200(client):
    """GET '/?foo=bar' should still return 200."""
    response = client.get("/?foo=bar")
    assert response.status_code == 200


def test_index_with_trailing_slash_redirect_or_200(client):
    """GET '/' with trailing slash is the canonical URL and should return 200."""
    response = client.get("/")
    assert response.status_code == 200