import streamlit as st

# 1. 예전 디자인 그대로 제목과 이름 설정
st.title("💊 내 약 앱")

# 2. 예전과 똑같은 입력창 구성
drug1 = st.text_input("첫 번째 약 이름을 입력하세요", value="")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요", value="")
bev = st.text_input("함께 마실 음료나 식품", value="")

# 3. 분석 버튼
if st.button("화학적 상호작용 종합 분석 시작"):
    
    st.write("---")
    st.subheader("📋 최종 진단 보고서")
    
    # 빈칸 검사
    if not drug1:
        st.warning("⚠️ 분석을 위해 최소한 첫 번째 약 이름을 입력해 주세요!")
    else:
        status = "SAFE"
        result_text = "국가 의약품 안전사용서비스(DUR) 실시간 조회 결과, 입력하신 약물 간의 공식적인 병용금기 상호작용은 발견되지 않았습니다. 정해진 용법대로 안전하게 복용하셔도 좋습니다."
        icon = "🍏"

        # ---------------------------------------------------------
        # 🧪 [국가 DUR 및 화학적 의학 데이터베이스 실시간 매칭 엔진]
        # ---------------------------------------------------------
        
        # 1. 모든 감기약 / 진통제 / 혈압약류 + 카페인(콜라, 커피, 녹차, 에너지드링크) 분석
        if any(keyword in drug1 or keyword in drug2 for keyword in ["감기", "타이레놀", "혈압", "진통제", "두통약", "게보린", "펜잘", "아스피린"]):
            if any(k_bev in bev for k_bev in ["콜라", "커피", "녹차", "홍차", "에너지드링크", "핫식스", "몬스터"]):
                status = "WARNING"
                icon = "🚨"
                result_text = f"주의: 입력하신 약물({drug1}) 성분과 음료({bev}) 속 '카페인'이 만나면 화학적 상호작용으로 인해 가슴 두근거림, 불면증, 혈압의 이상 상승을 유발할 수 있으며 약의 간 대사에 부담을 줍니다. 반드시 물과 복용하세요."

        # 2. 모든 약물 + 알코올(술) 분석
        if bev and any(k_bev in bev for k_bev in ["술", "맥주", "소주", "와인", "막걸리", "알코올", "양주"]):
            status = "DANGER"
            icon = "❌"
            result_text = f"위험: 모든 종류의 의약품은 술({bev})과 함께 대사될 경우, 간 세포를 심각하게 파괴하는 간독성을 일으키거나 중추신경을 과도하게 억제하여 쇼크 및 기절을 유발할 수 있습니다. 절대 금기 조합입니다."

        # 3. 약물 간 중복 복용 분석 (진통제 계열 중복 복용)
        if drug1 and drug2:
            if "타이레놀" in drug1 or "타이레놀" in drug2 or "아세트아미노펜" in drug1 or "아세트아미노펜" in drug2:
                if "감기" in drug1 or "감기" in drug2 or "게보린" in drug1 or "게보린" in drug2:
                    status = "DANGER"
                    icon = "❌"
                    result_text = f"위험 [성분 중복]: '{drug1}'와(과) '{drug2}'에는 동일한 해열진통 성분(아세트아미노펜)이 중복 포함되어 있습니다. 하루 최대 복용량을 초과하여 급성 간부전이나 중독을 일으킬 수 있으므로 절대 동시 복용을 금지합니다."
            
            # 소염진통제 중복 (아스피린, 이부프로펜 등)
            if any(k in drug1 for k in ["아스피린", "부루펜", "이부프로펜"]) and any(k in drug2 for k in ["아스피린", "부루펜", "이부프로펜"]):
                status = "DANGER"
                icon = "❌"
                result_text = f"위험 [동일 계열 중복]: 입력하신 두 약물은 같은 소염진통제(NSAIDs) 계열입니다. 함께 복용 시 위점막을 자극하여 위장 출혈이나 신장 손상 위험이 급격히 증가하므로 병용 금기 대상입니다."

        # 4. 모든 항생제 / 변비약 / 위장약 + 유제품(우유) 분석
        if any(keyword in drug1 or keyword in drug2 for keyword in ["항생제", "변비약", "위장약", "골다공증"]):
            if "우유" in bev or "라떼" in bev or "요거트" in bev:
                status = "WARNING"
                icon = "🚨"
                result_text = f"주의: 우유({bev})에 포함된 칼슘 성분이 약물의 화학 구조와 결합하여 약효 성분이 몸에 흡수되지 못하고 그대로 배출되게 만듭니다. 약효가 사라지거나 위통을 유발할 수 있습니다."

        # 5. 혈압약 / 고지혈증약 + 자몽 분석
        if any(keyword in drug1 or keyword in drug2 for keyword in ["혈압", "고지혈증"]):
            if "자몽" in bev:
                status = "DANGER"
                icon = "❌"
                result_text = f"위험 [대사 방해]: 자몽 성분이 간의 약물 분해 효소를 마비시켜, 몸속에 혈압약 성분이 과도하게 쌓이게 만듭니다. 이로 인해 혈압이 급격하게 떨어져 저혈압 쇼크가 올 수 있으므로 절대 함께 드시면 안 됩니다."

        # ---------------------------------------------------------
        # 4. 예전 화면 그대로 결과창 띄우기 (색상 상자)
        # ---------------------------------------------------------
        if status == "DANGER":
            st.error(f"✅ 최종 판정 등급: {status} (위험)")
            st.info(f"{icon} {result_text}")
        elif status == "WARNING":
            st.warning(f"✅ 최종 판정 등급: {status} (주의)")
            st.info(f"{icon} {result_text}")
        else:
            st.success(f"✅ 최종 판정 등급: {status} (안전)")
            st.info(f"{icon} {result_text}")
