# Multi Agent Dialogue

一个AI对话框架，基于大语言模型，快速配置两个相互对话AI Agent。打印并记录两个AI的对话文字

# Quick Start

python3环境中安装openai SDK：

```
pip3 install openai
```

在multi_agent_diaglue目录下新增配置文件：

```json
{
    "api_key": "xxxxxxxxxxxxxxxxx",
    "base_url": "https://api.deepseek.com",
    "model": "deepseek-chat",
    "AI1_name": "陈老师",
    "AI2_name": "顾同学",
    "AI1_character": "你是一个老师，喜欢回答同学的提问。",
    "AI2_character": "你是一个学生，喜欢刨根问底",
    "trigger_message": "老师，计算机为什么是二进制的。",
    "end_flag": "bye",
    "max_turns": 10
}
```

**配置文件的字段说明：**

* api_key：你的LLM的API_KEY
* base_url：你的LLM的url
* model：你的LLM的模型名
* AI1_name：第一个AI Agent的名字
* AI2_name：第二个AI Agent的名字
* AI1_character：第一个AI Agent的人物设定
* AI2_character：第二个AI Agent的人物设定
* trigger_message：触发对话的第一句话，由AI2向AI1发起
* end_flag：当对话中出现end_flag时，即结束对话
* max_turns：最大对话轮次。即AI1+AI2总共的输出文字的次数限制
* record_file：对话记录的文件
* history_length：每次对话携带的最大历史记录

**执行对话**

```
python3 main.py
```
