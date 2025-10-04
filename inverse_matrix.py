import copy

def print_matrix(matrix, n, title):
    print(f"\n{title}:")
    if not matrix:
        print("행렬이 비어있습니다.")
        return
        
    print("┌" + "          " * n + "┐")
    for i in range(n):
        print("│", end="")
        for j in range(n):
            print(f"{matrix[i][j]:>9.4f}", end=" ")
        print("│")
    print("└" + "          " * n + "┘")

def get_inverse_matrix_input():
    try:
        n = int(input("정방행렬의 차수를 입력하세요: "))
        if n <= 0:
            print("오류: 행렬의 차수는 1 이상의 정수여야 합니다.")
            return None, 0
        
        print(f"{n}x{n} 행렬의 원소를 한 행씩 입력하세요. (각 숫자는 공백으로 구분)")
        matrix = []
        for i in range(n):
            while True:
                try:
                    row_str = input(f"{i+1}행: ")
                    row_list = [float(x) for x in row_str.split()]
                    if len(row_list) != n:
                        print(f"오류: 정확히 {n}개의 숫자를 입력해야 합니다.")
                        continue
                    matrix.append(row_list)
                    break
                except ValueError:
                    print("오류: 숫자 형식의 데이터만 입력해주세요.")
        return matrix, n
    except ValueError:
        print("오류: 차수는 정수로 입력해야 합니다.")
        return None, 0

def get_minor(matrix, i, j):
    return [row[:j] + row[j+1:] for row in (matrix[:i] + matrix[i+1:])]

def get_determinant(matrix):
    if len(matrix) == 1: return matrix[0][0]
    if len(matrix) == 2: return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    
    determinant = 0
    for c in range(len(matrix)):
        determinant += ((-1)**c) * matrix[0][c] * get_determinant(get_minor(matrix, 0, c))
    return determinant

def get_inverse_by_determinant(matrix, n):
    determinant = get_determinant(matrix)
    if abs(determinant) < 1e-9: return None

    cofactors = [[(((-1)**(r+c)) * get_determinant(get_minor(matrix, r, c))) for c in range(n)] for r in range(n)]
    adjugate = [[cofactors[j][i] for j in range(n)] for i in range(n)]
    return [[elem / determinant for elem in row] for row in adjugate]

def get_inverse_by_gauss_jordan(matrix, n):
    m = copy.deepcopy(matrix)
    identity = [[float(i == j) for i in range(n)] for j in range(n)]
    aug = [m[i] + identity[i] for i in range(n)]

    for i in range(n):
        pivot_row = max(range(i, n), key=lambda r: abs(aug[r][i]))
        aug[i], aug[pivot_row] = aug[pivot_row], aug[i]
        
        pivot = aug[i][i]
        if abs(pivot) < 1e-9: return None
        
        for j in range(i, 2 * n): aug[i][j] /= pivot
        
        for k in range(n):
            if i != k:
                factor = aug[k][i]
                for j in range(i, 2 * n): aug[k][j] -= factor * aug[i][j]
                        
    return [row[n:] for row in aug]

def compare_matrices(matrix1, matrix2, n, tolerance=1e-9):
    for i in range(n):
        for j in range(n):
            if abs(matrix1[i][j] - matrix2[i][j]) > tolerance: return False
    return True

def run_inverse_matrix_calculator():
    matrix, n = get_inverse_matrix_input()
    if matrix is None: return

    inv_det = get_inverse_by_determinant(matrix, n)
    inv_gj = get_inverse_by_gauss_jordan(matrix, n)
    
    if inv_det is None or inv_gj is None:
        print("\n오류: 행렬식이 0이므로 역행렬을 계산할 수 없습니다.")
        return

    print_matrix(inv_det, n, "행렬식으로 구한 역행렬")
    print_matrix(inv_gj, n, "가우스-조던 소거법으로 구한 역행렬")
    
    if compare_matrices(inv_det, inv_gj, n):
        print("\n=> 두 방법으로 계산한 역행렬의 결과가 동일합니다.")
    else:
        print("\n=> 두 방법으로 계산한 역행렬의 결과가 다릅니다.")

# 추가 기능 (선형 연립방정식 풀이)
def get_linear_system_input():
    try:
        n = int(input("미지수의 개수(방정식의 차수)를 입력하세요: "))
        if n <= 0:
            print("오류: 미지수의 개수는 1 이상의 정수여야 합니다.")
            return None, None, 0

        print(f"\n{n}x{n} 계수 행렬 A를 입력하세요. (각 행은 공백으로 구분)")
        matrix_a = []
        for i in range(n):
            while True:
                try:
                    row_str = input(f"{i+1}행: ")
                    row_list = [float(x) for x in row_str.split()]
                    if len(row_list) != n:
                        print(f"오류: 정확히 {n}개의 숫자를 입력해야 합니다.")
                        continue
                    matrix_a.append(row_list)
                    break
                except ValueError:
                    print("오류: 숫자 형식의 데이터만 입력해주세요.")

        print("\n결과 벡터 b를 입력하세요. (각 숫자는 공백으로 구분)")
        while True:
            try:
                b_str = input("b = ")
                vector_b = [float(x) for x in b_str.split()]
                if len(vector_b) != n:
                    print(f"오류: 정확히 {n}개의 숫자를 입력해야 합니다.")
                    continue
                break
            except ValueError:
                print("오류: 숫자 형식의 데이터만 입력해주세요.")
        
        return matrix_a, vector_b, n
    except ValueError:
        print("오류: 차수는 정수로 입력해야 합니다.")
        return None, None, 0

def solve_linear_system(matrix_a, vector_b, n):
    aug = [matrix_a[i] + [vector_b[i]] for i in range(n)]

    for i in range(n):
        pivot_row = max(range(i, n), key=lambda r: abs(aug[r][i]))
        aug[i], aug[pivot_row] = aug[pivot_row], aug[i]

        pivot = aug[i][i]
        if abs(pivot) < 1e-9: 
            return None 
        
        for j in range(i + 1, n):
            factor = aug[j][i] / pivot
            for k in range(i, n + 1):
                aug[j][k] -= factor * aug[i][k]
    
    x = [0] * n
    for i in range(n - 1, -1, -1):
        s = sum(aug[i][j] * x[j] for j in range(i + 1, n))
        x[i] = (aug[i][n] - s) / aug[i][i]
        
    return x

def run_linear_system_solver():
    matrix_a, vector_b, n = get_linear_system_input()
    if matrix_a is None: return

    solution = solve_linear_system(matrix_a, vector_b, n)

    if solution is None:
        print("\n해가 유일하게 존재하지 않습니다 (해가 없거나 무수히 많습니다).")
    else:
        print("\n연립방정식의 해:")
        for i in range(n):
            print(f"  x{i+1} = {solution[i]:.4f}")

def main():
    while True:
        print("\n" + "="*40)
        print("  수행할 작업을 선택하세요:")
        print("    1. 역행렬 계산")
        print("    2. 선형 연립방정식 풀이 (추가 기능)")
        print("    3. 프로그램 종료")
        print("="*40)
        
        choice = input("선택 > ")

        if choice == '1':
            run_inverse_matrix_calculator()
        elif choice == '2':
            run_linear_system_solver()
        elif choice == '3':
            print("프로그램을 종료합니다.")
            break
        else:
            print("오류: 1, 2, 3 중에서 선택해주세요.")

if __name__ == "__main__":
    main()