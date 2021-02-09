import datetime
import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import webbrowser
from threading import Thread
import dash_bootstrap_components as dbc
import dash_auth
from . import _verifications as ver
import flask
import pandas as pd
import plotly
import json
import inspect
from . import user_functions as user
from io import BytesIO

# TODO save THEME parameter for use in chart generation

# TODO make a redirect function to the download route
# TODO criar estrutura unica de acesso à session store
external_css = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'


class Application:
    def __init__(self, host: str = '127.0.0.1:8050',
                 assets_folder: str = os.path.join(os.getcwd(), '/assets'),
                 auth: dict = None, title: str = 'My app',
                 page_div_id: str = 'main_div', url_id: str = 'url',
                 export_file_path: str = os.path.join(os.getcwd(), '/export'),
                 theme: str = dbc.themes.SLATE, id_main_alert: str = 'main_alert', session_store_id: str = 'session',
                 user_class=None,
                 tempo_refresh_user: int = 600, default_page: str = '/', tipo_server: str = 'host',
                 server: flask.Flask = None, base_layout: dash.development.base_component.Component = None,
                 navbar_type: str = 'v', navbar_id: str = 'navbar_id'):
        """
        creates an Application, based on dash and a couple of quality of life imporvements, paired with Page class
        :param host: ip and port to host app
        :type host: str
        :param assets_folder: path of folder with main assets
        :type assets_folder: str
        :param auth: pairs of usernames and password
        :type auth: dict
        :param title: title for the app
        :type title: str
        :param base_layout: basic layout for the app
        :type base_layout: dash component
        :param page_div_id: id of the main page container
        :type page_div_id: str
        :param url_id: id of the url component
        :type url_id: str
        :param export_file_path: path of folder with exportable files
        :type export_file_path: str
        :param theme: theme for bootstrap
        :type theme: str
        """
        self.storage_funcs = []
        self.default_page = default_page
        if navbar_type == 'v':
            basic_layout = html.Div(
                [html.Div(
                    [html.Div([dcc.Link(html.Img(src=os.path.split(assets_folder)[1] + '/logo.png'), href=default_page),
                               html.Button(html.Img(src=os.path.split(assets_folder)[1] + '/menu_icon.png'),
                                           className='navbar-toggler', id='toggle_sidebar',
                                           style={'display': 'inline-block', 'text-align': 'center',
                                                  'margin-bottom': '25px'})],
                              style={'backgroundColor': 'black', 'width': '-webkit-fill-available'}),
                     dcc.Store(id=session_store_id, storage_type='session'),
                     dbc.Alert(id=id_main_alert, is_open=False, fade=True, duration=10000, dismissable=True,
                               color="warning"), dcc.Location(id='url', refresh=False),
                     html.Div(id=page_div_id, style={'padding': '2rem'}), ],
                    style={'display': 'inline-block', 'height': '100%', 'width': '-webkit-fill-available',
                           'vertical-align': 'top'})],
                style={'height': '100%', 'vertical-align': 'top', 'width': '-webkit-fill-available'})
        elif navbar_type == 'h':
            navbar = dbc.NavbarSimple([

            ],
                id=navbar_id,
                brand=title,
                color='#333',
                brand_href=self.default_page,
                dark=True
            )
            navbar = dbc.Navbar(
                [dcc.Link(dbc.Row(dbc.Col([html.Span(html.Img(src=os.path.split(assets_folder)[1] + '/logo.png')),
                                           html.Span(dbc.NavbarBrand(title))],
                                  style={'display': 'flex', 'align-items': 'center'}), align='center'), href='/'),
                 dbc.Collapse(dbc.Nav(id=navbar_id, navbar=True, className='ml-auto'), navbar=True,
                              style={'paddingRight': '3rem'})], dark=True,
                color='#333')
            basic_layout = html.Div(
                [html.Div([navbar,
                           dcc.Store(id=session_store_id, storage_type='session'),
                           dbc.Alert(id=id_main_alert, is_open=False, fade=True, duration=10000, dismissable=True,
                                     color="warning"), dcc.Location(id='url', refresh=False),
                           html.Div(id=page_div_id, style={'padding': '2rem'}), ],
                          style={'display': 'inline-block', 'height': '100%', 'width': '-webkit-fill-available',
                                 'vertical-align': 'top'})],
                style={'height': '100%', 'vertical-align': 'top', 'width': '-webkit-fill-available'})
        else:
            basic_layout = html.Div(
                [html.Div([html.Div(
                    [dcc.Link(html.Img(src=os.path.split(assets_folder)[1] + '/logo.png'), href=self.default_page), ],
                    style={'backgroundColor': 'black', 'width': '-webkit-fill-available'}),
                    dcc.Store(id=session_store_id, storage_type='session'),
                    dbc.Alert(id=id_main_alert, is_open=False, fade=True, duration=10000, dismissable=True,
                              color="warning"), dcc.Location(id='url', refresh=False),
                    html.Div(id=page_div_id, style={'padding': '2rem'}), ],
                    style={'display': 'inline-block', 'height': '100%', 'width': '-webkit-fill-available',
                           'vertical-align': 'top'})],
                style={'height': '100%', 'vertical-align': 'top', 'width': '-webkit-fill-available'})

        if base_layout is None:
            base_layout = basic_layout
        base_layout.children += [dcc.Interval(id='interval_refresh_premissoes', interval=tempo_refresh_user * 1000)]
        self.interval_refresh_premissoes = 'interval_refresh_premissoes'
        self.tempo_refresh_user = tempo_refresh_user
        self.id_main_alert = id_main_alert
        css_files = [assets_folder + '/' + f for f in os.listdir(assets_folder) if '.css' in f]
        if tipo_server == 'host':
            self.app = dash.Dash(__name__,
                                 assets_folder=assets_folder,
                                 external_stylesheets=[theme, external_css] + css_files,
                                 suppress_callback_exceptions=True)
        else:
            self.app = dash.Dash(__name__,
                                 server=server,
                                 assets_folder=assets_folder,
                                 external_stylesheets=[theme, external_css] + css_files,
                                 suppress_callback_exceptions=True)
        self.app.title = title
        self.basic_layout = base_layout
        self.app.layout = self.basic_layout
        self.addr = host
        self.pages = {}
        self.page_div_id = page_div_id
        self.url_id = url_id
        self.navbar_id = navbar_id
        self.id_list = self.get_id_from_children(
            json.loads(json.dumps(self.basic_layout, cls=plotly.utils.PlotlyJSONEncoder)))
        if page_div_id not in self.id_list:
            raise (Exception("Atributo page_div_id deve ser uma id contida em base_layout"))
        if url_id not in self.id_list:
            raise (Exception("Atributo url_id deve ser uma id contida em base_layout"))
        if id_main_alert not in self.id_list:
            raise (Exception("Atributo id_main_alert deve ser uma id contida em base_layout"))
        if session_store_id not in self.id_list:
            raise (Exception("Atributo id_main_alert deve ser uma id contida em base_layout"))
        self.alert_funcs = []
        self.download_funcs = []
        self.session_store_id = session_store_id
        self.user_class = user_class
        server = self.app.server
        self.export_file_path = export_file_path
        self.navbar_type = navbar_type

        @server.route('/download/<path:path>')
        def download_from_directory(path):
            out = BytesIO()
            try:
                out.write(open(self.export_file_path + '/' + path, 'rb').read())
                out.seek(0)
                os.remove(self.export_file_path + '/' + path)
            finally:
                out.seek(0)
            return flask.send_file(out, as_attachment=True, cache_timeout=0, attachment_filename=path.split('/')[-1])

        if auth:
            basicauth = dash_auth.BasicAuth(
                self.app,
                auth
            )

    def start(self):
        """
        starts the server for the app
        :return:
        :rtype:
        """
        self.app.run_server(host=self.addr.split(':')[0], port=os.getenv("PORT", int(self.addr.split(':')[1])))

    def open(self):
        """
        opens the server host ip address
        :return:
        :rtype:
        """
        webbrowser.open('http://' + self.addr)

    def start_and_open(self):
        """
        start and open app server
        :return:
        :rtype:
        """
        t1 = Thread(target=self.start)
        # print("##########")

        t2 = Thread(target=self.open)
        t1.start()

        t2.start()

    def add_page(self, page):
        """
        appends a page to the app, easing page management
        :param page: Page object, created through app_page.Page()
        :type page: app_page.Page
        :return:
        :rtype:
        """
        self._checa_validez_ids(page)
        self._checa_validez_link(page)
        self.pages[page.link] = {'layout': page.layout,
                                 'name': page.name,
                                 'section': page.section,
                                 'permissoes_suficientes': page.permissoes_suficientes,
                                 'icon_class': page.icon_class}
        self.id_list += page.get_id_list()

    def set_page_callback(self):
        """
        Sets the callback for page management
        :return:
        :rtype:
        """
        if self.navbar_type == 'v':
            self._update_layout_for_sidebar()

            @self.app.callback(dash.dependencies.Output('main_sidebar', 'children'),
                               [dash.dependencies.Input(self.url_id, 'pathname')],
                               [dash.dependencies.State(self.session_store_id, 'data'),
                                dash.dependencies.State(self.session_store_id, 'modified_timestamp')])
            def set_sidebar_items(path, data, ts):

                data = self.atualiza_data_perm(data, ts)
                sidebar_children = dbc.Nav(
                    self._auto_generate_sidebar_items(data),
                    vertical=True,
                    pills=True,

                )
                return sidebar_children
        elif self.navbar_type == 'h':
            @self.app.callback(dash.dependencies.Output(self.navbar_id, 'children'),
                               [dash.dependencies.Input(self.url_id, 'pathname')],
                               [dash.dependencies.State(self.session_store_id, 'data'),
                                dash.dependencies.State(self.session_store_id, 'modified_timestamp')])
            def set_navbar_items(path, data, ts):
                data = self.atualiza_data_perm(data, ts)
                navbar = self.auto_generate_navbar(data)
                return navbar

        # @self.app.callback(dash.dependencies.Output(self.session_store_id, 'data'),
        #                    [dash.dependencies.Input(self.url_id, 'pathname')],
        #                    [dash.dependencies.State(self.session_store_id, 'data'),
        #                     dash.dependencies.State(self.session_store_id, 'modified_timestamp')]
        #                    )
        def recalcula_permissoes(path, data, ts):
            # print(data, ts)
            data = self.atualiza_data_perm(data, ts)

            return data

        self.add_session_storage_callback(recalcula_permissoes, [(self.interval_refresh_premissoes, 'n_intervals')],
                                          [(self.session_store_id, 'data'),
                                           (self.session_store_id, 'modified_timestamp')])

        @self.app.callback(dash.dependencies.Output(self.page_div_id, 'children'),
                           [dash.dependencies.Input(self.url_id, 'pathname')],
                           [dash.dependencies.State(self.session_store_id, 'data'),
                            dash.dependencies.State(self.session_store_id, 'modified_timestamp')])
        def redireciona(path, data, ts):
            # print(data, ts)
            data = self.atualiza_data_perm(data, ts)

            if path in self.pages.keys():
                return self._get_page_layout(path, data)

            else:
                return self._get_page_layout(self.default_page, data)

        self.set_alert_callback()
        self.set_download_callbacks()
        self.set_session_storage_callback()

    def atualiza_data_perm(self, data, ts):
        if data is None:
            perm, uid = self._get_id_perm()
            data = dict()
            data.update({'user': uid,
                         'permissoes': perm})
        elif data.get('user') is None or data.get('permissoes') is None:
            perm, uid = self._get_id_perm()
            data = dict()
            data.update({'user': uid,
                         'permissoes': perm})
        else:
            # print((datetime.datetime.today() - datetime.datetime.fromtimestamp(ts / 1000)).seconds)
            if (datetime.datetime.today() - datetime.datetime.fromtimestamp(
                    ts / 1000)).seconds > self.tempo_refresh_user:
                perm, uid = self._get_id_perm()
                data.update({'user': uid,
                             'permissoes': perm})
            else:
                data = data
        return data

    def add_download_callback(self, func, inp, states):
        if isinstance(inp, list) and len(inp) != 1:
            raise Exception("para usar downloads globais apenas um input deve ser passado")
        ver.checa_compatibilidade(func, inp, states)
        self.download_funcs.append({'input': inp,
                                    'states': states,
                                    'function': func
                                    })

    def add_session_storage_callback(self, func, inp, states):
        if isinstance(inp, list) and len(inp) != 1:
            raise Exception("para usar downloads globais apenas um input deve ser passado")
        ver.checa_compatibilidade(func, inp, states)
        self.storage_funcs.append({'input': inp,
                                   'states': states,
                                   'function': func
                                   })

    def set_session_storage_callback(self):

        list_inputs = [y for x in self.storage_funcs for y in x['input']]
        list_states = [y for x in self.storage_funcs for y in x['states']]

        @self.app.callback(dash.dependencies.Output(self.session_store_id, 'data'),
                           [dash.dependencies.Input(i[0], i[1]) for i in list_inputs],
                           [dash.dependencies.State(i[0], i[1]) for i in list_states]
                           )
        def storage(*args):
            # print(args)
            ctx = dash.callback_context
            list_inputs2 = [y for x in self.storage_funcs for y in x['input']]
            list_states2 = [y for x in self.storage_funcs for y in x['states']]
            args_completo = [i[0] + '.' + i[1] for i in list_inputs2 + list_states2]
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            triggered = [i for i in self.storage_funcs if i['input'][0][0] == button_id]
            if len(triggered) > 0:
                triggered = triggered[0]
                inputs_triggered = triggered['input'][0][0] + '.' + triggered['input'][0][1]
                states_triggered = [i[0] + '.' + i[1] for i in triggered['states']]
                args_triggered = [inputs_triggered] + states_triggered
                args_trig = [args[args_completo.index(a)] for a in args_triggered]
                return triggered['function'](*args_trig)
            # return button_id, 'True', 'warning'

    def set_download_callbacks(self):

        list_inputs = [y for x in self.download_funcs for y in x['input']]
        list_states = [y for x in self.download_funcs for y in x['states']]
        # TODO encontrar maneira de fazer redirecionamento para rota via server - equivalente à webbrowser.open()
        self.app.clientside_callback("""function (data){
                                     st = JSON.parse(window.sessionStorage.getItem('session'));
                                     if (st != undefined){
                                         if (st.filename != undefined) {
                                            var fn = st.filename;
                                            var link = '/download/' + fn;
                                            delete (st["filename"]);
                                            window.sessionStorage.session = JSON.stringify(st)
                                            console.log(link);
                                            window.open(link);
                                            }
                                            return window.location.host + link;}
                                     }""",
                                     output=dash.dependencies.Output('testecb', 'children'),
                                     inputs=[dash.dependencies.Input(self.session_store_id, 'data')])

        list_inputs = [y for x in self.download_funcs for y in x['input']]
        list_states = [y for x in self.download_funcs for y in x['states']]

        def download(*args):
            ctx = dash.callback_context
            list_inputs = [y for x in self.download_funcs for y in x['input']]
            list_states = [y for x in self.download_funcs for y in x['states']]
            args_completo = [i[0] + '.' + i[1] for i in list_inputs + list_states]
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            triggered = [i for i in self.download_funcs if i['input'][0][0] == button_id]
            print(args[-1])
            data = args[-1]
            if data is None:
                data = dict()
            if len(triggered) > 0 and ctx.triggered[0].get('value') is not None:
                triggered = triggered[0]
                inputs_triggered = triggered['input'][0][0] + '.' + triggered['input'][0][1]
                states_triggered = [i[0] + '.' + i[1] for i in triggered['states']]
                args_triggered = [inputs_triggered] + states_triggered
                args_trig = [args[args_completo.index(a)] for a in args_triggered]
                result = triggered['function'](*args_trig)
                data.update({'filename': result})
                # flask.redirect('/download/' + triggered['function'](*args_trig))

                return data
            return data

        if len(list_inputs + list_states) > 0:
            self.add_session_storage_callback(download, [(i[0], i[1]) for i in list_inputs],
                                              [(i[0], i[1]) for i in list_states] + [(self.session_store_id, 'data')])

    def _get_page_layout(self, path, data):
        perm = self.pages[path]['permissoes_suficientes']
        status = self._checa_validez_permissao(perm, data)
        if status:
            return self.pages[path]['layout']
        else:
            # print(path)
            return self._get_page_layout(self.default_page, data)

    def _checa_validez_permissao(self, perm, data):
        if inspect.isclass(self.user_class) and issubclass(self.user_class, user.User):
            perm_user = set(data['permissoes'])
            if perm is not None:
                # print(perm)
                if isinstance(perm, list):
                    for permission_group in perm:
                        if isinstance(permission_group, str):
                            if {permission_group}.issubset(perm_user):
                                # print('usuario permitido!')
                                return True
                            else:
                                # print('usuario sem permissao!')
                                return False
                        elif isinstance(permission_group, list):
                            if set(permission_group).issubset(perm_user):
                                # print('usuario permitido!')
                                return True
                            else:
                                # print('usuario sem permissao!')
                                return False
                        else:
                            print('pagina mal configurada! permissoes tem que ser lista de permissoes ou string'
                                  'com permissao unica')
                            return False

                elif isinstance(perm, str):
                    if {perm}.issubset(perm_user):
                        # print('usuario permitido str!')
                        return True
                    else:
                        # print('usuario sem permissao!')
                        return False
                else:
                    print('pagina mal configurada! permissoes tem que ser lista de permissoes ou string'
                          'com permissao unica')
                    return False
            else:
                # print('page n requer permissao!')
                return True
        else:
            # print('app nao usa classe user')
            return True

    def _get_id_perm(self):
        if inspect.isclass(self.user_class) and issubclass(self.user_class, user.User):
            ip = flask.request.remote_addr
            usr = self.user_class()
            usr.get_user_from_ip(ip)
            uid, perm = usr.codigo_unico, usr.permissoes
            # print(uid, perm)
        else:
            uid, perm = None, None
        return perm, uid

    def _auto_generate_sidebar_items(self, data):
        """
        Generate sidebar items based on pages appended to the app
        :return:
        :rtype:
        """
        sidebar_items = [html.Button('X', id='toggle_sidebar_close',
                                     style={'backgroundColor': '#202020', 'text-align': 'right', 'color': 'white'}),
                         html.Br()]
        df = pd.DataFrame([(i, self.pages[i]['name'], self.pages[i]['section'], self.pages[i]['icon_class'],
                            self.pages[i]['permissoes_suficientes']) for i in self.pages.keys()],
                          columns=['link', 'name', 'section', 'icon_class', 'permissoes_suficientes'])
        df['PERMITIDO'] = df.apply(lambda row: self._checa_validez_permissao(row.permissoes_suficientes, data), axis=1)
        df = df.loc[df.PERMITIDO]
        # print('')

        for section in df.section.drop_duplicates():
            pages = df.loc[df.section == section]
            details_section = [html.Details([
                html.Summary(html.Strong(section), style={'width': '90%'}),
                html.Div([
                             dbc.NavLink([html.I(className=pag['icon_class'],
                                                 style={'margin-right': '0.4rem', 'font-size': '0.6rem'}), pag['name']],
                                         href=pag['link'],
                                         style={'backgroundColor': '#202020', 'padding': '0px',
                                                'background-image': 'none',
                                                'border': 0, 'margin-left': '1rem'}) for i, pag in pages.iterrows()
                         ] + [html.Br()]),
            ]),
            ]
            sidebar_items += details_section
        # print(sidebar_items)
        return sidebar_items

    def auto_generate_navbar(self, data):

        sidebar_items = []
        df = pd.DataFrame([(i, self.pages[i]['name'], self.pages[i]['section'], self.pages[i]['icon_class'],
                            self.pages[i]['permissoes_suficientes']) for i in self.pages.keys()],
                          columns=['link', 'name', 'section', 'icon_class', 'permissoes_suficientes'])
        df['PERMITIDO'] = df.apply(lambda row: self._checa_validez_permissao(row.permissoes_suficientes, data), axis=1)
        df = df.loc[df.PERMITIDO]
        # print('')
        df = df.loc[df.link != self.default_page]
        for section in df.section.drop_duplicates():
            pages = df.loc[df.section == section]
            details_section = [dbc.DropdownMenu([
                dbc.DropdownMenuItem([dbc.NavLink([html.I(className=pag['icon_class'],
                                                          style={'margin-right': '0.4rem', 'font-size': '0.6rem'}),
                                                   pag['name']],
                                                  href=pag['link'],
                                                  style={'padding': '0.1rem'})
                                      ]) for i, pag in
                pages.iterrows()
            ], label=section, color='primary', ),

            ]
            sidebar_items += details_section
        return sidebar_items

    @staticmethod
    def _get_sidebar():
        """
        generate sidebar for the app, based on pages appended to the app
        :return:
        :rtype:
        """
        return dbc.Collapse(

            id='main_sidebar',
            is_open=False,
            className='mat-elevation-z0 mat-card col-md-2',
            style={'backgroundColor': '#202020', 'height': '-webkit-fill-available', 'margin': 0, 'position': 'fixed',
                   'zIndex': '999999', 'padding': '0px'}

        )

    def _update_layout_for_sidebar(self):
        """
        adds the sidebar to the original layout
        :return:
        :rtype:
        """
        self.app.layout.children = [self._get_sidebar()] + self.app.layout.children

        @self.app.callback(dash.dependencies.Output('main_sidebar', 'is_open'),
                           [dash.dependencies.Input('toggle_sidebar', 'n_clicks'),
                            dash.dependencies.Input('toggle_sidebar_close', 'n_clicks')],
                           [dash.dependencies.State('main_sidebar', 'is_open')])
        def toggle_main_sidebar(n1, n2, is_open):
            if n1 or n2:
                return not is_open

    def _get_id_list(self):
        return self.id_list

    def get_id_from_children(self, dicio):
        list_ids = []
        if isinstance(dicio, dict):
            if 'props' in dicio.keys():
                if isinstance(dicio['props'], dict):
                    if 'id' in dicio['props'].keys():
                        list_ids.append(dicio['props']['id'])
                    if 'children' in dicio['props'].keys():
                        if dicio['props']['children'] is not None:
                            for child in list(dicio['props']['children']):
                                list_ids += self.get_id_from_children(child)
        elif isinstance(dicio, list) and len(dicio) > 0:
            for dic in dicio:
                list_ids += self.get_id_from_children(dic)
        return list_ids

    def _checa_validez_ids(self, page):
        ids_page = page.get_id_list()
        if len(set(ids_page).intersection(set(self.id_list))) > 0:
            raise Exception(
                f"Encontrei ids na nova pagina {page.section}/{page.name} que "
                f"ja estao sendo utilizadas por outras paginas: {list(set(ids_page).intersection(set(self.id_list)))}")

    def _checa_validez_link(self, page):
        link_page = page.link
        if link_page in self.pages.keys():
            raise Exception(
                f"O link da nova pagina {page.section}/{page.name} já está sendo"
                f" utilizado pela pagina {self.pages[link_page]['section']}/{self.pages[link_page]['name']}")

    def add_alert_callback(self, func, inp, states, color="warning"):
        if isinstance(inp, list) and len(inp) != 1:
            raise Exception("para usar alertas globais apenas um input deve ser passado")
        ver.checa_compatibilidade(func, inp, states)
        self.alert_funcs.append({'input': inp,
                                 'states': states,
                                 'function': func,
                                 'color': color
                                 })

    def set_alert_callback(self):

        list_inputs = [y for x in self.alert_funcs for y in x['input']]
        list_states = [y for x in self.alert_funcs for y in x['states']]

        if len(list_inputs + list_states) > 0:

            @self.app.callback([dash.dependencies.Output(self.id_main_alert, 'children'),
                                dash.dependencies.Output(self.id_main_alert, 'is_open'),
                                dash.dependencies.Output(self.id_main_alert, 'color')],
                               [dash.dependencies.Input(i[0], i[1]) for i in list_inputs],
                               [dash.dependencies.State(i[0], i[1]) for i in list_states])
            def alerta(*args):
                # print(args)
                ctx = dash.callback_context
                list_inputs2 = [y for x in self.alert_funcs for y in x['input']]
                list_states2 = [y for x in self.alert_funcs for y in x['states']]
                args_completo = [i[0] + '.' + i[1] for i in list_inputs2 + list_states2]
                button_id = ctx.triggered[0]["prop_id"].split(".")[0]
                triggered = [i for i in self.alert_funcs if i['input'][0][0] == button_id]
                if len(triggered) > 0:
                    triggered = triggered[0]
                    inputs_triggered = triggered['input'][0][0] + '.' + triggered['input'][0][1]
                    states_triggered = [i[0] + '.' + i[1] for i in triggered['states']]
                    args_triggered = [inputs_triggered] + states_triggered
                    args_trig = [args[args_completo.index(a)] for a in args_triggered]
                    return triggered['function'](*args_trig), True, triggered['color']
                # return button_id, 'True', 'warning'
