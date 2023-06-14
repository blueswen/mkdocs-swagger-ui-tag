Disable the "Try It Out" feature using the `supportedSubmitMethods` option. This is particularly useful for pure documentation purposes when there is no live backend server.

## Markdown

With local configurations:

```html
<swagger-ui supportedSubmitMethods="[]" src="./openapi-spec/sample.yaml"/>
```

With global configurations:

```yaml
plugins:
  - swagger-ui:
      supportedSubmitMethods: []
```

## Swagger UI

<swagger-ui supportedSubmitMethods="[]" src="./openapi-spec/sample.yaml"/>
