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

---

### Usage
1. Choose a test file (or test files) from one of the files inside the `test/examples` directory of the project. 

    * If you'd like to bring your own test file, be sure to put it inside of the `test/examples` directory. The file extension is irrelevant.

2. Run the `scanner.py` file as a module, specifying which test files you want to run. Depending on the alias of your Python installation, this can be either:

    `python -m src.scanner.scanner {FILENAME} ... {FILENAME}`
    
    or 

    `python3 -m src.scanner.scanner {FILENAME} ... {FILENAME}`

    In this case, if you wanted to run both `test3.cmm` and `test4.cmm` from the provided test files in the `test/examples directory`, the command would need to be:

    `python -m src.scanner.scanner test3.cmm test4.cmm`

3. See the result of the scanning process on your terminal output. You will see the token identifier list as reference, the `output` list of all tokens with their identifiers, as well as all the `symbol_tables` with their respective entries.

---

### Testing
1. Before running the test suite, make sure you run the following command on the base directory of the project to install the required testing dependencies:

    `python -m pip install -r requirements.txt`

2. Now all you have to do is run the following command to execute unit testing on each of the 12 test files in the `test/examples` directory:

    `python -m pytest -v`

    * Just as before, if you'd like to test a specific source file, include it in the `test/examples` directory, and then create a new `test_{FILENAME}.py` file inside the `test/scripts` directory. After you've asserted what your test needs to return, just run the above command once again.
