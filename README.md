# C-- Compiler

## Lexical Analyzer

### Specification

The __lexical analyzer__ or __scanner__ is the first phase of the translation process of a compiler for any given programming language. Following is the `C--` language specification.

- Blanks: `'', ' ', '\n', '\t', '\r'`
- Letters: `[a-zA-Z]`
- Digits: `[0-9]`
- Identifiers: `letter(letter | digit)*`
- Numbers: `digit+(. digit+)?`
- Strings: `" •* "`
- Comments: `/* •* */`
- Keywords: `int, float, string, void, if, else, for, while, read, write, return`
- Special symbols: `'+', '-', '*', '/', '<', '>', '=', '!', ';', ',', '"', '.', '(', ')', '[', ']', '{', '}', '<=', '>=', '==', '!='`
- Symbol tables: `'IDENTIFIER', 'INT_CONST', 'FLOAT_CONST', 'STRING', 'COMMENT'`

### Usage
1. Choose a test file (or test files) from one of the files inside the `test` directory of the project. 

    * If you'd like to bring your own test file, be sure to put it inside of the `test` directory. The file extension is irrelevant.

2. Run the `scanner.py` file as a module, specifying which test files you want to run. Depending on the alias of your Python installation, this can be either:

    `python -m src.scanner.scanner {FILENAME} ... {FILENAME}`
    
    or 

    `python3 -m src.scanner.scanner {FILENAME} ... {FILENAME}`

    In this case, if you wanted to run both `test3.cmm` and `test4.cmm` from the provided test files in the `test directory`, the command would need to be:

    `python -m src.scanner.scanner test3.cmm test4.cmm`

3. See the result of the scanning process on your terminal output. You will see the token identifier list as reference, the `output` list of all tokens with their identifiers, as well as all the `symbol_tables` with their respective entries.