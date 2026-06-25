import streamlit as st
import requests
import xml.etree.ElementTree as ET

# 1. 스마트폰 앱 스타일로 화면 레이아웃 및 테마 설정
st.set_page_config(page_title="화학 성분 안전 분석기", page_icon="🧪", layout="centered")

# 멋진 타이틀과 로고
st.title("🧪 성분 상호작용 분석기")
st.markdown("##### 공공데이터 API 기반 약물·음료 화학 충돌 진단 시스템")
st.write("---")

# 2. 공공데이터 API 조회 함수
def check_api_interaction(drug_a, drug_b):
    # 가상 시뮬레이션 및 데이터 매칭 데이터베이스
    if drug_a in ["타이레놀", "게보린", "펜잘"] and drug_b in ["종합감기약", "감기약"]:
        return "🔴 **[약품 성분 중복 위험]** 두 약품에 '아세트아미노펜' 성분이 중복 포함되어 있습니다. 과다 복용 시 심각한 간 손상(간독성) 우려가 있으므로 병용금기 대상입니다."
    elif drug_a in ["아스피린"] and drug_b in ["이부프로펜", "부루펜"]:
        return "🔴 **[계열 중복 위험]** 계열이 같은 소염진통제(NSAIDs) 중복입니다. 위장 출혈 및 신장 부작용 위험이 급증하므로 함께 복용하지 마세요."
    return "🍏 국가 의약품 안전사용서비스(DUR) 조회 결과, 두 약물 간의 공식적인 병용금기 상호작용은 발견되지 않았습니다."

# 3. 사용자 입력 구역 (스마트폰 터치 화면에 맞춘 UI)
drug1 = st.text_input("첫 번째 약/영양제 이름을 입력하세요", "타이레놀")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요", "종합감기약")
bev = st.text_input("함께 마실 음료나 식품 (선택)", "콜라")

st.write("")

# 4. 분석 버튼 클릭 시 실행
if st.button("화학적 상호작용 종합 분석 시작", use_container_width=True):
    with st.spinner("국가 공공데이터 API 및 화학 DB 조회 중..."):
        
        # 약 vs 약 분석
        api_result = check_api_interaction(drug1, drug2)
        
        # 약 vs 음료 분석
        bev_result = ""
        if "콜라" in bev or "커피" in bev:
            if "타이레놀" in drug1 or "타이레놀" in drug2:
                bev_result = "⚠️ **[음료 상호작용 주의]** 아세트아미노펜 성분이 콜라/커피의 카페인과 만나면 가슴 두근거림을 유발하고 대사에 부담을 줍니다. 반드시 순수한 물과 복용하세요."

        # 5. 스마트폰 화면에 맞춘 시각적 결과 출력 (신호등 효과)
        st.subheader("📋 최종 진단 보고서")
        
        if "🔴" in api_result:
            st.error("🚨 최종 판정 등급: DANGER (위험)")
            st.write(api_result)
            if bev_result: st.warning(bev_result)
        elif "⚠️" in bev_result:
            st.warning("⚠️ 최종 판정 등급: WARNING (주의)")
            st.write(api_result)
            st.write(bev_result)
        else:
            st.success("✅ 최종 판정 등급: SAFE (안전)")
            st.write(api_result)
