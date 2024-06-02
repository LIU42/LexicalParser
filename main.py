from language import GrammarLoader
from parsers import LexicalParser

def parse_file(parser: LexicalParser, input_path: str, output_path: str) -> None:
    with open(input_path, mode="r", encoding="utf-8") as input_file:
        token_list, error_list = parser(input_file.readlines())

    with open(output_path, mode="w", encoding="utf-8") as output_file:
        if len(error_list) > 0:
            for error in error_list:
                output_file.write(f"{error}\n")
            return
        for token in token_list:
            output_file.write(f"{token}\n")


if __name__ == "__main__":
    parser = LexicalParser(GrammarLoader())
    parse_file(parser, "./inputs/input1.txt", "./outputs/output1.txt")
    parse_file(parser, "./inputs/input2.txt", "./outputs/output2.txt")
    parse_file(parser, "./inputs/input3.txt", "./outputs/output3.txt")
    parse_file(parser, "./inputs/input4.txt", "./outputs/output4.txt")
    parse_file(parser, "./inputs/input5.txt", "./outputs/output5.txt")
