# import matplotlib.pyplot as plt
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate

import math
import plotly.graph_objects as go
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
            pixel = 40 + round(name_length * PIXEL_FOR_CHAR)


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


TYPES = {'int64': 'numeric',
         'uint64': 'numeric',
         'int32': 'numeric',
         'uint32': 'numeric',
         'float64': 'numeric',
         'float32': 'numeric',
         'double': 'numeric',
         'object': 'text',
         'bool': 'bool',
         'datetime[ns]': 'datetime',
         }
FORMATS = {'int64': number(0, group=FormatTemplate.Group.no),
           'uint64': number(0, group=FormatTemplate.Group.no),
           'uint32': number(0, group=FormatTemplate.Group.no),
           'float64': number(2),
           'int32': number(0, group=FormatTemplate.Group.no),
           'float32': number(2),
           'double': number(2),
           'object': '',
           'bool': '',
           'datetime[ns]': '',

           }
CELL_STYLES = []
STYLE_HEAD = {
    'backgroundColor': 'gray',
    'color': 'white',
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
def generate_table_selectable(dataframe, title, id_table='', max_height='650px', selectable='multi', filt='none',
                              sor='none', tooltips=[], style_cells=CELL_STYLES, style_head=STYLE_HEAD,
                              fixed_cols=0, bgcolor='#484e55', textcolor='white'):
    # print(create_conditional_style(dataframe))
    out = html.Div([html.Div([
        html.Div(children=[
            html.Strong(title, style={'horizontal-align': 'center', 'vertical-align': 'top'}),
            html.Div(dash_table.DataTable(columns=[
                {"name": i[0], "id": i[0],
                 'type': TYPES[i[1]],
                 'format': FORMATS[i[1]]
                 }
                for i in [(i, str(row)) if 'datetime' not in str(row) else(i, 'datetime[ns]') for i, row in dataframe.dtypes.iteritems()]],

                data=dataframe.to_dict('records'),
                style_cell={'padding': '1px 8px 1px', 'vertical-align': 'top', 'overflow-y': 'hidden', 'backgroundColor': bgcolor, 'color': textcolor},

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

                style_table={'width': '95%', 'maxHeight': max_height, 'overflowY': 'auto',
                             'overflowX': 'auto', 'font-size': '12px', 'text-align': 'left', 'padding': '2px 8px 2px'},
                fixed_rows={'headers': True, 'data': 0},
                fixed_columns={'headers': False, 'data': fixed_cols},
                id=id_table), style={'vertical-align': 'top', 'z-Index': -1, })
        ], style={'vertical-align': 'top', 'z-Index': -1, }),
        html.Br()], style={'vertical-align': 'top', 'z-Index': -1, 'margin-left': '10px'}
    )])
    return out


def gera_fig_pie_chart(labels, values, titulo, textposition='inside', text='', showleg=True, height=SIZE_CHART - 20,
                       width=320-8, bgcolor='#454545', textcolor='white'):
    if type(text) == "<class 'str'>":
        text = values
    if showleg:
        leg = {'x': -1, 'y': 0}
        marg = {'l': 10, 'b': 40, 't': 30, 'r': 10}
    else:
        leg = {'x': 0, 'y': 0}
        marg = {'b': 10, 't': 60}
    fig = {
        'data': [
            {
                'labels': labels,
                'values': values,
                'marker': {'colors': colors},
                "textposition": textposition,
                'text': text,
                'type': 'pie',
            },
        ],
        'layout': go.Layout(
            title=titulo,
            plot_bgcolor=bgcolor,
            paper_bgcolor=bgcolor,

            font=dict(
                color=textcolor,
                size=12
            ),
            height=height,
            width=width,
            margin=marg,
            legend=leg,
            showlegend=showleg,
            hovermode='closest',
        ),

    }
    return fig
