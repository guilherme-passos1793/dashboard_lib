from dashboard_lib import app_page, graph_utils, app_initialization
import user_teste
import dash_core_components as dcc
import dash_html_components as html
from dashboard_lib import figures
import os
import pandas as pd
import time
app = app_initialization.Application(host='192.168.0.47:'
                                          '8050', assets_folder=os.getcwd() + '/assets',
                                     export_file_path=os.getcwd() + '/export', user_class=user_teste.UserTeste, navbar_type='v', tempo_refresh_user=30)

lab = ['adsa', 'asbjdb', 'asjdoias']
val = [50, 30, 20]
fig = figures.DashChart(width=None)
dados = ['Linha', [12, 3, 2, 4], [200, 150, 12, 250], '#aabbcc', 'y2', 'linha1']
dados2 = ['Barra', [12, 3, 2, 4], [200, 150, 12, 250], '#debbcc', 'y1', 'linha2']
fig.adiciona_dados(dados)
fig.adiciona_dados(dados2)
fig.set_title('Titulo')
fig = fig.fig
fig = graph_utils.gera_fig_pie_chart(['a', 'b', 'c', 'd'],  [200, 150, 12, 250], '', width=None)
df = pd.DataFrame([[1, 2, 3,4], [4, 3, 2, 1], [1, 3, 2, 4], [2, 3, 4, 1]], columns=['a', 'b', 'c', 'd'])
tab = graph_utils.generate_table_selectable(df, '', selectable=True)


def teste(n_clicks):
    if n_clicks is not None:
        with open(app.export_file_path + '/teste.txt', 'w') as f:
            f.write('teste.txt')

    return 'teste.txt'#str(args[0]) + str(args[1])


def teste2(n_clicks, timestamp):
    return str(n_clicks) + str(timestamp)


def teste3(n_clicks, timestamp):
    return str(n_clicks) + str(timestamp)


lay = [html.Div([dcc.Graph(figure=fig, style={'border-radius': '10px', 'display': 'inline-block', 'margin': '5px', 'width': '15rem'}),
                 dcc.Link(html.I(id='home - button', n_clicks = 0, className ='fas fa-balance-scale',
                                 style = {'height': '10px', 'width': '10px' ,'color': 'red', 'fontSize': '3 rem', 'paddingLeft': '1 %'}),
                          href='/'),
                 tab,
                 html.Strong('teste', id='testecb'),
                 html.Button('btn_alerta', id='btn_alerta', n_clicks=None),
                 html.Button('btn_alerta2', id='btn_alerta2'),
                 html.Button('btn_alerta3', id='btn_alerta3')])]
page = app_page.Page('/', [html.H1('INDEX')], app, name='index', permissoes_suficientes=[['all'], ['other', 'third']])
page.add_download_callback(teste, [('btn_alerta', 'n_clicks')])
page.add_alert_callback(teste2, [('btn_alerta2', 'n_clicks')], [('btn_alerta2', 'n_clicks_timestamp')])
page.add_alert_callback(teste3, [('btn_alerta3', 'n_clicks')], [('btn_alerta3', 'n_clicks_timestamp')])
page.add_callback(teste3, ('btn_alerta3', 'children'), [('btn_alerta3', 'n_clicks')], [('btn_alerta3', 'n_clicks_timestamp')])
app.add_page(page)
page = app_page.Page(f'/asd', lay, app, f'pagesad')
app.add_page(page)
for i in range(5):
    page = app_page.Page(f'/{i}', [html.H1(f'Pagina_primario{i}')], app, f'page_{i}', permissoes_suficientes=['all'])
    app.add_page(page)
for i in range(5):
    page2 = app_page.Page(f'/s{i}', [html.H1(f'Pagina_secundario{i}')], app, f'page_{i}', section='Secundaria', permissoes_suficientes=['TRADER'], icon_class=f'fa fa-wifi')
    app.add_page(page2)
for i in range(5):
    page2 = app_page.Page(f'/t{i}', [html.H1(f'Pagina_terciario{i}')], app, f'page_{i}', section='third')
    app.add_page(page2)


app.set_page_callback()
if __name__ == '__main__':
    app.start()

