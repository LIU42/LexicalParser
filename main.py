from language import GrammarLoader
from parsers import LexicalParser

class MainProgram:

    def __init__(self) -> None:
        self.parser = LexicalParser(GrammarLoader())

    def parse_file(self, input_path: str = "./inputs/input1.txt", output_path: str = "./outputs/output1.txt") -> None:
        with open(input_path, "r", encoding = "utf-8") as input_file:
            token_list, error_list = self.parser(input_file.readlines())
            
        with open(output_path, "w+", encoding = "utf-8") as output_file:
            if len(error_list) > 0:
                for error in error_list:
                    output_file.write(f"{error}\n")
                return
            for token in token_list:
                output_file.write(f"{token}\n")


if __name__ == "__main__":
    main_program = MainProgram()
    main_program.parse_file("./inputs/input1.txt", "./outputs/output1.txt")
    main_program.parse_file("./inputs/input2.txt", "./outputs/output2.txt")
    main_program.parse_file("./inputs/input3.txt", "./outputs/output3.txt")
    main_program.parse_file("./inputs/input4.txt", "./outputs/output4.txt")
    main_program.parse_file("./inputs/input5.txt", "./outputs/output5.txt")
