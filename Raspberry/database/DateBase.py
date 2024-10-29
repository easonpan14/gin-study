import pymysql


################################################    about class    ################################################
# 數據庫連接配置
DB_CONFIG = {
    'host': '18.180.122.148',
    'user': 'admin',
    'password': 'LCivpNcrALc6YDK',
    'database': 'my_database',  # 替換為你的數據庫名稱
    'charset': 'utf8mb4',
}

# 用戶類 ID為唯一編號請以ID進行判斷
class User:
    def __init__(self, uID:int, name:str):
        self.uID = uID
        self.name = name



# 群組消息類    消息越晚,group_message_ID越大   uID為發送者 gID為群組
class GroupMessage:
    def __init__(self, group_message_ID:int, message:str,Group_ID:int, uID:int):
        self.gmID = group_message_ID                
        self.message = message
        self.Group_ID=Group_ID
        self.uID = uID


class Gpt:
    def __init__(self, Gpt_ID:int, subject:str,day:str, uID:int):
        self.Gpt_ID = Gpt_ID                
        self.subject = subject
        self.day=day
        self.uID = uID


class GptMessage:
    def __init__(self, group_message_ID:int, GPT_ID:int,message:str, sender:bool):
        self.gmID = group_message_ID 
        self.GPT_ID=GPT_ID               
        self.message = message
        self.sender=sender



################################################    about function    ################################################

# 連接到數據庫
def connect_db():
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except pymysql.MySQLError as e:
        print(f"SQL連線失敗: {e}")
        return None

# 1. 登錄檢查，返回 User 類，如果失敗返回 User(0, "")
def login_check(account:str, password:str)->User:
    user = User(0, "")
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT uID, name FROM User WHERE account = %s AND password = %s'
            cursor.execute(sql, (account, password))
            result = cursor.fetchone()
            if result:
                user = User(result[0], result[1])
              # 返回用戶信息
    finally:
        connection.close()
    return user

# 2. 註冊並檢查，返回 User 類，如果註冊失敗返回 User(0, "")
def register_and_login(name:str, account:str, password:str)->User:
    user = User(0, "")
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 先檢查賬號是否已存在
            sql = 'SELECT uID FROM User WHERE account = %s'
            cursor.execute(sql, (account,))
            result = cursor.fetchone()
            if result:
                return User(0, "")  # 如果賬號已存在，返回失敗

            # 插入新用戶數據
            sql = "INSERT INTO User (name, account, password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (name, account, password))
            connection.commit()  # 提交插入操作

            # 插入成功後自動登錄
            return login_check(account, password)
    finally:
        connection.close()





# 2. 根據 uID 查找姓名
def get_name_by_uid(uID:int)->str:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT name FROM User WHERE uID = %s"
            cursor.execute(sql, (uID))
            return cursor.fetchone()[0]  # 返回姓名
    finally:
        connection.close()

# 3. 根據 uID 查找群組，返回關於 list group_IDs about Group_ID
def get_groups_by_uid(uID:int)->list[int]:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT Group_ID FROM Group_Relation WHERE uID = %s"
            cursor.execute(sql, (uID))
            gropuIDs=[]
            get=cursor.fetchall()
            for row in get:
                gropuIDs.append(row[0])
            return gropuIDs # 返回群組列表
    finally:
        connection.close()

# 4. 根據 Group_ID 查找成員
def get_members_by_group_id(group_id:int)->list[int]:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT uID FROM Group_Relation WHERE Group_ID = %s"
            cursor.execute(sql, (group_id))
            uIDs=[]
            get=cursor.fetchall()
            for row in get:
                uIDs.append(row[0])
            return uIDs
    finally:
        connection.close()

# 5. 根據 Group_ID 查找對話記錄
def get_messages_by_group_id(group_id:int)->list[GroupMessage]:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT Group_Message_ID,Message,Group_ID,uID FROM Group_message WHERE Group_ID = %s"
            cursor.execute(sql, (group_id))
            messages=[]
            get=cursor.fetchall()
            for row in get:
                
                messages.append(GroupMessage(row[0],row[1],row[2],row[2]))
            return messages  # 返回對話記錄
    finally:
        connection.close()

# 6. 根據 uID 查找父母 uid
def get_parents_uid_by_uid(uID:int)->list[int]:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            parents=[]
            # 查找父母
            sql_parents = "SELECT Parent_uID FROM ParentChild WHERE Child_uID = %s"
            cursor.execute(sql_parents, (uID))
            get = cursor.fetchall()
            for row in get:
                parents.append(row[0])
            
            return parents
    finally:
        connection.close()

# 6.1 根據 uID 查找小孩 uid
def get_children_uid_by_uid(uID:int)->list[int]:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 查找小孩
            children=[]
            sql_children = "SELECT Child_uID FROM ParentChild WHERE Parent_uID = %s"
            cursor.execute(sql_children, (uID))
            get = cursor.fetchall()
            for row in get:
                children.append(row[0])
            return children  # 返回小孩
    finally:
        connection.close()

# 7. 建立群組，返回 Group_ID，如果失敗返回 -1
def create_group(group_name:str, uID:int)->int:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 插入群组
            sql = "INSERT INTO `Group` (Group_name) VALUES (%s)"
            cursor.execute(sql, (group_name,))
            # 獲得取插入的 Group_ID
            group_ID = cursor.lastrowid  # 獲得最後插入ID
            
            # 將用户加入群組
            relation_sql = "INSERT INTO Group_Relation (Group_ID, uID) VALUES (%s, %s)"
            cursor.execute(relation_sql, (group_ID, uID))
            
            connection.commit() 
            return group_ID  # 返回新建的 Group_ID
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()  # 出错时回滚
        return -1  # 返回 -1 表示失败
    finally:
        connection.close()

