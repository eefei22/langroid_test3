import os
import langroid as lr
from dotenv import load_dotenv
from langroid.language_models import OpenAIGPTConfig
from langroid.agent.chat_agent import ChatAgent, ChatAgentConfig
from langroid.agent.task import Task

from app.services import journal_Manager

# Load API keys from .env
load_dotenv()

# Use DeepSeek with OpenAI-compatible wrapper
llm_cfg = OpenAIGPTConfig(
    chat_model="deepseek/deepseek-chat",
    api_base="https://api.deepseek.com/v1",
    api_key=os.getenv("DEEPSEEK_API_KEY")
)

agent_cfg = ChatAgentConfig(
    name="WellBot",
    llm=llm_cfg,
    system_message=(
        "You are Well-Bot"
    ),
)

class JournalAgent(lr.ChatAgent):
    def __init__(self, config: ChatAgentConfig, websocket=None):
        super().__init__(config)
        self.websocket = websocket

    def chat_response(self, message: str) -> str:
        msg_lower = message.lower()

        if "start journal" in msg_lower:
            result = journal_Manager.start_journal(self.websocket)
            return result.get("status", "Started.")

        elif "stop journal" in msg_lower:
            result = journal_Manager.stop_journal(self.websocket)
            return result.get("text", "Stopped.")

        elif "attach image" in msg_lower:
            image_path = journal_Manager.attach_image(webcam_service=None)
            return f"Image captured at: {image_path}"

        # Default: forward to LLM
        return self.llm_response(message)


def create_agent(websocket=None) -> JournalAgent:
    return JournalAgent(agent_cfg, websocket)


# CLI Test
if __name__ == "__main__":
    agent = create_agent()
    task = Task(agent)
    task.run("Hi Well-Bot")
