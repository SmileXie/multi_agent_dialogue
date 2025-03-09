import json
from openai import OpenAI

# 读取配置文件
with open('config.json', 'r') as file:
    config = json.load(file)

AI1_name = config["AI1_name"]
AI2_name = config["AI2_name"]

client = OpenAI(api_key=config['api_key'], base_url=config['base_url'])

def generate_ai_response(dialogue_history, system_message, model):
    # 将系统消息和对话历史拼接为 API 输入
    messages = [{"role": "system", "content": system_message}]
    messages.extend(dialogue_history)
    
    # 调用 OpenAI API
    response = client.chat.completions.create(
        model=model,
        messages=messages
    )
    return response.choices[0].message.content

def ai_dialogue(ai1_system_message, ai2_system_message, trigger_message, end_flag, max_turns=10):
    dialogue = []  # 用于存储完整的对话内容
    ai1_history = []  # AI 1 的对话历史
    ai2_history = []  # AI 2 的对话历史
    current_message = trigger_message  # 当前消息
    current_speaker = AI1_name  # 当前发言者
    ai1_history.append({"role": "user", "content": current_message})
    ai2_history.append({"role": "assistant", "content": current_message})

    for turn in range(max_turns):
        # 根据当前发言者选择系统消息和对话历史
        if current_speaker == AI1_name:
            system_message = ai1_system_message
            dialogue_history = ai1_history
        else:
            system_message = ai2_system_message
            dialogue_history = ai2_history
        
        # 生成 AI 的回复
        ai_response = generate_ai_response(dialogue_history, system_message, config['model'])
        dialogue.append(f"{current_speaker}: {ai_response}")
        print(f"{current_speaker}: {ai_response}")
        
        # 将对方的消息（当前消息）添加到自己的对话历史中，作为 "assistant" 的角色
        if current_speaker == AI1_name:
            ai2_history.append({"role": "user", "content": ai_response})
            ai1_history.append({"role": "assistant", "content": ai_response})
        else:
            ai1_history.append({"role": "user", "content": ai_response})
            ai2_history.append({"role": "assistant", "content": ai_response})
        
        # 检查是否达到结束标志
        if end_flag in ai_response:
            return dialogue
        
        # 更新当前消息和切换发言者
        current_message = ai_response
        current_speaker = AI2_name if current_speaker == AI1_name else AI1_name
    
    return dialogue

# 执行对话
shared_system_message = "请你基于你的人物设定，模拟真实人类的对话，与你的对话对象进行交流。你的人物设定是：\n"
AI1_system_message = shared_system_message + "你是" + config["AI1_name"] + "，" + config["AI1_character"] + "。\n" + "你现在的对话对象是：" + config["AI2_name"]
AI2_system_message = shared_system_message + "你是" + config["AI2_name"] + "，" + config["AI2_character"] + "。\n" + "你现在的对话对象是：" + config["AI1_name"]
dialogue = ai_dialogue(AI1_system_message, AI2_system_message, config['trigger_message'], config["end_flag"], config["max_turns"])

# 输出对话内容
# for line in dialogue:
#     print(line)
