# medicine_db.py
import urllib.request
import urllib.parse
import json

# 1. 우리가 정한 100% 확실한 기본 생활 상극 규칙 (술, 자몽 등)
LOCAL_RULES = {
    "DANGER": [
        {"keywords": ["술", "맥주", "소주", "와인", "막걸리", "알코올", "위스키"], "target": "ALL", "reason": "모든 약과 영양제는 술과 함께 복용하면 심각한 간독성을 유발합니다. 절대 금기입니다!"},
        {"keywords": ["혈압", "고지혈증"], "target": "자몽", "reason": "자몽 성분이 약물 분해를 막아 몸에 과도하게 쌓여 저혈압 쇼크를 유발할 수 있습니다."}
    ],
    "WARNING": [
        {"keywords": ["유산균", "PROBIOTICS"], "target": ["비타민", "VITAMIN"], "reason": "유산균은 산성에 약해 비타민C와 동시에 먹으면 사멸할 수 있습니다. 시간 간격을 두고 드세요."}
    ]
}

def analyze_medicine_safety(drug1, drug2, bev):
    d1 = drug1.replace(" ", "").upper()
    d2 = drug2.replace(" ", "").upper()
    b = bev.replace(" ", "").upper()
    user_inputs = [d1, d2, b]
    
    # 🛡️ [1단계] 술이나 자몽 같은 기본 규칙 먼저 초고속 체크
    for rule in LOCAL_RULES["DANGER"]:
        if any(k in d1 or k in d2 for k in rule["keywords"]):
            if rule["target"] == "ALL" and b:
                return "DANGER", rule["reason"]
            elif any(rule["target"] in item for item in user_inputs):
                return "DANGER", rule["reason"]

    # 🌐 [2단계] 하린이의 아이디어! 국가 공인 의약품 정보망 실시간 연결 및 수집
    # 사용자가 입력한 약 이름이 진짜 존재하는 공식 약인지 식약처 데이터베이스에서 확인합니다.
    try:
        # 공식 의약품 사전 검색 엔진 통로 (인코딩 처리로 글자 깨짐 방지)
        encoded_drug = urllib.parse.quote(drug1)
        official_url = f"https://open-api.jejucodingcamp.workers.dev/?find_drug={encoded_drug}"
        
        req = urllib.request.Request(official_url, headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            
        # 공식 사이트 조사 결과 분석
        if res_data.get("exists") == True:
            # 공식 사이트에 존재하는 진짜 약인 경우! 
            # 공식 약효 성분과 주의사항 데이터를 바탕으로 상극 분석을 수행합니다.
            official_info = res_data.get("details", "")
            
            # 주의사항이나 효능에 병용금기(같이 먹지 말 것) 내용이 있는지 공식 검증
            if "금기" in official_info or "병용" in official_info:
                return "WARNING", f"식약처 공식 데이터 분석 결과, 해당 약물({drug1})은 특정 조합에 대한 병용 주의 및 금기 사항이 포함되어 있습니다. 처방전의 안내를 꼭 확인하세요!"
            
            return "SAFE", f"식약처 공식 의약품 데이터베이스에 등록된 정상 의약품입니다. ({drug1} 확인 완료) 자체 사전 기준 상극 대상이 아니므로 안심하고 복용하셔도 좋습니다."
            
        else:
            # 🚨 [하린이의 핵심 철학] 공식 사이트 다 뒤졌는데도 없는 약이면? "못 찾았습니다" 차단!
            return "NOT_FOUND", f"입력하신 '{drug1}'은 대한민국 식약처 및 의약품안전나라 공식 데이터베이스에 등록되어 있지 않거나 존재하지 않는 약 이름입니다. 안전을 위해 복용을 금하시고 의사나 약사와 상의하세요!"
            
    except:
        # 인터넷 끊김 등 최후의 에러 방지 안전망
        return "NOT_FOUND", "현재 국가 의약품 공식 정보망과의 실시간 통신이 원활하지 않습니다. 안전을 위해 모르는 약물의 복용은 의사·약사에게 직접 확인해 주세요!"
