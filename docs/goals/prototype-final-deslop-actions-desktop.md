/goal

## 1) 작업 핵심 목표 및 범위
- 목표: `prototype-final.html`이 아래 6)의 세 가지 기준(AI 슬롭 · 조작 완비 · 대표 조작 하나)을 화면마다 모두 통과해, 감사 명령 세 개가 각각 `AUDIT_RESULT:ALL_PASS`를 출력하는 상태로 만든다.
- 시작 지점: 저장소 `axyourbody-prototype`의 현재 `main` HEAD(`507a3b5` 이후). 먼저 `git status --porcelain`과 `git branch -a`를 실행해 결과를 대화에 남긴다.
- 작업 대상: 루트의 `prototype-final.html` 한 파일(단독 실행 HTML 유지). 감사 도구 `tools/audit_static.py`, `tools/audit.html`과 작업 기록 `docs/goals/logs/deslop-log.md`는 새로 만든다.
- 작업 자율성:
  - 화면마다 **핵심 메시지의 방향**(아래 표)을 바꾸지 않는 한, 레이아웃·문구·위계·컴포넌트 표현은 사용자 확인 없이 충분히 고친다.
  - 사용자에게 질문하지 않는다. 판단이 필요한 지점에서는 스스로 결정하고, 결정마다 나중에 이어받을 사람을 위한 **의도 설명**을 기록한다(2)의 결정 기록 형식).
  - 자율 결정 예산: CORE 최대 5건, MINOR 최대 30건. 예산을 넘기는 결정이 필요해지면 목표 달성 전이라도 멈춘다(3) 종료 조건).

| 화면 | 바꾸면 안 되는 핵심 메시지 |
|---|---|
| 퇴실 알림 | 오늘 할 운동 하나를 알려 출발을 돕는다 |
| 오늘 · 추운 날 · 마감 2일 전 | 오늘 할 일은 하나로 정해져 있고, 이유가 있다 |
| 운동 코스 상세 | 순서와 시간이 정해져 있어 고민할 필요가 없다 |
| 운동 중 · 끝내기 시트 | 지금 동작 하나에 집중하고, 언제든 그만둬도 기록된다 |
| 운동 끝 · 오류 | 해낸 것을 인정하고, 기록은 사라지지 않는다 |
| 좋아지는 흐름 | 하루 숫자보다 흐름과 지킨 횟수가 중요하다 |
| 오늘은 못 가요 · 운동 약속 | 미뤄도 괜찮고, 다음을 가볍게 정한다 |
| 기록(빈 상태) · 나 | 비어 있어도 괜찮고, 하나만 남기면 된다 |

## 2) 작업 세부 규칙
- 참고 문서(읽기 전용): `context/service-structure.md`(5장 사용자 용어 · 8장 "하지 말 것"), `context/screen-flow.md`, `context/screen-layouts.md`.
- **고치는 방식: 일괄 코드 처리 금지, 위치마다 읽고 판단한다.**
  - `sed`·정규식 일괄 치환·스크립트로 여러 위치를 한꺼번에 바꾸지 않는다. 고칠 위치를 하나씩 읽고, 그 자리의 맥락(화면, 핵심 메시지, 주변 요소)에 맞는 표현을 골라 개별로 수정한다.
  - 감사 도구는 **찾기와 증명에만** 쓴다. 감사가 FAIL로 짚은 위치도 같은 방식으로 하나씩 검토해 고친다.
  - 슬롭 신호가 기계적으로는 통과해도 문장·위계가 여전히 "어디서나 쓸 수 있는 말"이면 고친다(예: 경쟁 서비스가 그대로 써도 되는 문장).
- **라운드 단위:** 한 라운드 = 한 화면을 골라 검토 → 고치기 → 감사 재실행 → 기록. 한 라운드에서 고치는 위치는 최대 30개. 같은 화면은 최대 5라운드까지 반복한다.
- 단계 순서. 각 단계가 끝날 때마다 감사를 다시 실행하고 출력을 대화에 남긴 뒤 커밋한다.
  - 0단계: 작업 브랜치 준비(4) 참고)와 감사 도구 작성. 6)의 기준을 그대로 코드로 옮기고 기준값을 느슨하게 바꾸지 않는다. 고치기 전 결과를 한 번 실행해 대화에 남긴다(기준선).
  - 1단계: AI 슬롭 개선 → `audit_static.py` 통과.
  - 2단계: 화면에 암시된 조작 완비 → `audit.html`의 ACTIONS 항목 통과.
  - 3단계: 데스크톱 레이아웃과 대표 조작 하나 → `audit.html`의 PRIMARY · DESKTOP · CONTRAST 항목을 1440×900과 390×844에서 모두 통과.
