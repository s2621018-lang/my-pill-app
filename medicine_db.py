# medicine_db.py
import urllib.request
import json

# 1. 우리가 확실하게 알고 있는 초고속 안전 데이터베이스
LOCAL_RULES = {
    "DANGER": [
        {"keywords": ["술", "맥주", "소주", "와인", "막걸리", "알코올", "위스키"], "target": "ALL", "reason": "모든 약과 영양제는 술과 함께 복용하면 심각한 간독성이나 쇼크를 유발합니다."},
        {"keywords": ["혈압", "고지혈증"], "target": "자몽", "reason": "자몽 성분이 약물 분해를 막아 몸에 과도하게 쌓여 저혈압 쇼크를 유발할 수 있습니다."},
        {"keywords": ["타이레놀", "아세트아미노펜"], "target": ["감기", "펜잘", "게보린", "판콜"], "reason": "동일한 해열진통 성분이 중복 포함되어 급성 간 손상을 일으킬 수 있습니다."}
    ],
    "WARNING": [
        {"keywords": ["유산균", "프로바이오"], "target": ["비타민", "VITAMIN"], "reason": "유산균은 산성에 약해 비타민C와 동시에 먹으면 사멸할 수 있습니다. 시간 간격을 두세요."},
        {"keywords": ["철분"], "target": ["칼슘", "마그네슘", "아연"], "reason": "서로 흡수 통로가 같아 동시에 복용하면 둘 다 흡수가 되지 않고 배출됩니다."}
    ]
}

# 2. app.py가 호출하면 약을 분석해서 결과만 돌려주는 마법의 AI 함수
def analyze_medicine_safety(drug1, drug2, bev):
    d1 = drug1.replace(" ", "").upper()
    d2 = drug2.replace(" ", "").upper()
    b = bev.replace(" ", "").upper()
    user_inputs = [d1, d2, b]
    
    status = None
    reason_text = ""
    
    # 🛡️ [1차] 로컬 사전에서 초고속 검색
    for rule in LOCAL_RULES["DANGER"]:
        if any(k in d1 or k in d2 for k in rule["keywords"]):
            if rule["target"] == "ALL" and b:
                return "DANGER", rule["reason"]
            elif any(rule["target"] in item for item in user_inputs):
                return "DANGER", rule["reason"]
                
    for rule in LOCAL_RULES["WARNING"]:
        if any(k in d1 or k in d2 for k in rule["keywords"]):
            if isinstance(rule["target"], list):
                if any(any(t in item for item in user_inputs) for t in rule["target"]):
                    return "WARNING", rule["reason"]
            else:
                if any(rule["target"] in item for item in user_inputs):
                    return "WARNING", rule["reason"]

    # 🤖 [2차] 사전에 없으면 이 파일 안에 숨겨진 AI 뇌를 깨웁니다!
    prompt = (
        f"약물1: {drug1}, 약물2: {drug2 if drug2 else '없음'}, 음료: {bev if bev else '물'}\n"
        "너는 의사이자 약사야. 이 조합의 상극이나 부작용을 분석해줘.\n"
        "반드시 결과는 딱 3가지 등급 중 하나여야 해: [DANGER], [WARNING], [SAFE]\n"
        "답변은 반드시 아래 양식으로만 딱 두 줄로 보내줘.\n"
        "등급: [등급 이름]\n"
        "이유: [이유를 초등학생도 이해할 수 있게 설명]"
    )
    
    try:
        api_url = "https://open-api.jejucodingcamp.workers.dev/"
        req = urllib.request.Request(
            api_url, headers={'Content-Type': 'application/json'},
            data=json.dumps({"model": "gpt-4o-mini", "messages": [{"role": "user", "content": prompt}]}).encode('utf-8')
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            ai_response = res_data['choices'][0]['message']['content']
        
        ai_upper = ai_response.upper()
        reason_text = ai_response.split("이유:")[1].strip() if "이유:" in ai_response else ai_response
        
        if "DANGER" in ai_upper or "위험" in ai_upper: status = "DANGER"
        elif "WARNING" in ai_upper or "주의" in ai_upper: status = "WARNING"
        else: status = "SAFE"
        
        return status, reason_text
    except:
        # AI 에러 시 최후의 안전장치
        return "WARNING", "실시간 안전 분석 엔진 연결이 일시적으로 원활하지 않습니다. 안전을 위해 복용 전 의사나 약사와 상의하세요!"
