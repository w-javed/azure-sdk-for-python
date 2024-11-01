def target_multimodal_fn1(conversation) -> str:
    if conversation is not None and "messages" in conversation:
        messages = conversation["messages"]
        messages.append(
            {
                "role": "assistant",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": "https://cdn.britannica.com/68/178268-050-5B4E7FB6/Tom-Cruise-2013.jpg"},
                    }
                ],
            }
        )
        conversation["messages"] = messages
    return conversation
