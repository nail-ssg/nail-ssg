from .site_builder import SiteBuilder, register_render, register_folder_handler, register_builder
from .renders import plain_render, mustache_render
from .folder_handlers import *
from .builders import build_pages, build_static

register_render('plain', plain_render)
register_render('mustache', mustache_render)
register_folder_handler('*', file_handler)
register_folder_handler('*', collection_handler)
register_folder_handler('*', page_handler)
register_builder(build_static)
register_builder(build_pages)
