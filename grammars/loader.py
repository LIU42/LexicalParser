import json
import functools

from grammars.elements import AutomataGrammar
from grammars.elements import SymbolGrammar


@functools.cache
def load_config():
    with open('configs/grammar.json', 'r', encoding='utf-8') as grammar_json:
        return json.load(grammar_json)


def constants():
    config = load_config()

    return AutomataGrammar(
        config['constants']['formulas'],
        config['alias'],
        config['constants']['start'],
        config['constants']['final'],
    )


def identifiers():
    config = load_config()

    return AutomataGrammar(
        config['identifiers']['formulas'],
        config['alias'],
        config['identifiers']['start'],
        config['identifiers']['final'],
    )


def symbols():
    config = load_config()

    return SymbolGrammar(
        config['keywords'],
        config['operators'],
        config['bounds'],
        config['spaces'],
        config['constants']['specials'],
    )
