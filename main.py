from parsers import LexicalParser


def lexical_parse(parser, source_path, result_path):
    with open(source_path, 'r') as sources:
        token_list, error_list = parser(sources.readlines())

    with open(result_path, 'w') as results:
        if len(error_list) == 0:
            results.writelines(f'{token}\n' for token in token_list)
        else:
            results.writelines(f'{error}\n' for error in error_list)


def main():
    parser = LexicalParser()
    lexical_parse(parser, 'sources/source1.txt', 'results/result1.txt')
    lexical_parse(parser, 'sources/source2.txt', 'results/result2.txt')
    lexical_parse(parser, 'sources/source3.txt', 'results/result3.txt')
    lexical_parse(parser, 'sources/source4.txt', 'results/result4.txt')
    lexical_parse(parser, 'sources/source5.txt', 'results/result5.txt')


if __name__ == '__main__':
    main()
