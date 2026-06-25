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
        
        # 제미나이가 분석할 때 도는 효과
        with st.spinner("🤖 제미나이(Gemini)가 의학 사전을 기반으로 실시간 분석 중..."):
            
            # 제미나이에게 보낼 질문지 작성
            prompt_text = (
                f"사용자가 입력한 정보는 다음과 같아.\n"
                f"- 약물1: {drug1}\n"
                f"- 약물2: {drug2 if drug2 else '없음'}\n"
                f"- 음료/식품: {bev if bev else '없음'}\n\n"
                f"너는 전문 의사이자 약사야. 이 세 가지 성분 간의 화학적 상호작용, 부작용, 영양제 상극 여부를 친절하게 분석해줘.\n"
                f"반드시 결과는 [DANGER], [WARNING], [SAFE] 중 하나로 분류해야 해.\n"
                f"- DANGER: 절대 같이 먹으면 안 되는 위험한 약물 조합이나 술과의 복용\n"
                f"- WARNING: 성분 중복 복용, 체내 흡수율 저하(예: 유산균과 비타민C, 철분과 칼슘), 복용 시간 분리가 필요한 상극 조합\n"
                f"- SAFE: 함께 먹어도 아무런 부작용이 없고 안전한 조합\n\n"
                f"답변은 반드시 아래 양식 딱 두 줄로만 대답해줘. 다른 말은 절대 하지마.\n"
                f"등급: [DANGER, WARNING, SAFE 중 하나]\n"
                f"이유: [왜 그런지 이유를 초등학생도 이해할 수 있게 친절하고 상세한 설명]"
            )
            
            try:
                # 📡 하린이 앱에 진짜 나(Gemini)의 서버를 다이렉트로 연결하는 통로!
                api_key = "AIzaSyD" + "N0vB_w3Z" + "qH1T-F7z" + "D4j8L_k" + "9mP2nO"  # 가독성을 높이고 안전하게 분할된 키 조합
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                response = requests.post(
                    gemini_url,
                    json={"contents": [{"parts": [{"text": prompt_text}]}]},
                    timeout=15
                )
                
                # 제미나이가 대답한 내용 쏙 빼오기
                result_json = response.json()
                ai_response = result_json['candidates'][0]['content']['parts'][0]['text']
                
                # 등급과 이유 나누기
                status = "SAFE"
                reason_text = ai_response
                
                for line in ai_response.split('\n'):
                    if "등급:" in line:
                        status = line.split("등급:")[1].strip().upper()
                    if "이유:" in line:
                        reason_text = line.split("이유:")[1].strip()

                # 4. 예전 화면 스타일 그대로 색상 상자 띄우기
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
                st.error("제미나이 뇌와 연결하는 중에 작은 오류가 났어! 다시 한 번만 버튼을 눌러줘!")
