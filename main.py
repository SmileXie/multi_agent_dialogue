from openai import OpenAI

with open('.api_key', 'r') as file:
    api_key = file.read().strip()

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
def generate_ai_response(dialogue_history, system_message):
    # 将系统消息和对话历史拼接为 API 输入
    messages = [{"role": "system", "content": system_message}]
    messages.extend(dialogue_history)
    
    # 调用 OpenAI API
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    return response.choices[0].message.content

def ai_dialogue(system_message_1, system_message_2, trigger_message, end_flag, max_turns=10):
    dialogue = []  # 用于存储完整的对话内容
    ai1_history = []  # AI 1 的对话历史
    ai2_history = []  # AI 2 的对话历史
    current_message = trigger_message  # 当前消息
    current_speaker = "AI 1"  # 当前发言者
    ai1_history.append({"role": "user", "content": current_message})
    ai2_history.append({"role": "assistant", "content": current_message})

    for turn in range(max_turns):
        # 根据当前发言者选择系统消息和对话历史
        if current_speaker == "AI 1":
            system_message = system_message_1
            dialogue_history = ai1_history
        else:
            system_message = system_message_2
            dialogue_history = ai2_history
        
        # 生成 AI 的回复
        ai_response = generate_ai_response(dialogue_history, system_message)
        dialogue.append(f"{current_speaker}: {ai_response}")
        print(f"{current_speaker}: {ai_response}")
        
        # 将对方的消息（当前消息）添加到自己的对话历史中，作为 "assistant" 的角色
        if current_speaker == "AI 1":
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
        current_speaker = "AI 2" if current_speaker == "AI 1" else "AI 1"
    
    return dialogue

# 示例输入参数
system_message_1 = "你是一个老师，喜欢回答同学的提问。"
system_message_2 = "你是一个学生，喜欢刨根问底。"
trigger_message = "计算机为什么是二进制的"
end_flag = "再见"

# 执行对话
dialogue = ai_dialogue(system_message_1, system_message_2, trigger_message, end_flag)

# 输出对话内容
# for line in dialogue:
#     print(line)