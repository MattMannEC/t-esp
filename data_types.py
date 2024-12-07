from typing import Sequence

from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import add_messages
from typing import List
from langchain_core.messages import BaseMessage
from langchain_core.documents import Document


class State(TypedDict):
    input: str
    messages: Annotated[Sequence[BaseMessage], add_messages]
    context: List[Document]
    summary: str