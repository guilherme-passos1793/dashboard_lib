import sys
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import webbrowser
from threading import Thread
import dash_bootstrap_components as dbc
print(os.getcwd())
import dash_auth
import inspect
import flask


class Application:
    def __init__(self, host='127.0.0.1:8050', assets_folder=os.path.join(os.getcwd(), '/assets'), auth=None,
                 title='My app',
                 basic_layout=html.Div([dcc.Location(id='url', refresh=False), html.Div(id='main_div')]),
                 page_div_id='main_div', url_id='url', export_file_path=os.path.join(os.getcwd(), '/export'), theme=dbc.themes.SLATE):
        """

        :param host:
        :param assets_folder:
        :param auth: pairs of usernames and passwords
        :type auth: dict
        :param title:
        :param basic_layout:
        :param page_div_id:
        :param url_id:
        :param export_file_path:
        """
        self.app = dash.Dash(__name__, assets_folder=assets_folder, external_stylesheets=[theme], suppress_callback_exceptions=True)
        self.app.title = title
        self.app.layout = basic_layout
        self.addr = host
        self.pages = {}
        self.page_div_id = page_div_id
        self.url_id = url_id
        if auth:
            basicauth = dash_auth.BasicAuth(
                self.app,
                auth
            )
    def start(self):
        # self.app.run_server()
        self.app.run_server(host=self.addr.split(':')[0], port=os.getenv("PORT", int(self.addr.split(':')[1])))

    def open(self):
        webbrowser.open('http://' + self.addr)

    def start_and_open(self):
        # self.set_page_callback()

        t1 = Thread(target=self.start)
        print("##########")

        t2 = Thread(target=self.open)
        t1.start()

        t2.start()

    def add_page(self, page):
        self.pages[page.link] = page.layout

    def set_page_callback(self):
        @self.app.callback(dash.dependencies.Output(self.page_div_id, 'children'),
                           [dash.dependencies.Input(self.url_id, 'pathname')])
        def redireciona(path):
            print(path)
            print(self.pages.keys())
            if path in self.pages.keys():
                print(path)
                return self.pages[path]
            else:
                return ''
