# 신촌역 맛집 일일 크롤러

이 레포지토리는 매일 오전 11시 20분에 신촌역 근처 맛집 정보를 크롤링하여 Slack 채널에 자동으로 전송하는 GitHub Actions 워크플로우를 포함하고 있습니다.

## 설정 방법

1. GitHub Secrets에 다음 두 항목을 설정해야 합니다:
   - `ANTHROPIC_API_KEY`: Claude API 키
   - `SLACK_BOT_TOKEN`: Slack Bot 토큰 (채널에 메시지를 보낼 권한 필요)

2. Slack 앱 설정:
   - Slack API 사이트에서 새로운 앱 생성
   - "Bot Token Scopes"에 `chat:write` 권한 추가
   - 앱을 워크스페이스에 설치하고, 채널 C08M48UU75K에 봇 초대
   - 발급받은 Bot User OAuth Token을 GitHub Secrets에 저장

## 수동 실행

GitHub Actions 탭에서 "Daily Sinchon Restaurant Crawler" 워크플로우를 선택하고 "Run workflow" 버튼을 클릭하여 수동으로 실행할 수 있습니다.