
# SQL目前構想
* 使用者相關 Tables
* 題目相關 Tables
* other Tables


# 其他需求設計撰寫處
* 歡迎補充或提出需求


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