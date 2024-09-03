import json
import functools

from grammars.elements import AutomataGrammar
from grammars.elements import SymbolGrammar


@functools.cache
def load_configs():
    with open('configs/grammar.json', 'r', encoding='utf-8') as configs:
        return json.load(configs)


def constants():
    configs = load_configs()

    return AutomataGrammar(
        configs['constants']['formulas'],
        configs['alias'],
        configs['constants']['start'],
        configs['constants']['final'],
    )


def identifiers():
    configs = load_configs()

    return AutomataGrammar(
        configs['identifiers']['formulas'],
        configs['alias'],
        configs['identifiers']['start'],
        configs['identifiers']['final'],
    )


def symbols():
    configs = load_configs()

    return SymbolGrammar(
        configs['keywords'],
        configs['operators'],
        configs['bounds'],
        configs['spaces'],
        configs['constants']['specials'],
    )
