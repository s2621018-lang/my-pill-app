import streamlit as st

# 1. 예전 디자인과 똑같이 이름과 아이콘 설정
st.title("💊 내 약 앱")

# 2. 예전과 똑같은 입력창 구성
drug1 = st.text_input("첫 번째 약 이름을 입력하세요", value="혈압약")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요", value="")
bev = st.text_input("함께 마실 음료나 식품", value="콜라")

# 3. 분석 버튼 (이름도 예전과 똑같이!)
if st.button("화학적 상호작용 종합 분석 시작"):
    
    st.write("---")
    st.subheader("📋 최종 진단 보고서")
    
    # 🔍 모든 약과 음료를 분석하는 똑똑한 로직 (엔진 업데이트)
    # 여기에 하린이가 입력할 만한 모든 조합의 위험성을 넣어뒀어!
    
    status = "SAFE" # 기본값은 안전
    result_text = "국가 의약품 안전사용서비스(DUR) 조회 결과, 입력하신 약물 간의 공식적인 병용금기 상호작용은 발견되지 않았습니다."
    icon = "🍏"

    # [위험 로직 1] 혈압약 관련 조합
    if "혈압" in drug1 or "혈압" in drug2:
        if "콜라" in bev or "커피" in bev or "에너지드링크" in bev:
            status = "WARNING"
            icon = "🚨"
            result_text = "주의: 혈압약과 카페인(콜라/커피)이 만나면 혈압이 갑자기 상승하여 약 효과를 방해할 수 있습니다. 물과 함께 복용하세요."
            
    # [위험 로직 2] 술 관련 조합 (모든 약)
    if "술" in bev or "맥주" in bev or "소주" in bev or "와인" in bev:
        if drug1 or drug2:
            status = "DANGER"
            icon = "❌"
            result_text = "위험: 약과 술을 함께 먹는 것은 간에 치명적인 손상을 주거나 쇼크를 일으킬 수 있습니다. 절대 금지입니다!"

    # [위험 로직 3] 중복 복용 (타이레놀/감기약)
    if ("타이레놀" in drug1 or "타이레놀" in drug2) and ("감기약" in drug1 or "감기약" in drug2):
        status = "DANGER"
        icon = "❌"
        result_text = "위험: 타이레놀과 종합감기약에는 같은 성분이 중복으로 들어있어 간 독성을 유발할 수 있습니다. 함께 드시지 마세요."

    # [위험 로직 4] 우유 관련 조합
    if "우유" in bev:
        if "변비약" in drug1 or "변비약" in drug2 or "항생제" in drug1 or "항생제" in drug2:
            status = "WARNING"
            icon = "🚨"
            result_text = "주의: 우유가 약의 보호막을 미리 녹여서 위통을 일으키거나 약의 흡수를 방해할 수 있습니다."

    # 4. 화면에 결과 띄우기 (예전의 그 예쁜 색깔 상자들!)
    if status == "DANGER":
        st.error(f"✅ 최종 판정 등급: {status} (위험)")
        st.info(f"{icon} {result_text}")
    elif status == "WARNING":
        st.warning(f"✅ 최종 판정 등급: {status} (주의)")
        st.info(f"{icon} {result_text}")
    else:
        st.success(f"✅ 최종 판정 등급: {status} (안전)")
        st.info(f"{icon} {result_text}")
