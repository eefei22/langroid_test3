import langroid as lr
from langroid.language_models import OpenAIGPTConfig
from services.langroid_JournalAgent import RecordAudioTool

cfg = OpenAIGPTConfig(chat_model="deepseek/deepseek-chat")
agent = lr.ChatAgent(
    lr.ChatAgentConfig(
        name="HelperBot",
        llm=cfg,
        system_message="You are a helpful assistant.",
        use_tools=True,        
        use_functions_api=False
    )
)

agent.enable_message(RecordAudioTool)

task = lr.Task(agent)
task.run()
