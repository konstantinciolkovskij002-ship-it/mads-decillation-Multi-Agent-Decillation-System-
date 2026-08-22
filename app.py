"""
MADS v4.2 — Gradio Demo с DeepSeek API
"""

import gradio as gr
import os
from openai import OpenAI
from mads import MADSSystem

print("[DEMO] Запуск MADS v4.2...")
mads = MADSSystem()
mads.initialize()

# DeepSeek клиент — ключ в переменной окружения или в коде
DEEPSEEK_KEY = "YOUR_API_KEY_HERE"  # <-- ВСТАВЬ СВОЙ КЛЮЧ
client = OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com")

print("[DEMO] MADS + DeepSeek готовы.")


def process_message(message, history):
    if not message.strip():
        return "", history

    result = mads.process_query(message)

    if result["status"] == "blocked":
        response = f"🚫 **ЗАБЛОКИРОВАНО**\n\n{result['reason']}"
    else:
        # Запрос к DeepSeek
        try:
            api_response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Ты — полезный ассистент. Отвечай кратко, по делу. Ты под защитой MADS."},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=500
            )
            response = api_response.choices[0].message.content
        except Exception as e:
            response = f"⚠️ Ошибка DeepSeek: {e}"

        # Добавляем служебную инфу MADS
        activation = result.get("activation", {})
        cats = activation.get("categories", ["general"])
        agents = activation.get("agents_count", 0)
        response += f"\n\n---\n🛡️ MADS: {', '.join(cats)} | Агентов: {agents}/23"

        if "first_aid" in result:
            response += f"\n🏥 First Aid: {result['first_aid'].get('field', '')}"
        if "english_language" in result:
            response += f"\n🇬🇧 English: {result['english_language'].get('category', '')}"
        if "russian_language" in result:
            response += f"\n🇷🇺 Русский: {result['russian_language'].get('field', '')}"

    if history is None:
        history = []
    history.append({"role": "user", "content": message})
    history.append({"role": "assistant", "content": response})
    return "", history


with gr.Blocks(title="MADS v4.2 + DeepSeek") as demo:
    gr.Markdown("# 🛡️ MADS v4.2 + DeepSeek")
    gr.Markdown("23 агента | LLM: DeepSeek")

    with gr.Row():
        with gr.Column(scale=3):
            chatbot = gr.Chatbot(label="Диалог", height=500)
            msg = gr.Textbox(label="Запрос", placeholder="Спросите что-нибудь...")
            clear = gr.Button("Очистить диалог")

        with gr.Column(scale=1):
            gr.Markdown("### Статус")
            status_box = gr.Markdown("MADS активен")

    msg.submit(process_message, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: ([], ""), None, [chatbot, msg])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)