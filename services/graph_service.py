"""Service for interacting with the LangGraph."""
import streamlit as st
from langchain_core.messages import AIMessage
from virtual_sales_agent.graph import graph

def invoke_graph(payload=None):
    """
    Invoke the graph with optional payload.
    
    Args:
        payload: Optional payload to send to the graph.
        
    Returns:
        The result of the graph invocation.
    """
    config = st.session_state.config
    return graph.invoke(payload, config)

def stream_graph(messages):
    """
    Stream events from the graph.
    
    Args:
        messages: The messages to stream to the graph.
        
    Returns:
        A list of events from the graph.
    """
    config = st.session_state.config
    return list(
        graph.stream(
            {"messages": messages},
            config,
            stream_mode="values",
        )
    )

def get_graph_state():
    """
    Get the current state of the graph.
    
    Returns:
        The current state of the graph.
    """
    config = st.session_state.config
    return graph.get_state(config)

def extract_tool_call(event):
    """
    Extract tool call from an event if present.
    
    Args:
        event: The event to extract the tool call from.
        
    Returns:
        The tool call if present, None otherwise.
    """
    if isinstance(event, dict) and "messages" in event:
        messages = event["messages"]
        last_message = messages[-1] if messages else None

        if isinstance(last_message, AIMessage):
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return last_message.tool_calls[0]
    
    return None

def process_result(result, seen_ids=None):
    """
    Process a result from the graph and extract any messages.
    
    Args:
        result: The result to process.
        seen_ids: A set of already processed message IDs.
        
    Returns:
        A tuple of (updated_seen_ids, last_message) where last_message is the last AIMessage
        extracted from the result, or None if no new message was found.
    """
    if seen_ids is None:
        seen_ids = set()
        
    last_message = None
    
    if isinstance(result, dict) and "messages" in result:
        messages = result["messages"]
        message = messages[-1] if messages else None
        
        if isinstance(message, AIMessage):
            if message.id not in seen_ids and message.content:
                seen_ids.add(message.id)
                last_message = message
    
    return seen_ids, last_message