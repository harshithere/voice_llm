import base64

class ChatGptClient:
    def __init__(self, client, model):
        self.__client = client
        self.__model = model
    
    def get_response(self, prompt, context):
        completion_response = self.__client.chat.completions.create(
        model=self.__model,
        messages=[
            {"role": "system", "content": context},
            {
                "role": "user",
                "content": prompt
            }
        ]
        )
        return completion_response

    def get_voice_response(self, encoded_audio, messages = []):
        completion = self.__client.chat.completions.create(
            model=self.__model,
            modalities=["text", "audio"],
            audio={"voice": "alloy", "format": "wav"},
            messages= messages + [
                {
                    "role": "user",
                    "content": [
                        { 
                            "type": "text",
                            "text": "Respond to the query asked by the user?"
                        },
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": encoded_audio,
                                "format": "wav"
                            }
                        }
                    ]
                }
            ]
        )

        return completion.choices[0].message