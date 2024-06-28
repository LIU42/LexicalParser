from language import GrammarLoader
from parsers import LexicalParser


def parse_file(parser, source_path, result_path):
    with open(source_path, mode='r', encoding='utf-8') as source_file:
        token_list, error_list = parser(source_file.readlines())

    with open(result_path, mode='w', encoding='utf-8') as result_file:
        if len(error_list) == 0:
            for token in token_list:
                result_file.write(f'{token}\n')
        else:
            for error in error_list:
                result_file.write(f'{error}\n')


def main():
    parser = LexicalParser(GrammarLoader())
    parse_file(parser, 'inputs/input1.txt', 'outputs/output1.txt')
    parse_file(parser, 'inputs/input2.txt', 'outputs/output2.txt')
    parse_file(parser, 'inputs/input3.txt', 'outputs/output3.txt')
    parse_file(parser, 'inputs/input4.txt', 'outputs/output4.txt')
    parse_file(parser, 'inputs/input5.txt', 'outputs/output5.txt')


if __name__ == '__main__':
    main()
