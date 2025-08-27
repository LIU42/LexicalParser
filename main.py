import argparse

from analyzer import LexicalAnalyzer


def main(args):
    analyzer = LexicalAnalyzer()

    source_paths = args.sources
    output_paths = args.outputs

    for source_path, output_path in zip(source_paths, output_paths):
        with open(source_path, 'r') as sources:
            tokens, errors = analyzer.analysis(sources.readlines())

        with open(output_path, 'w') as outputs:
            if len(errors) == 0:
                outputs.writelines(f'{token}\n' for token in tokens)
            else:
                outputs.writelines(f'{error}\n' for error in errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--sources', nargs='+', required=True)
    parser.add_argument('-o', '--outputs', nargs='+', required=True)

    main(parser.parse_args())
