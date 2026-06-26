import streamlit as st
# 📡 하린이가 말한 바로 그 'AI가 들어있는 약 파일'에서 분석 기능을 쏙 빼옵니다!
from medicine_db import analyze_medicine_safety

# 1. 앱 설정 및 제목
st.set_page_config(page_title="약 결합 안전 분석기", page_icon="🛡️")
st.title("🛡️ 약 결합 안전 분석기")
st.markdown("##### AI 기반 실시간 의약품 및 식품 상호작용 분석 시스템")

# 2. 클린 시작 모드 (빈 입력창)
drug1 = st.text_input("첫 번째 약 이름을 입력하세요", value="")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요 (선택)", value="")
bev = st.text_input("함께 마실 음료나 식품을 입력하세요 (선택)", value="")

# 3. 분석 시작 버튼
if st.button("실시간 상호작용 분석 시작"):
    if not drug1:
        st.warning("⚠️ 분석을 위해 최소한 첫 번째 약 이름을 입력해 주세요!")
    else:
        st.write("---")
        st.subheader("📋 안전 분석 보고서")
        
        # 🤖 약 파일 안에 들어있는 AI에게 약 이름을 보내서 정답 받아오기!
        with st.spinner("🔍 약물 분석 엔진이 실시간 검사 중입니다..."):
            status, reason_text = analyze_medicine_safety(drug1, drug2, bev)

        # 4. 세련된 결과 상자 출력
        if status == "DANGER":
            st.error("✅ 최종 판정 등급: DANGER (위험)")
            st.info(f"❌ {reason_text}")
        elif status == "WARNING":
            st.warning("✅ 최종 판정 등급: WARNING (주의)")
            st.info(f"🚨 {reason_text}")
        else:
            st.success("✅ 최종 판정 등급: SAFE (안전)")
            st.info(f"🍏 {reason_text}")
