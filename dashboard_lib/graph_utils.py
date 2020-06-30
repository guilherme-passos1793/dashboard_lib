# import matplotlib.pyplot as plt
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate

import math
SIZE_DIV_CHART = 200
SIZE_CHART = 196-4
WIDTH_CHART_MESA = 410

colors = [
    'rgb(241, 189, 15)',
    'rgb(96, 107, 109)',
    'rgb(179, 179, 179)',
    'rgb(137, 137, 137)',
    'rgb(33, 33, 33)',
    'rgb(220, 220, 220)',
    'rgb(170, 170, 170)',
    'rgb(124, 124, 124)',
    'rgb(76, 76, 76)',
    'rgb(190, 190, 190)',
    'rgb(150, 150, 150)',
    'rgb(95, 95, 95)',
    'rgb(80, 80, 80)',
    'rgb(240, 240, 240)',
    'rgb(160, 160, 160)',
    'rgb(255, 175, 30)',
    'rgb(110, 93, 124)',
    'rgb(193, 165, 194)',
    'rgb(151, 123, 152)',
    'rgb(47, 19, 48)',
    'rgb(234, 206, 235)',
    'rgb(184, 156, 185)',
    'rgb(138, 110, 139)',
    'rgb(90, 62, 91)',
    'rgb(204, 176, 205)',
    'rgb(164, 136, 165)',
    'rgb(109, 81, 110)',
    'rgb(94, 66, 95)',
    'rgb(254, 226, 255)',
    'rgb(174, 146, 175)',
    'rgb(227, 203, 0)',
    'rgb(82, 121, 94)',
    'rgb(165, 193, 164)',
    'rgb(123, 151, 122)',
    'rgb(19, 47, 18)',
    'rgb(206, 234, 205)',
    'rgb(156, 184, 155)',
    'rgb(110, 138, 109)',
    'rgb(62, 90, 61)',
    'rgb(176, 204, 175)',
    'rgb(136, 164, 135)',
    'rgb(81, 109, 80)',
    'rgb(66, 94, 65)',
    'rgb(226, 254, 225)',
    'rgb(146, 174, 145)'

]
PIXEL_FOR_CHAR = 6


def create_conditional_style(df):
    style = []
    for col in df.columns:
        name_length = max(df[col].astype('str').str.len().max(), len(str(col)))
        if col == 'Escritório':
            pixel = 240
        elif name_length == 0 or math.isnan(name_length):
            pixel = 50
        else:
            pixel = 30 + round(name_length * PIXEL_FOR_CHAR)


        pixel = str(pixel) + "px"
        style.append({'if': {'column_id': col}, 'minWidth': pixel})

    return style


def number(decimals, sign=FormatTemplate.Sign.default, group=FormatTemplate.Group.yes):
    return FormatTemplate.Format(
        group=group,
        precision=decimals,
        scheme=FormatTemplate.Scheme.fixed,
        sign=sign,
        symbol=FormatTemplate.Symbol.no,
        group_delimiter='.',
        decimal_delimiter=','

    )


TYPES = {'int64:dense': 'numeric',
         'uint64:dense': 'numeric',
         'int32:dense': 'numeric',
         'uint32:dense': 'numeric',
         'float64:dense': 'numeric',
         'float32:dense': 'numeric',
         'double': 'numeric',
         'object:dense': 'text',
         'bool:dense': 'bool',
         'datetime64[ns]:dense': 'datetime'
         }
FORMATS = {'int64:dense': number(0, group=FormatTemplate.Group.no),
           'uint64:dense': number(0, group=FormatTemplate.Group.no),
           'float64:dense': number(2),
           'int32:dense': number(0, group=FormatTemplate.Group.no),
           'float32:dense': number(2),
           'float64': number(2),
           'int64': number(2, group=FormatTemplate.Group.no),
           'uint64': number(2, group=FormatTemplate.Group.no),
           'double': number(2),
           'object:dense': '',
           'bool:dense': '',
           'datetime64[ns]:dense': ''

           }
