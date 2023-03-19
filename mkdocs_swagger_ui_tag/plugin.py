import json
import logging
import os
import uuid
from urllib.parse import unquote as urlunquote
from urllib.parse import urlsplit, urlunsplit

from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader
from markdown.util import AMP_SUBSTITUTE
from mkdocs import utils
from mkdocs.config import config_options
from mkdocs.plugins import BasePlugin

log = logging.getLogger(__name__)
base_path = os.path.dirname(os.path.abspath(__file__))


class SwaggerUIPlugin(BasePlugin):
    """Create Swagger UI with swagger-ui tag"""

    config_scheme = (
        ("background", config_options.Type(str, default="")),
        # Display
        (
            "docExpansion",
            config_options.Choice(("list", "full", "none"), default="list"),
        ),
        ("filter", config_options.Type(object, default=False)),
        (
            "syntaxHighlightTheme",
            config_options.Choice(
                ("agate", "arta", "monokai", "nord", "obsidian", "tomorrow-night"),
                default="agate",
            ),
        ),
        ("tryItOutEnabled", config_options.Type(bool, default=False)),
        # Network
        ("oauth2RedirectUrl", config_options.Type(str, default=None)),
        (
            "supportedSubmitMethods",
            config_options.Type(
                list,
                default=[
                    "get",
                    "put",
                    "post",
                    "delete",
                    "options",
                    "head",
                    "patch",
                    "trace",
                ],
            ),
        ),
        ("validatorUrl", config_options.Type(str, default="none")),
        ("extra_css", config_options.Type(list, default=[])),
        ("dark_scheme_name", config_options.Type(str, default="slate")),
    )

    def on_pre_page(self, page, config, files, **kwargs):
        """Add files for validate swagger-ui tag src"""

        self.files = files
        return page

    def path_to_url(self, page_file, url):
        """Validate swagger-ui tag src and parse url"""

        scheme, netloc, path, query, fragment = urlsplit(url)

        if (
            scheme
            or netloc
            or not path
            or url.startswith("/")
            or url.startswith("\\")
            or AMP_SUBSTITUTE in url
            or "." not in os.path.split(path)[-1]
        ):
            # Ignore URLs unless they are a relative link to a source file.
            # AMP_SUBSTITUTE is used internally by Markdown only for email.
            # No '.' in the last part of a path indicates path does not point to a file.
            return url

        # Determine the filepath of the target.
        target_path = os.path.join(
            os.path.dirname(page_file.src_path), urlunquote(path)
        )
        target_path = os.path.normpath(target_path).lstrip(os.sep)

        # Validate that the target exists in files collection.
        if target_path not in self.files:
            log.warning(
                f"Documentation file '{page_file.src_path}' contains Swagger UI scr to "
                f"'{target_path}' which is not found in the documentation files."
            )
            return url

        target_file = self.files.get_file_from_path(target_path)
        path = target_file.url_relative_to(page_file)
        components = (scheme, netloc, path, query, fragment)
        return urlunsplit(components)

    def on_post_page(self, output, page, config, **kwargs):
        """Replace swagger-ui tag with iframe
        Add javascript code to update iframe height
        Create a html with Swagger UI for iframe
        """

        soup = BeautifulSoup(output, "html.parser")
        swagger_ui_list = soup.find_all("swagger-ui")
        iframe_id_list = []
        grouped_list = []

        if len(swagger_ui_list) > 0:
            css_dir = utils.get_relative_url(
                utils.normalize_url("assets/stylesheets/"), page.url
            )
            js_dir = utils.get_relative_url(
                utils.normalize_url("assets/javascripts/"), page.url
            )
            default_oauth2_redirect_file = utils.get_relative_url(
                utils.normalize_url("assets/swagger-ui/oauth2-redirect.html"), page.url
            )
            env = Environment(
                loader=FileSystemLoader(os.path.join(base_path, "swagger-ui"))
            )
            template = env.get_template("swagger.html")
            extra_css_files = list(
                map(
                    lambda f: utils.get_relative_url(utils.normalize_url(f), page.url),
                    self.config["extra_css"],
                )
            )

            page_dir = os.path.dirname(
                os.path.join(config["site_dir"], urlunquote(page.url))
            )
            if not os.path.exists(page_dir):
                os.makedirs(page_dir)

            for swagger_ui_ele in swagger_ui_list:
                if swagger_ui_ele.has_attr("grouped"):
                    grouped_list.append(swagger_ui_ele)
                    continue

                cur_id = str(uuid.uuid4())[:8]
                iframe_filename = f"swagger-{cur_id}.html"
                iframe_id_list.append(cur_id)
                cur_options = self.process_options(config, swagger_ui_ele)
                cur_oath2_prop = self.process_oath2_prop(swagger_ui_ele)
                oauth2_redirect_url = cur_options.pop("oauth2RedirectUrl", "")
                if not oauth2_redirect_url:
                    oauth2_redirect_url = default_oauth2_redirect_file

                openapi_spec_url = self.path_to_url(
                    page.file, swagger_ui_ele.get("src", "")
                )
                output_from_parsed_template = template.render(
                    css_dir=css_dir,
                    extra_css_files=extra_css_files,
                    js_dir=js_dir,
                    background=self.config["background"],
                    id=cur_id,
                    openapi_spec_url=openapi_spec_url,
                    oauth2_redirect_url=oauth2_redirect_url,
                    validatorUrl=self.config["validatorUrl"],
                    options_str=json.dumps(cur_options, indent=4)[1:-1],
                    oath2_prop_str=json.dumps(cur_oath2_prop),
                )
                with open(os.path.join(page_dir, iframe_filename), "w") as f:
                    f.write(output_from_parsed_template)
                self.replace_with_iframe(soup, swagger_ui_ele, cur_id, iframe_filename)

            if grouped_list:
                cur_id = str(uuid.uuid4())[:8]
                iframe_filename = f"swagger-{cur_id}.html"
                iframe_id_list.append(cur_id)
                openapi_spec_url = []
                for swagger_ui_ele in grouped_list:
                    cur_url = self.path_to_url(page.file, swagger_ui_ele.get("src", ""))
                    cur_name = swagger_ui_ele.get("name", swagger_ui_ele.get("src", ""))
                    openapi_spec_url.append({"url": cur_url, "name": cur_name})

                # only use options from first grouped swagger ui tag
                cur_options = self.process_options(config, grouped_list[0])
                cur_oath2_prop = self.process_oath2_prop(grouped_list[0])
                oauth2_redirect_url = cur_options.pop("oauth2RedirectUrl", "")
                if not oauth2_redirect_url:
                    oauth2_redirect_url = default_oauth2_redirect_file

                output_from_parsed_template = template.render(
                    css_dir=css_dir,
                    extra_css_files=extra_css_files,
                    js_dir=js_dir,
                    background=self.config["background"],
                    id=cur_id,
                    openapi_spec_url=openapi_spec_url,
                    oauth2_redirect_url=oauth2_redirect_url,
                    validatorUrl=self.config["validatorUrl"],
                    options_str=json.dumps(cur_options, indent=4)[1:-1],
                    oath2_prop_str=json.dumps(cur_oath2_prop),
                )
                with open(os.path.join(page_dir, iframe_filename), "w") as f:
                    f.write(output_from_parsed_template)
                self.replace_with_iframe(soup, grouped_list[0], cur_id, iframe_filename)
                # only keep first grouped swagger ui tag
                for rest_swagger_ui_ele in grouped_list[1:]:
                    rest_swagger_ui_ele.extract()

        js_code = soup.new_tag("script")
        # trigger from iframe body ResizeObserver
        js_code.string = """
            window.update_swagger_ui_iframe_height = function (id) {
                var iFrameID = document.getElementById(id);
                if (iFrameID) {
                    full_height = (iFrameID.contentWindow.document.body.scrollHeight + 80) + "px";
                    iFrameID.height = full_height;
                    iFrameID.style.height = full_height;
                }
            }
        """
        # listen scroll event to update modal position in iframe
        js_code.string += """
            let iframe_id_list = []
            var iframes = document.getElementsByClassName("swagger-ui-iframe");
            for (var i = 0; i < iframes.length; i++) { 
                iframe_id_list.push(iframes[i].getAttribute("id"))
            }
        """
        if len(iframe_id_list) == 0:
            js_code.string += """
            let ticking = true;
            """
        else:
            js_code.string += """
            let ticking = false;
            """
        js_code.string += """
            document.addEventListener('scroll', function(e) {
                if (!ticking) {
                    window.requestAnimationFrame(()=> {
                        let half_vh = window.innerHeight/2;
                        for(var i = 0; i < iframe_id_list.length; i++) {
                            let element = document.getElementById(iframe_id_list[i])
                            if(element==null){
                                return
                            }
                            let diff = element.getBoundingClientRect().top
                            if(element.contentWindow.update_top_val){
                                element.contentWindow.update_top_val(half_vh - diff)
                            }
                        }
                        ticking = false;
                    });
                    ticking = true;
                }
            });
        """
        if config["theme"].name == "material":
            # synchronized dark mode with mkdocs-material
            js_code.string += f"""
            const dark_scheme_name = "{self.config['dark_scheme_name']}"
            """
            js_code.string += """
            window.scheme = document.body.getAttribute("data-md-color-scheme")
            const options = {
                attributeFilter: ['data-md-color-scheme'],
            };
            function color_scheme_callback(mutations) {
                for (let mutation of mutations) {
                    if (mutation.attributeName === "data-md-color-scheme") {
                        scheme = document.body.getAttribute("data-md-color-scheme")
                        var iframe_list = document.getElementsByClassName("swagger-ui-iframe")
                        for(var i = 0; i < iframe_list.length; i++) {
                            var ele = iframe_list.item(i);
                            if (ele) {
                                if (scheme === dark_scheme_name) {
                                    ele.contentWindow.enable_dark_mode();
                                } else {
                                    ele.contentWindow.disable_dark_mode();
                                }
                            }
                        }
                    }
                }
            }
            observer = new MutationObserver(color_scheme_callback);
            observer.observe(document.body, options);
            """
            # support compatible with mkdocs-material Instant loading feature
            js_code.string = "document$.subscribe(() => {" + js_code.string + "})"
        soup.body.append(js_code)

        return str(soup)

    def replace_with_iframe(self, soup, swagger_ui_ele, cur_id, iframe_filename):
        """Replace swagger-ui tag with iframe"""
        iframe = soup.new_tag("iframe")
        iframe["id"] = cur_id
        iframe["src"] = iframe_filename
        iframe["frameborder"] = "0"
        iframe["style"] = "overflow:hidden;width:100%;"
        iframe["width"] = "100%"
        iframe["class"] = "swagger-ui-iframe"
        swagger_ui_ele.replaceWith(iframe)

    def process_options(self, config, swagger_ui_ele):
        """Retrieve Swagger UI options from attribute and use config options as default"""
        skip_option_keys = ["background", "custom_css_files"]
        global_options = {
            k: v for k, v in dict(self.config).items() if k not in skip_option_keys
        }
        options_keys = global_options.keys()
        cur_options = {}
        for k in options_keys:
            val = swagger_ui_ele.get(k.lower(), None)
            if val is not None:
                if k == "supportedSubmitMethods":
                    try:
                        val = json.loads(val.replace("'", '"'))
                        if not isinstance(val, list):
                            raise ValueError(
                                f"Attribute supportedSubmitMethods: {val} is not a list."
                            )
                        cur_options[k] = val
                    except Exception as e:
                        logging.warning(e)
                        logging.warning(
                            "Ignore supportedSubmitMethods attribute setting."
                        )
                        cur_options[k] = None
                else:
                    cur_options[k] = val
            else:
                cur_options[k] = global_options[k]
            if cur_options[k] is None:
                cur_options.pop(k)
        if "syntaxHighlightTheme" in cur_options:
            cur_options["syntaxHighlight.theme"] = cur_options.pop(
                "syntaxHighlightTheme"
            )
        return cur_options

    def process_oath2_prop(self, swagger_ui_ele):
        """Retrieve Swagger UI OAuth 2.0 configuration from tag attributes"""
        oath_prop_keys = [
            "clientId",
            "clientSecret",
            "realm",
            "appName",
            "scopes",
            "additionalQueryStringParams",
            "useBasicAuthenticationWithAccessCodeGrant",
            "usePkceWithAuthorizationCodeGrant",
        ]
        cur_prop = {}
        for k in oath_prop_keys:
            val = swagger_ui_ele.get(k.lower(), None)
            if val is not None:
                if k == "additionalQueryStringParams":
                    try:
                        val = json.loads(val.replace("'", '"'))
                        if not isinstance(val, dict):
                            raise ValueError(
                                f"attribute additionalQueryStringParams: {val} is not a dict."
                            )
                        cur_prop[k] = val
                    except Exception as e:
                        logging.warning(e)
                        logging.warning(
                            "Ignore additionalQueryStringParams attribute setting."
                        )
                elif k in [
                    "useBasicAuthenticationWithAccessCodeGrant",
                    "usePkceWithAuthorizationCodeGrant",
                ]:
                    cur_prop[k] = val.lower().strip() == "true"
                else:
                    cur_prop[k] = val
        return cur_prop

    def on_post_build(self, config, **kwargs):
        """Copy Swagger UI css and js files to assets directory"""

        output_base_path = os.path.join(config["site_dir"], "assets")
        css_path = os.path.join(output_base_path, "stylesheets")
        for file_name in os.listdir(
            os.path.join(base_path, "swagger-ui", "stylesheets")
        ):
            utils.copy_file(
                os.path.join(base_path, "swagger-ui", "stylesheets", file_name),
                os.path.join(css_path, file_name),
            )

        js_path = os.path.join(output_base_path, "javascripts")
        for file_name in os.listdir(
            os.path.join(base_path, "swagger-ui", "javascripts")
        ):
            utils.copy_file(
                os.path.join(base_path, "swagger-ui", "javascripts", file_name),
                os.path.join(js_path, file_name),
            )

        swagger_ui_path = os.path.join(output_base_path, "swagger-ui")
        if not os.path.exists(swagger_ui_path):
            os.mkdir(swagger_ui_path)
        utils.copy_file(
            os.path.join(base_path, "swagger-ui", "oauth2-redirect.html"),
            os.path.join(swagger_ui_path, "oauth2-redirect.html"),
        )
