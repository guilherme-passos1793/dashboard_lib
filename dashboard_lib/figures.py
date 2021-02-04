from plotly import graph_objects as go
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
fig = go.Figure()
dados = ['Barra', [1, 2, 3, 4], [200, 150, 12, 250], '#cccccc', 'y', 'name']

def my_formatter_fun(y, p):
	return '{:,.0f}'.format(y).replace('.', ';').replace(',', '.').replace(';', ',')

class Chart:
	def __init__(self, tipo='plotly'):
		self.manager = tipo
		if tipo == 'plotly':
			self.fig = go.Figure()
		else:
			self.fig = plt.Figure()


class DashChart:
	def __init__(self, bgcolor='#484e53', pagebgcolor='#32383e', textcolor='#ffffff', height=300, width=400):
		"""

        :param bgcolor: cor do bg interno
        :type bgcolor: str
        :param pagebgcolor: cor do bg da pagina
        :type pagebgcolor: str
        :param textcolor: cor do texto no grafico
        :type textcolor: str
        :param height: altura em px ou None - passar None se ajustara ao dcc.Graph (util para unidades rem)
        :type height: int|None
        :param width: largura em px ou None - passar None se ajustara ao dcc.Graph (util para unidades rem)
        :type width: int|None
        """
		self.manager = 'plotly'
		self.bgcolor = bgcolor
		self.pagebgcolor = pagebgcolor
		self.font = dict(
			color=textcolor,
			size=12
		)
		self.fig = go.Figure()
		self.height = height
		self.width = width
		self.fig.update_layout(self.get_layout())

	def adiciona_dados(self, list_dados):
		tipo = list_dados[0]
		cor = list_dados[3]
		eixo_y = list_dados[4]
		axis_name = list_dados[5]
		if self.manager == 'plotly':
			if tipo == 'Barra':
				self.fig.add_bar(x=list_dados[1], y=list_dados[2], yaxis=eixo_y, marker={'color': cor}, name=axis_name)
			elif tipo == 'Linha':
				self.fig.add_scatter(x=list_dados[1], y=list_dados[2], yaxis=eixo_y, marker={'color': cor}, name=axis_name)
			elif tipo == 'Pontos':
				self.fig.add_scatter(x=list_dados[1], y=list_dados[2], yaxis=eixo_y, marker={'color': cor}, mode='markers',
                                     name=axis_name)
			elif tipo == 'Pizza':
				self.fig.add_pie(labels=list_dados[1], values=list_dados[2])
			self.fig.update_layout(self.get_layout())
			self.altera_limites_eixo(eixo_y, 0, max(list_dados[2]))
		return self.fig

	def altera_limites_eixo(self, eixo_y='y', ymin=None, ymax=None):
		if self.manager == 'plotly':
			self.fig.update_layout({eixo_y[:1] + 'axis' + eixo_y[1:]: {'range': (ymin, ymax)}})

	def get_layout(self):
		layout = {
			'barmode': 'group',
			'hovermode': 'x',
			'plot_bgcolor': self.bgcolor,
			'paper_bgcolor': self.pagebgcolor,
			'height': self.height,
			'width': self.width,
			'font': self.font,
			'margin': {'l': 10, 'b': 40, 't': 30, 'r': 10},
			'legend': {'orientation': 'h'},
			'yaxis2': {'anchor': 'x', 'overlaying': 'y', 'side': 'right'},
			'yaxis3': {'anchor': 'x', 'overlaying': 'y', 'side': 'right'}
		}
		return layout

	def set_title(self, title):
		if self.manager == 'plotly':
			self.fig.update_layout({'title': {'text': title,
			                                  # 'y':0.9,
			                                  'x': 0.5,
			                                  'xanchor': 'center',
			                                  'yanchor': 'top'}})

	def set_yaxis_title(self, eixo_y, title):
		if self.manager == 'plotly':
			if eixo_y[1:] == '':
				self.fig.update_layout({'yaxis': {'title': title}})
			else:
				self.fig.update_layout({'yaxis' + eixo_y[1:]: {'title': title}})





class MplibChart:
	def __init__(self, legend_pos='top', legend_width=0.41, n_cols_leg=2):
		self.manager = 'mplib'
		self.fig, self.host = plt.subplots()
		self.par1 = None
		self.par2 = None
		self.legend_position = legend_pos
		self.legend_width = legend_width
		self.n_cols_leg = n_cols_leg
		self.lines = []


	def adiciona_dados(self, list_dados):
		tipo = list_dados[0]
		cor = list_dados[3]
		eixo_y = list_dados[4]
		axis_name = list_dados[5]
		if eixo_y[1:] == '':
			ax = self.host
		elif int(eixo_y[1:]) + 1 > len(self.fig.axes):
			if self.par1 is None:
				self.par1 = self.host.twinx()
			ax = self.par1
		else:
			if self.par2 is None:
				self.par2 = self.host.twinx()
			ax = self.par2
		if tipo == 'Barra':
			p = ax.bar(list_dados[1], list_dados[2], color=cor, label=axis_name)
			self.lines.append(p)
		elif tipo == 'Linha':
			p = ax.plot(list_dados[1], list_dados[2], color=cor, label=axis_name)
			self.lines.append(p[0])
		elif tipo == 'Pontos':
			p = ax.scatter(list_dados[1], list_dados[2], color=cor, label=axis_name)
			self.lines.append(p)
		elif tipo == 'Pizza':
			p = ax.pie(labels=list_dados[1], values=list_dados[2], colors=cor)
			self.lines.append(p)
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


	def set_legend(self, legend_position=None):
		self.host.legend(self.lines, [l.get_label() for l in self.lines])
		for a in plt.gcf().axes:
			a.get_yaxis().set_major_formatter(ticker.FuncFormatter(my_formatter_fun))
		self.host.xaxis.set_major_locator(plt.MaxNLocator(5))


	# if legend_position is None:
	#     legend_position = self.legend_position
	# if legend_position == 'right':
	#     bbox_to_anchor = (1.1, 0.3)
	#     self.host.legend(self.lines, [l.get_label() for l in self.lines], bbox_to_anchor=bbox_to_anchor)
	# elif legend_position == 'left':
	#     bbox_to_anchor = (-0.2, 0.3)
	#     self.host.legend(self.lines, [l.get_label() for l in self.lines], bbox_to_anchor=bbox_to_anchor)
	#
	# elif legend_position == 'top':
	#     bbox_to_anchor = (0.5 - self.legendwidth, 1.1, self.legendwidth, 0)
	#     self.host.legend(self.lines, [l.get_label() for l in self.lines], bbox_to_anchor=bbox_to_anchor, ncol=self.n_cols_leg, mode="expand", borderaxespad=0.)
	#
	# elif legend_position == 'bottom':
	#     bbox_to_anchor = (0.5 - self.legendwidth/2, -0.1, self.legendwidth, 0)
	#     self.host.legend(self.lines, [l.get_label() for l in self.lines], bbox_to_anchor=bbox_to_anchor, ncol=self.n_cols_leg, mode="expand", borderaxespad=0.)
	def save_fig(self, path):
		if path == '':
			plt.show()
		else:
			plt.savefig(path, bbox_inches='tight')