CELL_STYLES = [
    {
        'if': {'column_id': 'Núm ops'},
        'width': '80px'
    },
    {
        'if': {'column_id': 'Cliente'},
        'width': '80px'
    },
    {
        'if': {'column_id': 'Cod assessor'},
        'width': '80px'
    },
    {
        'if': {'column_id': 'Sexo'},
        'width': '80px'
    },
    {
        'if': {'column_id': 'Tipo pessoa'},
        'width': '100px'
    },
    {
        'if': {'column_id': 'Idade'},
        'width': '70px'
    },
    {
        'if': {'column_id': 'Suitability'},
        'width': '100px'
    },
    {
        'if': {'column_id': 'Outros'},
        'width': '70px'
    },
    {
        'if': {'column_id': 'Cadastro (meses)'},
        'width': '80px'
    },
    {
        'if': {'column_id': 'Primeiro aporte (meses)'},
        'width': '80px'
    },

    {
        'if': {'column_id': 'Vol Câmbio USD'},
        'minWidth': '115px'
    },
    {
        'if': {'column_id': 'Duração (min)'},
        'minWidth': '95px'
    },
    {
        'if': {'column_id': 'Maior cliente'},
        'minWidth': '130px'
    },
    {
        'if': {'column_id': 'Milionários'},
        'minWidth': '100px'
    },
    {
        'if': {'column_id': 'UF'},
        'minWidth': '40px'
    },
    # {
    #     'if': {'column_id': 'Início'},
    #     'minWidth': '150px'
    # },
    # {
    #     'if': {'column_id': 'Assunto'},
    #     'minWidth': '223px'
    # }

]
STYLE_HEAD = {
    'backgroundColor': 'white',
    'fontWeight': 'bold',
    'padding': '2px 8px 2px',
    'whiteSpace': 'normal',

    # 'overflow': 'fragments',
    # 'height': 'auto',
}
STYLE_HEAD2 = {
    'backgroundColor': 'white',
    'fontWeight': 'bold',
    'padding': '2px 8px 2px',
    'whiteSpace': 'normal',

    # 'overflow': 'fragments',
}
def generate_table_selectable(dataframe, title, id_table='', max_height='210px', selectable='multi', filt='none',
                              sor='none', min_width='0px', tooltips=[], style_cells=CELL_STYLES, style_head=STYLE_HEAD,
                              fixed_cols=0):
    print(create_conditional_style(dataframe))
    out = html.Div([html.Div([
        html.Div(children=[
            html.Strong(title, style={'horizontal-align': 'center', 'vertical-align': 'top'}),
            html.Div(dash_table.DataTable(columns=[
                {"name": i, "id": i, 'type': TYPES[dataframe[i].ftype],
                 'format': FORMATS[dataframe[i].ftype]}
                for i in dataframe.columns],

                data=dataframe.to_dict('records'),
                style_cell={'padding': '1px 8px 1px', 'vertical-align': 'top',
                            'max-width': '240px', 'overflow-y': 'hidden', 'minWidth': min_width},

                # style_cell_conditional=style_cells,
                tooltip=tooltips,
                editable=False,
                filter_action=filt,
                sort_action=sor,
                style_cell_conditional=create_conditional_style(dataframe) + style_cells,
                style_as_list_view=True,
                # style_data=style_data,
                style_header=style_head,

                row_selectable=selectable,

                style_table={'maxWidth': '95%', 'maxHeight': max_height, 'overflowY': 'auto',
                             'overflowX': 'auto', 'font-size': '12px', 'text-align': 'left', 'padding': '2px 8px 2px'},
                fixed_rows={'headers': True, 'data': 0},
                fixed_columns={'headers': False, 'data': fixed_cols},
                id=id_table), style={'vertical-align': 'top', 'z-Index': -1, })
        ], style={'vertical-align': 'top', 'z-Index': -1, }),
        html.Br()], style={'vertical-align': 'top', 'z-Index': -1, 'margin-left': '10px'}
    )])
    return out