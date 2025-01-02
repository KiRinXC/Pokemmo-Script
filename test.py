from collections import deque

class Window:
    def __init__(self, size=6):
        self.size = size
        self.window = deque(maxlen=size)  # 创建一个固定大小的双端队列

    def add(self, element):
        self.window.appendleft(element)  # 新元素放到队列最前面

    def get_window(self):
        return list(self.window)  # 返回当前窗口中的元素

# 测试
window = Window(size=6)
window.get_window()
# 添加元素并观察窗口状态
for i in range(10):
    window.add(i)
    print(window.get_window())

print(window.get_window()[0])