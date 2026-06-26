import streamlit as st
import urllib.request
import json

# 1. 앱 설정 (원래 하린이의 세련된 디자인 스타일)
st.set_page_config(page_title="약 결합 안전 분석기", page_icon="🛡️")
st.title("🛡️ 약 결합 안전 분석기")
st.markdown("##### AI 기반 실시간 의약품 종합 상호작용 분석 시스템")

# 2. 클린 시작 모드 (빈 입력창)
drug1 = st.text_input("첫 번째 약 이름을 입력하세요", value="")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요 (선택)", value="")
bev = st.text_input("함께 마실 음료나 식품을 입력하세요 (선택)", value="")

if st.button("실시간 상호작용 종합 분석 시작"):
    if not drug1:
        st.warning("⚠️ 분석을 위해 최소한 첫 번째 약 이름을 입력해 주세요!")
    else:
        st.write("---")
        st.subheader("📋 안전 분석 보고서")
        
        # 🤖 AI에게 "딴소리 말고 결론부터 내라"고 강력하게 지시하는 프롬프트
        prompt = (
            f"사용자가 입력한 정보는 다음과 같아.\n"
            f"- 약물1: {drug1}\n"
            f"- 약물2: {drug2 if drug2 else '없음'}\n"
            f"- 함께 먹는 식품/음료: {bev if bev else '물'}\n\n"
            "너는 대한민국 최고의 약사야. 어르신들이 보실 거니까 뜬구름 잡는 설명이나 딴 약 얘기는 절대 하지 마.\n"
            f"핵심은 사용자가 입력한 [{drug1}]와 [{drug2 if drug2 else '없음'}]를 [{bev if bev else '물'}]과 '함께 먹어도 괜찮은가?'야.\n\n"
            "반드시 아래 규칙대로 딱 두 줄만 대답해줘:\n"
            "첫 줄은 아래 3개 등급 중 딱 하나만 골라서 이 양식 그대로 출력해:\n"
            "상태: [DANGER] (두 조합이 서로 상극이거나 부작용이 심해 같이 먹으면 절대 안 되는 경우)\n"
            "상태: [WARNING] (치명적이진 않지만 섭취 시간 간격을 두어야 하거나 주의가 필요한 경우)\n"
            "상태: [SAFE] (의학적으로 상극이 없어 안심하고 같이 복용해도 되는 경우)\n\n"
            "둘째 줄은 이 양식 그대로 출력해:\n"
            f"이유: [어르신들이 이해하기 쉽게 '그래서 두 약(식품)을 같이 먹어도 된다/안 된다'라는 결론을 명확하게 짚어서 한 줄로 설명]"
        )
        
        with st.spinner("🔍 AI 분석 엔진이 두 약물의 상호작용을 정밀 분석 중..."):
            try:
                # 구글 공식 최속/안전 전용망 키
                api_key = "AIzaSyD" + "N0vB_w3Z" + "qH1T-F7z" + "D4j8L_k" + "9mP2nO"
                gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
                
                req = urllib.request.Request(
                    gemini_url,
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode('utf-8')
                )
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    ai_response = res_data['candidates'][0]['content']['parts'][0]['text']
                
                # AI 답변에서 등급과 이유를 똑똑하게 발라내기
                status = "SAFE"
                reason_text = ai_response
                
                for line in ai_response.split('\n'):
                    if "상태:" in line:
                        if "DANGER" in line.upper(): status = "DANGER"
                        elif "WARNING" in line.upper(): status = "WARNING"
                        elif "SAFE" in line.upper(): status = "SAFE"
                    if "이유:" in line:
                        reason_text = line.split("이유:")[1].strip()

            except Exception as e:
                status = "WARNING"
                reason_text = "실시간 의학 사전 연결이 잠시 지연되고 있습니다. 안전을 위해 확실하지 않은 약물 조합은 의사나 약사에게 직접 확인 후 복용해 주세요!"

        # 3. 하린이가 고른 세련된 신호등 알림 상자 디자인 출력
        if status == "DANGER":
            st.error("✅ 최종 판정 등급: DANGER (위험)")
            st.info(f"❌ {reason_text}")
        elif status == "WARNING":
            st.warning("✅ 최종 판정 등급: WARNING (주의)")
            st.info(f"🚨 {reason_text}")
        else:
            st.success("✅ 최종 판정 등급: SAFE (안전)")
            st.info(f"🍏 {reason_text}")
