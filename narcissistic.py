# 定义一个生成器函数来生成水仙花数
def narcissistic_number_generator():
    for num in range(100, 1000):
        temp = num
        _sum = 0
        while temp > 0:
            digit = temp % 10
            _sum += digit ** 3
            temp //= 10
        if _sum == num:
            yield num


# 使用迭代器打印输出结果
narcissistic_iter = narcissistic_number_generator()
if __name__ == '__main__':
    for narcissistic_num in narcissistic_iter:
        print(narcissistic_num)
