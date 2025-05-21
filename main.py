import gradio as gr
from reading_page import read_github_profile
from model_functions import format_text_for_LLM, api_key, call_llm
from logger import return_logger
from colorama import Fore, Style

File_logger = return_logger()

github_info_store = {"username": "massimilianoSirgiovanni"}

def load_github_profile(username):
    try:
        read_github_profile(username)
        github_info_store["username"] = username
        File_logger.info(f"LOADED PROFILE: {username}\n")
        return f"✅ Loaded profile GitHub: {username}"
    except Exception as e:
        File_logger.info(f"ERROR DORING LOGGING TO: {username}\n    - FOUND EXCEPTION: {e}")
        return f"❌ ERROR: Unable to load {username}! Please double check if the username is correct."

def chat_with_model_gradio(user_input, history):
    if history is None:
        history = []
    github_info = read_github_profile(username=github_info_store.get("username"))
    context_list = []
    for msg in history:
        context_list.extend(msg)
    File_logger.info(f"[User] {user_input}\n")
    context_list.append(user_input)
    prompt = format_text_for_LLM(user_input, "\n".join(context_list), github_info)
    response = call_llm(api_key, "deepseek/deepseek-chat-v3-0324", prompt)
    File_logger.info(f"[G.H.O.S.T.] {response}\n")
    history.append((user_input, response))

    if len(history) > 4:
        history = history[-4:]

    return history, history, ""

with gr.Blocks() as demo:
    gr.Markdown("## 🤖 G.H.O.S.T. (GitHub Overview & Summary Tool)")
    github_profile = github_info_store.get("username")
    with gr.Row():
        github_username = gr.Textbox(label="Name GitHub User", value="massimilianoSirgiovanni")
        load_button = gr.Button("Load Profile")
    github_status = gr.Markdown(f"Load Github profile: {github_profile}")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(label="", placeholder="Ask a Question...")
    clear = gr.Button("Clean_chat")

    state = gr.State([])

    load_button.click(load_github_profile, github_username, github_status)

    msg.submit(chat_with_model_gradio, [msg, state], [chatbot, state, msg])
    clear.click(lambda: ([], []), None, [chatbot, state])

print(f"{Fore.LIGHTMAGENTA_EX}G.H.O.S.T. is available at:{Style.RESET_ALL} http://localhost:9999", flush=True)
demo.launch(server_name="0.0.0.0", server_port=7860, share=True)
