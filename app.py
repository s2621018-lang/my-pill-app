import streamlit as st
from medicine_db import analyze_medicine_safety

st.set_page_config(page_title="약 결합 안전 분석기", page_icon="🛡️")
st.title("🛡️ 약 결합 안전 분석기")
st.markdown("##### 하이브리드 AI 기반 실시간 약물 안전 분석 시스템")

drug1 = st.text_input("첫 번째 약 이름을 입력하세요", value="")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요 (선택)", value="")
bev = st.text_input("함께 마실 음료나 식품을 입력하세요 (선택)", value="")

if st.button("실시간 상호작용 분석 시작"):
    if not drug1:
        st.warning("⚠️ 분석을 위해 최소한 첫 번째 약 이름을 입력해 주세요!")
    else:
        st.write("---")
        st.subheader("📋 안전 분석 보고서")
        
        with st.spinner("🔍 약물 분석 엔진이 정밀 검사 중입니다..."):
            status, reason_text = analyze_medicine_safety(drug1, drug2, bev)

        # 하린이의 안전 철학이 반영된 4단계 결과 화면
        if status == "DANGER":
            st.error("✅ 최종 판정 등급: DANGER (위험)")
            st.info(f"❌ {reason_text}")
        elif status == "WARNING":
            st.warning("✅ 최종 판정 등급: WARNING (주의)")
            st.info(f"🚨 {reason_text}")
        elif status == "NOT_FOUND":
            st.warning("⚠️ 최종 판정 등급: 정보를 찾을 수 없음")
            st.info(f"💡 {reason_text}")
        else:
            st.success("✅ 최종 판정 등급: SAFE (안전)")
            st.info(f"🍏 {reason_text}")
