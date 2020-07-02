from plotly import graph_objects as go
import matplotlib.pyplot as plt

fig = go.Figure()
dados = ['Barra', [1, 2, 3, 4], [200, 150, 12, 250], '#cccccc', 'y']


class Chart():
    def __init__(self, tipo='plotly'):
        self.manager = tipo
        if tipo == 'plotly':
            self.fig = go.Figure()
        else:
            self.fig = plt.Figure()

    def adiciona_dados(self, dados):
        tipo = dados[0]
        cor = dados[3]
        eixo_y = dados[4]
        if self.manager == 'plotly':
            if tipo == 'Barra':
                self.fig.add_bar(x=dados[1], y=dados[2], yaxis=eixo_y, marker={'color': cor})
            elif tipo == 'Linha':
                self.fig.add_scatter(x=dados[1], y=dados[2], yaxis=eixo_y, marker={'color': cor})
            elif tipo == 'Pontos':
                self.fig.add_scatter(x=dados[1], y=dados[2], yaxis=eixo_y, marker={'color': cor}, mode='markers')
            self.fig.update_layout(self.get_layout())
        else:
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
                ax.bar(dados[1], dados[2], color=cor)
            elif tipo == 'Linha':
                ax.plot(dados[1], dados[2], color=cor)
            elif tipo == 'Pontos':
                ax.scatter(dados[1], dados[2], color=cor)
        return self.fig

    def altera_limites_eixo(self, eixo_y='y', ymin=None, max=None):
        if self.manager == 'plotly':
            pass
        else:
            if eixo_y[1:] == '':
                ax = self.fig.axes[0]
            else:
                ax = self.fig.axes[eixo_y[1:]]
            ax.set_ylim(ymin=ymin, ymax=max)

    def get_layout(self):
        layout = {}
        return layout
