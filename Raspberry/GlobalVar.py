from datetime import datetime
from openai import OpenAI

class GlobalVar:
    # Static variables
    uID = 0
    gpt_id = 0
    gpt_data = []
    client = OpenAI(
        api_key="sk-uJ3B62eXV4XouZSH7htWKYzf5QFj1W0WQd4AAn072WQPzptn",
        base_url="https://api.chatanywhere.tech/v1"
    )
    date_str = datetime.now().strftime("%Y-%m-%d")