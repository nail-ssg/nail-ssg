import os
import re
from .debug import *
from .dir_runner import DirRunner
from .config import Config
from .common import dict_concat
from collections import OrderedDict

_renders = OrderedDict()
_folder_handlers = {}
_builders = []
_priority = {
    'renders': 0,
    'folder_handlers': 0,
    'builders': 0
}


def slug(s: str) -> str:
    return re.sub('[^a-zA-Z0-9]', '_', s)


def run_folder_handlers(folder, data, site_builder, any_folder=False):
    fld = '*' if any_folder else folder
    if fld in _folder_handlers:
        for h in _folder_handlers[fld]:
            h(folder, data, site_builder)


_txt_files = ['.html', '.js', '.css', '.tpl', '.yml', '.json', '.part', '.txt']


class SiteBuilder:
    allData = {
        'allPages': [],
        'files': {},
        'aliases': {}
    }
    folders = set()
    defaultAlias = ''

    def __init__(self, filename):
        print(Config)
        self.conf = Config(filename)

    def build(self):
        dr = DirRunner(self.conf.config('core.src', 'src'), self._file_handler)
        dr.run()
        yprint(self.allData)
        for builder in _builders:
            builder(self)
        if self.conf.config('core.autoUpdateConfig', True):
            self.conf.save()

    @staticmethod
    def _extract_yaml_data(filename: str):
        striped_line = ''
        with open(filename, 'r', encoding='utf-8') as f:
            yaml_lines = []
            checked_yaml = False
            for line in f.readlines():
                striped_line = line.strip()
                if not checked_yaml and (striped_line != '---'):
                    break
                checked_yaml = True
                yaml_lines += [line]
                if striped_line == '...':
                    break
        if striped_line != '...':
            return {}
        yaml_str = ''.join(yaml_lines)
        result = yaml.load(yaml_str)
        if not result:
            result = {}
        return result

    def _file_handler(self, dr: DirRunner, full_path: str, is_dir: bool) -> bool:
        root, ext = os.path.splitext(full_path)
        if ext.lower() not in self.conf.config('core.txtFiles', _txt_files):
            return True
        print(full_path)
        if not is_dir:
            start_path = dr.path
            relpath = os.path.relpath(full_path, start_path)
            folder = relpath.split(os.sep)[0]
            slug_path = slug(relpath)
            data = self._extract_yaml_data(full_path)
            data['$filePath'] = relpath.replace(os.sep, '/')
            data['$filePathSlug'] = slug_path
            run_folder_handlers(folder, data, self, any_folder=True)
            run_folder_handlers(folder, data, self)
            if '$$globalCollections' in data:
                dict_concat(self.allData, data['$$globalCollections'])
        return True

    @staticmethod
    def concatCollection(collection1, collection2) -> None:
        dict_concat(collection1, collection2)

    def getText(self, rel_path: str) -> str:
        path = os.sep.join([self.conf.config('core.src'), rel_path])
        lines = []
        for line in open(path, 'r', encoding='utf-8').readlines():
            if line[0:3] != '...':
                lines += [line]
            else:
                lines = []
        result = ''.join(lines)
        return result

    def renderPage(self, page: dict) -> str:
        if page is None:
            return ''
        context = page.copy()
        context['$allData'] = self.allData
        loc_coll = {}  # Локальные коллекции
        if '$$localCollections' not in context:
            context['$$localCollections'] = {}
        dict_concat(loc_coll, context['$$localCollections'])
        if '$collections' not in context:
            context['$collections'] = {}
        dict_concat(context['$collections'], loc_coll)
        if '$$use' in context:
            for var_name in context['$$use']:
                var_options = context['$$use'][var_name]
                coll_name = var_options['from'] if 'from' in var_options else var_name
                if coll_name in loc_coll:
                    coll = context['$collections'][coll_name].copy()
                elif coll_name in context:
                    coll = context[coll_name].copy()
                else:
                    coll = None
                if coll is not None:
                    if 'sort' in var_options:
                        sort = var_options['sort']
                        reverse = False
                        if sort[0] in '+-':
                            key = sort[1:]
                            reverse = sort[0] == '-'
                        else:
                            key = sort
                        coll.sort(key=lambda row: row[key], reverse=reverse)
                    offset = (var_options['offset']) if 'offset' in var_options else 0
                    count = (var_options['count']) if 'count' in var_options else None
                    end = offset + count if count is not None else None
                    context[var_name] = coll[offset:end]
        if '$$renders' not in context:
            context['$$renders'] = [
                # По умолчанию страницы без рендера содержат простой текст
                {'type': 'plain', 'name': None, 'layout': None}]
        if '$$load' in context:
            for var in context['$$load']:
                other_page_path = context['$$load'][var]
                context[var] = self.renderFile(other_page_path, context)
        if '$$text' in context:
            text = context['$$text']
        else:
            text = self.getText(context['$filePath'])

        for render_options in context['$$renders']:
            if 'data' in render_options:
                dict_concat(context, render_options['data'])
            render_type = render_options['type']
            render_type = 'plain' if render_type not in _renders else render_type
            render = _renders[render_type]
            text = render(self, text, context, render_options)
            if 'extend' in render_options:
                if 'blockName' in render_options:
                    block_name = render_options['blockName']
                else:
                    block_name = '$content'
                context[block_name] = text
                text = self.renderFile(render_options['extend'], context)
        return text

    def renderFile(self, other_page_path, context):
        if other_page_path not in self.allData['files']:
            alias = self.defaultAlias + '.' + other_page_path
            if alias not in self.allData['aliases']:
                return None
            else:
                other_page_path = self.allData['aliases'][alias]
        other_page = context.copy()
        if '$$localCollections' in other_page:
            del other_page['$$localCollections']
        if '$$renders' in other_page:
            del other_page['$$renders']
        if '$$load' in other_page:
            del other_page['$$load']
        dict_concat(other_page, self.allData['files'][other_page_path])
        return self.renderPage(other_page)


def register_render(name, render, priority=None):
    global _renders
    global _priority
    priority = priority if priority else _priority['renders']+10
    setattr(render, 'priority', priority)
    if _priority['renders'] < priority:
        _priority['renders'] = priority
    _renders[name] = render


def register_folder_handler(folders, handler, priority=None):
    global _folder_handlers
    global _priority
    priority = priority if priority else _priority['folder_handlers']+10
    setattr(handler, 'priority', priority)
    if _priority['folder_handlers'] < priority:
        _priority['folder_handlers'] = priority
    for folder in folders:
        if folder not in _folder_handlers:
            _folder_handlers[folder] = []
        _folder_handlers[folder] += [handler]


def register_builder(handler, priority=None):
    global _builders
    global _priority
    priority = priority if priority else _priority['builders']+10
    setattr(handler, 'priority', priority)
    if _priority['builders'] < priority:
        _priority['builders'] = priority
    if handler not in _builders:
        _builders += [handler]
