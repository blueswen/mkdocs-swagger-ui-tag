# standard lib
import logging
import os
import re
import shutil
from pathlib import Path
from unittest.mock import MagicMock

# other 3rd party
from bs4 import BeautifulSoup
from click.testing import CliRunner

# MkDocs
from mkdocs.__main__ import build_command

# ##################################
# ######## Globals #################
# ##################################

# custom log level to get plugin info messages
logging.basicConfig(level=logging.INFO)

# ##################################
# ########## Helpers ###############
# ##################################


def setup_clean_mkdocs_folder(
    mkdocs_yml_path: str, output_path: str, docs_path: str = "tests/fixtures/docs"
):
    """
    Sets up a clean mkdocs directory
    outputpath/testproject
    ├── docs/
    └── mkdocs.yml
    Args:
        mkdocs_yml_path (str): Path of mkdocs.yml file to use
        output_path (str): Path of folder in which to create mkdocs project
    Returns:
        testproject_path (str): Path to test project
    """

    testproject_path = os.path.join(output_path, "testproject")

    # Create empty 'testproject' folder
    if os.path.exists(str(testproject_path)):
        logging.warning(
            """This command does not work on windows.
        Refactor your test to use setup_clean_mkdocs_folder() only once"""
        )
        shutil.rmtree(str(testproject_path))

    # Copy correct mkdocs.yml file and our test 'docs/'
    shutil.copytree(docs_path, os.path.join(testproject_path, docs_path.split("/")[-1]))

    shutil.copyfile(mkdocs_yml_path, os.path.join(testproject_path, "mkdocs.yml"))

    return testproject_path


def build_docs_setup(testproject_path: str):
    """
    Runs the `mkdocs build` command
    Args:
        testproject_path (Path): Path to test project
    Returns:
        command: Object with results of command
    """

    # TODO: Try specifying path in CliRunner, this function could be one-liner
    cwd = os.getcwd()
    os.chdir(str(testproject_path))

    try:
        runner = CliRunner()
        run = runner.invoke(build_command)
        os.chdir(cwd)
        return run
    except:
        os.chdir(cwd)
        raise


def validate_build(testproject_path: str, plugin_config: dict = {}):
    """
    Validates a build from a testproject
    Args:
        testproject_path (Path): Path to test project
    """
    assert os.path.exists(os.path.join(testproject_path, "site"))

    # Make sure index file exists
    index_file = os.path.join(testproject_path, "site/index.html")
    assert os.path.exists(index_file), "%s does not exist" % index_file


def validate_mkdocs_file(
    temp_path: str, mkdocs_yml_file: str, docs_path: str = "tests/fixtures/docs"
):
    """
    Creates a clean mkdocs project
    for a mkdocs YML file, builds and validates it.
    Args:
        temp_path (PosixPath): Path to temporary folder
        mkdocs_yml_file (PosixPath): Path to mkdocs.yml file
    """
    testproject_path = setup_clean_mkdocs_folder(
        mkdocs_yml_path=mkdocs_yml_file, output_path=temp_path, docs_path=docs_path
    )
    result = build_docs_setup(
        str(testproject_path),
    )
    assert result.exit_code == 0, "'mkdocs build' command failed"

    # validate build with locale retrieved from mkdocs config file
    validate_build(testproject_path)

    return Path(testproject_path)


def validate_iframe(html_content, iframe_src_dir):
    """
    Validate target iframe html exist
    """
    iframe_content_list = []
    # <iframe class="swagger-ui-iframe" frameborder="0" id="767c835c" src="swagger-767c835c.html" style="overflow: hidden; width: 100%; height: 868px;" width="100%" height="868px"></iframe>
    iframe_list = re.findall(
        r'<iframe class="swagger-ui-iframe" .*><\/iframe>',
        html_content,
    )
    validate_additional_script_code(html_content)
    iframe_id_list = []
    for iframe in iframe_list:
        iframe_tag = BeautifulSoup(iframe, "html.parser").iframe
        iframe_id = iframe_tag.attrs.get("id")
        iframe_src = iframe_tag.attrs.get("src")
        assert iframe_id is not None
        assert iframe_src is not None
        assert f"swagger-{iframe_id}.html" == iframe_src
        iframe_file = iframe_src_dir / iframe_src
        assert iframe_file.exists()
        iframe_content = iframe_file.read_text(encoding="utf8")
        assert (
            f'parent.update_swagger_ui_iframe_height("{iframe_id}");' in iframe_content
        )
        iframe_content_list.append(iframe_content)
        iframe_id_list.append(iframe_id)

    return iframe_content_list


