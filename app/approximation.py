def log_data(data):
    with open("resources/logs.txt", "a", encoding="utf-8") as f:
        f.write(data + "\n")

def simp_calc(f, a, b):
    c = (a + b) / 2.0
    h = (b - a) / 6.0
    result = c, f(c), h * (f(a) + 4.0 * f(c) + f(b))
    log_data(f"Вычисление simp_calc: a={a}, b={b}, c={c}, h={h}, результат={result}")
    return result

def _adaptive_simpsons(f, a, fa, b, fb, eps, whole, c, fc, max_iter, current_iter=0):
    log_data(f"\nИтерация {current_iter}: a={a}, b={b}, eps={eps}, whole={whole}")
    log_data(f"Текущий интервал: [{a}, {b}], c={c}, fc={fc}")
    
    if current_iter >= max_iter:
        log_data(f"Достигнуто максимальное число итераций ({max_iter}). whole={whole}")
        return whole
    
    lc, flc, left = simp_calc(f, a, c)
    rc, frc, right = simp_calc(f, c, b)
    delta = left + right - whole
    
    log_data(f"Левая часть: [{a}, {c}], интеграл={left}")
    log_data(f"Правая часть: [{c}, {b}], интеграл={right}")
    log_data(f"Дельта: {delta}, 15*eps={15*eps}")
    
    if abs(delta) <= 15 * eps:
        result = left + right + delta / 15
        log_data(f"Сходимость достигнута. Результат={result}")
        return result
    
    log_data(f"Рекурсивный вызов с eps/2={eps/2}")
    left_integral = _adaptive_simpsons(f, a, fa, c, fc, eps/2, left, lc, flc, max_iter, current_iter + 1)
    right_integral = _adaptive_simpsons(f, c, fc, b, fb, eps/2, right, rc, frc, max_iter, current_iter + 1)
    
    total = left_integral + right_integral
    log_data(f"Суммарный результат после рекурсии: {total}")
    return total

def adaptive_simpsons(f, a, b, eps, max_iter):
    log_data(f"\nНачало adaptive_simpsons: a={a}, b={b}, eps={eps}, max_iter={max_iter}")
    fa, fb = f(a), f(b)
    c, fc, whole = simp_calc(f, a, b)
    log_data(f"Начальное приближение интеграла: {whole}")
    
    result = _adaptive_simpsons(f, a, fa, b, fb, eps, whole, c, fc, max_iter)
    log_data(f"Финальный результат: {result}")
    return result