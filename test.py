from flask_wysiwyg.wysiwyg import WysiwygField as WysiwygField
from dashboard_lib.app_initialization import Application
app = Application(basic_layout=WysiwygField("txteditor"))
app.start_and_open()