def validate_additional_script_code(html_content, exists=True):
    assert exists == ("window.update_swagger_ui_iframe_height" in html_content)
    assert exists == (
        "document.addEventListener('scroll', function(e) {" in html_content
    )


def validate_additional_script_code_for_material(html_content, exists=True):
    assert exists == (
        'const schemeAttr = document.body.getAttribute("data-md-color-scheme")'
        in html_content
    )
    assert exists == (
        """document$.subscribe(() => {
            window.update_swagger_ui_iframe_height = function (id) {"""
        in html_content
    )


def validate_default_oauth2_html(iframe_contents, iframe_src_dir):
    regex_obj = re.search(
        r'"oauth2RedirectUrl": .*"(.*)".*,',
        iframe_contents,
    )
    assert regex_obj
    oauth2_url = regex_obj.group(1)
    assert (iframe_src_dir / oauth2_url).resolve().exists()


# ##################################
# ########### Tests ################
# ##################################


def test_basic(tmp_path):
    """
    Minimal sample
    """
    mkdocs_file = "mkdocs.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/index.html"
    contents = file.read_text(encoding="utf8")
    validate_additional_script_code_for_material(contents, exists=False)

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1
    iframe_contents = iframe_content_list[0]

    # validate OpenAPI spec exist
    regex_obj = re.search(
        r'url: "(.*)"',
        iframe_contents,
    )
    assert regex_obj
    openapi_spec_url = regex_obj.group(1)
    assert (file.parent / openapi_spec_url).resolve().exists()

    validate_default_oauth2_html(iframe_contents, file.parent)


def test_basic_sub_dir(tmp_path):
    """
    Minimal sample
    """
    mkdocs_file = "mkdocs.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/sub_dir/page_in_sub_dir/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1
    iframe_contents = iframe_content_list[0]

    # validate OpenAPI spec exists
    regex_obj = re.search(
        r'url: "(.*)"',
        iframe_contents,
    )
    assert regex_obj
    openapi_spec_url = regex_obj.group(1)
    assert (file.parent / openapi_spec_url).resolve().exists()

    validate_default_oauth2_html(iframe_contents, file.parent)


def test_use_directory_urls(tmp_path):
    """
    Compatible with use_directory_urls is false or with --use-directory-urls and --use-directory-urls as args
    https://www.mkdocs.org/user-guide/configuration/#use_directory_urls
    https://www.mkdocs.org/user-guide/cli/
    """
    mkdocs_file = "mkdocs-target-file.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1
    iframe_contents = iframe_content_list[0]

    # validate OpenAPI spec exist
    regex_obj = re.search(
        r'url: "(.*)"',
        iframe_contents,
    )
    assert regex_obj
    openapi_spec_url = regex_obj.group(1)
    assert (file.parent / openapi_spec_url).resolve().exists()

    validate_default_oauth2_html(iframe_contents, file.parent)


def test_use_directory_urls_sub_dir(tmp_path):
    """
    Compatible with use_directory_urls is false or with --use-directory-urls and --use-directory-urls as args
    https://www.mkdocs.org/user-guide/configuration/#use_directory_urls
    https://www.mkdocs.org/user-guide/cli/
    """
    mkdocs_file = "mkdocs-target-file.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/sub_dir/page_in_sub_dir.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1
    iframe_contents = iframe_content_list[0]

    # validate OpenAPI spec exist
    regex_obj = re.search(
        r'url: "(.*)"',
        iframe_contents,
    )
    assert regex_obj
    openapi_spec_url = regex_obj.group(1)
    assert (file.parent / openapi_spec_url).resolve().exists()

    validate_default_oauth2_html(iframe_contents, file.parent)


def test_material(tmp_path):
    """
    Integrate with Material for MkDocs
    """
    mkdocs_file = "mkdocs-material.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/index.html"
    contents = file.read_text(encoding="utf8")
    validate_additional_script_code_for_material(contents, exists=True)
    assert 'const dark_scheme_name = "slate"' in contents

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1
    iframe_contents = iframe_content_list[0]

    # validate OpenAPI spec exist
    regex_obj = re.search(
        r'url: "(.*)"',
        iframe_contents,
    )
    assert regex_obj
    openapi_spec_url = regex_obj.group(1)
    assert (file.parent / openapi_spec_url).resolve().exists()


