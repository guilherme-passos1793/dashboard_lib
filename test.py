from flask_wysiwyg.wysiwyg import WysiwygField as WysiwygField
import dash_html_components as html
from dashboard_lib.app_initialization import Application
app = Application(basic_layout=html.Div(WysiwygField("txteditor")))
app.start_and_open()
