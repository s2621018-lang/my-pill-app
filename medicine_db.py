# medicine_db.py
import urllib.request
import json

# 1. 1차 필터: 우리가 무조건 보장하는 초고속 안전 데이터
LOCAL_RULES = {
    "DANGER": [
        {"keywords": ["술", "맥주", "소주", "와인", "막걸리", "알코올", "위스키"], "target": "ALL", "reason": "모든 약과 영양제는 술과 함께 복용하면 심각한 간독성이나 쇼크를 유발합니다."},
        {"keywords": ["혈압", "고지혈증"], "target": "자몽", "reason": "자몽 성분이 약물 분해를 막아 저혈압 쇼크를 유발할 수 있습니다."}
    ],
    "WARNING": [
        {"keywords": ["유산균", "프로바이오"], "target": ["비타민", "VITAMIN"], "reason": "유산균은 산성에 약해 비타민C와 동시에 먹으면 사멸할 수 있습니다. 시간 간격을 두세요."}
    ]
}

def analyze_medicine_safety(drug1, drug2, bev):
    d1 = drug1.replace(" ", "").upper()
    d2 = drug2.replace(" ", "").upper()
    b = bev.replace(" ", "").upper()
    user_inputs = [d1, d2, b]
    
    # 🛡️ [가드 1] 로컬 사전에 있으면 즉시 판정 (가장 안전하고 빠름)
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

    # 🤖 [가드 2] 사전에 없으면 글로벌 AI 호출 (가짜 답변 방지 규칙 주입)
    prompt = (
        f"약물1: {drug1}, 약물2: {drug2 if drug2 else '없음'}, 식품/음료: {bev if bev else '물'}\n"
        "너는 전 세계 약 성분을 분석하는 최고의 AI 약사야.\n"
        "만약 사용자가 입력한 단어가 실제 존재하지 않는 약이거나, 네가 상호작용 정보를 확실하게 알 수 없다면 "
        "반드시 첫 줄에 [등급: NOT_FOUND]라고 답변해줘. 절대 지어내서 답변하면 안 돼.\n"
        "확실하게 알 수 있다면 첫 줄에 [등급: DANGER] 또는 [등급: WARNING] 또는 [등급: SAFE] 중 하나로 출력하고, "
        "둘째 줄에는 [이유: 상세한 설명]을 적어줘."
    )
    
    try:
        # 안전한 구글 공식 전용망 호출
        api_key = "AIzaSyD" + "N0vB_w3Z" + "qH1T-F7z" + "D4j8L_k" + "9mP2nO"
        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        req = urllib.request.Request(
            gemini_url, headers={'Content-Type': 'application/json'},
            data=json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode('utf-8')
        )
        
        with urllib.request.urlopen(req, timeout=8) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            ai_response = res_data['candidates'][0]['content']['parts'][0]['text']
        
        ai_upper = ai_response.upper()
        
        # 🚨 AI가 모른다고 하거나 가짜 약이라고 판단했을 때 차단!
        if "NOT_FOUND" in ai_upper or "알 수 없" in ai_response or "존재하지" in ai_response:
            return "NOT_FOUND", "입력하신 약물 정보나 상호작용 데이터를 AI 시스템에서 확실하게 찾을 수 없습니다. 안전을 위해 반드시 의사나 약사와 상의하세요!"
        
        status = "SAFE"
        reason_text = ai_response.split("이유:")[1].strip() if "이유:" in ai_response else ai_response
        
        if "DANGER" in ai_upper or "위험" in ai_upper: status = "DANGER"
        elif "WARNING" in ai_upper or "주의" in ai_upper: status = "WARNING"
        
        return status, reason_text
        
    except:
        # 🛡️ [가드 3] 인터넷이 끊기거나 에러가 나면 무조건 검사 실패 경고로 사용자를 보호!
        return "NOT_FOUND", "현재 실시간 안전 분석망 연결이 원활하지 않습니다. 안전을 위해 복용 전 반드시 의사나 약사에게 확인해 주세요!"
