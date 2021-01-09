from dotenv import load_dotenv
load_dotenv()

# -*- Sanic configg 4 fest deploiment -*-
from sanic import Sanic
app = Sanic("HeadsInTheCloud2")
app.static('/static', './static')


# -*- Jinja2 setup -*-
from jinja2 import Environment, PackageLoader, select_autoescape
J2env = Environment(loader=PackageLoader('server', './templates'),
                    autoescape=select_autoescape(['html', 'xml']),
                    enable_async=True)
J2env.globals["url_for"] = app.url_for
app.J2env = J2env


# -*- Sanic Extensions -*-
from sanic.exceptions import SanicException
from sanic.response import html
@app.exception(SanicException)
async def catch_exceptions_4xx_5xx(req, excp):
    template = J2env.get_template('/pages/Error_4xx_5xx.jinja2')
    _html = await template.render_async(title="What in tarnation... | HITC2")
    return html(_html)


# -*- Blueprint Registration -*-
from blueprints.HeaderBrowser import HeaderBrowserBP
app.blueprint(HeaderBrowserBP)


# -*- DEBUG HEADERS -*-
@app.middleware('response')
async def debug_headers(req, res):
    res.headers['Cache-Control'] = "no-cache, no-store, must-revalidate"
    res.headers['Pragma'] = "no-cache"
    res.headers['Expires'] = "0"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
