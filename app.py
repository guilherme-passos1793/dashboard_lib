from dashboard_lib import app_page, graph_utils, app_initialization
import dash_core_components as dcc
import dash_html_components as html
from dashboard_lib import figures

app = app_initialization.Application()
lab = ['adsa', 'asbjdb', 'asjdoias']
val = [50, 30, 20]
fig = figures.DashChart()
dados = ['Linha', [12, 3, 2, 4], [200, 150, 12, 250], '#aabbcc', 'y2', 'linha1']
dados2 = ['Barra', [12, 3, 2, 4], [200, 150, 12, 250], '#debbcc', 'y1', 'linha2']
fig.adiciona_dados(dados)
fig.adiciona_dados(dados2)
fig.set_title('Titulo')

lay = [html.Div([dcc.Graph(figure=fig.fig, style={'border-radius': '10px', 'display': 'inline-block', 'margin': '5px'}),
                 html.Strong('teste')])]
page = app_page.Page('/', lay, app, name='index')
app.add_page(page)
app.set_page_callback()
app.start_and_open()

