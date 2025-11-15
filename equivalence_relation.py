import copy

def print_matrix(matrix, title=""):
    if title:
        print(title)
    if not matrix:
        print(" (빈 행렬)")
        return
    
    for row in matrix:
        print(" ".join(map(str, row)))
    print()

def boolean_product(A, B, n):
    C = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = C[i][j] or (A[i][k] and B[k][j])
    return C

def get_path_n_matrix(matrix, n, path_length):
    if path_length <= 0:
        print("경로 길이는 1 이상이어야 합니다.")
        return None
    
    if path_length == 1:
        return copy.deepcopy(matrix)

    result_matrix = boolean_product(matrix, matrix, n)
    
    for _ in range(path_length - 2):
        result_matrix = boolean_product(result_matrix, matrix, n)
        
    return result_matrix

def is_reflexive(matrix, n):
    for i in range(n):
        if matrix[i][i] == 0:
            return False
    return True

def is_symmetric(matrix, n):
    for i in range(n):
        for j in range(i + 1, n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True

def is_transitive(matrix, n):
    for i in range(n):
        for j in range(n):
            if matrix[i][j] == 1:
                for k in range(n):
                    if matrix[j][k] == 1:
                        if matrix[i][k] == 0:
                            return False
    return True

def print_equivalence_classes(matrix, n, A):
    print("\n[각 원소의 동치류]")
    
    partition = []
    visited_elements = set()

    for i in range(n):
        element_a = A[i]
        current_class = set()
        
        for j in range(n):
            if matrix[i][j] == 1:
                current_class.add(A[j])
        
        print(f"  [{element_a}] = {sorted(list(current_class))}")
        
        if element_a not in visited_elements:
            partition.append(sorted(list(current_class)))
            visited_elements.update(current_class)

    print(f"\n[집합 A의 분할 (Partition)]\n  {partition}")


def check_equivalence_and_print_classes(matrix, n, A):
    is_r = is_reflexive(matrix, n)
    is_s = is_symmetric(matrix, n)
    is_t = is_transitive(matrix, n)

    print("\n--- 관계 성질 판별 결과 ---")
    print(f"  1. 반사 관계 (Reflexive)  : {'예' if is_r else '아니오'}")
    print(f"  2. 대칭 관계 (Symmetric)  : {'예' if is_s else '아니오'}")
    print(f"  3. 추이 관계 (Transitive) : {'예' if is_t else '아니오'}")

    is_equivalence = is_r and is_s and is_t

    if is_equivalence:
        print("\n[최종 판결] 이 관계는 동치 관계입니다.")
        print_equivalence_classes(matrix, n, A)
        return True, is_r, is_s, is_t
    else:
        print("\n[최종 판결] 이 관계는 동치 관계가 아닙니다.")
        if not is_r: print("  (사유: 반사 관계가 아님)")
        if not is_s: print("  (사유: 대칭 관계가 아님)")
        if not is_t: print("  (사유: 추이 관계가 아님)")
        return False, is_r, is_s, is_t

def get_reflexive_closure(matrix, n):
    closure_matrix = copy.deepcopy(matrix)
    for i in range(n):
        closure_matrix[i][i] = 1
    return closure_matrix

def get_symmetric_closure(matrix, n):
    closure_matrix = copy.deepcopy(matrix)
    for i in range(n):
        for j in range(i + 1, n):
            if closure_matrix[i][j] == 1 or closure_matrix[j][i] == 1:
                closure_matrix[i][j] = 1
                closure_matrix[j][i] = 1
    return closure_matrix

def get_transitive_closure(matrix, n):
    closure_matrix = copy.deepcopy(matrix)
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                closure_matrix[i][j] = closure_matrix[i][j] or \
                                        (closure_matrix[i][k] and closure_matrix[k][j])
    return closure_matrix

def get_reachability_matrix(transitive_closure, n):
    reachability_matrix = copy.deepcopy(transitive_closure)
    for i in range(n):
        reachability_matrix[i][i] = 1
    return reachability_matrix

def get_relation_matrix(n):
    matrix = []
    print(f"집합 A = {{1, 2, 3, 4, 5}}에 대한 5x5 관계 행렬을 입력하세요.")
    print("각 행의 숫자 5개를 공백으로 구분하여 입력합니다. (예: 1 0 0 1 0)")
    
    for i in range(n):
        while True:
            try:
                row_input = input(f"  {i+1}행: ")
                row = list(map(int, row_input.split()))
                
                if len(row) != n:
                    print(f"오류: {n}개의 숫자를 입력해야 합니다.")
                    continue
                
                if not all(val in [0, 1] for val in row):
                    print("오류: 0 또는 1만 입력해야 합니다.")
                    continue
                    
                matrix.append(row)
                break
            except ValueError:
                print("오류: 유효한 숫자를 입력하세요.")
    return matrix

def main():
    N = 5
    A = [1, 2, 3, 4, 5]

    original_matrix = get_relation_matrix(N)
    print_matrix(original_matrix, "\n[입력된 원본 관계 행렬 M_R]")

    print("\n" + "="*40)
    print("✨ [추가 기능] 연결 관계 / 도달 관계 계산")
    print("="*40)
    
    connectivity_matrix = get_transitive_closure(original_matrix, N)
    print_matrix(connectivity_matrix, "\n[연결 관계 행렬 M_(R^∞) (추이 폐포)]")
    
    reachability_matrix = get_reachability_matrix(connectivity_matrix, N)
    print_matrix(reachability_matrix, "\n[도달 관계 행렬 M_(R*)]")

    print("\n" + "="*40)
    print("기존 기능 (동치 관계 판별)을 시작합니다.")
    print("="*40)

    is_equiv, is_r, is_s, is_t = check_equivalence_and_print_classes(original_matrix, N, A)

    if not is_equiv:
        print("\n" + "="*40)
        print("동치 관계가 아니므로, 폐포 변환을 시작합니다.")
        print("목표: R을 포함하는 가장 작은 동치 관계 생성")
        print("="*40 + "\n")
        
        processed_matrix = copy.deepcopy(original_matrix)
        
        print("--- (단계 1) 반사 폐포 적용 ---")
        if not is_r:
            reflexive_matrix = get_reflexive_closure(processed_matrix, N)
            print_matrix(processed_matrix, "(변환 전)")
            print_matrix(reflexive_matrix, "(변환 후: 반사 폐포 M_r)")
            processed_matrix = reflexive_matrix
        else:
            print("이미 반사 관계이므로 통과합니다.\n")

        print("--- (단계 2) 대칭 폐포 적용 ---")
        if not is_symmetric(processed_matrix, N): 
            symmetric_matrix = get_symmetric_closure(processed_matrix, N)
            print_matrix(processed_matrix, "(변환 전)")
            print_matrix(symmetric_matrix, "(변환 후: 대칭 폐포 M_s)")
            processed_matrix = symmetric_matrix
        else:
            print("이미 대칭 관계이므로 통과합니다.\n")

        print("--- (단계 3) 추이 폐포 적용 ---")
        if not is_transitive(processed_matrix, N):
            final_matrix = get_transitive_closure(processed_matrix, N)
            print_matrix(processed_matrix, "(변환 전)")
            print_matrix(final_matrix, "(변환 후: 추이 폐포 M_t)")
            processed_matrix = final_matrix
        else:
            print("이미 추이 관계이므로 통과합니다.\n")

        print("\n" + "="*40)
        print("모든 폐포 적용 완료. 최종 관계를 다시 판별합니다.")
        print("="*40)
        
        check_equivalence_and_print_classes(processed_matrix, N, A)


if __name__ == "__main__":
    main()