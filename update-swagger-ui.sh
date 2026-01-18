SWAGGER_UI_VERSION=${1}
DEST="./mkdocs_swagger_ui_tag/swagger-ui"
SOURCE="./node_modules/swagger-ui-dist"
JS_LIST="swagger-ui-bundle.js.map swagger-ui-standalone-preset.js.map swagger-ui-bundle.js swagger-ui-standalone-preset.js"
CSS_LIST="swagger-ui.css swagger-ui.css.map"
OAUTH2_LIST="oauth2-redirect.html oauth2-redirect.js"

if [ -z "${SWAGGER_UI_VERSION}" ]; then
    echo "Please provide a Swagger UI version as the first argument."
    exit 1
fi

rm -rf ${SOURCE}

npm install swagger-ui-dist@${SWAGGER_UI_VERSION}

for f in $JS_LIST; do
    cp ${SOURCE}/${f} ${DEST}/javascripts/${f}
done

for f in $CSS_LIST; do
    cp ${SOURCE}/${f} ${DEST}/stylesheets/${f}
done

for f in $OAUTH2_LIST; do
    cp ${SOURCE}/${f} ${DEST}/${f}
done