def test_material_dark_scheme_name(tmp_path):
    """
    Integrate with Material for MkDocs
    """
    mkdocs_file = "mkdocs-material-options.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/index.html"
    contents = file.read_text(encoding="utf8")
    validate_additional_script_code_for_material(contents, exists=True)
    assert 'const dark_scheme_name = "white"' in contents


def test_url(tmp_path):
    """
    Validate online OpenAPI Spec
    """
    mkdocs_file = "mkdocs.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/url/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1
    iframe_contents = iframe_content_list[0]

    # validate OpenAPI spec exist
    regex_obj = re.search(
        r'url: "(.*)"',
        iframe_contents,
    )
    assert regex_obj
    assert regex_obj.group(1) == "https://petstore.swagger.io/v2/swagger.json"


def test_multiple(tmp_path):
    """
    Validate multiple Swagger UI in the same page
    """
    mkdocs_file = "mkdocs.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/multiple/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 3
    for ind, iframe_contents in enumerate(iframe_content_list):
        # validate OpenAPI spec exist
        regex_obj = re.search(
            r'url: "(.*)"',
            iframe_contents,
        )
        assert regex_obj
        if ind == 0 or ind == 1:
            openapi_spec_url = regex_obj.group(1)
            assert (file.parent / openapi_spec_url).resolve().exists()
        elif ind == 2:
            assert regex_obj.group(1) == "https://petstore.swagger.io/v2/swagger.json"


def test_build_in_multiple(tmp_path):
    """
    Validate Swagger UI build-in multiple feature
    """
    mkdocs_file = "mkdocs.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/build_in_multiple/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 2
    for ind, iframe_contents in enumerate(iframe_content_list):
        if ind == 0:
            spec_url_list = re.findall(
                r'{url: "(.*)", name:"(.*)" }',
                iframe_contents,
            )
            for spec_url in spec_url_list:
                if spec_url.startswith("http"):
                    assert spec_url == "https://petstore.swagger.io/v2/swagger.json"
                else:
                    assert (file.parent / spec_url).resolve().exists()
        elif ind == 1:
            regex_obj = re.search(
                r'url: "(.*)"',
                iframe_contents,
            )
            assert regex_obj
            openapi_spec_url = regex_obj.group(1)
            assert (file.parent / openapi_spec_url).resolve().exists()


def test_oauth2_options(tmp_path):
    """
    Validate Swagger UI build-in multiple feature
    """
    mkdocs_file = "mkdocs.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/oauth2/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1
    iframe_content = iframe_content_list[0]
    oauth2_options = {
        "clientId": "your-client-id",
        "clientSecret": "your-client-secret-if-required",
        "realm": "your-realms",
        "appName": "your-app-name",
        "scopes": "openid profile",
        "additionalQueryStringParams": '{"test": "hello"}',
        "useBasicAuthenticationWithAccessCodeGrant": False,
        "usePkceWithAuthorizationCodeGrant": False,
    }
    for key, val in oauth2_options.items():
        if isinstance(val, bool):
            assert f'"{key}": {"true" if val else "false"}' in iframe_content
        elif key == "additionalQueryStringParams":
            assert f'"{key}": {val}' in iframe_content
        else:
            assert f'"{key}": "{val}"' in iframe_content


