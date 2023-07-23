# MkDocs Swagger UI Tag

<p align="center">
<a target="_blank" href="https://pypi.org/project/mkdocs-swagger-ui-tag"><img src="https://img.shields.io/pypi/v/mkdocs-swagger-ui-tag.svg" alt="PyPI version"/></a>
<a target="_blank" href="https://pypi.org/project/mkdocs-swagger-ui-tag"><img src="https://img.shields.io/pypi/dm/mkdocs-swagger-ui-tag.svg" alt="PyPI downloads"/></a>
<a target="_blank" href="https://codecov.io/gh/blueswen/mkdocs-swagger-ui-tag"><img src="https://codecov.io/gh/blueswen/mkdocs-swagger-ui-tag/branch/main/graph/badge.svg?token=1D1B0GAQN1" alt="Codecov"/></a>
</p>

A MkDocs plugin supports for add [Swagger UI](https://github.com/swagger-api/swagger-ui) in page.

[Live demo](https://blueswen.github.io/mkdocs-swagger-ui-tag/) with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/).

## Features

1. OpenAPI Specification file from online over URL or static file in docs
2. All dependencies are using static files handled by plugin not from CDN, especially suitable for those documents been deployed in the intranet
3. Multiple Swagger UI in same page
4. Synchronized dark mode with [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
5. Configure [Swagger UI configuration](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/) through plugin options and tag attributes
6. Support multiple OAS in single Swagger UI with top bar selector
7. Support Swagger UI [initOAuth](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/) method

## Dependency

1. Python Package
    1. beautifulsoup4>=4.11.1
2. [Swagger UI dist](https://www.npmjs.com/package/swagger-ui-dist) javascript file and css file
    1. swagger-ui-dist==5.1.3

## Usage

1. Install plugin from pypi

    ```bash
    pip install mkdocs-swagger-ui-tag
    ```

2. Add ```swagger-ui-tag``` plugin in to your mkdocs.yml plugins sections:

    ```yaml
    plugins:
       - swagger-ui-tag
    ```

3. Add ```swagger-ui``` tag in markdown to include Swagger UI

    ```markdown
    <swagger-ui src="https://petstore.swagger.io/v2/swagger.json"/>
    ```

    ![Swagger UI Sample Image](https://blueswen.github.io/mkdocs-swagger-ui-tag/sample.png)

4. You may customize the plugin by passing options in mkdocs.yml, check more details on [options](https://blueswen.github.io/mkdocs-swagger-ui-tag/options/):

    ```yaml
    plugins:
       - swagger-ui-tag:
            background: White
            docExpansion: none
            filter: ""
            syntaxHighlightTheme: monokai
            tryItOutEnabled: ['get', 'post']
    ```

    | Options | Type | Description |
    |---|---|---|
    | background | String | Default: "". Swagger UI iframe body background attribute value. You can use any css value for background for example "#74b9ff" or "Gainsboro" or "" for nothing. |
    | docExpansion | String | Default: "list". Controls the default expansion setting for the operations and tags. It can be "list" (expands only the tags), "full" (expands the tags and operations) or "none" (expands nothing). |
    | filter | String or Boolean | Default: False. If set, enables filtering. The top bar will show an edit box that you can use to filter the tagged operations that are shown. Can be Boolean to enable or disable, or a string, in which case filtering will be enabled using that string as the filter expression. Filtering is case sensitive matching the filter expression anywhere inside the tag. |
    | syntaxHighlightTheme | String | Default: "agate". [Highlight.js](https://highlightjs.org/static/demo/) syntax coloring theme to use. It can be "agate", "arta", "monokai", "nord", "obsidian" or "tomorrow-night" |
    | tryItOutEnabled | Boolean | Default: False. This setting determines the default editability of the "Try it out" section, including parameters or body. |
    | oauth2RedirectUrl | String | Default: Absolute URL of "/assets/swagger-ui/oauth2-redirect.html" relative with site_url in mkdocs.yml or document root path on site without site_url, e.g. "[https://blueswen.github.io/mkdocs-swagger-ui-tag/assets/swagger-ui/oauth2-redirect.html](https://blueswen.github.io/mkdocs-swagger-ui-tag/assets/swagger-ui/oauth2-redirect.html)". OAuth redirect URL. |
    | supportedSubmitMethods | Array | Default: All Http Methods. Array=["get", "put", "post", "delete", "options", "head", "patch", "trace"]. List of HTTP methods that have the "Try it out" feature enabled. An empty array disables "Try it out" for all operations. This does not filter the operations from the display. |
    | validatorUrl | String | Default: "https://validator.swagger.io/validator". By default, Swagger UI attempts to validate specs against swagger.io's online validator in multiple OAS Swagger UI. You can use this parameter to set a different validator URL, for example for locally deployed validators ([Validator Badge](https://github.com/swagger-api/validator-badge)). Setting it "none" to disable validation. |

## How it works

1. Copy Swagger UI script file into `site/assets/javascripts/` directory, CSS file into `site/assets/stylesheets/` directory, and the [default Oauth2 redirect html](https://github.com/blueswen/mkdocs-swagger-ui-tag/blob/main/mkdocs_swagger_ui_tag/swagger-ui/oauth2-redirect.html) into `site/assets/swagger-ui/` directory
2. Search all swagger-ui tags, then convert them to an iframe tag and generate the iframe target html with the given OpenAPI Specification src path and options

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Blueswen/mkdocs-swagger-ui-tag/blob/main/LICENSE) file for details.

## Reference

1. [Amoenus Swagger Dark Theme](https://github.com/Amoenus/SwaggerDark/): source of dark mode css
