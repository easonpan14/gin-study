#####
# 檔案功能整理

# gin_study
### pycache檔案
此檔案是用來加速編譯速度的快取檔，可以刪除，但通常沒必要。
- utils
此資料夾中的db.py，是用於連接料庫、操作資料庫的功能檔案，可以從此檔案中調用class去database獲取所需的資料出來。
- init
是一個執行檔，需要存在。
- asgi
Django被設置為asgi伺服器運行
- urls
定義url路由配置，將特定的 URL 模式映射到相應的視圖函數。
- views
Django 框架的视图模块，定义了多个视图函数和辅助函数，用于处理用户请求、与数据库交互以及呈现模板。
- wsgi
WSGI 是 Python 应用程序与 Web 服务器之间的标准接口，用于处理 Web 请求。

# static
本地端存放暫存或圖片資料的地方

# templates
介面模板，各功能都被存放於此
