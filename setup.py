from setuptools import setup, find_packages

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(name="mkdocs-swagger-ui-tag",
      version="0.6.3",
      author="Blueswen",
      author_email="blueswen.tw@gmail.com",
      url="https://blueswen.github.io/mkdocs-swagger-ui-tag",
      project_urls={
          "Source": "https://github.com/Blueswen/mkdocs-swagger-ui-tag",
      },
      keywords=["mkdocs", "plugin", "swagger-ui", "openapi"],
      packages=find_packages(),
      license="MIT",
      description="A MkDocs plugin supports for add Swagger UI in page.",
      long_description=long_description,
      long_description_content_type="text/markdown",
      install_requires=["beautifulsoup4>=4.11.1"],
      include_package_data=True,
      entry_points={
          "mkdocs.plugins": [
              "swagger-ui-tag = mkdocs_swagger_ui_tag.plugin:SwaggerUIPlugin",
          ]
      })
