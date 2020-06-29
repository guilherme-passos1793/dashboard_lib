from dashboard_lib import app_page as ap
import dash_html_components as html
import dash_core_components as dcc
from plotly import graph_objects as go




class Page1(ap.Page):
    layout = [html.Div('pagina 1'), html.Div(id='texto')]
    link = '/link'

    def cb(self, n_clicks):
        print(n_clicks)
        if n_clicks is not None:
            return str('clicado {} vezes'.format(n_clicks))
        else:
            return None

    def __init__(self,parent):
        super().__init__(self.link, self.layout, parent)
        self.add_callback(func=self.cb, outputs=('texto', 'children'), inputs=[('main_button', 'n_clicks')])
