from plotly import graph_objects as go
import matplotlib.pyplot as plt

fig = go.Figure()
dados = ['Barra', [1, 2, 3, 4], [200, 150, 12, 250], '#cccccc', 'y', 'name']


class Chart:
    def __init__(self, tipo='plotly'):
        self.manager = tipo
        if tipo == 'plotly':
            self.fig = go.Figure()
        else:
            self.fig = plt.Figure()


class DashChart:
    def __init__(self):
        self.manager = 'plotly'
        self.fig = go.Figure()

    def adiciona_dados(self, dados):
        tipo = dados[0]
        cor = dados[3]
        eixo_y = dados[4]
        axis_name = dados[5]
        if self.manager == 'plotly':
            if tipo == 'Barra':
                self.fig.add_bar(x=dados[1], y=dados[2], yaxis=eixo_y, marker={'color': cor}, name=axis_name)
            elif tipo == 'Linha':
                self.fig.add_scatter(x=dados[1], y=dados[2], yaxis=eixo_y, marker={'color': cor}, name=axis_name)
            elif tipo == 'Pontos':
                self.fig.add_scatter(x=dados[1], y=dados[2], yaxis=eixo_y, marker={'color': cor}, mode='markers',
                                     name=axis_name)
            elif tipo == 'Pizza':
                self.fig.add_pie(labels=dados[1], values=dados[2])
            self.fig.update_layout(self.get_layout())
        return self.fig

    def altera_limites_eixo(self, eixo_y='y', ymin=None, ymax=None):
        if self.manager == 'plotly':
            pass

    def get_layout(self):
        layout = {
            'barmode': 'group',
            'hovermode': 'x',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'legend': {'orientation': 'h'},
            'yaxis2': {'anchor': 'x', 'overlaying': 'y', 'side': 'right'},
            'yaxis3': {'anchor': 'x', 'overlaying': 'y', 'side': 'right'}
        }
        return layout

    def set_title(self, title):
        if self.manager == 'plotly':
            self.fig.update_layout({'title': title})

    def set_yaxis_title(self, eixo_y, title):
        if self.manager == 'plotly':
            if eixo_y[1:] == '':
                self.fig.update_layout({'yaxis': {'title': title}})
            else:
                self.fig.update_layout({'yaxis' + eixo_y[1:]: {'title': title}})


class MplibChart:
    def __init__(self):
        self.manager = 'mplib'
        self.fig = plt.Figure()

    def adiciona_dados(self, dados):
        tipo = dados[0]
        cor = dados[3]
        eixo_y = dados[4]
        axis_name = dados[5]

        if len(self.fig.axes) > 0:
            if eixo_y[1:] == '':
                ax = self.fig.axes[0]
            elif int(eixo_y[1:]) + 1 > len(self.fig.axes):
                ax = self.fig.axes[0].twinx()
            else:
                ax = self.fig.axes[int(eixo_y[1:])]
        else:
            ax = self.fig.subplots()
        if tipo == 'Barra':
            ax.bar(dados[1], dados[2], color=cor, label=axis_name)
        elif tipo == 'Linha':
            ax.plot(dados[1], dados[2], color=cor, label=axis_name)
        elif tipo == 'Pontos':
            ax.scatter(dados[1], dados[2], color=cor, label=axis_name)
        elif tipo == 'Pizza':
            ax.pie(labels=dados[1], values=dados[2], colors=cor)
        return self.fig

    def altera_limites_eixo(self, eixo_y='y', ymin=None, ymax=None):

        if eixo_y[1:] == '':
            ax = self.fig.axes[0]
        else:
            ax = self.fig.axes[eixo_y[1:]]
        ax.set_ylim(ymin=ymin, ymax=ymax)

    def set_title(self, title):
        self.fig.suptitle(title)

    def set_yaxis_title(self, eixo_y, title):
        if eixo_y[1:] == '':
            ax = self.fig.axes[0]
        else:
            ax = self.fig.axes[eixo_y[1:]]
        ax.title = title

