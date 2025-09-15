import sys
from hanul.runtime import janghanul  

def main():
    if len(sys.argv) != 2:
        print("사용법: hanul <파일.eagen>")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith(".eagen"):
        print("확장자는 .eagen으로 되어야함")
        sys.exit(1)

    with open(filename, "r", encoding="utf-8") as file:
        code = file.read()

    interpreter = janghanul()
    interpreter.compile(code)
