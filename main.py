import dashboard_lib.app_initialization as ai
import dashboard_lib.app_page as ap
from threading import Thread
import dash_html_components as html
import dash_core_components as dcc
import page_1
base_layout = html.Div([dcc.Location(id='url', refresh=False), html.Div(id='main_div'),
 html.Button('teste', id='main_button')])
app = ai.Application(basic_layout=base_layout)
page1 = page_1.Page1(app)
app.add_page(page1)



app.start_and_open()