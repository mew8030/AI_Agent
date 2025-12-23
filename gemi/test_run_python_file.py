from functions.run_python_file import run_python_file

def main():
    # Test 1: should print calculator usage
    print(run_python_file("calculator", "main.py"))

    # Test 2: should run calculator with args
    print(run_python_file("calculator", "main.py", ["3 + 5"]))

    # Test 3: should run tests
    print(run_python_file("calculator", "tests.py"))

    # Test 4: should error - outside directory
    print(run_python_file("calculator", "../main.py"))

    # Test 5: should error - file doesn't exist
    print(run_python_file("calculator", "nonexistent.py"))
    # Test 6: should error - not a python file
    print(run_python_file("calculator", "lorem.txt"))

main()