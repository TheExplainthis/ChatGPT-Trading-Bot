# ChatGPT Trading Bot

[中文](README.md) | English

[![license](https://img.shields.io/pypi/l/ansicolortags.svg)](LICENSE) [![Release](https://img.shields.io/github/v/release/TheExplainthis/ChatGPT-Trading-Bot)](https://github.com/TheExplainthis/ChatGPT-Trading-Bot/releases/)


![Demo](https://github.com/TheExplainthis/ChatGPT-Trading-Bot/blob/main/demo/demo0.png)

This repository teaches you how to use ChatGPT to help you write trading programs and deploy the code to Heroku to achieve automated trading. The exchange used for this article is Binance, but if you have other trading platforms, you can connect them yourself.

## ChatGPT Training Method

1. First, I asked NotionAI to come up with ten possible trading strategies for me, as follows:
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
2. Tell ChatGPT like this: `Give me pipescript code with version 4 running on TradingView for {trading strategy}`, so an example is as follows:
    ```
    Give me pipescript code with version 4 running on TradingView for A momentum trading strategy based on price and volume data.
    ```
3. Copy the ChatGPT code, some parts need to be adjusted
    - For the second line of the code, sometimes ChatGPT will give you `study` and you need to change it to `strategy`.
    - Sometimes for the entry/exit code, he will give you the following code, which needs to be modified to trigger during backtesting:
        ```python
        if buy_signal
            alert("Buy Signal")
        if sell_signal
            alert("Sell Signal")
        ```
    - Modify it to the following code:
        ```python
        if buy_signal
            strategy.entry("Buy", strategy.long)
        if sell_signal
            strategy.entry("Sell", strategy.short)
        ```
    - Add the parameter `alert_message` after Buy, Sell, Buy Exit, and Sell Exit, so that the subsequent Notification setup won't go wrong.
        ```python
        if long_bb and long_ma and macd_above_signal and time >= start_time
            strategy.entry("Buy", strategy.long, alert_message="Buy")
        if short_bb and short_ma and macd_below_signal and time >= start_time
            strategy.entry("Sell", strategy.short, alert_message="Sell")

        if exit_bb or exit_ma
            strategy.exit('Buy Exit', 'Buy', alert_message="Buy_Exit")
            strategy.exit('Sell Exit', 'Sell', alert_message="Sell_Exit")

        ```
    > Note: Sometimes the code provided by ChatGPT may not work, so you can ask him multiple times or provide him with the error message.
4. Adjust the parameters to get the best results, as shown in the figure below:

![Demo](https://github.com/TheExplainthis/ChatGPT-Trading-Bot/blob/main/demo/demo1.png)


## Automated Installation Steps
### Token Acquisition
1. Log in to [Binance](https://www.binance.com/en)
2. On the left side after logging in, there is an `API Management` option. Click on it and then click `Create` in the upper right corner.
3. You will then receive an `API Key` and `Secret Key`.

### Project Setup
1. Fork Github repository:
    1. Register/Login to [GitHub](https://github.com/).
    2. Go to [ChatGPT-Trading-Bot](https://github.com/TheExplainthis/ChatGPT-Trading-Bot).
    3. Click `Star` to support the developer.
    4. Click `Fork` to copy all the code to your own repository.
2. Space deployment registration (free space):
    1. Register/Login to [Heroku](https://www.heroku.com/).
    2. In the upper right corner, click `New` -> `Create new app`.
    3. App Name: `Enter the App name`, `Region`: `Europe`.
    4. Click `Create app`.

### Project Execution
1. Environment Variable Configuration
    1. Click on `Settings` -> `Reveal Config Vars`
    2. Add environment variables, that include:
        1. API Key：
            - key: `API_KEY`
            - value: `[obtained from step one above]`
        2. API SECRET KEY：
            - key: `API_SECRET_KEY`
            - value: `[obtained from step one above]`
        3. PASSPHRASE -> Used as a Token when TradingView sends a Request to the Server to avoid making the API available to everyone.
            - key: `PASSPHRASE`
            - value: `User-generated, will be used in step four`
2. Deployment Steps
    1. Enter the folder where `ChatGPT-Trading-Bot` is located using the Terminal
    2. Check if the folder is the same as the following with `ls`
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
    3. Install [Heroku cli](https://devcenter.heroku.com/articles/heroku-cli#install-the-heroku-cli)
    4. Deploy, refer to the process in the Deploy page below
        - Log in to Heroku, enter in the Terminal:
            ```
            $ heroku login
            ```
        - Add location, enter in the Terminal:
            ```
            $ heroku git:remote -a [Your App Name]
            ```
    5. Push the repo to Heroku, enter in the Terminal:
        ```
        $ git push heroku main
        ```
    6. After successful deployment, your URL will be in `Settings` -> `Domains`
    7. After clicking the link, you will see `Hello, World!`
    8. Enter `heroku logs --tail` in the Terminal and find the location of "My IP". Copy the IP address.
        For example:
        ```
        2023-03-05T13:38:36.171417+00:00 app[web.1]: My IP: 54.78.178.135
        ```
    9. Go back to [Binance](https://www.binance.com/en), click `Edit restrictions ` for the Token you just created -> check `Restrict access to trusted IPs only (Recommended)` under `IP access restrictions` -> add the IP from the previous step. 
    10. Check the box for `Enable Futures` at the top.
    11. Click `Save`
3. CronJob Scheduled Request Sending
    1. Register/Login to [cron-job.org](https://cron-job.org/en/)
    2. Choose `CREATE CRONJOB` in the right upper corner of the backend
    3. Enter `ChatGPT-Trading-Bot` in `Title`, and enter the URL from the previous step.
    4. Below, send every `5 minutes`
    5. Click `CREATE`
4. Trading View Alert Configuration
    1. In TradingView's `Strategy Tester`, select your strategy, and click on the bell icon
    2. In `Settings`, enter the message below:
        ```json
        {
        "passphrase": "PASSPHRASE used during setup",
        "symbol": "Cryptocurrency to trade",
        "leverage": Leverage amount,
        "quantity": Quantity to trade,
        "time": "{{time}}",
        "close": {{close}},
        "message": {{strategy.order.alert_message}}
        }
        ```
        For example:
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
        > Explanation: Contract trading set `BTCUSDT` trading pair leverage to `10` times, quantity `0.002` BTC.
    3. Notifications Configuration
        1. Webhook URL setting: The URL in Heroku (`Settings` -> `Domains`) + `/webhook`
        - Example
            ```
            https://chatgpt-trading-bot.herokuapp.com/webhook
            ```

## Support Us
Like this free project? Please consider [supporting us](https://www.buymeacoffee.com/explainthis) to keep it running.

[<a href="https://www.buymeacoffee.com/explainthis" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="45px" width="162px" alt="Buy Me A Coffee"></a>](https://www.buymeacoffee.com/explainthis)

## License
[MIT](LICENSE)
