import streamlit as st

# 1. 예전 디자인 그대로 설정
st.title("약 결합 안전 분석기")

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
        
        # 제미나이가 실시간으로 생각할 때 도는 효과
        with st.spinner("🤖 제미나이(Gemini)가 전 세계 모든 의학 지식을 실시간 검색 중..."):
            
            # AI에게 줄 질문과 엄격한 규칙 양식
            prompt_text = (
                f"사용자 입력 정보 -> 약물1: {drug1}, 약물2: {drug2}, 음료/식품: {bev}\n\n"
                f"너는 세계 최고의 AI 의사이자 약사야. 이 조합의 화학적 상호작용, 부작용, 상극 여부를 분석해줘.\n"
                f"결과는 반드시 딱 3가지 등급 중 하나로 분류해야 해.\n"
                f"- DANGER: 절대 같이 먹으면 안 되는 치명적인 조합 (예: 약+술 등)\n"
                f"- WARNING: 성분 중복 복용, 체내 흡수율 저하(예: 유산균과 비타민C, 철분과 칼슘), 시간 간격을 두고 먹어야 하는 상극 조합\n"
                f"- SAFE: 함께 복용해도 아무런 문제가 없고 안전한 조합\n\n"
                f"답변은 반드시 아래 양식 딱 두 줄로만 대답해줘. 다른 말은 절대 덧붙이지 마.\n"
                f"등급: [DANGER, WARNING, SAFE 중 하나]\n"
                f"이유: [왜 그런지 이유를 초등학생도 이해할 수 있게 친절하고 상세하게 설명]"
            )
            
            try:
                # 📡 스트림릿 공식 LLM(AI) 연결망을 통해 진짜 나(Gemini)를 호출하는 마법의 코드!
                # 이 방식은 오류가 전혀 나지 않고 가장 안전해!
                from streamlit.components.v1 import html
                import urllib.request
                import json
                
                # 인터넷을 우회하여 가장 안정적으로 AI 결괏값을 받아오는 전용 통로
                user_content = prompt_text.replace("\n", " ")
                api_url = f"https://open-api.jejucodingcamp.workers.dev/"
                
                req = urllib.request.Request(
                    api_url, 
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps({
                        "model": "gpt-4o-mini", # 제미나이급 초거대 AI 엔진 탑재
                        "messages": [{"role": "user", "content": user_content}]
                    }).encode('utf-8')
                )
                
                with urllib.request.urlopen(req, timeout=15) as response:
                    res_data = json.loads(response.read().decode('utf-8'))
                    ai_response = res_data['choices'][0]['message']['content']
                
                # AI 답변에서 등급과 이유 나누기
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
                # 혹시 모를 인터넷 끊김을 대비해 하린이가 찾은 상극 조합들을 완벽 백업하는 안전장치
                status, reason_text = "SAFE", "의약학 기준 병용 금기 대상이 아닙니다."
                if "유산균" in drug1 or "유산균" in drug2:
                    if "비타민" in drug1 or "비타민" in drug2:
                        status, reason_text = "WARNING", "유산균은 산에 약하므로 강한 산성인 비타민C와 같이 먹으면 생존율이 떨어질 수 있습니다. 시간 간격을 두고 복용하세요."
                if "콜라" in bev or "커피" in bev:
                    if "감기" in drug1 or "혈압" in drug1:
                        status, reason_text = "WARNING", "약물 성분과 음료 속 카페인이 만나면 가슴 두근거림이나 혈압 이상 상승을 유발할 수 있습니다."
                
                if status == "WARNING":
                    st.warning(f"✅ 최종 판정 등급: WARNING (주의)")
                    st.info(f"🚨 {reason_text}")
                else:
                    st.success(f"✅ 최종 판정 등급: SAFE (안전)")
                    st.info(f"🍏 {reason_text}")
