# runtime.py
import sys

class janghanul:
    def __init__(self):
        self.data = [0] * (2**16)  # 메모리

    # ===== 토큰 파싱 =====
    def parseNum(self, token: str) -> int:
        # 양수: "호 ... 엥" (내부 규칙: '에' 개수 + 2 - '.' 개수)
        if token.startswith("호") and "엥" in token:
            base = token.count("에") + 2
            value = base - token.count(".")
            return value

        # 음수: "하와..." (내부 규칙: '와' 개수 * -1  + '.' 개수)
        elif token.startswith("하와"):
            base = token.count("와") * -1
            value = base + token.count(".")
            return value
        
        # 변수 참조: "디이...미"
        elif token.startswith("디") and "미" in token:
            idx = token.count("이")
            return self.data[idx]

        else:
            raise ValueError(f"{token}도 에겐같이 하네;;")

    def ParseOp(self, token: str) -> str:
        if token == "21대3":
            return "+"
        elif token == "훌쩍":
            return "*"
        else:
            raise ValueError(f"{token}도 에겐같이 하네;;")

    def GetIndex(self, token: str) -> int:
        if not (token.startswith("디") and token.endswith("미")):
            raise ValueError(f"{token}도 에겐같이 하네;;")
        return token.count("이")

    # ===== 식 계산 (곱셈 우선) =====
    def calculate(self, code: str) -> int:
        tokens = code.split()
        seq = []
        for tok in tokens:
            if tok in ("21대3", "훌쩍"):
                seq.append(self.ParseOp(tok))
            else:
                seq.append(str(self.parseNum(tok)))

        # 1) 곱셈 먼저 처리
        stack = []
        i = 0
        while i < len(seq):
            cur = seq[i]
            if cur == "*":
                if not stack:
                    raise ValueError("'*'도 에겐같이 하네;;")
                if i + 1 >= len(seq):
                    raise ValueError("'*'도 에겐같이 하네;;")
                prev = int(stack.pop())
                nxt = int(seq[i + 1])
                stack.append(str(prev * nxt))
                i += 2
            else:
                stack.append(cur)
                i += 1

        # 2) 덧셈 처리
        result = 0
        expect_num = True
        for s in stack:
            if s == "+":
                if expect_num:
                    raise ValueError("'+'도 에겐같이 하네;;")
                expect_num = True
            else:
                result += int(s)
                expect_num = False
        return result

    # ===== 문장 타입 판별 =====
    @staticmethod
    def TYPe(code: str):
        code = code.strip()
        if not code:
            return None
        head = code.split(maxsplit=1)[0] if code.strip() else ""

        if "가을야구?" in code:
            return "IF"
        if "디떨!" in code:
            return "MOVE"
        if "서류제출" in code:
            return "PRINT"
        if "키움아래" in code:
            return "INPUT"
        # 첫 토큰이 변수 형태면 대입
        if head.startswith("디") and head.endswith("미"):
            return "DEF"
        if "에겐" in code:
            return "PRINTCHAR"
        if "탈선린" in code:
            return "END"
        if "30실점" in code:
            return "JUMP"
        return None
    def stripComment(self, line: str) -> str:
        # '#' 또는 'ㅋㅋ' 나오면 그 뒤로 다 버림
        for marker in "#":
            if marker in line:
                return line.split(marker, 1)[0]
        return line
    # ===== 한 줄 실행 =====
    def compileLine(self, code: str):
        code = self.stripComment(code).strip()
        if code == "":
            return None
        
        TYPE = self.TYPe(code)
        
        if TYPE == "DEF":
            parts = code.split(maxsplit=1)
            if len(parts) != 2:
                raise ValueError("대입도 에겐같이 하네;;")
            var, expr = parts
            idx = self.GetIndex(var)
            self.data[idx] = self.calculate(expr)
            return None

        elif TYPE == "INPUT":
            expr = code.replace("키움아래", "", 1).strip()
            idx = self.GetIndex(expr)
            try:
                self.data[idx] = int(input())
            except ValueError:
                raise ValueError("입력도 에겐같이 하네;;")
            return None

        elif TYPE == "PRINT":
            expr = code.replace("서류제출", "", 1).strip()
            
            newline = False
            if expr.endswith("제발"):
                newline = True
                expr = expr[:-2].strip()
            val = self.calculate(expr)
            if newline:

                print(val)
            else:
                print(val,end='')
            return None

        elif TYPE == "PRINTCHAR":
            expr = code.replace("에겐", "", 1).strip()
            newline = False
            if expr.endswith("제발"):
                newline = True
                expr = expr[:-2].strip()

            val = self.calculate(expr)
            try:
                ch = chr(val)
            except (ValueError, TypeError):
                raise ValueError("문자도 에겐같이 하네;;")

            if newline:
                print(ch)
            else:
                print(ch, end="")
            return None  # ← str 리턴 금지(무한루프 방지)

        elif TYPE == "MOVE":
            body = code.replace("디떨!", "", 1).strip()
            if "->" in body:
                src_tok, dst_tok = map(str.strip, body.split("->", 1))
            else:
                parts = body.split()
                if len(parts) != 2:
                    raise ValueError("MOVE도 에겐같이 하네;;")
                src_tok, dst_tok = parts
            src_idx = self.GetIndex(src_tok)
            dst_idx = self.GetIndex(dst_tok)
            self.data[dst_idx] = self.data[src_idx]
            return None

        elif TYPE == "IF":
            # "가을야구? <조건식> 그러면 <then> [아니면 <else>]"
            if "그러면" not in code:
                raise ValueError("IF도 에겐같이 하네;;")
            head, tail = code.split("그러면", 1)
            cond_expr = head.replace("가을야구?", "", 1).strip()
            then_code = tail.strip()
            else_code = None
            if "아니면" in then_code:
                then_code, else_code = map(str.strip, then_code.split("아니면", 1))
            cond_val = self.calculate(cond_expr)
            if cond_val != 0:
                r = self.compileLine(then_code)
                return r if isinstance(r, int) else None
            else:
                if else_code is not None:
                    r = self.compileLine(else_code)
                    return r if isinstance(r, int) else None
                return None
        elif TYPE == "JUMP":
            expr = code.replace("30실점", "", 1).strip()
            try:
                target = int(expr)
            except ValueError:
                raise ValueError(f"{expr}도 에겐같이 하네;;")
            return target

        elif TYPE == "END":
            raise SystemExit("\n탈선린해도 디미는 못간다 한울한울아")

        # 알 수 없는 라인 or 빈 줄
        return None

    # ===== 전체 실행 =====
    def compile(self, code: str, check: bool = True, errors: int = 100000):
        spliter = "\n" if "\n" in code else "~"
        code = code.rstrip().split(spliter)
        
        if not code:
            return

        if check:
            head = code[0].replace(" ", "")
            tail = code[-1].strip()
            if not head.startswith("대체누가") or tail != "디미고를 서류로 떨어짐?":
                raise SyntaxError("이게 어떻게 에겐이냐 ㅋㅋ")

        index = 0
        steps = 0
        while index < len(code):
            c = code[index].strip()
            res = self.compileLine(c)

            # int 리턴만 점프(1-based 가정)
            if isinstance(res, int):
                index = res - 2  # 곧 +1 되니까 -2
            # str 리턴 로직은 제거! (무한루프 방지)

            index += 1
            steps += 1
            if steps >= errors:
                raise RecursionError(f"{index}번째 줄에서 무한 루프가 감지되었습니다.")

    def compilePath(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            code = f.read()
        self.compile(code)
