if [ -z "$1" ]
  then
    echo "No version supplied"
    exit 1
fi

VER="$1"
DEST="./mkdocs_swagger_ui_tag/swagger-ui"
SOURCE="https://raw.githubusercontent.com/swagger-api/swagger-ui/$1/dist"
JS_LIST="swagger-ui-bundle.js.map swagger-ui-standalone-preset.js.map swagger-ui-bundle.js swagger-ui-standalone-preset.js"
CSS_LIST="swagger-ui.css swagger-ui.css.map"
HTML_LIST="oauth2-redirect.html"

for f in $JS_LIST; do
    wget ${SOURCE}/${f} -O ${DEST}/javascripts/${f}
done

for f in $CSS_LIST; do
    wget ${SOURCE}/${f} -O ${DEST}/stylesheets/${f}
done

for f in $HTML_LIST; do
    wget ${SOURCE}/${f} -O ${DEST}/${f}
done
