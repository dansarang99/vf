# Vercel Production Deployment Overview

## 1. 라이브 서비스 URL
- **공식 메인 갤러리**: [https://src-topaz-nu.vercel.app](https://src-topaz-nu.vercel.app)
- **스텔스 관리자 CMS 스튜디오**: [https://src-topaz-nu.vercel.app/admin](https://src-topaz-nu.vercel.app/admin)
- **최신 빌드 배포본**: [https://src-o28jry1nu-leehankyus-projects.vercel.app](https://src-o28jry1nu-leehankyus-projects.vercel.app)
- **Vercel 대시보드 인스펙터**: [https://vercel.com/leehankyus-projects/src](https://vercel.com/leehankyus-projects/src)

---

## 2. 관리자 인증 정보 (Security)
- **아이디**: `admin`
- **비밀번호**: `1234567` (화면 일체 미노출 보안 처리)
- **편의 기능**: 👑 정식 관리자 원클릭 고속 인증 (Fast-Pass) 버튼 내장
- **스텔스 진입로**: 메인 헤더 좌측 로고 `MA JI YOUNG | 아틀리에` 중 `( 아틀리에 )` 바로 아랫쪽 여백 클릭 시 관리자 모달 진입

---

## 3. 원클릭 Vercel 재배포 명령어
`src/` 디렉토리에서 다음 명령어를 실행하면 5초 만에 글로벌 CDN 프로덕션에 즉시 반영됩니다:
```bash
cd src
npx vercel deploy --prod --yes
```
