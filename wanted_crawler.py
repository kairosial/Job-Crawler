import csv
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def crawl_wanted_jobs_detail():
    # 1. Selenium 설정
    options = webdriver.ChromeOptions()
    # 헤드리스 모드
    # options.add_argument("--headless")
    # options.add_argument("--disable-gpu")  # 일부 환경에서 필요할 수 있음
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    
    try:
        # 2. 필터가 적용된 URL (개발 + 선택된 직무 + 경력)로 이동
        url = (
            "https://www.wanted.co.kr/wdlist/518"
            "?country=kr&job_sort=job.latest_order"
            "&years=-1"
            "&selected=899&selected=1634&selected=655&selected=1024&selected=1025"
            "&locations=all"
        )
        driver.get(url)
        
        # 3. 공고 카드가 로딩될 때까지 대기
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "li[class^='Card_Card__']")))
        print("페이지 로딩 완료. 무한 스크롤 시작...")
        
        # 4. 무한 스크롤로 모든 공고 로딩
        SCROLL_PAUSE_TIME = 2
        last_height = driver.execute_script("return document.body.scrollHeight")
        
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(SCROLL_PAUSE_TIME)
            
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                # 더 이상 불러올 공고가 없으면 중단
                break
            last_height = new_height
        
        print("무한 스크롤 완료. 모든 공고가 로딩되었습니다.")
        
        # 5. 공고 목록에서 링크를 추출하고, 상세 페이지 진입
        job_cards = driver.find_elements(By.CSS_SELECTOR, "li[class^='Card_Card__']")
        print(f"공고 카드 개수: {len(job_cards)}")
        
        # 수집할 정보를 저장할 리스트
        results = []
        
        for idx, card in enumerate(job_cards, start=1):
            # 공고 상세 링크 추출
            try:
                link_element = card.find_element(By.TAG_NAME, "a")
                job_link = link_element.get_attribute("href")
            except:
                # 만약 a 태그가 없거나 링크가 없으면 건너뜀
                continue
            
            # 상세 페이지를 새 탭에서 열기
            driver.execute_script("window.open(arguments[0]);", job_link)
            driver.switch_to.window(driver.window_handles[-1])
            
            # "상세 정보 더 보기" 버튼이 있다면 클릭
            try:
                more_button_selector = (
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > section "
                    "> article.JobDescription_JobDescription__dq8G5 > div > button"
                )
                more_button = driver.find_element(By.CSS_SELECTOR, more_button_selector)
                if more_button.is_displayed():
                    more_button.click()
                    time.sleep(1)  # 펼쳐지는 애니메이션 기다리기
            except:
                # 버튼이 없거나 클릭 실패 시 그냥 넘어감
                pass
            
            # 6. 상세 페이지에서 데이터 추출
            try:
                company_name = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > header > div > div:nth-child(1) > a"
                ).text
            except:
                company_name = ""
            
            try:
                job_title = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > header > h1"
                ).text
            except:
                job_title = ""
            
            try:
                career_info = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > header > div > div:nth-child(1) > span:nth-child(5)"
                ).text
            except:
                career_info = ""
            
            try:
                main_task = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > section "
                    "> article.JobDescription_JobDescription__dq8G5 > div > div:nth-child(2) > span"
                ).text
            except:
                main_task = ""
            
            try:
                qualification = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > section "
                    "> article.JobDescription_JobDescription__dq8G5 > div > div:nth-child(3) > span"
                ).text
            except:
                qualification = ""
            
            try:
                preference = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > section "
                    "> article.JobDescription_JobDescription__dq8G5 > div > div:nth-child(4) > span"
                ).text
            except:
                preference = ""
            
            try:
                hiring_process = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > section "
                    "> article.JobDescription_JobDescription__dq8G5 > div > div:nth-child(6) > span"
                ).text
            except:
                hiring_process = ""
            
            try:
                tech_stack = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > section "
                    "> article.JobSkillTags_JobSkillTags__UA0s6 > ul"
                ).text
            except:
                tech_stack = ""
            
            try:
                work_location = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > header > div > div:nth-child(1) > span:nth-child(3)"
                ).text
            except:
                work_location = ""
            
            try:
                deadline = driver.find_element(
                    By.CSS_SELECTOR,
                    "#__next > main > div.JobDetail_contentWrapper__E1lNI > div > section > section "
                    "> article.JobDueTime_JobDueTime__3yzxa > span"
                ).text
            except:
                deadline = ""
            
            # 7. 추출 데이터 정리
            job_data = {
                "회사이름": company_name,
                "직무": job_title,
                "경력": career_info,
                "주요업무": main_task,
                "자격요건": qualification,
                "우대사항": preference,
                "채용 전형": hiring_process,
                "기술 스택 및 툴": tech_stack,
                "근무지역": work_location,
                "마감일": deadline,
                "상세링크": job_link
            }
            results.append(job_data)
            
            # 탭 닫기 후, 다시 원래 탭으로 돌아옴
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            
            # 진행 상황 출력
            print(f"[{idx}/{len(job_cards)}] {company_name} - {job_title} 수집 완료")
        
        # 8. CSV로 저장하기
        # 파일명: yymmdd_HHMMSS-JC.csv
        timestamp_str = datetime.now().strftime("%y%m%d_%H%M%S")
        filename = f"{timestamp_str}-JC.csv"
        
        # CSV 파일 생성 (utf-8-sig로 인코딩해서 한글 깨짐 방지)
        with open(filename, mode="w", encoding="utf-8-sig", newline="") as f:
            writer = csv.writer(f)
            # 헤더 작성
            writer.writerow(["회사이름","직무","경력","주요업무","자격요건","우대사항","채용 전형","기술 스택 및 툴","근무지역","마감일","상세링크"])
            
            # 실제 데이터 작성
            for r in results:
                writer.writerow([
                    r["회사이름"],
                    r["직무"],
                    r["경력"],
                    r["주요업무"],
                    r["자격요건"],
                    r["우대사항"],
                    r["채용 전형"],
                    r["기술 스택 및 툴"],
                    r["근무지역"],
                    r["마감일"],
                    r["상세링크"]
                ])
        
        print(f"총 수집 공고 수: {len(results)}")
        print(f"CSV 저장 완료: {filename}")
        
    finally:
        # 9. 마무리
        driver.quit()

if __name__ == "__main__":
    crawl_wanted_jobs_detail()
