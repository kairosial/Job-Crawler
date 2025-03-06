# 크롤링할 URL (원티드에서 필터 적용 후 주소창에 나타나는 최종 URL)
URL="https://www.wanted.co.kr/wdlist/518?country=kr&job_sort=job.popularity_order&years=-1&selected=655&selected=899&selected=1024&selected=1634&selected=1025&locations=all"

# CSV 파일 이름
FILENAME="dev-py_ml_dte_dts_bdte-carrer_all-loc_all-pop_ord"

# "$@" 부분을 --headless로 바꾸면 헤드리스 모드로 실행
# 헤드리스 모드? 브라우저 창이 열리지 않고, 백그라운드에서 실행
python3 wanted_crawler.py \
    --url "$URL" \
    --filename "$FILENAME" \
    --scroll_limit 2 \
    "$@"
