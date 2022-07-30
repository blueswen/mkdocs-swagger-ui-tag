Support configure OAuth 2.0 authorization by setting attributes for [initOAuth](https://swagger.io/docs/open-source-tools/swagger-ui/usage/oauth2/) method.

| Attribute                                 | Description                                                                                                                                                                                                                                                                                                                                                                           |
|-------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| clientId                                  | Default clientId.                                                                                                                                                                                                                                                                                                                                                                     |
| clientSecret                              | Default clientSecret.<br>**🚨 Never use this parameter in your production environment. It exposes crucial security information. This feature is intended for dev/test environments only. 🚨**                                                                                                                                                                                           |
| realm                                     | Realm query parameter (for oauth1) added to **authorizationUrl** and **tokenUrl**.                                                                                                                                                                                                                                                                                                    |
| appName                                   | Application name, displayed in authorization popup.                                                                                                                                                                                                                                                                                                                                   |
| scopes                                    | Scope space separated string of initially selected oauth scopes, e.g. "openid profile", default is empty.                                                                                                                                                                                                                                                                             |
| additionalQueryStringParams               | Additional query parameters were added to **authorizationUrl** and **tokenUrl**, default is empty.<br>MUST be a JSON, but could wrap string with single quote when attribute value wrapped with double quote, e.g. ```additionalQueryStringParams="{'test': 'hello'}"```, ```additionalQueryStringParams='{"test": "hello"}'```                                                       |
| useBasicAuthenticationWithAccessCodeGrant | Only activated for the **accessCode** flow. During the **authorization_code** request to the **tokenUrl**, pass the [Client Password](https://tools.ietf.org/html/rfc6749#section-2.3.1) using the HTTP Basic Authentication scheme (**Authorization** header with **Basic base64encode(client_id + client_secret)**).<br>The default is false, setting true with any case of "true". |
| usePkceWithAuthorizationCodeGrant         | Only applies to **authorizationCode** flows. [Proof Key for Code Exchange](https://tools.ietf.org/html/rfc7636) brings enhanced security for OAuth public clients.<br>The default is false, setting true with any case of "true".                                                                                                                                                     |

## Markdown

```html
<swagger-ui src="./openapi-spec/sample-oauth2.yaml"
            clientId="your-client-id"
            clientSecret="your-client-secret-if-required"
            realm="your-realms"
            appName="your-app-name"
            scopes="openid profile"
            additionalQueryStringParams="{'test': 'hello'}"
            useBasicAuthenticationWithAccessCodeGrant="false"
            usePkceWithAuthorizationCodeGrant="false"/>
```

## Swagger UI

<swagger-ui src="./openapi-spec/sample-oauth2.yaml"
            clientId="your-client-id"
            clientSecret="your-client-secret-if-required"
            realm="your-realms"
            appName="your-app-name"
            scopes="openid profile"
            additionalQueryStringParams="{'test': 'hello'}"
            useBasicAuthenticationWithAccessCodeGrant="false"
            usePkceWithAuthorizationCodeGrant="false"/>
