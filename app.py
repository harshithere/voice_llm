import gradio as gr
from openai import OpenAI
import base64
import shutil

from gpt_client import ChatGptClient

_OPEN_AI_API_KEY = ''
_OPEN_AI_MODEL = 'gpt-4o-audio-preview'
client = OpenAI(api_key=_OPEN_AI_API_KEY)
chatgpt_client = ChatGptClient(client=client, model=_OPEN_AI_MODEL)
turn_number, response_id_list, input_encodings = 0, [], []

def get_conversation_context():
    global turn_number, response_id_list, input_encodings
    messages = []
    print("Turn_number: " + str(turn_number))

    if turn_number == 0:
        return messages
    for i in range(turn_number):
        messages.append({
                "role": "user",
                "content": [
                        { 
                            "type": "text",
                            "text": "Respond to the query asked by the user?"
                        },
                        {
                            "type": "input_audio",
                            "input_audio": {
                                "data": input_encodings[i],
                                "format": "wav"
                            }
                        }
                    ]
            })
        messages.append({
                "role": "assistant",
                "audio": {
                    "id": response_id_list[i]
                }
            })
        
    return messages    
        

def get_voice(audio_file):
    print(audio_file)
    global turn_number, response_id_list
    fd = open(audio_file, 'rb')
    contents = fd.read()
    fd.close()

    encoded_string = base64.b64encode(contents).decode('utf-8')
    print("Encoded the voice input")
    input_encodings.append(encoded_string)
    response = chatgpt_client.get_voice_response(encoded_string, get_conversation_context())
    wav_bytes = base64.b64decode(response.audio.data)

    shutil.copyfile(audio_file, "user_input_" + str(turn_number) + ".wav")
    turn_number+=1
    response_id = response.audio.id
    response_id_list.append(response_id)
    print(response_id_list)
    return wav_bytes
    

demo = gr.Interface(
    fn=get_voice,
    inputs=gr.Audio(sources="microphone", type="filepath", format="wav"),
    outputs=gr.Audio(),
    title="Ask your query",
)

demo.launch()