- 감사 명령(프로젝트 루트에서 실행. 출력 마지막 줄이 `AUDIT_RESULT:ALL_PASS` 또는 `AUDIT_RESULT:FAIL n`):
  - `python3 tools/audit_static.py prototype-final.html`
  - `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --allow-file-access-from-files --window-size=1440,900 --virtual-time-budget=15000 --dump-dom "file://$PWD/tools/audit.html?w=1440&h=900" | grep -E 'AUDIT_(LINE|RESULT)'`
  - 위와 같은 명령을 `--window-size=390,844`와 `?w=390&h=844`로 한 번 더 실행한다.
- `tools/audit.html`은 같은 폴더 기준 `../prototype-final.html`을 주어진 크기의 iframe으로 열고, 앱이 노출하는 `window.go(id)`·`window.jump(id)`·`window.SCREENS`로 화면을 차례로 띄워 검사한다. 항목마다 `AUDIT_LINE:<항목> <화면> PASS|FAIL <세부>`와 마지막 `AUDIT_RESULT:` 줄을 `<pre id="audit">`에 적는다. 앱에는 감사 전용 코드를 넣지 않는다(`window.SCREENS` 배열과 `jump` 노출만 허용).
- **결정 기록** `docs/goals/logs/deslop-log.md`:
  - 기준에 없는 판단은 한 줄씩 남긴다. 형식: `[CORE|MINOR] <화면> · <무엇을 정했나> · 의도: <왜 이렇게 정했고, 이어받는 사람이 무엇을 알아야 하나>`.
  - CORE = 화면 구조·흐름·새 화면 추가·대표 조작 선택처럼 다른 화면에 영향을 주는 결정. MINOR = 문구·간격·위계·아이콘처럼 한 화면 안에서 끝나는 결정.
  - 파일 맨 위에 grep 가능한 카운터를 각각 별도 줄로 유지한다: `CORE: N`, `MINOR: M`, `STALL: K`, 그리고 화면마다 `ROUNDS <화면 id>: R`.
  - 감사 실패 수가 직전 라운드보다 줄지 않은 라운드는 `STALL`을 1 올리고, 줄면 0으로 되돌린다.
