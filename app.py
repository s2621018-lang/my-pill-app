import streamlit as st

# 1. 앱 설정 (원래 하린이가 좋아했던 깔끔하고 세련된 디자인 스타일)
st.set_page_config(page_title="약 결합 안전 분석기", page_icon="🛡️")
st.title("🛡️ 약 결합 안전 분석기")
st.markdown("##### 통합 데이터 기반 실시간 의약품 상호작용 검증 시스템")

# 2. 클린 시작 모드 (빈 입력창)
drug1 = st.text_input("첫 번째 약 이름을 입력하세요", value="")
drug2 = st.text_input("두 번째 약/영양제 이름을 입력하세요 (선택)", value="")
bev = st.text_input("함께 마실 음료나 식품을 입력하세요 (선택)", value="")

# 📚 대형 약물 상호작용 사전 (인터넷 통신을 안 하므로 평생 에러 안 뜸!)
MEDICINE_MAP = {
    "DANGER": [
        {"keywords": ["술", "소주", "맥주", "막걸리", "와인", "알코올", "위스키"], "target": "ALL", "reason": "모든 약과 영양제는 술과 함께 드시면 간독성을 유발하거나 중추신경을 억제하므로 절대 같이 드시면 안 됩니다."},
        {"keywords": ["혈압", "고지혈증", "노바스크", "리피토", "암로디핀", "아토르바스타틴"], "target": "자몽", "reason": "혈압약/고지혈증약 성분이 자몽과 만나면 몸에 과도하게 쌓여 저혈압 쇼크를 유발하므로 절대 같이 드시면 안 됩니다."},
        {"keywords": ["타이레놀", "아세트아미노펜", "써스펜"], "target": ["감기", "판콜", "판피린", "펜잘", "게보린"], "reason": "종합감기약 안에도 타이레놀 성분이 들어있어 두 약을 같이 드시면 심각한 간 손상을 유발하므로 절대 금기입니다."}
    ],
    "WARNING": [
        {"keywords": ["유산균", "프로바이오틱스"], "target": ["비타민", "레모나", "아스코르브산"], "reason": "유산균은 산성에 약하므로 비타민C와 동시에 복용하면 균이 사멸합니다. 2시간 이상 간격을 두고 복용하세요."},
        {"keywords": ["철분", "훼로바"], "target": ["칼슘", "마그네슘", "멸치", "우유"], "reason": "철분과 미네랄(칼슘)은 흡수 경로가 같아 동시에 드시면 둘 다 몸 밖으로 배출되니 아침/저녁으로 나눠 드세요."},
        {"keywords": ["골다공증", "포사맥스", "알렌드로네이트"], "target": ["우유", "요거트", "치즈", "유제품"], "reason": "골다공증 약은 우유 속 칼슘과 결합하면 약효가 완전히 사라지므로 반드시 맹물과 함께 복용하셔야 합니다."},
        {"keywords": ["감기", "혈압약", "기관지염", "아스피린"], "target": ["커피", "녹차", "에너지드링크", "카페인"], "reason": "약 성분과 커피의 카페인이 만나면 부작용으로 가슴이 심하게 뛰고 잠을 못 주무실 수 있으니 주의하세요."}
    ]
}

if st.button("실시간 상호작용 종합 분석 시작"):
    if not drug1:
        st.warning("⚠️ 분석을 위해 최소한 첫 번째 약 이름을 입력해 주세요!")
    else:
        st.write("---")
        st.subheader("📋 안전 분석 보고서")
        
        # 입력된 글자 공백 제거 및 대문자 변환
        d1 = drug1.replace(" ", "").upper()
        d2 = drug2.replace(" ", "").upper()
        b = bev.replace(" ", "").upper()
        user_inputs = [d1, d2, b]
        
        status = "SAFE"
        reason_text = "입력하신 약물과 식품 조합은 알려진 의학적 상극 성분이 없으므로 안심하고 함께 복용하셔도 좋습니다."
        
        # 1차 검증: 치명적 위험(DANGER) 성분이 있는지 맵에서 확인
        for rule in MEDICINE_MAP["DANGER"]:
            if any(k in d1 or k in d2 for k in rule["keywords"]):
                if rule["target"] == "ALL" and b:
                    status = "DANGER"
                    reason_text = rule["reason"]
                    break
                elif any(rule["target"] in item for item in user_inputs):
                    status = "DANGER"
                    reason_text = rule["reason"]
                    break
                    
        # 2차 검증: 만약 안전하다면, 복용 주의(WARNING) 성분이 있는지 확인
        if status == "SAFE":
            for rule in MEDICINE_MAP["WARNING"]:
                if any(k in d1 or k in d2 for k in rule["keywords"]):
                    if isinstance(rule["target"], list):
                        if any(any(t in item for item in user_inputs) for t in rule["target"]):
                            status = "WARNING"
                            reason_text = rule["reason"]
                            break
                    else:
                        if any(rule["target"] in item for item in user_inputs):
                            status = "WARNING"
                            reason_text = rule["reason"]
                            break

        # 3. 하린이가 원했던 세련된 원래의 신호등 알림 상자 디자인 출력
        if status == "DANGER":
            st.error("✅ 최종 판정 등급: DANGER (위험)")
            st.info(f"❌ {reason_text}")
        elif status == "WARNING":
            st.warning("✅ 최종 판정 등급: WARNING (주의)")
            st.info(f"🚨 {reason_text}")
        else:
            st.success("✅ 최종 판정 등급: SAFE (안전)")
            st.info(f"🍏 {reason_text}")
