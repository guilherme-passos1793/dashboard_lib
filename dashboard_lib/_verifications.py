import inspect


def checa_compatibilidade(func, inp, states):

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
        if len(inspect.signature(func).parameters) != len(inp) + len(states) and \
                '*args' not in str(inspect.signature(func).parameters) and \
                '*kwargs' not in str(inspect.signature(func).parameters):
            raise Exception(
                f"Função {func.__name__} tem {len(inspect.signature(func).parameters)} "
                f"parâmetros, mas esta sendo configurada com {len(inp) + len(states)}")
    else:
        raise Exception("input tem de ser lista de tuplas [(id, propriedade)]")
# TODO adicionar formatador de hoverlabel