def test_plugin_options(tmp_path):
    mkdocs_file = "mkdocs-options.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1
    iframe_content = iframe_content_list[0]
    plugin_options = {
        "background": "gray",
        "docExpansion": "none",
        "filter": "Pet",
        "syntaxHighlight.theme": "monokai",
        "tryItOutEnabled": True,
        "oauth2RedirectUrl": "https://google.com",
        "validatorUrl": "https://validator.swagger.io/validator",
    }
    for key, val in plugin_options.items():
        if isinstance(val, bool):
            assert f'"{key}": {"true" if val else "false"}' in iframe_content
        elif key == "background":
            assert f"{key}: {val}" in iframe_content
        else:
            assert f'"{key}": "{val}"' in iframe_content
    assert re.search(
        r'"supportedSubmitMethods": \[(\n|\r)        "get"(\n|\r)    \]', iframe_content
    )

    assert (testproject_path / "site/stylesheets/extra-1.css").exists()
    assert (testproject_path / "site/stylesheets/sub_dir/extra-2.css").exists()
    assert '"stylesheets/extra-1.css"' in iframe_content
    assert '"stylesheets/sub_dir/extra-2.css"' in iframe_content

    file = testproject_path / "site/sub_dir/page_in_sub_dir/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1
    iframe_content = iframe_content_list[0]
    assert '"../../stylesheets/extra-1.css"' in iframe_content
    assert '"../../stylesheets/sub_dir/extra-2.css"' in iframe_content

    file = testproject_path / "site/multiple/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 3
    for iframe_content in iframe_content_list:
        assert '"../stylesheets/extra-1.css"' in iframe_content
        assert '"../stylesheets/sub_dir/extra-2.css"' in iframe_content


def test_attribute_options(tmp_path):
    mkdocs_file = "mkdocs.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/options/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1


def test_static(tmp_path):
    """
    Validate static files
    """
    mkdocs_file = "mkdocs.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    assert (testproject_path / "site/assets/swagger-ui/oauth2-redirect.html").exists()
    js_files = [
        "swagger-ui-bundle.js",
        "swagger-ui-bundle.js.map",
        "swagger-ui-standalone-preset.js",
        "swagger-ui-standalone-preset.js.map",
    ]
    for file_name in js_files:
        assert (testproject_path / "site/assets/javascripts/" / file_name).exists()
    css_files = ["swagger-ui-dark.css", "swagger-ui.css", "swagger-ui.css.map"]
    for file_name in css_files:
        assert (testproject_path / "site/assets/stylesheets/" / file_name).exists()
    assert (testproject_path / "site/assets/swagger-ui/oauth2-redirect.html").exists()


def test_empty(tmp_path):
    """
    Validate static files
    """
    mkdocs_file = "mkdocs.yml"
    testproject_path = validate_mkdocs_file(tmp_path, f"tests/fixtures/{mkdocs_file}")
    file = testproject_path / "site/empty/index.html"
    contents = file.read_text(encoding="utf8")

    validate_additional_script_code(contents, exists=False)


def test_error(tmp_path):
    mkdocs_file = "mkdocs-error.yml"
    validate_mkdocs_file(
        tmp_path, f"tests/fixtures/{mkdocs_file}", docs_path="tests/fixtures/error_docs"
    )


def test_template(tmp_path):
    mkdocs_file = "mkdocs-material-template.yml"
    testproject_path = validate_mkdocs_file(
        tmp_path,
        f"tests/fixtures/{mkdocs_file}",
        docs_path="tests/fixtures/template_docs",
    )
    file = testproject_path / "site/index.html"
    contents = file.read_text(encoding="utf8")

    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 2


def test_filter_files(tmp_path):
    mkdocs_file = "mkdocs-filter-files.yml"
    testproject_path = validate_mkdocs_file(
        tmp_path,
        f"tests/fixtures/{mkdocs_file}",
    )
    file = testproject_path / "site/index.html"
    contents = file.read_text(encoding="utf8")
    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1

    file = testproject_path / "site/sub_dir/page_in_sub_dir/index.html"
    contents = file.read_text(encoding="utf8")
    iframe_content_list = validate_iframe(contents, file.parent)
    assert len(iframe_content_list) == 1

    file = testproject_path / "site/empty/index.html"
    contents = file.read_text(encoding="utf8")
    validate_additional_script_code(contents, exists=False)

    file = testproject_path / "site/multiple/index.html"
    contents = file.read_text(encoding="utf8")
    validate_additional_script_code(contents, exists=False)


def test_import_error(monkeypatch):
    # Simulate ImportError for 'get_plugin_logger'
    with monkeypatch.context() as m:
        m.setattr(
            "mkdocs.plugins.get_plugin_logger", MagicMock(side_effect=ImportError)
        )

        # Reload the module to apply the monkeypatch
        import importlib

        from mkdocs_swagger_ui_tag import plugin

        importlib.reload(plugin)
        # Test that the fallback logger is used
        assert plugin.log.name == f"mkdocs.plugins.{plugin.__name__}"

        # Ensure the logger works without raising errors
        plugin.log.info("Test message")
