# 詳細結構
## 使用者相關 Tables
### User
```
CREATE TABLE `User` (
  `uID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `account` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`uID`),
  UNIQUE KEY `account` (`account`),
  CONSTRAINT `User_chk_1` CHECK ((char_length(`account`) between 1 and 100)),
  CONSTRAINT `User_chk_2` CHECK ((char_length(`password`) between 1 and 100)),
  CONSTRAINT `User_chk_3` CHECK (regexp_like(`password`,_utf8mb4'^[a-zA-Z0-9]+$'))
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

```

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


### family_request
```
CREATE TABLE `family_request` (
  `parent_ID` int NOT NULL,
  `child_ID` int NOT NULL,
  PRIMARY KEY (`parent_ID`,`child_ID`),
  KEY `fk_child` (`child_ID`),
  CONSTRAINT `fk_child` FOREIGN KEY (`child_ID`) REFERENCES `User` (`uID`) ON DELETE CASCADE,
  CONSTRAINT `fk_parent` FOREIGN KEY (`parent_ID`) REFERENCES `User` (`uID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```


| Parent_uID  | Child_uID |
| :-----:|:-----:|
| 15| 9     |




### ParentChild
```
CREATE TABLE `ParentChild` (
  `Parent_uID` int NOT NULL,
  `Child_uID` int NOT NULL,
  PRIMARY KEY (`Parent_uID`,`Child_uID`),
  KEY `Child_uID` (`Child_uID`),
  CONSTRAINT `ParentChild_ibfk_1` FOREIGN KEY (`Parent_uID`) REFERENCES `User` (`uID`) ON DELETE CASCADE,
  CONSTRAINT `ParentChild_ibfk_2` FOREIGN KEY (`Child_uID`) REFERENCES `User` (`uID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```


| Parent_uID  | Child_uID |
| :-----:|:-----:|
| 3      | 0     |
| 6      | 0     |
| 4      | 1     |
| 7      | 1     |
| 5      | 2     |
| 8      | 2     |



## GPT Tabel
### GPT
```
CREATE TABLE `GPT` (
  `GPT_ID` int NOT NULL AUTO_INCREMENT,
  `subject` varchar(5) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `day` date NOT NULL,
  `uID` int NOT NULL,
  PRIMARY KEY (`GPT_ID`),
  KEY `fk_user` (`uID`),
  CONSTRAINT `fk_user` FOREIGN KEY (`uID`) REFERENCES `User` (`uID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=144 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

```
| GPT_ID   |suject|day| uID|
| :-----:|:----:|:------:|:------|
| 1      |   國文 |"2024-10-23"|   1    |
| 2      |    數學 | "2024-10-23"|    2   |
| 3      |     英文 |"2024-10-23" |    3   |
| 4      |   國文 | "2024-10-24" | 1    |

### GPT_MESSAGE
```
CREATE TABLE `GPT_MESSAGE` (
  `GPT_MESSAGE_ID` int NOT NULL AUTO_INCREMENT,
  `GPT_ID` int NOT NULL,
  `message` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `sender` tinyint(1) NOT NULL,
  PRIMARY KEY (`GPT_MESSAGE_ID`),
  KEY `fk_gpt` (`GPT_ID`),
  CONSTRAINT `fk_gpt` FOREIGN KEY (`GPT_ID`) REFERENCES `GPT` (`GPT_ID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=271 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

```
| GPT_MESSAGE_ID  | GPT_ID | message | sender (sender=0 gpt 傳給 user,否則表示 user 傳給 gpt) |
| :-----:|:-----:|:-----:|:-----:|
| 1      | 1     |赤壁賦的作者是誰|1|
| 2      | 1     | 蘇軾|0|
| 3      | 2     |1+1=?|1|
| 4      | 2     |2|0|
| 5      | 3    |HI|1|
| 6      | 3     |你好！有什么我能帮忙的吗？😊|0|
| 7      | 4    |  幫我找錯字  1.機器一按裝好，馬上就可以開工了。|1|
| 8      | 4     |按裝->安裝|0|

## 專注相關資料
### focus_time
```
CREATE TABLE `Focus_time` (
  `Focus_time_ID` int NOT NULL AUTO_INCREMENT,
  `uID` int NOT NULL,
  `day` date NOT NULL,
  `time` time NOT NULL,
  PRIMARY KEY (`Focus_time_ID`),
  KEY `fk_user_focus` (`uID`),
  CONSTRAINT `fk_user_focus` FOREIGN KEY (`uID`) REFERENCES `User` (`uID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

```
|focus_time_ID|uID|day|time|
|:----:|:---:|:---:|:---:|
|1|1|"2024-10-23"|2:01:25|
|2|3|"2024-10-23"|2:05:19|
|3|2|"2024-10-23"|3:52:09|
|4|2|"2024-10-24"|1:48:08|


## 群組相關 Tables

### Group
```
CREATE TABLE `Group` (
  `Group_ID` int NOT NULL AUTO_INCREMENT,
  `Group_name` varchar(100) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  PRIMARY KEY (`Group_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

```
| Group_ID  | Group_name |
| :-----:|:-----:|
| 0      | 家長群     |
| 1      | 學生群     |
| 2      | 相親相愛一家     |

### Group_Relation
```
CREATE TABLE `Group_Relation` (
  `Group_ID` int NOT NULL,
  `uID` int NOT NULL,
  PRIMARY KEY (`Group_ID`,`uID`),
  KEY `uID` (`uID`),
  CONSTRAINT `Group_Relation_ibfk_1` FOREIGN KEY (`Group_ID`) REFERENCES `Group` (`Group_ID`) ON DELETE CASCADE,
  CONSTRAINT `Group_Relation_ibfk_2` FOREIGN KEY (`uID`) REFERENCES `User` (`uID`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
```
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
```
CREATE TABLE `Group_message` (
  `Group_Message_ID` int NOT NULL AUTO_INCREMENT,
  `Message` varchar(255) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci NOT NULL,
  `Group_ID` int NOT NULL,
  `uID` int NOT NULL,
  PRIMARY KEY (`Group_Message_ID`),
  KEY `Group_ID` (`Group_ID`),
  KEY `uID` (`uID`),
  CONSTRAINT `Group_message_ibfk_1` FOREIGN KEY (`Group_ID`) REFERENCES `Group` (`Group_ID`) ON DELETE CASCADE,
  CONSTRAINT `Group_message_ibfk_2` FOREIGN KEY (`uID`) REFERENCES `User` (`uID`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

```
| Group_Message_ID | Message   | Group_ID|uID |
| :-----:|:-----:|:---:|:---: |
| 0      | 親師座談日通知     |  0   |    9 |
| 1      | 數學考試通知     |   1  |  1   |
| 2      | @明父明天記得參加親師座談     |   2  |  6   |
