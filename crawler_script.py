import os
import json
import requests
from anthropic import Anthropic

# API 키 설정
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_CHANNEL = "C08M48UU75K"  # 지정된 Slack 채널 ID

# Anthropic 클라이언트 초기화
client = Anthropic(api_key=ANTHROPIC_API_KEY)

# 크롤링 프롬프트 - Firecrawl을 사용해 신촌역 맛집 정보 수집
prompt = """
다음 URL에서 신촌역 근처 맛집 정보를 수집하고 TOP 10 목록으로 정리해주세요:
https://section.blog.naver.com/Search/Post.naver?pageNo=1&rangeType=ALL&orderBy=sim&keyword=%EC%8B%A0%EC%B4%8C%EC%97%AD%20%EA%B7%BC%EC%B2%98%20%EB%A7%9B%EC%A7%91

각 맛집마다 다음 정보를 포함해 주세요:
- 가게 이름
- 주요 메뉴
- 위치 정보
- 특징

마크다운 형식으로 보기 좋게 정리해주세요.
"""

# Claude API 호출하여 크롤링 및 정리
def get_restaurant_list():
    try:
        message = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4000,
            temperature=0,
            system="당신은 웹 정보를 정확하게 크롤링하고 정리하는 도우미입니다. firecrawl 기능을 사용해 정보를 수집하고 깔끔하게 정리합니다.",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return message.content
    except Exception as e:
        return f"에러 발생: {str(e)}"

# Slack에 메시지 전송
def post_to_slack(message):
    try:
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}"
        }
        
        data = {
            "channel": SLACK_CHANNEL,
            "text": "🍽️ *오늘의 신촌역 맛집 TOP 10* 🍽️",
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": "🍽️ 오늘의 신촌역 맛집 TOP 10 🍽️",
                        "emoji": True
                    }
                },
                {
                    "type": "divider"
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": message
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "매일 자동 업데이트 되는 신촌역 맛집 정보입니다."
                        }
                    ]
                }
            ]
        }
        
        response = requests.post("https://slack.com/api/chat.postMessage", 
                                headers=headers, 
                                data=json.dumps(data))
        
        if response.status_code != 200 or not response.json().get("ok", False):
            print(f"Slack 메시지 전송 실패: {response.text}")
        else:
            print("Slack 메시지 전송 성공")
            
    except Exception as e:
        print(f"Slack 전송 중 에러 발생: {str(e)}")

# 메인 실행
if __name__ == "__main__":
    # 맛집 정보 가져오기
    restaurant_info = get_restaurant_list()
    
    # Slack에 전송
    post_to_slack(restaurant_info)