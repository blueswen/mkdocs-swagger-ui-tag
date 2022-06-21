# Support render multiple Swagger UI

## Markdown

Add two attribute in swagger-ui tag:

1. grouped: every swagger-ui with grouped attribute in same page will be collect into single Swagger UI
2. name: Swagger UI top bar selector display text, default value is the src content

The Swagger UI with multiple OAS takes the first grouped swagger-ui tag position.

```markdown
<swagger-ui grouped name="Pet Store" src="https://petstore.swagger.io/v2/swagger.json"/>
<swagger-ui grouped name="Sample" src="./openapi-spec/sample.yaml"/>
<swagger-ui grouped name="Sample First" src="./openapi-spec/sample-first.yaml"/>
<swagger-ui grouped name="Sample Second" src="./openapi-spec/sample-second.yaml"/>
<swagger-ui grouped name="Sample Third" src="./openapi-spec/sample-third.yaml"/>
```

## Multiple OAS in single Swagger UI

<swagger-ui grouped name="Pet Store" src="https://petstore.swagger.io/v2/swagger.json"/>
<swagger-ui grouped name="Sample" src="./openapi-spec/sample.yaml"/>
<swagger-ui grouped name="Sample First" src="./openapi-spec/sample-first.yaml"/>
<swagger-ui grouped name="Sample Second" src="./openapi-spec/sample-second.yaml"/>
<swagger-ui grouped name="Sample Third" src="./openapi-spec/sample-third.yaml"/>

## Other independent Swagger UI

<swagger-ui src="./openapi-spec/sample.yaml"/>
