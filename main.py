from parsers import LexicalParser


def lexical_parse(parser, source_path, result_path):
    with open(source_path, mode='r') as sources:
        tokens, errors = parser(sources.readlines())

    with open(result_path, mode='w') as results:
        if len(errors) == 0:
            results.writelines(f'{token}\n' for token in tokens)
        else:
            results.writelines(f'{error}\n' for error in errors)


def main():
    parser = LexicalParser()
    lexical_parse(parser, 'inputs/input1.txt', 'outputs/output1.txt')
    lexical_parse(parser, 'inputs/input2.txt', 'outputs/output2.txt')
    lexical_parse(parser, 'inputs/input3.txt', 'outputs/output3.txt')
    lexical_parse(parser, 'inputs/input4.txt', 'outputs/output4.txt')
    lexical_parse(parser, 'inputs/input5.txt', 'outputs/output5.txt')


if __name__ == '__main__':
    main()
