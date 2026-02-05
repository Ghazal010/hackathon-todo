from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List, Dict, Any

from .chat_models import ChatRequest, ChatResponse, ToolCall
from .database import get_session
from .chat_queries import create_conversation, get_conversation, get_conversation_history, add_message
from .openai_client import chat_with_ai, execute_function, get_final_response

router = APIRouter(prefix="/api", tags=["chat"])

@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_session)
):
    """
    Main chat endpoint - handles user messages and AI responses.

    Flow:
    1. Get or create conversation
    2. Fetch message history
    3. Send to OpenAI
    4. Execute any function calls
    5. Get final AI response
    6. Store messages
    7. Return response
    """

    try:
        # Step 1: Get or create conversation
        if request.conversation_id:
            conversation = get_conversation(
                db, request.conversation_id
            )
            if not conversation or conversation.user_id != user_id:
                raise HTTPException(404, "Conversation not found")
        else:
            conversation = create_conversation(db, user_id)

        # Step 2: Fetch conversation history (last 10 messages)
        history = get_conversation_history(
            db, conversation.id, limit=10
        )

        # Format history for OpenAI
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ]

        # Add new user message
        messages.append({"role": "user", "content": request.message})

        # Step 3: Send to OpenAI
        ai_response = chat_with_ai(messages, user_id)

        # Step 4: Execute function calls (if any)
        tool_calls = []
        if ai_response.get("requires_function_execution"):
            function_results = []

            for tool_call in ai_response["tool_calls"]:
                result = execute_function(
                    function_name=tool_call["function"],
                    arguments=tool_call["arguments"],
                    user_id=user_id,
                    db=db
                )

                function_results.append({
                    "tool_call_id": tool_call["id"],
                    **result
                })

                tool_calls.append({
                    "function": tool_call["function"],
                    "arguments": tool_call["arguments"],
                    "result": result
                })

            # Step 5: Get final response from AI
            final_response = get_final_response(messages, function_results)
        else:
            # No functions called, use direct response
            final_response = ai_response["content"]

        # Step 6: Store messages in database
        # Store user message
        user_msg = add_message(
            db=db,
            conversation_id=conversation.id,
            user_id=user_id,
            role="user",
            content=request.message
        )

        # Store AI response
        ai_msg = add_message(
            db=db,
            conversation_id=conversation.id,
            user_id=user_id,
            role="assistant",
            content=final_response,
            tool_calls={"calls": tool_calls} if tool_calls else None
        )

        # Step 7: Return response
        return ChatResponse(
            conversation_id=conversation.id,
            message_id=ai_msg.id,
            response=final_response,
            tool_calls=tool_calls
        )

    except HTTPException:
        raise
    except Exception as e:
        # Log error
        print(f"Chat error: {str(e)}")

        # Return error response
        raise HTTPException(500, f"Chat failed: {str(e)}")