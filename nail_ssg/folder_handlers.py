import os
from .site_builder import SiteBuilder


def add_to_collection(site_builder: SiteBuilder, collection_name, data):
    if collection_name not in site_builder.allData:
        site_builder.allData[collection_name] = []
    site_builder.allData[collection_name] += [data]


def collection_handler(folder, data, site_builder: SiteBuilder):
    if '$$collections' in data:
        for collection_name in data['$$collections']:
            add_to_collection(site_builder, collection_name, data)


def file_handler(folder, data, site_builder: SiteBuilder):
    files = site_builder.allData['files']
    files[data['$filePath']] = data


def page_handler(folder, data, site_builder: SiteBuilder):
    if folder == site_builder.conf.config('pages.folder', 'pages'):
        if not data:
            data = {'renders': {'plain': None}}
        add_to_collection(site_builder, 'allPages', data)
        if 'pages' not in site_builder.allData:
            site_builder.allData['pages'] = {}
        site_builder.allData['pages'][data['$filePath']] = data
        data['$url'] = data['$filePath'].replace(os.sep, '/').replace(site_builder.conf.config('pages.folder'), '').replace('index.html', '')
