import subprocess
import time
import os
import pytest
from playwright.sync_api import Page

from .test_builds import validate_mkdocs_file

pytestmark = pytest.mark.e2e

MKDOCS_URL = "http://localhost:8000"
PATHS = ["index.html", "build_in_multiple/index.html", "empty/index.html", "multiple/index.html", "oauth2/index.html", "options/index.html", "url/index.html", "sub_dir/page_in_sub_dir/index.html"]

@pytest.fixture(scope="session", autouse=True)
def start_mkdocs_server(tmp_path_factory):
    """ Start a local server to serve the MkDocs site """

    tmp_path = tmp_path_factory.mktemp("mkdocs_test")
    mkdocs_file = "mkdocs-material.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")

    process = subprocess.Popen(["uv", "run", "-m", "http.server", "-d", os.path.join(testproject_path, "site")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)  # wait for server to start

    yield

    process.terminate()
    process.wait()

@pytest.fixture
def page_context(page: Page):
    """
    Create a new page context with a longer timeout
    """
    page.set_default_timeout(5000)
    return page

@pytest.mark.parametrize("path", PATHS)
def test_no_console_errors(page_context: Page, path):
    """
    Validate that there are no console errors
    """
    url = f"{MKDOCS_URL}/{path}"
    errors = []
    
    page_context.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
    page_context.goto(url)

    assert not errors, f"Got {len(errors)} console errors: {errors}"

@pytest.mark.parametrize("path", PATHS)
def test_mkdocs_screenshot(page_context: Page, path):
    """
    Take a screenshot of the MkDocs
    """
    url = f"{MKDOCS_URL}/{path}"

    page_context.goto(url)
    time.sleep(3)
    screenshot_path = f"playwright-results/{path.replace('/', '_')}.png"
    page_context.screenshot(path=screenshot_path, full_page=True)
