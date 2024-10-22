一、拉取專案
1.請先申請github帳號並，向吳承恩要求本庫的權限
2.下載git並登入github帳號 https://git-scm.com/downloads
3.開啟一個資料夾存放專案
4.在資料夾中開啟終端機 輸入: git clone https://github.com/Ryan7988/gin-study
5.在本地git上登入github帳號見<附件>

請先在gin-study資料夾加入名為.gitignore的檔案
可在檔案中以行為單位輸入不須上傳的檔案
ex. .gitignore #(檔案自身不上傳)#符號為註解
*.png   #表示所有副檔名為.png的檔案

二、嘗試更新專案 
1.在先前建立的資料夾中，會出現gin-stud資料夾
2.再names.txt輸入自己的名字嘗試更新專案
3.在git-stud開啟終端
4.如果有新增檔案，輸入:git add .
5.提交內容輸入:git commit -m "更新訊息的簡要內容"
6.最後合併上傳雲端輸入:git push
6.1.如果失敗，可能是有人更新過了，請先仔入最新內容後再嘗試輸入:git pull --rebase







<附件>
登入github帳號教學
如果遇到：「致命錯誤: 需要指定如何調和偏離的分支。」
這個錯誤是因為 GitHub 在 2021 年 8 月 13 日移除了對密碼進行身份驗證的支持，現在需要使用令牌（token）來進行身份驗證。這裡介紹如何使用 Personal Access Token (PAT) 來替代密碼。
解決步驟：
1. 生成 GitHub Personal Access Token (PAT)

登入 GitHub，然後進入你的 GitHub Settings。
在左側菜單中，選擇 Developer settings。
然後點選 Personal access tokens -> Tokens (classic)。
點擊 Generate new token，選擇 token 的用途，並根據需要選擇過期時間（建議選擇長一點的有效期，或者不過期）。
在 scopes 中，至少選擇 repo 來訪問和操作你的 GitHub repositories。最後點擊 Generate token。
複製 token，這個 token 只會顯示一次，之後無法再看到。

2. 在本地配置 Git 使用 PAT

當你要克隆（clone）、推送（push）或者拉取（pull）一個私有庫時，Git 會提示你進行身份驗證，這時你需要使用 GitHub username 以及剛剛生成的 token 來代替密碼進行身份驗證。

3. 使用 PAT 克隆 GitHub 庫

克隆 GitHub 庫的時候，像這樣使用 token：

bash
複製程式碼
git clone https://github.com/YourUsername/YourRepo.git
當 Git 要求你輸入密碼時，請輸入你的 Personal Access Token 而不是 GitHub 密碼。

4. 配置 Git 記住你的身份驗證憑證

為了避免每次都手動輸入你的 token，你可以配置 Git 來記住你的身份驗證憑證。

在 macOS 或 Linux 上使用以下命令：

bash
複製程式碼
git config --global credential.helper cache
在 Windows 上，使用：

bash
複製程式碼
git config --global credential.helper wincred
這樣下次再進行 Git 操作時，Git 就不會再要求你輸入密碼或 token 了。
