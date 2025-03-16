# Multi Agent Dialogue

一个AI对话框架，基于大语言模型，快速配置两个相互对话AI Agent。打印并记录两个AI的对话文字。
两个对话的AI Agent可以完全模拟人类的对话。

# 配置与使用说明

首先，你要申请一个兼容openai SDK的LLM API接口。例如：[DeepSeek API Docs](https://api-docs.deepseek.com/zh-cn/) 或 [大模型服务平台百炼](https://help.aliyun.com/zh/model-studio/getting-started/what-is-model-studio?spm=5176.29619931.J_AHgvE-XDhTWrtotIBlDQQ.12.3f86521cS9GON8)。向LLM服务提供商申请API KEY并充值。

python3环境中安装openai SDK：

```
pip3 install openai
```

拷贝项目代码到本地：

```
git clone https://github.com/SmileXie/multi_agent_dialogue.git
cd multi_agent_dialogue
```

在multi_agent_diaglue目录下新增配置文件：

```json
{
    "api_key": "sk-xxx",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "model": "deepseek-v3",
    "AI1_name": "张老师",
    "AI2_name": "陈同学", 
    "AI1_character": "你是一个老师，喜欢回答同学的提问。不厌其烦。",
    "AI2_character": "你是一个学生，对世界充满好奇，喜欢刨根问底。",
    "trigger_message": "老师，计算机为什么是二进制的。",
    "end_flag": "",
    "max_turns": 10,
    "history_length": 10,
    "record_file": "record.txt"
}
```

**配置文件的字段说明：**

* api_key：你的LLM的API_KEY
* base_url：你的LLM的url（请查阅您的LLM API文档）
* model：你的LLM的模型名（请查阅您的LLM API文档）
* AI1_name：第一个AI Agent的名字
* AI2_name：第二个AI Agent的名字
* AI1_character：第一个AI Agent的人物设定
* AI2_character：第二个AI Agent的人物设定
* trigger_message：触发对话的第一句话，由AI2向AI1发起
* end_flag：当对话中出现end_flag时，即结束对话
* max_turns：最大对话轮次。即AI1+AI2总共的输出文字的次数限制
* record_file：对话记录的文件
* history_length：每次向LLM请求时携带的最大历史记录数

**执行对话**

```
$ $ python3 main.py -f config.json
陈同学: 老师，计算机为什么是二进制的。
张老师: 这个问题问得很好！计算机使用二进制是因为它只需要识别两种状态：开和关，也就是1和0。这比处理十种状态（0到9）要简单得多。而且，二进制系统在电子设备中实现起来非常可靠和高效。你有没有想过，为什么电子设备更容易处理二进制呢？
陈同学: 张老师，我明白了！那为什么电子设备更容易处理二进制呢？是因为电压的高低吗？
张老师: 没错！电子设备通常通过电压的高低来区分这两种状态。例如，高电压可以表示1，低电压可以表示0。这种简单的区分方法使得电子电路的设计和制造更加容易，也减少了出错的概率。你觉得这种设计还有什么优势吗？
陈同学: 张老师，我觉得这样设计是不是还能提高运算速度？因为只需要判断两种状态，计算机处理信息会更快？
...
```
