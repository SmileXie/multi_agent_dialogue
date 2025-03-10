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

def ai_dialogue(ai1_system_message, ai2_system_message, trigger_message, end_flag, max_turns=10, history_length=20):
    dialogue = []  # 用于存储完整的对话内容
    ai1_history = []  # AI 1 的对话历史
    ai2_history = []  # AI 2 的对话历史
    current_message = trigger_message  # 当前消息
    current_speaker = AI1_name  # 当前发言者
    ai1_history.append({"role": "user", "content": current_message})
    ai2_history.append({"role": "assistant", "content": current_message})

    with open(config['record_file'], 'w') as record_file:
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
            record_file.write(f"{current_speaker}: {ai_response}\n")
            
            # 将对方的消息（当前消息）添加到自己的对话历史中，作为 "assistant" 的角色
            if current_speaker == AI1_name:
                ai2_history.append({"role": "user", "content": ai_response})
                ai1_history.append({"role": "assistant", "content": ai_response})
            else:
                ai1_history.append({"role": "user", "content": ai_response})
                ai2_history.append({"role": "assistant", "content": ai_response})
            
            if len(ai1_history) > history_length:
                ai1_history.pop(0)
            if len(ai2_history) > history_length:
                ai2_history.pop(0)

            # 检查是否达到结束标志
            if len(end_flag) > 0 and (end_flag in ai_response):
                return dialogue
            
            # 更新当前消息和切换发言者
            current_message = ai_response
            current_speaker = AI2_name if current_speaker == AI1_name else AI1_name
    
    return dialogue

# 执行对话
shared_system_message = "请你基于你的人物设定，模拟最自然最真实人类的对话，与你的对话对象进行交流。要求如下：\n\
    * 当对话涉及场景切换时，可以在下一轮对话中进入新的场景。例如：如果对话双方约定周末再见，那么在相互告别后，下一轮对话就模拟两人周末见面的对话。\n\
    * 在输出的文字中，请以圆括号来表示内心活动，以方括号来表示人物动作和场景相关的信息，不加括号的内容表示说出的话。例如：'(看着吵吵闹闹的同学们，心里烦得很)[站在讲台上]全部给我起立。'\n\
    * 随着对话的推进和影响，你的人物设定可以有所变更，但变更方向和速度应符合通常的人类性格变化的逻辑和规则。\n\
    你的初始人物设定是："
AI1_system_message = shared_system_message + "你是" + config["AI1_name"] + "，" + config["AI1_character"] \
    + "。\n" + "你现在的对话对象是：" + config["AI2_name"]
AI2_system_message = shared_system_message + "你是" + config["AI2_name"] + "，" + config["AI2_character"] \
    + "。\n" + "你现在的对话对象是：" + config["AI1_name"]
dialogue = ai_dialogue(AI1_system_message, AI2_system_message, config['trigger_message'], 
                       config["end_flag"], config["max_turns"], config['history_length'])
