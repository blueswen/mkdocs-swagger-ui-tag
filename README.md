# MkDocs Swagger UI Tag

[![PyPI version](https://img.shields.io/pypi/v/mkdocs-swagger-ui-tag.svg)](https://pypi.org/project/mkdocs-swagger-ui-tag)
[![PyPI downloads](https://img.shields.io/pypi/dm/mkdocs-swagger-ui-tag.svg)](https://pypi.org/project/mkdocs-swagger-ui-tag)

A MkDocs plugin supports for add [Swagger UI](https://github.com/swagger-api/swagger-ui) in page.

[Live demo](https://blueswen.github.io/mkdocs-swagger-ui-tag/) with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme.

## Features

1. OpenAPI Specification file from online over URL or static file in docs 
2. Multiple Swagger UI in same page
3. Synchronized dark mode with [mkdocs-material](https://squidfunk.github.io/mkdocs-material/)

## Dependency

1. Python Package
    1. beautifulsoup4==4.11.1
2. [Swagger UI dist](https://www.npmjs.com/package/swagger-ui-dist) javascript file and css file
    1. swagger-ui-dist==4.12.0

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

3. You may customize the plugin by passing options in mkdocs.yml:

    ```yaml
    plugins:
       - swagger-ui-tag:
            background: White
    ```

    | Option     | Default | Description                                                                                                                                       |
    |------------|---------|---------------------------------------------------------------------------------------------------------------------------------------------------|
    | background |   ""    | Swagger UI iframe body background attribute value. You can use any css value for background for example "#74b9ff" or Gainsboro or "" for nothing. |

4. Add ```swagger-ui``` tag in markdown to include Swagger UI

    ```markdown
    <swagger-ui src="https://petstore.swagger.io/v2/swagger.json"/>
    ```

    ![Swagger UI Sample Image](https://blueswen.github.io/mkdocs-swagger-ui-tag/sample.png)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/Blueswen/mkdocs-swagger-ui-tag/blob/main/LICENSE) file for details.

## Reference

1. [Amoenus Swagger Dark Theme](https://github.com/Amoenus/SwaggerDark/): source of dark mode css
