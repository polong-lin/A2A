import mesop as me
from typing import Literal, Optional, Tuple, Any
from pydantic.dataclasses import dataclass
import dataclasses
from common.types import Task, Message
from service.types import Conversation, Event

ContentPart = str | dict[str,Any]

@dataclass
class StateConversation:
  """StateConversation provides mesop state compliant view of a conversation"""
  conversation_id: str = ""
  conversation_name: str = ""
  is_active: bool = True
  message_ids: list[str] = dataclasses.field(default_factory=list)

@dataclass
class StateMessage:
  """StateMessage provdes mesop state compliant view of a message"""
  message_id: str = ""
  role: str = ""
  # Each content entry is a content, media type pair.
  content: list[Tuple[ContentPart, str]] = dataclasses.field(default_factory=list)

@dataclass
class StateTask:
  """StateTask provides mesop state compliant view of task"""
  task_id: str = ""
  session_id: str | None = None
  state: str | None = None
  message: StateMessage = dataclasses.field(default_factory=StateMessage)
  artifacts: list[list[Tuple[ContentPart,str]]] = dataclasses.field(default_factory=list)

@dataclass
class SessionTask:
  """SessionTask organizes tasks based on conversation"""
  session_id: str = ""
  task: StateTask = dataclasses.field(default_factory=StateTask)

@dataclass
class StateEvent:
  """StateEvent provides mesop state compliant view of event"""
  conversation_id: str = ""
  actor: str = ""
  role: str = ""
  id: str = ""
  # Each entry is a pair of (content, media type)
  content: list[Tuple[ContentPart, str]] = dataclasses.field(default_factory=list)

@me.stateclass
class AppState:
  """Mesop Application State"""

  sidenav_open: bool = False
  theme_mode: Literal["system", "light", "dark"] = "system"

  current_conversation_id: str = ""
  conversations: list[StateConversation]
  messages: list[StateMessage]
  task_list: list[SessionTask] = dataclasses.field(default_factory=list)
  background_tasks: dict[str,str] = dataclasses.field(default_factory=dict)
  message_aliases: dict[str, str] = dataclasses.field(default_factory=dict)
  # This is used to track the data entered in a form
  completed_forms: dict[str, dict[str, Any] | None] = dataclasses.field(default_factory=dict)
  # This is used to track the message sent to agent with form data
  form_responses: dict[str, str] = dataclasses.field(default_factory=dict)
  polling_interval: int = 1

@me.stateclass
class SettingsState:
  """Settings State"""
  output_mime_types: list[str] = dataclasses.field(
    default_factory=lambda: [
      "image/*",
      "text/plain",
    ]
  )

