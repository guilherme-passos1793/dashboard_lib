import dash
from .app_initialization import Application
import plotly
import json
from . import _verifications as ver


class Page:
	def __init__(self, link, layout, parent, name, section='Principal',
	             permissoes_suficientes=None, icon_class='fa fa-pie-chart'):
		"""

        :param link: link to the page on the app
        :type link: str
        :param layout: base layout on the page
        :type layout: list
        :param parent: application from app_initialization module
        :type parent: Application
        :param name: nome da pagina
        :type name: str
        :param section: nome do grupo de paginas
        :type section: str
        :param permissoes_suficientes: lista de strings contendo lista de permissoes suficientes
        :type permissoes_suficientes: list
        """
		self.layout = layout
		self.name = name
		# self.func_def_callbacks=func_def_callbacks
		self.app = parent
		self.link = link
		self.section = section
		self.permissoes_suficientes = permissoes_suficientes
		self.icon_class = icon_class

	def add_callback(self, func, outputs, inputs, states=None):
		"""
        adds callback to parent
        :param func: callback function
        :param outputs: tuple or list of tuples in the form of (id, parameter to change)
        :param inputs: list of tuples in the form of (id, parameter to change)
        :param states: list of tuples in the form of (id, parameter to change)
        """
		if states is None:
			states = []
		ver.checa_compatibilidade(func, inputs, states)
		if type(outputs) == list:
			@self.app.app.callback([dash.dependencies.Output(*out) for out in outputs],
			                       [dash.dependencies.Input(*inp) for inp in inputs],
			                       [dash.dependencies.State(*state) for state in states])
			def function(*args):
				return func(*args)
		else:
			@self.app.app.callback(dash.dependencies.Output(*outputs),
			                       [dash.dependencies.Input(*inp) for inp in inputs],
			                       [dash.dependencies.State(*state) for state in states])
			def function(*args):
				return func(*args)

	def add_alert_callback(self, func, inputs, states=None, color='warning'):
		if states is None:
			states = []
		self.app.add_alert_callback(func, inputs, states, color=color)

	def add_download_callback(self, func, inputs, states=None):
		# raise Exception('Método add_download_callback ainda não implementado!')
		if states is None:
			states = []
		self.app.add_download_callback(func, inputs, states)

	def add_session_storage_callback(self, func, inputs, states=None):
		if states is None:
			states = []
		self.app.add_session_storage_callback(func, inputs, states)

	def get_id_list(self):
		return self.app.get_id_from_children(json.loads(json.dumps(self.layout, cls=plotly.utils.PlotlyJSONEncoder)))
