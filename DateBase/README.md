
# SQL目前構想
* 使用者相關 Tables
* 群組相關 Tables
* 題目相關 Tables
* other Tables


# 其他需求設計撰寫處
* 歡迎補充或提出需求


## GPT 相關資料
### GPT
| GPT_ID  | GPT_TITLE | uID|
| :-----:|:-----:|:------|
| 1      |  考古問題    |   1    |
| 2      | 數學問題     |    2   |
| 3      |   我的GPT   |    3   |

### GPT_MESSAGE
| GPT_MESSAGE_ID  | GPT_ID | message | sender (sender=0 gpt 傳給 user,否則表示 user 傳給 gpt) |
| :-----:|:-----:|:-----:|:-----:|
| 1      | 1     |python 的 if 怎麼寫?|1|
| 2      | 1     | if(條件判斷): /n /t 後續執行條件|0|
| 3      | 2     |1+1=?|1|
| 4      | 2     |2|0|
| 5      | 3    |HI|1|
| 6      | 3     |你好！有什么我能帮忙的吗？😊|0|



# 相關 class
* 注意所有ID <= 0接表示失敗
### class User
* uID --唯一識別碼-- 資料庫查找時使用
* name
### GroupMessage
* group_message_ID --訊息的唯一識別碼--大小由舊到新，越新的數字越大
* message --訊息內容--
* Group_ID --群組唯一識別碼--表示訊息發到哪個群組
* uID  --訊息發送源uID--

# 相關 function

* 登入和註冊接回傳 class User uID==0表示失敗
```
login_check(account, password)
register_and_login(name, account, password)
```

* 根據 uID 查找姓名

return string
```
get_name_by_uid(uID)
```

* 根據 uID 查找父母,子女 uid

return list about uID
```
get_parents_uid_by_uid(uID)
get_children_uid_by_uid(uID)
```
* 發送建立關係的請求 
```
send_family_request(parent_ID, child_ID)
```
* 查詢建立關係的請求 不論父母子女都可查詢
```
select_family_request(uID)
```

* 同意請求 agree==1為同意 否則 不同意 運行後 皆會刪除請求
def agree_family_request(parent_uID, child_uID, agree):






* 建立群組 會回傳新群組的 group_ID
```
create_group(group_name, uID)
```


* 加入群組
```
join_group(group_ID,uID)
```

* 傳送群組訊息
```
send_group_message(group_ID, message, uID)
```

* 根據 uID 查找群組

return list about groupID
```
get_groups_by_uid(uID)
```



* 根據 Group_ID 查找成員

return list about uID
```
get_members_by_group_id(group_id)
```

* 根據 Group_ID 查找對話記錄

return list about class message
```
get_messages_by_group_id(group_id)
```
### 待補充



# 詳細結構
## 使用者相關 Tables
### User

| uID | name   |   account     | password    |
|:---:|:------:|:-------------:|:-----------:|
| 0   | 小明   |  Xiao_Ming    |   whM28Krc  |
| 1   | 小王   |  Xiao_Wang    |   3b9wN3T9  |
| 2   | 小美   |  Xiao_Mei     |  N5nZcSqZ   |
| 3   | 明父   |  Ming_Father  |   2BhPDT2p  |
| 4   | 王父   |  Prince_Father|  PHH4WhQ8   |
| 5   | 美父   |  Meifu_Father |   KUQDwArp  |
| 6   | 明母   |  Ming_Mother  |   85b576Fk  |
| 7   | 王母   |  Queen_Mother |   Q2pxD3E2  |
| 8   | 美母   |  Mei_Mothe    |  9RY7kBy4   |
| 9   | 老師A  |  Teacher_A    |  E3r3Cd85   |

### Parent_Child_Relation



| Parent_uID  | Child_uID |
| :-----:|:-----:|
| 3      | 0     |
| 6      | 0     |
| 4      | 1     |
| 7      | 1     |
| 5      | 2     |
| 8      | 2     |

## 群組相關 Tables

### Group
| Group_ID  | Group_name |
| :-----:|:-----:|
| 0      | 家長群     |
| 1      | 學生群     |
| 2      | 相親相愛一家     |

### Group_Relation
| Group_ID  | uID |
| :-----:|:-----:|
| 0      | 9     |
| 0      | 3     |
| 0      | 4     |
| 0      | 5     |
| 0      | 6     |
| 0      | 7     |
| 0      | 8     |
| 1      | 0     |
| 1      | 1     |
| 1      | 2     |
| 2      | 0     |
| 2      | 3     |
| 2      | 6     |

### Group_message
| Group_Message_ID | Message   | Group_ID|uID |
| :-----:|:-----:|:---:|:---: |
| 0      | 親師座談日通知     |  0   |    9 |
| 1      | 數學考試通知     |   1  |  1   |
| 2      | @明父明天記得參加親師座談     |   2  |  6   |


## 題目相關 Tables
* 設計中
