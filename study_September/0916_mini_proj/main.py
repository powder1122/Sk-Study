# main.py
from splunk import execute_splunk_query
from openai_api import analyze_with_openai, nl_to_spl
import argparse

def main():
    print("S-GPT (NL→SPL→Splunk→분석)")
    print("-" * 40)

    ap = argparse.ArgumentParser()
    ap.add_argument("--query", required=False, help="자연어 질의(예: '지난 24시간 ssh 실패 상위 10')")
    ap.add_argument("--earliest", default=None, help="Splunk 검색 시작시각(예: -24h, 0)")
    ap.add_argument("--latest", default=None, help="Splunk 검색 종료시각(예: now)")
    args = ap.parse_args()

    # 1) 자연어 질의 입력
    nl_text = args.query or input("자연어 질의 입력: ").strip()
    if not nl_text:
        print("질의가 비어 있습니다.")
        return

    # 2) NL→SPL 변환
    print("\n[1/4] 자연어→SPL 변환 중...")
    nl2spl = nl_to_spl(nl_text, default_earliest=args.earliest, default_latest=args.latest)
    spl = nl2spl.get("spl", "").strip()
    earliest = nl2spl.get("earliest", args.earliest or "-24h")
    latest = nl2spl.get("latest", args.latest or "now")

    if not spl:
        print("SPL 변환 실패: 빈 SPL")
        return
    print(f"SPL: {spl}\n(earliest={earliest}, latest={latest})")

    # 3) Splunk 실행
    print("\n[2/4] Splunk 검색 실행 중...")
    rows = execute_splunk_query(spl, earliest=earliest, latest=latest)
    if rows is None:
        print("Splunk에서 결과를 가져오지 못했습니다.")
        return

    print(f"총 {len(rows)}개 이벤트 수신.")
    for r in rows[:3]:
        print(r)

    # 4) GPT 분석(+Snort 룰)
    print("\n[3/4] OpenAI 분석 중...")
    analysis = analyze_with_openai(rows, user_query=nl_text, used_spl=spl)

    print("\n[4/4] === AI 분석 결과 ===")
    print(analysis)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--query", default=None, help="자연어 질의가 주어지면 NL→SPL→Splunk→분석 경로 실행")
    ap.add_argument("--earliest", default=None)
    ap.add_argument("--latest", default=None)
    args = ap.parse_args()

    if not args.query:
        # 자연어 질의가 없으면 기존 main() 그대로 실행(기존 테스트 로직 유지)
        main()
    else:
        print("S-GPT (NL→SPL→Splunk→분석)")
        print("-" * 40)
        # 1) NL→SPL
        out = nl_to_spl(args.query, default_earliest=args.earliest, default_latest=args.latest)
        spl = out.get("spl", "").strip()
        earliest = out.get("earliest", args.earliest or "-24h")
        latest   = out.get("latest",   args.latest   or "now")
        if not spl:
            print("SPL 변환 실패(빈 결과)")
            raise SystemExit(2)
        print(f"\n[SPL]\n{spl}\n(earliest={earliest}, latest={latest})")

        # 2) Splunk 실행 (새 함수 우선 시도 → 없으면 구버전 호출)
        try:
            from splunk import execute_splunk_query_time
            rows = execute_splunk_query_time(spl, earliest=earliest, latest=latest)
        except Exception:
            # 타입/Import 오류 시 구버전으로 폴백
            rows = execute_splunk_query(spl)

        if not rows:
            print("Splunk에서 결과를 가져오지 못했습니다.")
            raise SystemExit(1)

        print(f"\n[프리뷰] 총 {len(rows)}건 (상위 3건):")
        for r in rows[:3]:
            print(r)

        # 3) 분석
        print("\n[분석 실행]")
        result = analyze_with_openai(rows, args.query)
        print("\n=== AI 분석 결과 ===")
        print(result)