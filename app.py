from dashboard_lib import app_page, graph_utils, app_initialization
import user_teste
import dash_core_components as dcc
import dash_html_components as html
from dashboard_lib import figures
import os
app = app_initialization.Application(host='192.168.0.47:'
                                          '8050', assets_folder=os.getcwd() + '/assets',
                                     export_file_path=os.getcwd() + '/export', user_class=user_teste.UserTeste)

lab = ['adsa', 'asbjdb', 'asjdoias']
val = [50, 30, 20]
fig = figures.DashChart()
dados = ['Linha', [12, 3, 2, 4], [200, 150, 12, 250], '#aabbcc', 'y2', 'linha1']
dados2 = ['Barra', [12, 3, 2, 4], [200, 150, 12, 250], '#debbcc', 'y1', 'linha2']
fig.adiciona_dados(dados)
fig.adiciona_dados(dados2)
fig.set_title('Titulo')


def teste(n_clicks, timestamp):
    return str(n_clicks) + str(timestamp)


def teste2(n_clicks, timestamp):
    return str(n_clicks) + str(timestamp)


def teste3(n_clicks, timestamp):
    return str(n_clicks) + str(timestamp)


lay = [html.Div([dcc.Graph(figure=fig.fig, style={'border-radius': '10px', 'display': 'inline-block', 'margin': '5px'}),
                 dcc.Link(html.I(id='home - button', n_clicks = 0, className ='fas fa-balance-scale',
                                 style = {'height': '10px', 'width': '10px' ,'color': 'red', 'fontSize': '3 rem', 'paddingLeft': '1 %'}),
                          href='/'),
                 html.Strong('teste'),
                 html.Button('btn_alerta', id='btn_alerta'),
                 html.Button('btn_alerta2', id='btn_alerta2'),
                 html.Button('btn_alerta3', id='btn_alerta3')])]
page = app_page.Page('/', lay, app, name='index', permissoes_suficientes=[['all'], ['other', 'third']])
app.add_alert_callback(teste, [('btn_alerta', 'n_clicks')], [('btn_alerta', 'n_clicks_timestamp')], color='info')
app.add_alert_callback(teste2, [('btn_alerta2', 'n_clicks')], [('btn_alerta2', 'n_clicks_timestamp')])
page.add_alert_callback(teste3, [('btn_alerta3', 'n_clicks')], [('btn_alerta3', 'n_clicks_timestamp')])
page.add_callback(teste3, ('btn_alerta3', 'children'), [('btn_alerta3', 'n_clicks')], [('btn_alerta3', 'n_clicks_timestamp')])
app.add_page(page)

app.set_page_callback()
app.set_alert_callback()
if __name__ == '__main__':
    app.start()

