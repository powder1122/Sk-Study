from openai import OpenAI
import os
import json, re

from dotenv import load_dotenv
load_dotenv()
# --- OpenAI API 키 설정 ---
# 환경 변수에서 키를 가져오는 것을 권장합니다.
# os.environ["OPENAI_API_KEY"] = "your_openai_api_key"
OpenAIKey = os.getenv("OPENAI_API_KEY")
oClient = OpenAI(api_key=OpenAIKey)
def analyze_with_openai(splunk_results, user_query=None, used_spl=None):
    """Splunk 결과를 OpenAI로 분석하고 요약, 대응 방안을 생성합니다."""
    if not splunk_results:
        return "분석할 Splunk 데이터가 없습니다."

    # 분석을 위해 데이터를 문자열로 변환
    data_string = "\n".join([str(item) for item in splunk_results])

    # OpenAI에 전달할 프롬프트
    prompt = f"""
    당신은 최고 수준의 보안 분석가입니다.

    아래 Splunk 검색 결과는 사용자가 실행한 다음 SPL 쿼리의 결과입니다.
    사용자 쿼리: "{user_query}"

    검색 결과:
    ```
    {data_string}
    ```

    위 데이터를 기반으로 다음 세 가지 항목에 대해 상세히 분석하고 응답해주세요.

    1.  **분석 결과**:
        - 이 데이터가 의미하는 바는 무엇인가요?
        - 보안 관점에서 어떤 종류의 활동이나 위협으로 해석될 수 있나요?
        - 특이사항이나 주목해야 할 패턴이 있다면 알려주세요.

    2.  **결과 요약**:
        - 전체 내용을 핵심만 간결하게 한두 문장으로 요약해주세요.

    3.  **대응 방안 (Snort 룰셋)**:
        - 만약 이 결과가 악의적인 활동으로 의심된다면, 이를 탐지할 수 있는 Snort 룰을 생성해주세요.
        - 룰에는 관련된 IP, 포트, 페이로드 등을 최대한 활용하여 구체적으로 작성해주세요.
        - 만약 룰 생성이 부적절하다면, 그 이유를 설명해주세요.
    """

    try:
        oResponse = oClient.responses.create(
            model="gpt-5",  
            reasoning={"effort": "low"},
            input=[
                {"role": "system", "content": "당신은 유능한 보안 분석가입니다."},
                {"role": "user", "content": prompt}
            ],
        )
        return oResponse.output_text 

    except Exception as e:
        return f"OpenAI API 호출 중 오류 발생: {e}"
    

# ===== 여기서부터 추가 (기존 코드 아래에 덧붙임) =====

# .env의 OPENAI_MODEL을 우선 사용, 없으면 안전한 기본값
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5")

def _chat_json(system: str, user: str) -> dict:
    if not OpenAIKey:
        raise RuntimeError("OPENAI_API_KEY 미설정(.env)")
    resp = oClient.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[{"role":"system","content":system},
                  {"role":"user","content":user}],
        # temperature=0  # ← 위 2)에서 제거 권장
    )
    text = (resp.choices[0].message.content or "").strip().strip("`").strip()
    m = re.search(r'\{.*\}', text, re.S)
    if m:
        text = m.group(0)
    return json.loads(text)

def nl_to_spl(nl_text: str, default_earliest: str = None, default_latest: str = None) -> dict:
    """
    자연어 → SPL 변환(비파괴 추가). 반환 예:
    {"spl":"index=_internal | head 3","earliest":"-24h","latest":"now"}
    """
    de = default_earliest or "-24h"
    dl = default_latest or "now"
    sys_prompt = (
        "역할: Splunk SPL 전문가.\n"
        "출력은 JSON으로만 응답: {\"spl\":\"...\",\"earliest\":\"...\",\"latest\":\"...\"}\n"
        "규칙:\n"
        f"- 기간이 명시되지 않으면 earliest='{de}', latest='{dl}'\n"
        "- 고비용 명령(join/transaction 대규모/map) 지양, 결과는 stats/table/head로 축소\n"
        "- SPL 최후단은 stats/table/head 중 하나로 종료\n"
        "- 공통 필드 예: src, src_ip, dest, user, uri_path, status, process_name, parent_process_name\n"
    )
    out = _chat_json(sys_prompt, nl_text)
    return {
        "spl":     out.get("spl", ""),
        "earliest":out.get("earliest", de),
        "latest":  out.get("latest", dl),
    }
# ===== 추가 끝 =====