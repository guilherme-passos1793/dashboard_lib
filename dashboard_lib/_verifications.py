import inspect


def checa_compatibilidade(func, out, inp, states):

    if not isinstance(states, list):
        raise Exception("states tem de ser lista de tuplas [(id, propriedade)]")
    else:
        if len(states) > 0:
            for i in states:
                if not isinstance(i, tuple) or len(i) != 2:
                    raise Exception("states tem de ser lista de tuplas [(id, propriedade)]")
    if isinstance(inp, list):
        for i in states:
            if not isinstance(i, tuple) or len(i) != 2:
                raise Exception("input tem de ser lista de tuplas [(id, propriedade)]")
        if len(inspect.signature(func).parameters) != len(inp) + len(states):
            raise Exception("Função de alerta tem {} parametros, mas alerta esta sendo configurado com {}".format(
                len(inspect.signature(func).parameters), len(inp) + len(states)))
    else:
        raise Exception("input tem de ser lista de tuplas [(id, propriedade)]")
