class BrowserHistory:
    """
    浏览历史记录，主要用于前进和后退
    """

    def __init__(self):
        self.back_stack = []  # 后退历史栈
        self.forward_stack = []  # 前进历史栈
        self.max_history = 10  # 最大历史记录数

    def visit(self, page):
        if len(self.back_stack) > self.max_history:
            self.back_stack.pop(0)  # 移除最旧的记录
        self.back_stack.append(page)
        self.forward_stack.clear()  # 清空前进历史，因为访问新页面后不能前进

    def back(self):
        if len(self.back_stack) > 1:  # 至少有两个页面才能后退
            self.forward_stack.append(self.back_stack.pop())
            return self.back_stack[-1]
        else:
            return None  # 或者返回首页，或者抛出异常，根据具体需求

    def forward(self):
        if self.forward_stack:
            self.back_stack.append(self.forward_stack.pop())
            return self.back_stack[-1]
        else:
            return None  # 或者保持当前页面，或者抛出异常，根据具体需求


# 浏览历史记录
browserHistory = BrowserHistory()
