from meet.Meet import Meet
from test.config import config
from test.router import Router

# 初始化APP
meet = Meet(config)
# 设置路由
meet.setRouter(Router())
meet.run()
