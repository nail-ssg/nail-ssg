from shutil import rmtree, copytree
from .site_builder import SiteBuilder
from time import sleep
import os

_default_distributive_folder = 'site'


def build_static(site_builder: SiteBuilder):
    dist = str(site_builder.conf.config('core.dist', _default_distributive_folder))
    rmtree(dist, True)
    sleep(1)
    static_path = os.sep.join([site_builder.conf.config('core.src'), site_builder.conf.config('static.folder', 'static')])
    if os.path.exists(static_path):
        copytree(static_path, dist)
    else:
        os.makedirs(dist, exist_ok=True)


def build_pages(site_builder: SiteBuilder):
    os.makedirs('tmp', exist_ok=True)
    for page in site_builder.allData['allPages']:
        page_content = site_builder.renderPage(page)
        src = site_builder.conf.config('core.src')
        src_filename = os.sep.join([src, page['$filePath']])
        p = os.sep.join([src, site_builder.conf.config('pages.folder')])
        rel_path = os.path.relpath(src_filename, p)
        dist = site_builder.conf.config('core.dist', _default_distributive_folder)
        dst_filename = os.sep.join([dist, rel_path])
        dst_folder = os.path.dirname(dst_filename)
        os.makedirs(dst_folder, exist_ok=True)
        with open(dst_filename, 'w+', encoding='utf-8') as f:
            f.write(page_content)
