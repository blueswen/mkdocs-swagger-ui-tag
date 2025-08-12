DEST="./mkdocs_swagger_ui_tag/swagger-ui"
SOURCE="./node_modules/swagger-ui-dist"
JS_LIST="swagger-ui-bundle.js.map swagger-ui-standalone-preset.js.map swagger-ui-bundle.js swagger-ui-standalone-preset.js"
CSS_LIST="swagger-ui.css swagger-ui.css.map"
HTML_LIST="oauth2-redirect.html"

for f in $JS_LIST; do
    cp ${SOURCE}/${f} ${DEST}/javascripts/${f}
done

for f in $CSS_LIST; do
    cp ${SOURCE}/${f} ${DEST}/stylesheets/${f}
done

for f in $HTML_LIST; do
    cp ${SOURCE}/${f} ${DEST}/${f}
done
