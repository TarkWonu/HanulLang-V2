import sys
from hanul.runtime import janghanul  
from enum import Enum
from importlib.metadata import version, PackageNotFoundError
from rich.console import Console
from rich.markdown import Markdown
from importlib.resources import files
import subprocess

class CliCommand(Enum):
    RUN = 'run'
    VERSION = 'version'
    DIMI = 'dimi'
    HELP = 'help'
    DOC = 'doc'     # README.md 출력
    KILL = 'kill'   # pip uninstall hanul
    HELLO = 'hello' # Hello, World! 코드 생성


def main():
    if len(sys.argv) == 1:
        print("[commands]")
        for c in list(CliCommand):
            print("\t"+c.value)
        sys.exit(1)

    command = sys.argv[1]
    
    match command:
        case CliCommand.RUN.value:
            filename = sys.argv[2]
            if not filename.endswith(".eagen"):
                print("확장자는 .eagen으로 되어야함")
                sys.exit(1)

            with open(filename, "r", encoding="utf-8") as file:
                code = file.read()

            interpreter = janghanul()
            interpreter.compile(code)
        case CliCommand.VERSION.value:
            try:
                pkg_version = version("hanul")
            except PackageNotFoundError:
                pkg_version = "unknown"

            print(f"Hanul version {pkg_version}")
        case CliCommand.DIMI.value:
            print("떨")
            sys.exit(1)
        case CliCommand.HELP.value:
            if len(sys.argv) < 3:
                print("Need argument")
                sys.exit(1)

            command = sys.argv[2]
            if command not in [c.value for c in CliCommand]:
                print(f"unknown command : {command}")
                sys.exit(1)

            print("usage: ", end="")
            match command:
                case CliCommand.RUN.value:
                    print("hanul run [file].eagen")
                    print("[file].eagen 을 실행합니다")
                case CliCommand.VERSION.value:
                    print("hanul version")
                    print("현재 버전을 출력합니다")
                case CliCommand.DOC.value:
                    print("hanul doc")
                    print("README.md 문서를 출력합니다")
                case CliCommand.KILL.value:
                    print("hanul kill")
                    print("죽입니다(pip uninstall hanul)")
                case CliCommand.HELLO.value:
                    print("hanul hello")
                    print("Hello, World! 를 출력하는 .eagen 파일을 생성합니다")
        case CliCommand.DOC.value:
            console = Console()
            readme_text = files("hanul").joinpath("README.md").read_text(encoding="utf-8")
            console.print(Markdown(readme_text))
        case CliCommand.KILL.value:
            package_name = "hanul"

            result = subprocess.run([sys.executable, "-m", "pip", "uninstall", package_name, "-y"],
                                    capture_output=True, text=True)

            print(result.stdout)
            print(result.stderr)
        case CliCommand.HELLO.value:
            file = open("./hello.eagen", "w", encoding="utf-8")
            file.write("""대체 누가\n에겐 호에에에에에에엥 훌쩍 호에에에에에에에엥\n에겐 호에에에에에에에엥 훌쩍 호에에에에에에에에에엥 21대3 호엥\n에겐 호에에에에에에에엥 훌쩍 호에에에에에에에에에에엥\n에겐 호에에에에에에에엥 훌쩍 호에에에에에에에에에에엥\n에겐 호에에에에에에에엥 훌쩍 호에에에에에에에에에에엥 21대3 호에엥\n에겐 호에에엥 훌쩍 호에에에에에에에에에엥\n에겐 호에에에에에에에엥 훌쩍 호에에에에에에에엥 21대3 호에에에에엥\n에겐 호에에에에에에에엥 훌쩍 호에에에에에에에에에에엥 21대3 호에엥\n에겐 호에에에에에에에엥 훌쩍 호에에에에에에에에에에엥 21대3 호에에에에엥\n에겐 호에에에에에에에엥 훌쩍 호에에에에에에에에에에엥\n에겐 호에에에에에에에에엥 훌쩍 호에에에에에에에에엥\n에겐 호에에에에에에에에에엥 훌쩍 호에엥 \n디미고를 서류로 떨어짐?""")
            file.close()
        case _:
            print(f"unknown command : {command}")
            sys.exit(1)

if __name__ == '__main__':
    main()