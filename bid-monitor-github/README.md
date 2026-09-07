# 입찰공고 모니터 (GitHub Pages 버전)

나라장터 OpenAPI에서 최근 30일 용역 입찰공고·사전규격을 매일 자동 수집해
`docs/index.html` 한 페이지로 만듭니다. 서버·PC 없이 GitHub Actions + Pages 로 동작.

- 관심 키워드·필터는 **각자 브라우저에 저장** (회사 기본값은 `config.yaml`)
- 기관 태그(LH/GH/IH/SH), 구분(공공기관/지자체/중앙정부/교육기관/기타) 자동 부여
- 갱신 주기: 매일 07:00, 평일 12:00 (`.github/workflows/collect.yml` 의 cron)

## 최초 설정
1. 이 폴더를 GitHub 저장소로 올리기 (Public)
2. Settings → Secrets and variables → Actions → New repository secret
   - Name: `G2B_SERVICE_KEY`  /  Secret: data.go.kr 인증키
3. Settings → Pages → Source: Deploy from a branch → Branch: `main`, Folder: `/docs` → Save
4. Actions 탭 → "입찰공고 수집" → Run workflow (첫 수집)
5. 몇 분 뒤 `https://<계정>.github.io/<저장소>/` 접속

## 기본 키워드 바꾸기
`config.yaml` 의 `filters` 수정 → 다음 수집부터 "회사 기본값"으로 반영.
