# ChatGPT Trading Bot

中文 | [English](README.en.md)

[![license](https://img.shields.io/pypi/l/ansicolortags.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/TheExplainthis/ChatGPT-Trading-Bot)](https://github.com/TheExplainthis/ChatGPT-Trading-Bot/releases/)


![Demo](https://github.com/TheExplainthis/ChatGPT-Trading-Bot/blob/main/demo/demo0.png)

這個 Repository 會教你如何叫 ChatGPT 幫你寫交易程式，並且將程式碼部署到 Heroku 上，實現自動化交易。本篇所串接的交易所為幣安交易所，若玩家們有其他交易平台，可以自行串接。

## ChatGPT 訓練方式
1. 首先，我先讓 NotionAI 幫我發想了十個可能的交易策略，如下：
    - A momentum trading strategy based on price and volume data
    - A mean reversion strategy using Bollinger Bands and RSI indicators
    - A trend following strategy using moving averages and MACD indicator
    - A breakout trading strategy based on support and resistance levels
    - A pairs trading strategy using cointegration analysis
    - A news-based trading strategy using sentiment analysis on financial news
    - An arbitrage trading strategy using cross-market analysis
    - A swing trading strategy using candlestick patterns and chart analysis
    - A quantitative trading strategy based on statistical models and machine learning algorithms
    - A position trading strategy using fundamental analysis and value investing principles
2. 跟 ChatGPT 這樣說：`Give me pipescript code with version 4 running on TradingView for {交易策略}` ，所以隨便一個範例如下：
    ```
    Give me pipescript code with version 4 running on TradingView for A momentum trading strategy based on price and volume data.
    ```
3. 複製 ChatGPT 的程式碼，有些部分需要微調
    - 針對程式碼的第二行，有時候 ChatGPT 會給你 `study` 要改成 `strategy` ，
    - 有時候進出場的那段程式碼，他會給你
        ```python
        if buy_signal
            alert("Buy Signal")
        if sell_signal
            alert("Sell Signal")
        ```
    - 要改成以下的程式碼，才會在回測時觸發
        ```python
        if buy_signal
            strategy.entry("Buy", strategy.long)
        if sell_signal
            strategy.entry("Sell", strategy.short)
        ```
    - 在 Buy, Sell, Buy Exit, Sell Exit 後面，需要添加參數 `alert_message`，這樣後續設定 Notification 時才不會出錯。
        ```python
        if long_bb and long_ma and macd_above_signal and time >= start_time
            strategy.entry("Buy", strategy.long, alert_message="Buy")
        if short_bb and short_ma and macd_below_signal and time >= start_time
            strategy.entry("Sell", strategy.short, alert_message="Sell")

        if exit_bb or exit_ma
            strategy.exit('Buy Exit', 'Buy', alert_message="Buy_Exit")
            strategy.exit('Sell Exit', 'Sell', alert_message="Sell_Exit")
        ```
    > 注意：有時候 ChatGPT 給你的程式碼會跑不動，因此可以多問他幾次，或者將錯誤訊息拋給他。
4. 調整參數，以獲得最好的成效，如下圖所示：

![Demo](https://github.com/TheExplainthis/ChatGPT-Trading-Bot/blob/main/demo/demo1.png)


## 自動化流程安裝步驟
### Token 取得
1. 登入 [Binance](https://www.binance.com/en)
2. 登入後左方有一個 `API Management` ，進入後再右上角按下 `Create`
3. 就會取得 `API Key` 和 `Secret Key`

### 專案設置
1. Fork Github 專案：
    1. 註冊/登入 [GitHub](https://github.com/)
    2. 進入 [ChatGPT-Trading-Bot](https://github.com/TheExplainthis/ChatGPT-Trading-Bot)
    3. 點選 `Star` 支持開發者
    4. 點選 `Fork` 複製全部的程式碼到自己的倉庫
2. 部署空間註冊（免費空間）：
    1. 註冊/登入 [Heroku](https://www.heroku.com/)
    2. 右上方有一個 `New` -> `Create new app`
    3. App Name: `輸入此 App 名稱` ， `Region`: `Europe`
    4. `Create app`
    > 注意：選擇部署平台時有兩個限制：幣安若需要合約交易，則需要有 IP 位置、幣安的 API 有地區限制，像是 IP 在美國的地區就無法使用。

### 專案執行
1. 環境變數設定
    1. 點擊 `Settings` -> `Reveal Config Vars`
    2. 新增環境變數，需新增：
        1. API Key：
            - key: `API_KEY`
            - value: `[由上方步驟一取得]`
        2. API SECRET KEY：
            - key: `API_SECRET_KEY`
            - value: `[由上方步驟一取得]`
        3. PASSPHRASE -> 用途是 TradingView 打 Request 到 Server 的時候，可以當作 Token 的東西，避免讓所有人都可以打 API
            - key: `PASSPHRASE`
            - value: `用戶自行生成，步驟四會再用到`
2. 部署步驟
    1. 利用 Terminal 進入 `ChatGPT-Trading-Bot` 所在的資料夾
    2. `ls` 看一下資料夾，是否和以下相同
        ```
        Procfile
        demo
        src
        main.py
        runtime.txt
        README.md
        README.en.md
        requirements.txt 
        ```
    3. 安裝 [Heroku cli](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)
    4. 部署，可參考 Deploy 頁面下方流程
        - 先登入 Heroku，在 Terminal 輸入：
            ```
            $ heroku login
            ```
        - 新增位置，在 Terminal 輸入：
            ```
            $ heroku git:remote -a [你的 App Name]
            ```
    5. 將 repo 推上 Heroku，在 Terminal 輸入：
        ```
        $ git push heroku main
        ```
    6. 部署成功後，你的網址列會在 `Settings` -> `Domains`
    7. 按下連結後，會看到 `Hello, World!`
    8. Terminal 輸入 `heroku logs --tail` 找到 "My IP" 的地方，把 IP 複製下來。例如：
        ```
        2023-03-05T13:38:36.171417+00:00 app[web.1]: My IP: 54.78.178.135
        ```
    9. 回到 [Binance](https://www.binance.com/en) ，剛剛那個 Token ，點擊 `Edit restrictions` -> 下方 `IP access restrictions` 勾選 `Restrict access to trusted IPs only (Recommended)` -> 並將上一步驟 IP 加進去。
    10. 上方 `Enable Futures` 打勾
    11. 按下 `Save`
3. CronJob 定時發送請求
    1. 註冊/登入 [cron-job.org](https://cron-job.org/en/)
    2. 進入後面板右上方選擇 `CREATE CRONJOB`
    3. `Title` 輸入 `ChatGPT-Trading-Bot`，網址輸入上一步驟的網址
    4. 下方則每 `5 分鐘` 打一次
    5. 按下 `CREATE`
4. Trading View Alert 設定
    1. 在 TradingView 下方 `Strategy Tester` ，選擇你的策略，並按下鬧鐘的 icon
    2. `Settings` 下方 Message 輸入：
        ```json
        {
        "passphrase": "環境設定時的 PASSPHRASE",
        "symbol": "要交易的幣種",
        "leverage": 槓桿數,
        "quantity": 要交易的數量,
        "time": "{{time}}",
        "close": {{close}},
        "message": {{strategy.order.alert_message}}
        }
        ```
        例如
        ```json
        {
        "passphrase": "Zw'4Tx^5/]f/pN>}fx*9m6<X,fxLx;x(",
        "symbol": "BTCUSDT",
        "leverage": 10,
        "quantity": 0.002,
        "time": "{{time}}",
        "close": {{close}},
        "message": {{strategy.order.alert_message}}
        }
        ```
        > 解釋：合約交易設定 `BTCUSDT` 交易對槓桿為 `10` 倍，數量為 `0.002` 個比特幣。
    3. Notifications 設定
        1. Webhook URL 設定： Heroku 裡的 URL （`Settings` -> `Domains` ）+ `/webhook`
        - 例如
            ```
            https://chatgpt-trading-bot.herokuapp.com/webhook
            ```

## 支持我們
如果你喜歡這個專案，願意[支持我們](https://www.buymeacoffee.com/explainthis)，可以請我們喝一杯咖啡，這會成為我們繼續前進的動力！

[<a href="https://www.buymeacoffee.com/explainthis" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="45px" width="162px" alt="Buy Me A Coffee"></a>](https://www.buymeacoffee.com/explainthis)

## 授權
[MIT](LICENSE)
