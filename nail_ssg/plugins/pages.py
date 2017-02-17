from .abstract_plugin import Plugin

class Pages(Plugin):
	"""docstring for Pages"""
	_config = None
	def __init__(self, config):
		super(Pages, self).__init__()
		self._config = config
