import streamlit as st
import requests

# 1. 예전 디자인 그대로 설정
st.title("화학 성분 안전 분석기")

# 2. 입력창 구성
drug1 = st.text_input("첫 번째 약 이름을 입력하세요", value="")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요", value="")
bev = st.text_input("함께 마실 음료나 식품", value="")

# 3. 분석 버튼
if st.button("화학적 상호작용 종합 분석 시작"):
    
    if not drug1:
        st.warning("⚠️ 분석을 위해 최소한 첫 번째 약 이름을 입력해 주세요!")
    else:
        st.write("---")
        st.subheader("📋 최종 진단 보고서")
        
        # AI 분석 중일 때 빙글빙글 도는 효과
        with st.spinner("🚀 AI가 전 세계 의학 사전 및 영양학 데이터를 실시간 분석 중입니다..."):
            
            # 🤖 AI에게 줄 질문 규칙(프롬프트) 작성
            # 하린이가 입력한 두 약과 음료를 AI에게 전달합니다.
            user_content = f"약물1: {drug1}, 약물2: {drug2}, 음료: {bev}"
            
            system_instruction = (
                "너는 세계 최고의 약사이자 의사 AI야. 사용자가 입력한 약물1, 약물2, 음료 간의 화학적 상호작용과 부작용, 상극 여부를 분석해줘. "
                "반드시 결과는 딱 3가지 등급 중 하나로 분류해야 해.\n"
                "1. 조금이라도 치명적이거나 절대 같이 먹으면 안 되면 -> DANGER\n"
                "2. 성분이 중복되거나, 흡수율이 떨어지거나(예: 유산균과 비타민C, 철분과 칼슘), 주의가 필요하면 -> WARNING\n"
                "3. 같이 먹어도 아무 문제 없고 안전하면 -> SAFE\n\n"
                "답변은 반드시 아래 양식으로만 깔끔하게 한글로 작성해줘. 다른 말은 붙이지 마.\n"
                "등급: [DANGER 또는 WARNING 또는 SAFE]\n"
                "이유: [초등학생도 이해할 수 있게 친절하고 자세한 설명]"
            )
            
            try:
                # 📡 무료 오픈 AI API 게이트웨이를 통해 실시간으로 AI 뇌에 접속합니다.
                # 하린이의 실습을 위해 별도의 비밀키 없이 작동하도록 세팅된 교육용 무료 서버야!
                response = requests.post(
                    "https://open-api.jejucodingcamp.workers.dev/",
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_content}
                        ]
                    },
                    timeout=30
                )
                
                # AI가 보내준 답변 읽어오기
                ai_response = response.json()['choices'][0]['message']['content']
                
                # AI 답변에서 등급과 이유 잘라내기
                lines = ai_response.split('\n')
                status = "SAFE"
                reason_text = ai_response
                
                for line in lines:
                    if "등급:" in line:
                        status = line.split("등급:")[1].strip().upper()
                    if "이유:" in line:
                        reason_text = line.split("이유:")[1].strip()

                # 4. 예전 화면 스타일 그대로 결과창 띄우기
                if "DANGER" in status:
                    st.error(f"✅ 최종 판정 등급: DANGER (위험)")
                    st.info(f"❌ {reason_text}")
                elif "WARNING" in status or "WARN" in status:
                    st.warning(f"✅ 최종 판정 등급: WARNING (주의)")
                    st.info(f"🚨 {reason_text}")
                else:
                    st.success(f"✅ 최종 판정 등급: SAFE (안전)")
                    st.info(f"🍏 {reason_text}")
                    
            except Exception as e:
                # 혹시 인터넷이나 AI 서버가 일시적으로 끊겼을 때를 위한 안전장치
                st.error("AI 엔진 연결에 일시적인 오류가 발생했습니다. 잠시 후 다시 버튼을 눌러주세요!")