- 커밋: 라운드마다 1회. 메시지 `deslop: <단계> <화면> <요약>`, 끝줄 `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. 단계가 끝날 때마다 작업 브랜치를 원격에 push한다.

## 3) 종료 조건 및 종료 방법
- 종료 조건 (아래 중 하나라도 충족되는 순간 루프를 즉시 멈춘다):
  - 감사 명령 세 개가 모두 `AUDIT_RESULT:ALL_PASS` → STOP REASON: ALL_PASS
  - 다음 결정이 `CORE` 6건째가 되는 순간 → STOP REASON: CORE_BUDGET
  - 다음 결정이 `MINOR` 31건째가 되는 순간 → STOP REASON: MINOR_BUDGET
  - `STALL` 카운터가 3에 도달 → STOP REASON: STALLED
  - 모든 화면이 PASS이거나 `ROUNDS`가 5에 도달해 더 고칠 화면이 없음 → STOP REASON: SCREEN_ROUNDS_EXHAUSTED (5라운드에 닿은 화면은 남은 FAIL을 로그에 적고 다음 화면으로 넘어간다)
  - 평가-진행 라운드(turn = /goal 평가자가 진행 상태를 한 번 점검하는 메인 에이전트 응답 사이클)가 누적 90회에 도달 → STOP REASON: TURN_CAP (= or stop after 90 turns. 화면 약 18개 × 5라운드의 안전 상한)
- 종료 방법:
  1) `docs/goals/logs/deslop-log.md` 마지막에 `STOP REASON: <코드>` 한 줄과, 이어받는 사람을 위한 **인수 메모**(남은 FAIL 목록 · CORE 결정 요약 · 다음에 할 일 3줄 이내)를 덧붙이고 커밋한 뒤 작업 브랜치를 push한다.
  2) 2)의 감사 명령 세 개를 실행해 `AUDIT_LINE`·`AUDIT_RESULT` 출력 전체를 대화에 남긴다.
  3) `git status --porcelain`, `git log --oneline -15`, `git diff --stat main...HEAD`, `git branch -vv`, `cat docs/goals/logs/deslop-log.md`를 실행해 출력을 대화에 남긴다. `git diff --stat`에는 4)에서 허용한 경로만 보여야 하고, `git branch -vv`에는 작업 브랜치가 원격을 추적하는 것이 보여야 한다.

## 4) 기타 제약조건
- 작업 브랜치: `goal/prototype-final-deslop-actions-desktop`. 0단계에서 이미 있으면 그대로 쓰고, 없으면 `main`에서 만든 뒤 `git push -u origin goal/prototype-final-deslop-actions-desktop`으로 원격에 올린다. 나중에 사용자가 `main` 기준으로 통합할 수 있게 이 브랜치에서만 작업한다.
- `main`에 커밋·병합·push하지 않는다. force push, 브랜치 삭제, 강제 리셋을 하지 않는다.
- 수정·커밋할 수 있는 경로: `prototype-final.html`, `tools/audit_static.py`, `tools/audit.html`, `docs/goals/logs/`, 그리고 이 goal 파일 자체(내용은 수정하지 않고 브랜치에 커밋만 허용). 그 밖의 파일(`context/`, `data/`, `worksheet.md`, `profile.md`, `README.md`, `context/stitch_.zip`)은 수정하거나 커밋하지 않는다.
- 새 화면·메뉴·기능을 만들지 않는다. **예외:** 6-2에 적힌 "반드시 동작해야 하는 조작"에 필요한 화면, 그리고 기존 기획에서 기능과 기능, 화면과 화면 사이에 끊기는 지점이 있어 부드럽게 이어 줄 연결이 필요한 경우에는 만들 수 있다. 이 예외로 만든 화면은 CORE 결정으로 기록하고 어느 끊김을 메웠는지 의도에 적는다.
- 단독 HTML 유지: 외부 `<script src>`·`<link href>`·원격 이미지·웹폰트를 쓰지 않는다. 데이터는 `data/` CSV에 있는 값이나 화면에 "예시"로 밝힌 값만 쓴다. 칼로리·심박수처럼 데이터에 없는 수치를 새로 만들지 않는다.
- 실제 이름·연락처·실제 신체 수치를 넣지 않는다. 사용자는 `my-general`로만 표시한다.
- 감사를 통과시키려고 기능을 지우지 않는다. 기존 화면(기본 흐름 7 · 갈림길 A~D · 상태 4 · 나)과 그 동작은 모두 남아 있어야 한다.

## 5) 보고 형식 (라운드마다 대화에 남길 것)
- `라운드 R · <화면> · 고친 위치 n/30 · 감사 FAIL a→b · CORE N/5 · MINOR M/30 · ROUNDS r/5`
- 그 라운드에서 내린 결정의 의도 설명(로그에 쓴 줄과 같은 내용)

## 6) 감사 기준 (감사 도구가 그대로 구현할 것)

### 6-1. AI 슬롭 — `audit_static.py` (출처: scalr.sg "20 signs a website was made by AI")
| 항목 | 신호 | 통과 기준 |
|---|---|---|
| GRADIENT | 1·2 보라-파랑 그라데이션, 글자 그라데이션 | `linear-gradient`·`radial-gradient`·`background-clip:text` 0개. 단, 로딩 뼈대 `.sk` 한 곳만 허용 |
| EMOJI | 3 제목 속 이모지 | 그림 문자(Extended_Pictographic) 0개 |
| TYPE | 4 한 가지 크기·굵기 | `font-size` 값은 `:root`의 `--fs-*` 토큰으로만 쓰고 토큰은 7개 이하. 가장 큰 제목과 본문 크기 비율이 2.0 이상 |
| LEFTBAR | 5 왼쪽 색 테두리 | `border-left` 선언 0개 |
| GLASS | 6 반투명 블러 카드 | `backdrop-filter` 0개, 알파 0.95 미만인 `rgba(` 배경 0개(어둡게 덮는 `.dim` 한 곳만 허용) |
| ICON | 10 의미 없는 장식 아이콘 | `<use href="#i-…">`에 쓰인 아이콘이 허용 목록(탭 4종, back, chev, check, play)에만 있음 |
| BUTTON | 11·14 기본 버튼, 투명도만 바뀌는 hover | `.btn:active`와 `:focus-visible` 규칙이 있음. `:hover` 규칙 안에 `opacity`만 있는 규칙 0개 |
| MOTION | 12·13 스크롤 페이드, 커서 따라오는 빛 | `IntersectionObserver`·`mousemove`·`pointermove` 0개. `@keyframes`는 뼈대용 하나만 |
| SPACING | 15 규칙 없는 간격 | `margin`·`padding`·`gap`·`inset`·`top/right/bottom/left`의 px 값(인라인 style 포함)이 모두 {0,2,4,8,12,16,20,24,32,40,48,64} 안 |
| DASH | 16 줄표 | `—`, `&mdash;`, `–` 0개 |
| BUZZ | 17 상투어 | seamless·robust·elevate·empower·leverage·혁신·스마트한·완벽한·최적의·손쉽게·간편하게·원활 0개 |
| SERIF | 18·19 이탤릭 세리프 강조, 유행 글꼴 조합 | `font-style:italic` 0개, `serif` 글꼴(‘sans-serif’ 제외) 0개 |
| GRAIN | 20 노이즈 질감 | `feTurbulence`·`noise`·`grain` 0개 |
| SELFCONTAINED | 단독 HTML | `<script src`·`<link … href="http`·`<img … src="http` 0개 |

### 6-2. 조작 완비 — `audit.html` ACTIONS (390×844와 1440×900 모두)
- PLACEHOLDER: 파일 안 `다음 버전에서` 문구 0개.
- DEAD_CLICK: 모든 화면에서 보이는 클릭 대상(`button`, `a`, `[onclick]`, `[data-go]`, `[data-jump]`, `[role=button]`)을 화면을 새로 띄운 상태에서 하나씩 눌렀을 때, ①보이는 화면이 바뀌거나 ②시트가 열리거나 ③지금 화면의 DOM이 바뀌어야 한다(`#toast`의 변화만 있는 경우는 실패). 실패 0개.
- FAKE_AFFORDANCE: `cursor:pointer`이거나 안에 `#i-chev` 아이콘이 있는데 클릭 대상이 아닌 요소 0개(예: 운동 중 "다음:" 줄).
- 반드시 실제로 동작해야 하는 조작(지금은 토스트만 뜨거나 비어 있음): 코스 목록(다른 코스 보기 → 고르면 오늘·상세에 반영), 몸무게 재기(입력 → 변화 화면 요약·흐름선에 반영), 식사 하나 기록하기(끼니와 탄·단·지 입력 → 빈 끼니 줄이 채워짐), 약속 시간 바꾸기·코스 바꾸기(선택 → 약속 화면과 확인 토스트에 반영), 실내 코스 운동 시작·10분 스트레칭(각자 동작 목록으로 운동 중 화면 진행), 운동 중 "다음:" 줄(누르면 다음 동작 미리 보기 또는 넘어가기).
- STATE: 위 조작의 결과가 다른 화면에 반영되는지 감사 도구가 입력 → 이동 → 값 확인 순서로 각 1회 검사한다.

### 6-3. 대표 조작 하나 — `audit.html` PRIMARY · DESKTOP · CONTRAST
- 대표 조작은 "주 버튼 모양(채운 배경 · 브랜드 주 색)인 클릭 대상"으로 정의한다. 화면 목록 패널, 탭, 시트 바깥 요소를 모두 포함해 **보이는 화면 전체에서** 센다.
- PRIMARY: 아래 화면마다 대표 조작이 정확히 1개이고, 그 글자가 표와 같다. 표에 없는 새 화면은 1개 이하이고 로그에 대표 조작을 적는다. 로딩은 0개.

| 화면 | 대표 조작 | 화면 | 대표 조작 |
|---|---|---|---|
| 퇴실 알림 | 시작하기 | 운동 끝 | 좋아지는 흐름 보기 |
| 오늘 · 추운 날 · 운동 코스 상세 | 운동 시작 | 오류(운동 끝) | 다시 저장하기 |
| 마감 2일 전 | 이대로 할게요 | 좋아지는 흐름 | 다음 운동 약속 정하기 |
| 오늘은 못 가요 | 10분만 하기 | 운동 약속 정하기 | 약속 정하기 |
| 운동 중 | 다음 동작 | 기록(빈 끼니 있음) | 식사 하나 기록하기 |
| 중간에 끝내기 시트 | 끝내고 기록하기 | 나 | 0개 또는 1개 |

- DESKTOP(1440×900에서만): 휴대폰 틀 대신 데스크톱 레이아웃을 쓴다. 앱 본문 폭이 720px 이상이고, 하단 탭 대신 화면 왼쪽 앱 메뉴(오늘·기록·변화·나 4개)를 쓰며, 대표 조작이 스크롤 없이 첫 화면 안에 완전히 보인다. 그 밖의 조작은 보조 버튼·텍스트 링크로 낮추거나 위치를 옮겨 대표 조작과 경쟁하지 않게 한다. 프로토타입 검토용 화면 목록은 기본으로 숨기고 작은 텍스트 링크로만 연다(열린 상태에서도 주 색 채움 없음).
- MOBILE(390×844): 기존 휴대폰 흐름을 유지하고, PRIMARY 기준을 똑같이 만족한다.
- CONTRAST: 보이는 모든 글자의 명도 대비가 4.5:1 이상(24px 이상 또는 19px 이상 굵은 글자는 3:1 이상).
