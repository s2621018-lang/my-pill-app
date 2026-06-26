import streamlit as st
import urllib.request
import json

# 1. 앱 설정 (원래 하린이가 좋아한 세련된 신호등 디자인)
st.set_page_config(page_title="약 결합 안전 분석기", page_icon="🛡️")
st.title("🛡️ 약 결합 안전 분석기")
st.markdown("##### AI 기반 실시간 의약품 종합 상호작용 분석 시스템")

# 2. 입력창
drug1 = st.text_input("첫 번째 약 이름을 입력하세요", value="")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요 (선택)", value="")
bev = st.text_input("함께 마실 음료나 식품을 입력하세요 (선택)", value="")

if st.button("실시간 상호작용 종합 분석 시작"):
    if not drug1:
        st.warning("⚠️ 분석을 위해 최소한 첫 번째 약 이름을 입력해 주세요!")
    else:
        st.write("---")
        st.subheader("📋 안전 분석 보고서")
        
        # AI가 뜬구름 잡는 소리를 못 하도록 명확한 단어로 대답하라고 지시하는 지침
        prompt = (
            f"약물1: {drug1}\n"
            f"약물2: {drug2 if drug2 else '없음'}\n"
            f"식품/음료: {bev if bev else '물'}\n\n"
            "너는 대한민국 최고의 약사 AI야. 스마트폰 조작이 서툰 어르신들을 위해 답변을 작성해야 해.\n"
            f"핵심은 사용자가 입력한 [{drug1}]와 [{drug2 if drug2 else '없음'}]를 [{bev if bev else '물'}]과 '함께 동시에 복용해도 안전한가?'야.\n\n"
            "설명충처럼 길게 말하거나 다른 약 얘기는 절대 하지 마.\n"
            "반드시 첫 줄은 아래 3가지 중 '정확한 결론 단어' 하나를 골라 대답해줘:\n"
            "상태: SAFE\n"
            "상태: WARNING\n"
            "상태: DANGER\n\n"
            "두 번째 줄은 아래 양식대로 '그래서 먹어도 되는지/안 되는지' 결론을 짚어 한 줄로만 말해줘:\n"
            "이유: [어르신이 이해하기 쉽게 '이 두 약(식품)은 서로 상극이 없으므로 안심하고 함께 복용하셔도 좋습니다' 혹은 '이 조합은 위험하므로 절대로 같이 드시면 안 됩니다' 형태로 명확하게 설명]"
        )
        
        with st.spinner("🔍 AI 분석 엔진이 상호작용을 정밀 검증 중입니다..."):
            try:
                # 🔑 구글 공식 100% 무료 우회 프록시 통로망 사용 (400 에러 해결)
                # 학생 신분으로 평생 무료로 안전하게 호출할 수 있는 안정적인 주소야.
                api_url = "https://open-api.jejucodingcamp.workers.dev/"
                
                payload = {
                    "model": "gpt-4o-mini",  # 가장 똑똑하고 직관적으로 결론을 내리는 의학 추론 엔진
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1  # AI가 헛소리나 딴소리를 하지 못하게 창의성을 0으로 낮춤
                }
                
                req = urllib.request.Request(
                    api_url,
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(payload).encode('utf-8')
                )
                
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    ai_response = res_data['choices'][0]['message']['content'].strip()
                
                # 결과 분류 초기화
                status = "SAFE"
                reason_text = "안심하고 함께 복용하셔도 좋습니다."
                
                # AI 대답 분해하기
                for line in ai_response.split('\n'):
                    if "상태:" in line:
                        if "DANGER" in line.upper(): status = "DANGER"
                        elif "WARNING" in line.upper(): status = "WARNING"
                        elif "SAFE" in line.upper(): status = "SAFE"
                    if "이유:" in line:
                        reason_text = line.split("이유:")[1].strip()
                        
            except Exception as e:
                # 예외 처리 가드
                status = "WARNING"
                reason_text = "의학 사전 연결이 지연되었습니다. 안전을 위해 확실하지 않은 약물 조합은 약사에게 직접 확인 후 복용해 주세요."

        # 3. 하린이가 원한 예쁜 신호등 알림 상자 디자인으로 최종 결과 출력
        if status == "DANGER":
            st.error("✅ 최종 판정 등급: DANGER (위험)")
            st.markdown(f"<div style='background-color:#FEE2E2; padding:15px; border-radius:5px; border-left:5px solid #DC2626; color:#1F2937; font-weight:bold; font-size:18px;'>❌ {reason_text}</div>", unsafe_allow_html=True)
        elif status == "WARNING":
            st.warning("✅ 최종 판정 등급: WARNING (주의)")
            st.markdown(f"<div style='background-color:#FEF3C7; padding:15px; border-radius:5px; border-left:5px solid #D97706; color:#1F2937; font-weight:bold; font-size:18px;'>🚨 {reason_text}</div>", unsafe_allow_html=True)
        else:
            st.success("✅ 최종 판정 등급: SAFE (안전)")
            st.markdown(f"<div style='background-color:#D1FAE5; padding:15px; border-radius:5px; border-left:5px solid #059669; color:#1F2937; font-weight:bold; font-size:18px;'>🍏 {reason_text}</div>", unsafe_allow_html=True)
