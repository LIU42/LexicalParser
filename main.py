from lexical import LexicalParser


def lexical_parse(parser, source_path, output_path):
    with open(source_path, 'r') as sources:
        token_list, error_list = parser(sources.readlines())

    with open(output_path, 'w') as outputs:
        if len(error_list) == 0:
            outputs.writelines(f'{token}\n' for token in token_list)
        else:
            outputs.writelines(f'{error}\n' for error in error_list)


def main():
    parser = LexicalParser()
    lexical_parse(parser, 'examples/sources/source1.txt', 'examples/outputs/output1.txt')
    lexical_parse(parser, 'examples/sources/source2.txt', 'examples/outputs/output2.txt')
    lexical_parse(parser, 'examples/sources/source3.txt', 'examples/outputs/output3.txt')
    lexical_parse(parser, 'examples/sources/source4.txt', 'examples/outputs/output4.txt')
    lexical_parse(parser, 'examples/sources/source5.txt', 'examples/outputs/output5.txt')


if __name__ == '__main__':
    main()
