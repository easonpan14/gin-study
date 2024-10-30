from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .utils.db import login_check, register_and_login, send_family_request,get_name_by_uid
import matplotlib.pyplot as plt
import io
import base64
from matplotlib import font_manager
import pymysql
from typing import List  # 新增這行
from datetime import date
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']  # 微軟正黑體


account=""
password=""
DB_CONFIG = {
    'host': '18.180.122.148',
    'user': 'admin',
    'password': 'LCivpNcrALc6YDK',
    'database': 'my_database',  # 替換為你的數據庫名稱
    'charset': 'utf8mb4',
}

class User:
    def __init__(self, uID:int, name:str):
        self.uID = uID
        self.name = name
    def __str__ (self):
        return f"User(uID={self.uID},name={self.name})"

class Gpt:
    def __init__(self, Gpt_ID:int, subject:str,day:str, uID:int):
        self.Gpt_ID = Gpt_ID                
        self.subject = subject
        self.day=day
        self.uID = uID
    def __str__ (self):
        return f"Gpt(Gpt_ID={self.Gpt_ID},subject={self.subject},day={self.day},uID={self.uID})"

class GptMessage:
    def __init__(self, group_message_ID:int, GPT_ID:int,message:str, sender:bool):
        self.gmID = group_message_ID 
        self.GPT_ID=GPT_ID               
        self.message = message
        self.sender=sender
    def __str__ (self):
        return f"GptMessage(group_message_ID={self.group_message_ID},GPT_ID={self.GPT_ID},message={self.message},sender={self.sender})"
    


def connect_db():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except pymysql.MySQLError as e:
        print(f"SQL連線失敗: {e}")
        return None
    
    
def find_gpt_message(GPT_ID: int) -> List[GptMessage]:  # 使用 List[GptMessage] 替代 list[GptMessage]
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM GPT_MESSAGE WHERE GPT_ID=%s"
            cursor.execute(sql, (GPT_ID,))
            get = cursor.fetchall()
            GPTs = []
            for GPT in get:
                GPTs.append(GptMessage(GPT[0], GPT[1], GPT[2], GPT[3]))  # 修正构造方式
            return GPTs
    except Exception as e:
        print(f"Error: {e}")
        return [GptMessage(-1, -1, "", 0)]  # 失败返回ID=-1
    finally:
        if connection:
            connection.close()
            
def find_gpt(uID:int) -> List[Gpt]:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT GPT_ID, subject, day, uID FROM GPT WHERE uID=%s"
            cursor.execute(sql, (uID,))
            get = cursor.fetchall()
            GPTs = []
            for GPT in get:
                GPTs.append(Gpt(GPT[0], GPT[1], GPT[2], GPT[3]))  # 修正构造方式
            return GPTs
    except Exception as e:
        print(f"Error: {e}")
        return [Gpt(-1, "", "", -1)]  # 返回空表示查询失败
    finally:
        connection.close()


def analysis_subject(request, subject):
    # 驗證用戶是否登入
    user = login_check(account, password)
    if user is None:
        return redirect('login')
    # 根據用戶的 uID 查詢 GPT 資料
    gpt_data = find_gpt(user.uID)
    display_data = []
    filtered_gpt_data = [gpt_item for gpt_item in gpt_data if gpt_item.subject == subject]
    for gpt_item in filtered_gpt_data:
        # 根據 GPT_ID 查詢相關訊息
        messages = find_gpt_message(gpt_item.Gpt_ID)
        
        sender0_message = "無訊息"
        sender1_message = "無訊息"

        for msg in messages:
            if msg.sender == 0:
                sender0_message = msg.message
            elif msg.sender == 1:
                sender1_message = msg.message

        date_str = gpt_item.day.strftime("%Y-%m-%d") if isinstance(gpt_item.day, date) else str(gpt_item.day)

        display_data.append({
            'sender0_message': sender0_message,
            'sender1_message': sender1_message,
            'date_str': date_str,
        })

    print("最終顯示資料:", display_data)

    return render(request, 'analysis_subject.html', {'display_data': display_data, 'subject': subject})



def home(request):
    return render(request, 'home.html')
        
def login_view(request):
    if request.method == 'POST':
        global password,account
        account = request.POST.get('account')
        password = request.POST.get('password')
        user = login_check(account, password)
        
        if user.uID != 0:
            # 登錄成功，傳遞 success 變量到前端
            return render(request, 'home.html', {'success': True})
        else:
            # 登錄失敗，傳遞 error 信息到前端
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        account = request.POST.get('account')
        password = request.POST.get('password')
        user = register_and_login(name, account, password)
        
        if user.uID != 0:
            # 註冊成功，重定向到登錄頁面
            return redirect('login')
        else:
            # 註冊失敗，重新渲染頁面並顯示錯誤信息
            return render(request, 'register.html', {'error': 'Registration failed'})
    
    return render(request, 'register.html')
def calculate_mistake_counts(gpt_data):
    # 設置要計算的科目
    subjects = ['國文', '英文', '數學', '自然', '社會']
    
    # 初始化錯題數量字典
    mistake_counts = {subject: 0 for subject in subjects}

    # 遍歷 gpt_data，統計每個科目的錯題數量
    for gpt_item in gpt_data:
        if gpt_item.subject in mistake_counts:
            mistake_counts[gpt_item.subject] += 1  # 增加對應科目的錯題數量

    # 將字典轉換為列表，保持科目的順序
    return [mistake_counts[subject] for subject in subjects]
def analysis_view(request):

    # 數據
    subjects = ["Chinese", 'English', 'Math', 'Science', 'Social']
    mistake_counts = [100, 150, 200, 130, 170]
    user = login_check(account, password)
    # 獲取用戶的 GPT 資料
    gpt_data = find_gpt(user.uID)  # 在這裡獲取 gpt_data
    mistake_counts = calculate_mistake_counts(gpt_data)
    
    # 生成圖表並應用字體
    plt.figure(figsize=(10, 5))
    plt.bar(subjects, mistake_counts, color=['#A8A8D3', '#D9B3FF', '#FFA7A7', '#FFE5B4', '#B0E0A8'])
    plt.xlabel("科目")
    plt.ylabel("錯題數量")
    plt.title("各科錯題數統計")

    # 將圖表轉為 Base64 編碼的圖片
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close()

    return render(request, 'analysis.html', {'chart_image': image_base64})


def emo_view(request):
    return render(request, 'emo.html')





from django.shortcuts import render, redirect
from .utils.db import login_check, send_family_request, get_name_by_uid


from django.contrib import messages  # 导入消息框架

def add_child_view(request):
    if request.method == 'POST':
        uID = request.POST.get('uID')

        # 驗證用戶登錄
        user = login_check(account, password)

        if user and user.uID != 0:  # 檢查用戶對象和 uID
            name = get_name_by_uid(uID)  # 獲取 UID 對應的姓名
            print(1)
            
            if name:  # 如果找到了對應的名字
                print(1)
                r = send_family_request(user.uID, uID)  # 發送家庭請求
                print(1)
                if r == -1:
                    print(1)
                    messages.error(request, '請求發送失敗')
                else:
                    messages.success(request, '已成功發送請求')
                    print(1)
            else:
                messages.error(request, '此 UID 不存在，請確認後再試')
                print(1)
        else:
            messages.error(request, '無效的憑證')  # 如果登錄失敗，使用消息框架提供錯誤信息

    return render(request, 'add_Child.html')
