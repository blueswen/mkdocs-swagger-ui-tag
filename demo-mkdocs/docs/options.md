# Swagger UI Options

Some configurations on [Swagger UI Doc](https://swagger.io/docs/open-source-tools/swagger-ui/usage/configuration/) could be used in this plugin. There are two ways to configure options:

1. Configure through plugin options as global configurations
2. Configure through swagger-ui tag attributes as local configurations

Supported configurations included:

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

## Through plugin options

```yaml
plugins:
    - swagger-ui-tag:
        docExpansion: none
        filter: ""
        syntaxHighlightTheme: monokai
```

## Through tag attributes

```html
<swagger-ui supportedSubmitMethods="['get']"
            docExpansion="none"
            filter=""
            syntaxHighlightTheme="monokai"
            src="./demo/openapi-spec/sample.yaml"/>
```

Tag attributes also supports setting [initOAuth](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/) method.

### Swagger UI with local configurations

<swagger-ui supportedSubmitMethods="['get']"
            docExpansion="none"
            filter=""
            syntaxHighlightTheme="monokai"
            src="./demo/openapi-spec/sample.yaml"/>

### Swagger UI without local configurations

<swagger-ui src="./demo/openapi-spec/sample.yaml"/>
