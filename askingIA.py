import requests
import json 

def askingIA(url, model, messages):

    IA_response = ""
    data = {
        "model" : model,
        "messages" : messages,
    }

    response = requests.post(url, json=data)

    response_content_str = response.content.decode('utf-8')
    lines = response_content_str.split("\n")
    jsonLines = [line for line in lines if line.strip() != "" and line.strip()[0] == '{' and line.strip()[-1] == '}']

    for line in jsonLines:
        try:
            obj = json.loads(line)
            if obj["message"]["content"] :
                IA_response += obj["message"]["content"]
        except Exception as error:
            print("Erreur lors du parsing du JSON:", error)
    
    return IA_response