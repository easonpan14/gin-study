# 相關 class
* 注意所有ID <= 0接表示失敗
### class User
* uID --唯一識別碼-- 資料庫查找時使用
* name


### class Gpt
* Gpt_ID --唯一識別碼--資料庫查找時使用
* subject --提問科目--
* day --提問日期--
* uID --提問者--


### class GptMessage
* gmID --唯一識別碼--資料庫查找時使用
* GPT_ID --屬於哪組Gpt的對話--
* message --對話內容--
* sender --誰傳送的消息:0為 gpt 傳給 user,否則表示 user 傳給 gpt--

### class FocusTime
* uID --屬於哪位user--
* day --日期--
* time --專注時間--

### GroupMessage
* group_message_ID --訊息的唯一識別碼--大小由舊到新，越新的數字越大
* message --訊息內容--
* Group_ID --群組唯一識別碼--表示訊息發到哪個群組
* uID  --訊息發送源uID--



# 相關 function

User
-
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

family
---
* 根據 uID 查找父母,子女 uid

return list about uID
```
get_parents_uid_by_uid(uID)
get_children_uid_by_uid(uID)
```
* 父母發送建立關係的請求 
```
send_family_request(parent_ID, child_ID)
```
* 查詢建立關係的請求 不論父母子女都可查詢
```
select_family_request(uID)
```

* 子女同意請求 agree==1為同意 否則 不同意 運行後 皆會刪除請求
```
agree_family_request(parent_uID, child_uID, agree):
```

GPT
---

* 新增GPT問題 day格式:"yyyy-mm-dd"

return gpt_ID
```
insert_gpt(subject, day, uID)
```

* 找出使用者的所有 

return GPT_ID in list
```
find_gpt(uID)
```

* 新增GTP訊息 send==1 user to gpt ,send==0 gpt to user
```
insert_gpt_message(gpt_id, message, sender)
```

* 找GPT_ID内的消息

return list[class GPTMessage]
```
find_gpt_message(GPT_ID)
```





FouseTime
---

* 插入FouseTime 
```
insert_focus_time(uID, day, time)
```
* 根據找uID查找每日注意力時間

return list[FocusTime]
```
find_focus_time(uID)
```

Group
---


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
