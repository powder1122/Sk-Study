import os
import requests
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv




#클래스 구조 만들기
class OpenAIAgent:
    def __init__(self):
        #키 가져오기
        load_dotenv()

        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        #tools
        self.ai_tools = None
        self.input_messages = []
        self.client = OpenAI(api_key=self.OPENAI_API_KEY)

    #AI 기능 호출
    def call_openai(self, prompt):
        #tools
        ai_tools_call = self.handle_function_call()

        response = self.client.responses.create(
            model='gpt-4.1',
            input=[{'role': 'user','content': [{'type':'input_text', 'text': prompt}
            ]}],
            tools= ai_tools_call
        )
        tool_call = response.output[0]
        #json 형태로 반환
        args = json.loads(tool_call.arguments) #arguments': '{"latitude":48.8566,"longitude":2.3522}',
        if tool_call.name == 'add_numbers':
            result = self.add_numbers(args["x"], args["y"])
            print(result)
        elif tool_call.name == 'convert_data_format':
            result = self.convert_data_format(args["date_str"], args["current_format"], args["target_format"])
            print(result)

        self.input_messages.append({
            'type': 'function_call_output',
            'call_id': tool_call.call_id,
            'output': str(result)
        })

        #최종 응답
        response2 = self.client.responses.create(
            model='gpt-4.1',
            input=prompt,
            tools=ai_tools_call
        )
        print(response2.output_text)



    #날짜 변환 메서드
    def convert_data_format(self, date_str, current_format, target_format):
        try:
            #문자열을 datetime 객체로 변환
            dt = datetime.strptime(date_str, current_format)
            #datetime 객체를 목표 문자열로 변환
            return dt.strftime(target_format)
        
        except ValueError:
            return "날짜 형식 또는 입력이 잘못됐습니다."
        

    #두 수를 더하는 메서드
    def add_numbers(self, x, y):
        x = float(x)
        y = float(y)
        return x + y
     
    #함수 호출을 관리하는 메서드
    def handle_function_call(self):
        self.ai_tools = [
            {
                "type" : "function",
                "name" : "convert_data_format",
                "description" : "입력받은 날짜를 %YYYY년 %MM월 %DD일 형식의 문자열로 반환합니다. ",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "date_str": {"type":"string", "description": "변환할 날짜 문자열, 형식: YYYY-MM-DD"},
                        "current_format": {"type": "string", "description": "입력 날짜의 포맷, 형식: %Y-%m-%d"},
                        "target_format": {"type": "string", "description": "출력할 날짜 포맷, %Y년 %m월 %d일"}
                    },
                    "required" : ["date_str","current_format","target_format"]
                }
            },
            {
                "type" : "function",
                "name" : "add_numbers",
                "description" : "입력받은 두 수를 더합니다. ",
                "parameters" : {
                    "type" : "object",
                    "properties" : {
                        "x":{"type": "number", "description": "숫자 x, 형식: 정수 또는 실수"},
                        "y":{"type": "number", "description": "숫자 y, 형식: 정수 또는 실수"},
                    },
                    "required" : ["x", "y"]
                }
            }
        ]
        return self.ai_tools
        

    #사용자 입력 처리 메서드
    def chat(self):
        print("AI 비서에게 무엇이든 물어보세요. ('종료'를 입력하면 종료됩니다)")
        #도구 설정
        self.handle_function_call()
        while True:
            user_input = input("사용자: ")
            if user_input.lower() in ["종료"]:
                print("대화를 종료합니다.")
                break
            #OpenAI 호출 및 응답 받기
            if isinstance(user_input, list):
                user_input = ' '.join(map(str, user_input))  # 리스트를 문자열로 변환
            else:
                user_input = str(user_input)

            self.input_messages.append({
                'role': 'user',
                'content': [{'type': 'input_text', 'text': str(user_input)}]
            })
            
            self.call_openai(user_input)





            


            









