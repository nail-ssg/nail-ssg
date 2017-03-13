from .print import *
from pystache import Renderer
# from .site_builder import dict_concat
from .builder import Builder as SiteBuilder


def plain_render(site_builder: SiteBuilder, text: str, model: dict, render_options: dict) -> str:
    return text


def mustache_render(site_builder: SiteBuilder, text: str, context: dict, render_options: dict) -> str:
    partials = {}
    if 'data' in render_options:
        context = context.copy()
        dict_concat(context, render_options['data'])
    if 'partials' in render_options:
        for partial_name in render_options['partials']:
            partial_path = render_options['partials'][partial_name]
            partials[partial_name] = site_builder.renderFile(partial_path, context)
    renderer = Renderer(partials=partials)
    s = renderer.render(text, context)
    return s
