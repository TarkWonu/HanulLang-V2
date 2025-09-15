from runtime import janghanul   # runtime.py 안에 있는 클래스 import

# VM 인스턴스 만들기
vm = janghanul()

print("===== HanulLang 테스트 시작 =====")

vm.compileLine("디미 호에엥..")                   # var0 = 1
vm.compileLine("디이미 호에에에에에에에에에엥")   # var1 = 11

# [3] 조건: (11 - var0) → 0이면 종료
vm.compileLine("가을야구? 디이미 21대3 하와 훌쩍 디미 그러면 서류제출 디미 제발 아니면 30실점 15")

# [4] var0 += 1
vm.compileLine("디미 디미 21대3 호엥.")

# [5] 조건으로 점프
vm.compileLine("30실점 8")

vm.compileLine("탈선린")
vm.compileLine("디미고를 서류로 떨어짐?")


print("\n===== HanulLang 테스트 끝 =====")