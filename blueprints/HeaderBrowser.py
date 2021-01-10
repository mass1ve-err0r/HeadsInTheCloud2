# -*- Blueprint setup -*-
from sanic.exceptions import NotFound
from sanic import Blueprint
from sanic.response import html, redirect
from utils import Mapping14, Mapping13, Mapping12

HeaderBrowserBP = Blueprint('HeaderBrowserBP')
_14_public = [*Mapping14.Mapping14Public]
_14_private = [*Mapping14.Mapping14Private]
_13_public = [*Mapping13.Mapping13Public]
_13_private = [*Mapping13.Mapping13Private]
_12_public = [*Mapping12.Mapping12Public]
_12_private = [*Mapping12.Mapping12Private]
_12_libs = [*Mapping12.Mapping12Libraries]


async def find_list(keyword, iso, target):
    if keyword == "public" and iso == 14:
        return Mapping14.Mapping14Public.get(target)
    elif keyword == "public" and iso == 13:
        return _13_public
    elif keyword == "public" and iso == 12:
        return Mapping12.Mapping12Public.get(target)
    elif keyword == "private" and iso == 14:
        return Mapping14.Mapping14Private.get(target)
    elif keyword == "private" and iso == 13:
        return _13_private
    elif keyword == "private" and iso == 12:
        return Mapping12.Mapping12Private.get(target)
    elif keyword == "dylib" and iso == 12:
        return Mapping12.Mapping12Libraries.get(target)
    else:
        return None


# -*- Routes -*-
@HeaderBrowserBP.route('/')
async def home(request):
    template = request.app.J2env.get_template('/pages/Index.jinja2')
    _html = await template.render_async(title="Home | HITC2")
    return html(_html)


@HeaderBrowserBP.route('/sdks')
async def selectSDK(request):
    template = request.app.J2env.get_template('/pages/SDKSelector.jinja2')
    _html = await template.render_async(title="Select SDK | HITC2",
                                        showNavbarTitle=True)
    return html(_html)


@HeaderBrowserBP.route('/sdks/<version:int>')
async def selectFramework(request, version):
    if version > 14 or version < 12:
        raise NotFound("Nope")
    template = request.app.J2env.get_template('/pages/FrameworkSelector.jinja2')
    _html = None
    if version == 14:
        _html = await template.render_async(title="Select Framework | HITC2",
                                            showNavbarTitle=True,
                                            secondNavbarIOS=version,
                                            fpub=_14_public,
                                            fpriv=_14_private)
    elif version == 13:
        _html = await template.render_async(title="Select Framework | HITC2",
                                            showNavbarTitle=True,
                                            secondNavbarIOS=version,
                                            prtcls=True,
                                            fpub=_13_public,
                                            fpriv=_13_private)
    else:
        _html = await template.render_async(title="Select Framework / Library | HITC2",
                                            showNavbarTitle=True,
                                            secondNavbarIOS=version,
                                            fpub=_12_public,
                                            fpriv=_12_private,
                                            prtcls=True,
                                            hasLibs=True,
                                            libs=_12_libs)
    return html(_html)


@HeaderBrowserBP.route('/sdks/<version:int>/<framework:string>')
async def selectHeader(request, version, framework):
    if version > 14 or version < 12 or request.args.get('type') is None:
        raise NotFound("Nope")
    listType = request.args.get('type')
    if listType == "protocols" and version == 13:
        target_url = request.app.url_for('static', filename='pages/Rendered_13_Protocols.html')
        return redirect(target_url)
    if listType == "protocols" and version == 12:
        target_url = request.app.url_for('static', filename='pages/Rendered_12_Protocols.html')
        return redirect(target_url)
    template = request.app.J2env.get_template('/pages/HeaderSelector.jinja2')
    hdrs = await find_list(listType, version, framework)
    if hdrs is None:
        raise NotFound("No bro.")
    _html = await template.render_async(title=f"Browsing {framework} | HITC2",
                                        showNavbarTitle=True,
                                        secondNavbarIOS=version,
                                        frame=framework,
                                        heads=hdrs)
    return html(_html)


@HeaderBrowserBP.route('/sdks/<version:int>/<framework:string>/<hdr:string>')
async def viewHeader(request, version, framework, hdr):
    fName = f"cdn/headers/SDK{version}/Frameworks/{framework}/{hdr}.html"
    target_url = request.app.url_for('static', filename=fName)
    return redirect(target_url)
