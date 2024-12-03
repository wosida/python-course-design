from sorting import quick_pass, bubble_pass, heap_pass

# 按间距中的绿色按钮以运行脚本。
arr = [1, 3, 5, 2, 8, 7, 4]
if __name__ == '__main__':
    print("快速排序：", quick_pass.quick_sort(arr))
    print("冒泡排序：", bubble_pass.bubble_sort(arr))
    print("堆排序：", heap_pass.heap_sort(arr))
