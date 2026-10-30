# ZIPY — 협업 규칙 (v1, 10/30)

## 브랜치
- `main` : 배포용. 직접 push 금지, PR로만.
- `dev`  : 통합용. feature 브랜치는 여기서 따고 여기로 PR.
- `feature/SCRUM-<번호>-<짧은설명>` : 작업 브랜치. **Jira 키를 꼭 넣기** → Jira 티켓에 커밋·PR 자동 연결.
  - 예: `feature/SCRUM-32-crawler`, `feature/SCRUM-48-fe-request-form`

## 커밋 메시지
- `SCRUM-32: 공식 뉴스룸 RSS 크롤러 초안` 처럼 **티켓 키로 시작**.

## 폴더
| 폴더 | 담당 | 내용 |
|---|---|---|
| `collector/` | 채목 | 상시 수집기(에이전트 A), 판정 규칙 3개, CronJob |
| `agents/` | 채목·하윤 | LangGraph 라우터, 에이전트 B(작성)·C(검증관) |
| `backend/` | 경락·하윤 | API, DB 스키마, RAG, PDF 렌더 |
| `frontend/` | 심혁·진우 | 화면 3개 (요청 입력 / 비교표 컨펌 / Sales Pack 검토) |
| `infra/` | 채목 | Docker, k8s, RDS 연결 |
| `docs/` | 전원 | 설계 문서, slots.json, Sales Pack 템플릿 예시 |

## PR
- 리뷰어 1명 이상 승인 후 머지. 본인 머지 가능(5명이라 가볍게).
- PR 제목도 `SCRUM-32: ...`.

## 환경
- 비밀값은 `.env` (git 제외). 샘플은 `.env.example`에만.
