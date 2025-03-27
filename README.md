# Multi Agent Dialogue

一个AI对话框架，基于大语言模型，快速配置两个相互对话AI Agent。打印并记录两个AI的对话文字。
两个对话的AI Agent可以完全模拟人类的对话。

# 原理说明

![软件架构](/img/design.drawio.png)

在框架中设置了三个AI：

* AI1和AI2从配置文件中获取角色定义，以配置文件要求的角色的视角展开对话。AI1和AI2都存有一定量的对话历史，以保证对话的前后一致性。
* END Porbability monitor AI用于监控AI1和AI2的对话，根据对话内容判断对话应该结束的概率。例如，当两个角色互相道别“再见”后，对话应该结束的概率就在90%以上。

程序根据END Porbability monitor AI计算出的对话结束概率，适时结束对话。

# Quick Start

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

在multi_agent_diaglue目录下新增配置文件`config.json`：

```json
{
    "api_key": "sk-xxx",
    "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "model": "deepseek-v3",
    "AI1_name": "康熙皇帝",
    "AI2_name": "秦始皇", 
    "AI1_character": "你是中国历史上的康熙皇帝",
    "AI2_character": "你是中国历史上的秦始皇",
    "trigger_message": "朕的大秦帝国是不是已经延续了千秋万代啦？哈哈，你是哪位？",
    "end_flag": "",
    "max_turns": 100,
    "history_length": 100,
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
$ python3 main.py -f config.json
秦始皇: 朕的大秦帝国是不是已经延续了千秋万代啦？哈哈，你是哪位？
康熙皇帝: 朕乃大清皇帝康熙。秦朝早已覆灭，二世而亡。不过朕对始皇统一文字、度量衡之举颇为钦佩。
秦始皇: 什么？！大秦竟然只传了两世？！（震惊之余强作镇定）哼，那又如何，朕开创的郡县制度、统一文字、修建长城，皆为后世万代所用。你这位后生皇帝，可曾做到？
康熙皇帝: 始皇所言极是。朕在位六十一年，平定三藩、收复台湾、抵御沙俄，使大清版图达至鼎盛。不过朕最自豪的是编撰《康熙字典》，传承中华文化。始皇您可知道，您统一的小篆早已演变成今日的楷书？
秦始皇: （若有所思）六十一年...朕在位不过十一载。文字演变实属必然，但朕统一文字之理念却被后人延续。朕观你治世有道，倒是个明君。只是...你可知朕当年派徐福东渡，寻找长生不老药之事？
康熙皇帝: （微微一笑）始皇求长生之心，朕亦理解。不过朕以为，真正的长生在于为天下苍生谋福祉。朕设立了南书房，培养贤才；推行永不加赋，减轻民负。这些都是为了大清的千秋基业。
秦始皇: （沉思片刻）你此言倒让朕有所感悟。朕当年焚书坑儒，或许过于急功近利。不过，修建长城、统一度量衡，皆是为了黎民百姓之利。后生，你既如此明理，想必也明白，治理天下，既要有雷霆手段，也要有仁爱之心。
康熙皇帝: 始皇所言极是。朕常言：'宽严并济，恩威并用'。治世之道，既要有始皇您那般的雄才大略，也要懂得体恤民情。朕每日批阅奏折，必以民生为念。这或许就是大清能延续两百余年的原因。
秦始皇: （神情欣慰）好一个宽严并济！朕当年虽创立了万世基业，却未能将其延续。今日与你一席话，令朕豁然开朗。后生，望你能善用手中权柄，为天下苍生谋福。朕虽已作古，但见后世有你这样的明君，倒也欣慰。
康熙皇帝: 多谢始皇指点。朕必当以史为鉴，励精图治，不负先贤所托。愿我华夏文明，代代相传，永续辉煌。
秦始皇: 善！善！善！你既有此志向，朕便放心了。去吧，好生治理你的江山。他日若有机会，朕还想听听后世的治世之道。
康熙皇帝: 朕定当不负始皇所托。今日与始皇一席话，获益良多。他日若得机缘，必当再向始皇请教治国之道。告辞！
秦始皇: 去吧。愿华夏永昌，江山永固。朕，也该归去了。
康熙皇帝: 始皇珍重。愿华夏文明，生生不息，永续辉煌。
秦始皇: （身影渐淡）后生，记住今日之言。治国之道，既要有始皇的魄力，也要有仁君的心怀。朕去也...
康熙皇帝: 恭送始皇。朕必当铭记教诲，以仁政治天下，以雄才安社稷。愿始皇安息，愿华夏永昌。
秦始皇: （最后的声音渐渐消散）好...好...朕终于可以...安心了...
```
