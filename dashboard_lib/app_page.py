import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table
from .app_initialization import Application


class Page():
    def __init__(self, link, layout, parent, name, section='Principal'):
        """

        :param link: link to the page on the app
        :param layout: base layout on the page
        :param parent: application from app_initialization module
        """
        self.layout = layout
        self.name = name
        # self.func_def_callbacks=func_def_callbacks
        self.app = parent
        self.link = link
        self.section = section

    def add_callback(self, func, outputs, inputs, states=[]):
        """
        adds callback to parent
        :param func: callback function
        :param outputs: tuple or list of tuples in the form of (id, parameter to change)
        :param inputs: list of tuples in the form of (id, parameter to change)
        :param states: list of tuples in the form of (id, parameter to change)
        :return:
        """
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

