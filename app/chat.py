import langroid as lr
from langroid.language_models import OpenAIGPTConfig, Role, LLMMessage

cfg = OpenAIGPTConfig(
    chat_model="deepseek/deepseek-chat"
)

agent = lr.ChatAgent(
    lr.ChatAgentConfig(
        name="HelperBot",
        llm=cfg,
        system_message="You are a helpful assistant."
    )
)

task = lr.Task(agent)
task.run()
