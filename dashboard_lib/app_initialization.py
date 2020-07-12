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
import pandas as pd

class Application:
    def __init__(self, host='127.0.0.1:8050', assets_folder=os.path.join(os.getcwd(), '/assets'), auth=None,
                 title='My app',
                 basic_layout=html.Div([html.Div([html.Div([dcc.Link(html.Img(src='/assets/logo.png'), href='/'),
                                                  html.Button(html.Img(src='/assets/menu_icon.png'),
                                                              className='navbar-toggler',
                                                              id='toggle_sidebar',
                                                              style={'display': 'inline-block', 'text-align': 'center',
                                                                     'margin-bottom': '25px'})], style={'backgroundColor': 'black', 'width': '-webkit-fill-available'}),


                     dbc.Alert(id='main_alert',is_open=False, fade=True, duration=10000, dismissable=True, color="warning"),
                                        dcc.Location(id='url', refresh=False), html.Div(id='main_div')], style={'display': 'inline-block', 'height': '100%', 'width': '-webkit-fill-available', 'vertical-align': 'top'})], style={'height': '100%', 'vertical-align': 'top', 'width': '-webkit-fill-available'}),
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
        self.pages[page.link] = {'layout': page.layout,
                                 'name': page.name,
                                 'section': page.section}

    def set_page_callback(self):
        self.update_layout_for_sidebar()
        @self.app.callback(dash.dependencies.Output(self.page_div_id, 'children'),
                           [dash.dependencies.Input(self.url_id, 'pathname')])
        def redireciona(path):
            print(path)
            print(self.pages.keys())
            if path in self.pages.keys():
                print(path)
                return self.pages[path]['layout']
            else:
                return ''

    def auto_generate_sidebar_items(self):
        sidebar_items = [html.Button('X', id='toggle_sidebar_close', style={'backgroundColor': '#202020', 'text-align': 'right', 'color': 'white'}), html.Br()]
        df = pd.DataFrame([(i, self.pages[i]['name'], self.pages[i]['section']) for i in self.pages.keys()], columns=['link', 'name', 'section'])
        for section in df.section.drop_duplicates():
            pages = df.loc[df.section == section]
            details_section = [html.Details([
                html.Summary(html.Strong(section), style={'width': '90%'}),
                html.Div([
                    dbc.NavLink(pag['name'], href=pag['link'], style={'backgroundColor': '#202020', 'padding': '0px', 'background-image': 'none', 'border': 0}) for i, pag in pages.iterrows()
                ]),
            ]),
                html.Br()]
            sidebar_items += details_section
        print(sidebar_items)
        return sidebar_items

    def get_sidebar(self):
        return dbc.Collapse(
            dbc.Nav(
                self.auto_generate_sidebar_items(),
                vertical=True,
                pills=True,

            ),
            id='main_sidebar',
            is_open=True,
            className='mat-elevation-z0 mat-card col-md-2',
            style={'backgroundColor': '#202020', 'height': '-webkit-fill-available', 'margin': 0, 'position': 'fixed', 'zIndex': '999999', 'padding': '0px'}

        )

    def update_layout_for_sidebar(self):
        self.app.layout.children = [self.get_sidebar()] + self.app.layout.children

        @self.app.callback(dash.dependencies.Output('main_sidebar', 'is_open'),
                           [dash.dependencies.Input('toggle_sidebar', 'n_clicks'),
                            dash.dependencies.Input('toggle_sidebar_close', 'n_clicks')],
                           [dash.dependencies.State('main_sidebar', 'is_open')])
        def toggle_main_sidebar(n1, n2, is_open):
            if n1 or n2:
                return not is_open