# 8. 加入群組
def join_group(group_ID: int, uID: int)->int:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 插入 Group_Relation 表，將用戶加入群組
            relation_sql = "INSERT INTO Group_Relation (Group_ID, uID) VALUES (%s, %s)"
            cursor.execute(relation_sql, (group_ID, uID))
            connection.commit()  # 提交更改
            
            return 1  # 加入成功
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()  # 回滾事務以防止數據損壞
        return -1  # 加入失敗
    finally:
        connection.close()

# 9. 傳送群組訊息，返回訊息class GroupMessag，如果失敗返回 GroupMessage 包含任意ID <=0 表示失敗
def send_group_message(group_ID:int, message:str, uID:int)->GroupMessage|int:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 插入群組訊息
            sql = "INSERT INTO Group_message (Message, Group_ID, uID) VALUES (%s, %s, %s)"
            cursor.execute(sql, (message, group_ID, uID))

            # 取得新訊息的 Group_Message_ID
            message_id = cursor.lastrowid  

            # 提交變更
            connection.commit()
            return GroupMessage(message_id,message,group_ID,uID)
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()  # 出錯時回滾
        return GroupMessage(-1,"",-1,-1)  # 包含任意ID <=0 表示失敗
    finally:
        connection.close()  # 關閉資料庫連接

# 10.家長發送建立關係的請求 
def send_family_request(parent_ID:id, child_ID:id):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO family_request (parent_ID, child_ID)
                VALUES (%s, %s)
            """
            cursor.execute(sql, (parent_ID, child_ID))
            connection.commit()
            print("請求已成功發送")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()

#11.查詢建立關係的請求
def select_family_request(uID:int):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            # 查找該用戶作為父母發出的請求
            sql_parent = """
                SELECT parent_ID, child_ID 
                FROM family_request 
                WHERE parent_ID = %s
            """
            cursor.execute(sql_parent, (uID,))
            sent_requests = cursor.fetchall()

            # 查找該用戶作為孩子收到的請求
            sql_child = """
                SELECT parent_ID, child_ID 
                FROM family_request 
                WHERE child_ID = %s
            """
            cursor.execute(sql_child, (uID,))
            received_requests = cursor.fetchall()

            return {
                'sent_requests': sent_requests,     # 該用戶作為父母發出的請求
                'received_requests': received_requests  # 該用戶作為孩子收到的請求
            }
    except Exception as e:
        print(f"Error: {e}")
        return None  # 返回空表示查詢失敗
    finally:
        connection.close()



# 11.孩子同意請求 
def agree_family_request(parent_uID:int, child_uID:int, agree:int):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            if agree == 1:
                # 同意请求，插入 ParentChild 表
                sql_insert = """
                    INSERT INTO ParentChild (Parent_uID, Child_uID) 
                    VALUES (%s, %s)
                """
                cursor.execute(sql_insert, (parent_uID, child_uID))

            # 刪除 family_request 表中的請求
            sql_delete = """
                DELETE FROM family_request 
                WHERE parent_ID = %s AND child_ID = %s
            """
            cursor.execute(sql_delete, (parent_uID, child_uID))

            # 提交更改
            connection.commit()
            print(f"處理完成: {'同意' if agree == 1 else '拒絕'}")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()  # 遇到错误时回滚事务
    finally:
        connection.close()

#12 新增GPT問題 day格式:"yyyy-mm-dd"
def insert_gpt(subject:str, day:str, uID:int)->int:
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO GPT (subject, day, uID) VALUES (%s, %s, %s)"
            cursor.execute(sql, (subject, day, uID))
            connection.commit()
            print("插入成功")
            return  cursor.lastrowid
    except Exception as e:
        print(f"插入失敗: {e}")
        connection.rollback()
        return -1
    finally:
        connection.close()

# 13 找出使用者的所有 GPT in list
def find_gpt(uID:int) -> list[Gpt]:
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


# 14 新增GTP訊息 send==1 user to gpt ,send==0 gpt to user
def insert_gpt_message(gpt_id:int, message:str, sender:bool):
    connection = connect_db()
    try:
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO GPT_MESSAGE (GPT_ID, message, sender) 
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (gpt_id, message, sender))
            connection.commit()
            print("消息插入成功")
    except Exception as e:
        print(f"插入失败: {e}")
        connection.rollback()
    finally:
        connection.close()

# 15 找GPT_ID内的消息
def find_gpt_message(GPT_ID:int) -> list[GptMessage]:
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
        connection.close()








# 示例使用
if __name__ == "__main__":
    # 測試登錄檢查
    user = login_check('Xiao_Ming', 'whM28Krc')
    print('Login User:', user.name,user.uID)

    # 測試根據 uID 查找姓名
    name = get_name_by_uid(1)
    print('User Name:', name)

    # 測試根據 uID 查找群組
    groups = get_groups_by_uid(4)
    print('User Groups:', groups)

    # 測試根據 Group_ID 查找成員
    members = get_members_by_group_id(1)
    print('Group Members:', members)

    # 測試根據 Group_ID 查找對話記錄
    messages = get_messages_by_group_id(1)
    print('Group Messages:', messages[0].message)

    # 測試根據 uID 查找父母或小孩
    relationships = get_parents_uid_by_uid(3)
    print('Relationships:', relationships)

    relationships = get_children_uid_by_uid(6)
    print('Relationships:', relationships)