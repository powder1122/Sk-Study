import splunklib.client as client
import splunklib.results as results
import os, re

from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

# --- Splunk 연결 정보 ---
# 환경변수로 변경 예정
SPLUNK_HOST = "localhost"  # 예: localhost
SPLUNK_PORT = os.getenv("SPLUNK_PORT", 8089)  # 환경변수에서 가져오기, 기본값 8089
SPLUNK_USERNAME = os.getenv("SPLUNK_USERNAME", "admin")  # 환경변수에서 가져오기, 기본값 "admin"
SPLUNK_PASSWORD = os.getenv("SPLUNK_PASSWORD", "changeme")  # 환경변수에서 가져오기, 기본값 "changeme"

def execute_splunk_query(spl_query,earliest=None, latest=None):
    """Splunk에 SPL 쿼리를 실행하고 결과를 반환합니다."""
    try:
        # Splunk 서비스에 연결
        service = client.connect(
            host=SPLUNK_HOST,
            port=SPLUNK_PORT,
            username=SPLUNK_USERNAME,
            password=SPLUNK_PASSWORD
        )
        print("Splunk에 성공적으로 연결되었습니다.")

        
        # jobs.create(...) 하기 직전
        q = spl_query.lstrip()
        if not re.match(r'^(search\s|\||tstats\b|mstats\b|from\b|pivot\b|inputlookup\b)', q):
            q = 'search ' + q

        # SPL 쿼리 실행 (동기식)
        job = service.jobs.create(spl_query, exec_mode="blocking")
        print("SPL 쿼리 실행 완료. 결과를 가져오는 중...")

        # 결과 가져오기
        reader = results.ResultsReader(job.results())
        query_results = [event for event in reader]

        return query_results

    except Exception as e:
        print(f"Splunk 연동 중 오류 발생: {e}")
        return None

# # --- 테스트용 SPL 쿼리 ---
# test_query = "search index=_internal | head 5 | table _time, host, source, sourcetype"
# splunk_data = execute_splunk_query(test_query)

# if splunk_data:
#     for row in splunk_data:
#         print(row)


# ===== 여기서부터 추가 (기존 execute_splunk_query는 손대지 않음) =====
def execute_splunk_query_time(spl_query: str, earliest: str = "-24h", latest: str = "now"):
    """
    기간(earliest/latest) 지정 가능 버전. 기존 execute_splunk_query는 그대로 유지.
    환경변수(.env)가 있으면 우선 적용:
      - SPLUNK_HOST (예: https://127.0.0.1)
      - SPLUNK_PORT (기본 8089)
      - SPLUNK_USERNAME / SPLUNK_PASSWORD
    """
    try:
        host_env = os.getenv("SPLUNK_HOST", "")
        port_env = int(os.getenv("SPLUNK_PORT", SPLUNK_PORT))
        user_env = os.getenv("SPLUNK_USERNAME", SPLUNK_USERNAME)
        pass_env = os.getenv("SPLUNK_PASSWORD", SPLUNK_PASSWORD)

        # scheme/host 분리
        if host_env:
            p = urlparse(host_env)
            scheme = p.scheme or "https"
            host   = p.hostname or host_env
        else:
            scheme = "https"
            host   = SPLUNK_HOST

        service = client.connect(
            host=host,
            port=port_env,
            username=user_env,
            password=pass_env,
            scheme=scheme,
        )
        job = service.jobs.create(
            spl_query, exec_mode="blocking",
            earliest_time=earliest, latest_time=latest
        )
        reader = results.ResultsReader(job.results())
        return [event for event in reader if isinstance(event, dict)]
    except Exception as e:
        print(f"Splunk 연동 중 오류 발생(execute_splunk_query_time): {e}")
        return None
# ===== 추가 끝 =====