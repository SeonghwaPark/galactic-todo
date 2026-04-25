<!-- Banner -->
<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0a0e27,50:4fd1ff,100:ffe81f&height=200&section=header&text=Galactic%20Command&fontSize=52&fontColor=ffffff&fontAlignY=38&desc=Star%20Wars%20Themed%20Cloud-Synced%20To-Do&descSize=18&descAlignY=60&animation=fadeIn" />
</p>

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" />
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white" />
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" />
  <img src="https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black" />
  <img src="https://img.shields.io/badge/Status-Active-4fd1ff?style=for-the-badge" />
</p>

<p align="center">
  <i>"Do or do not. There is no try."</i> — 클라우드 동기화 할일 관리, 은하계 어디서든.
</p>

---

## ✨ 주요 기능

| 영역 | 기능 |
|---|---|
| 🌌 **인증** | Google OAuth + 화이트리스트 기반 액세스 제어 |
| ☁️ **동기화** | Firebase Realtime Database로 PC ↔ 모바일 즉시 반영 |
| 📅 **캘린더** | 월간 뷰 + 한국 공휴일·대체공휴일·임시공휴일 자동 표시 (2025-2027) |
| 🔍 **검색** | 제목/메모 전체 텍스트 검색 |
| 🔔 **알림** | 마감 임박 / 우선순위 기반 시각 알림 |
| 📊 **통계** | 일일 완료율, 누적 트렌드 |
| 🎨 **UI** | 홀로그램 스캔라인 · 네온 사이언 · 제국 로고 워터마크 |

---

## 🪐 디자인 컨셉

```css
/* Brand Palette */
--space-deep   : #0a0e27   /* 우주 배경 */
--neon-cyan    : #4fd1ff   /* 홀로그램 글로우 */
--imperial-gold: #ffe81f   /* 강조·CTA */
--scan-line    : rgba(79, 209, 255, 0.05)
```

- **Orbitron** + **Exo 2** 폰트로 SF 디스플레이 감성
- 다크 우주 배경 위에 **홀로그램 스캔라인** 오버레이
- 네온 글로우 인터랙션 + 제국 로고 워터마크

---

## 🛠️ 기술 스택

- **Frontend**: Vanilla HTML/CSS/JS — 빌드 도구 없는 단일 파일 (`index.html`)
- **Backend**: Firebase
  - Authentication (Google Sign-In)
  - Realtime Database (`users/{userId}/todos`)
- **CDN**: Firebase SDK는 CDN으로 로드
- **폰트**: Orbitron, Exo 2 (Google Fonts)

---

## 🚀 실행

```bash
git clone https://github.com/SeonghwaPark/galactic-todo.git
cd galactic-todo
# 브라우저로 index.html 열기 (별도 빌드/서버 불필요)
```

> 단일 HTML 파일이라 로컬에서 바로 더블클릭으로 실행 가능합니다.

---

## 📓 서브 프로젝트: GoodNotes Planner

`goodnotes-planner/` 디렉토리에는 iPad Pro 11" GoodNotes용 디지털 플래너 PDF 생성기가 포함되어 있습니다.

```bash
cd goodnotes-planner
python make_planner.py --year 2026               # 세로 버전
python make_planner.py --year 2026 --landscape   # 가로 버전
```

- 연간/월간/주간/프로젝트/미팅 페이지 자동 생성
- 하이퍼링크 네비게이션 내장
- 한국 공휴일 표기

---

## 📁 구조

```
galactic-todo/
├── index.html              # 메인 앱 (HTML + CSS + JS 단일 파일)
├── CLAUDE.md               # 프로젝트 컨텍스트 (Claude Code용)
└── goodnotes-planner/      # iPad 디지털 플래너 생성기
    ├── make_planner.py
    ├── fonts/
    └── *.pdf
```

---

<p align="center">
  <sub>⚡ Built with the Force ⚡</sub>
</p>
