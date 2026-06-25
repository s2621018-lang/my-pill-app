import streamlit as st
import urllib.request
import json

# 1. 하린이가 정해준 멋진 이름으로 앱 설정!
st.set_page_config(page_title="약 결합 안전 분석기", page_icon="🛡️")
st.title("🛡️ 약 결합 안전 분석기")
st.markdown("##### AI 기반 실시간 의약품 및 식품 상호작용 분석 시스템")

# 2. 클린 시작 모드: 빈 입력창
drug1 = st.text_input("첫 번째 약 이름을 입력하세요", value="")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요 (선택)", value="")
bev = st.text_input("함께 마실 음료나 식품을 입력하세요 (선택)", value="")

# 3. 분석 버튼
if st.button("실시간 상호작용 분석 시작"):
    
    if not drug1:
        st.warning("⚠️ 분석을 위해 최소한 첫 번째 약 이름을 입력해 주세요!")
    else:
        st.write("---")
        st.subheader("📋 안전 분석 보고서")
        
        with st.spinner("🤖 AI 엔진이 의학 데이터베이스를 정밀 분석 중입니다..."):
            
            user_content = f"약물1: {drug1}, 약물2: {drug2 if drug2 else '없음'}, 음료/식품: {bev if bev else '물'}"
            
            system_instruction = (
                "너는 세계 최고의 AI 의사이자 약사야. 사용자가 입력한 조합의 화학적 상호작용과 부작용을 분석해줘.\n"
                "결과는 반드시 아래의 3가지 등급 중 하나로만 판단해야 해.\n"
                "- DANGER: 절대 같이 먹으면 안 되는 위험한 조합 (예: 모든 약 + 술, 혈압약 + 자몽 등)\n"
                "- WARNING: 성분 중복 복용, 체내 흡수율 저하, 주의가 필요한 경우 (예: 유산균 + 비타민C 등)\n"
                "- SAFE: 함께 복용해도 아무런 문제가 없고 안전한 경우\n\n"
                "답변 양식:\n"
                "등급: [DANGER, WARNING, SAFE 중 하나]\n"
                "이유: [이유를 친절하고 전문적으로 상세하게 설명]"
            )
            
            try:
                # 📡 실시간 AI 서버 호출
                api_url = "https://open-api.jejucodingcamp.workers.dev/"
                req = urllib.request.Request(
                    api_url, 
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps({
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": system_instruction},
                            {"role": "user", "content": user_content}
                        ]
                    }).encode('utf-8')
                )
                
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    ai_response = res_data['choices'][0]['message']['content']
                
                # 🔍 안전장치: 위험 단어 완벽 감지 로직
                ai_upper = ai_response.upper()
                status = "SAFE"
                reason_text = ai_response
                
                if "이유:" in ai_response:
                    reason_text = ai_response.split("이유:")[1].strip()
                
                if any(k in ai_upper for k in ["DANGER", "위험", "금기", "불가"]):
                    status = "DANGER"
                elif any(k in ai_upper for k in ["WARNING", "주의", "경고", "상극"]):
                    status = "WARNING"

                # 4. 결과 화면 출력
                if status == "DANGER":
                    st.error(f"✅ 최종 판정 등급: DANGER (위험)")
                    st.info(f"❌ {reason_text}")
                elif status == "WARNING":
                    st.warning(f"✅ 최종 판정 등급: WARNING (주의)")
                    st.info(f"🚨 {reason_text}")
                else:
                    st.success(f"✅ 최종 판정 등급: SAFE (안전)")
                    st.info(f"🍏 {reason_text}")
                    
            except Exception as e:
                st.error("AI 엔진과 연결할 수 없습니다. 잠시 후 다시 시도해 주세요.")
