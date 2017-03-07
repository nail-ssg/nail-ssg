from .basemodule import BaseModule


class BaseRender(object):
	"""docstring for BaseRender"""
    module_type = 'render'
	def __init__(self, config, plugin):
		super().__init__(config)
		self._config = config
		self._plugin = plugin
