class BaseSort:
    @classmethod
    def quick_sort(cls, data):
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return cls.quick_sort(left) + middle + cls.quick_sort(right)

class ExtendedSort1(BaseSort):
    @classmethod
    def bubble_sort(cls, data):
        n = len(data)
        for i in range(n):
            for j in range(0, n-i-1):
                if data[j] > data[j+1]:
                    data[j], data[j+1] = data[j+1], data[j]
        return data

class ExtendedSort2(ExtendedSort1):
    @classmethod
    def heap_sort(cls, data):
        def heapify(arr, n, i):
            largest = i
            l = 2 * i + 1
            r = 2 * i + 2

            if l < n and arr[i] < arr[l]:
                largest = l

            if r < n and arr[largest] < arr[r]:
                largest = r

            if largest != i:
                arr[i], arr[largest] = arr[largest], arr[i]
                heapify(arr, n, largest)

        n = len(data)
        for i in range(n // 2 - 1, -1, -1):
            heapify(data, n, i)
        for i in range(n - 1, 0, -1):
            data[i], data[0] = data[0], data[i]
            heapify(data, i, 0)
        return data

# 在主程序中实例化 "ExtendedSort2" 类，使用不同的方法对给定的列表进行排序
data = [1, 3, 5, 2, 8, 7, 4]
if __name__ == '__main__':
  print("基类：",ExtendedSort2.quick_sort(data))  # 使用基类的排序方法
  print("第一个子类：",ExtendedSort2.bubble_sort(data))  # 使用第一个子类的排序方法
  print("第二个子类；",ExtendedSort2.heap_sort(data))  # 使用最后一个子类的排序方法
