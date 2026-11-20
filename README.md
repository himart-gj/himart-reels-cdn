# 롯데하이마트 경기광주점 — 초고화질(UHD 60FPS) 릴스 공개 미디어 CDN (`himart-reels-cdn`)

외부 업로드 용량 한계로 인한 영상 비트레이트 저하를 방지하고, **방송 마스터급 초고화질(`1080x1920 @ 60FPS`, `CRF 17`, `5,000~8,500kbps`, 파일당 최대 `2GB`)** 릴스 MP4를 외부 자동화 워크플로우 및 SNS 채널에 무인증 직결 공급하는 공개 미디어 CDN 저장소입니다.

## 직결 URL 규격 (영구 무인증 HTTPS · Fastly CDN)
```text
https://github.com/himart-gj/himart-reels-cdn/releases/download/<release_tag>/<filename>.mp4
```

## 연동 구조
1. **프라이빗 생성 워커**: 초고화질 60FPS 마스터 합성 완료 후 본 공개 저장소의 GitHub Releases로 무압축 UHD MP4를 업로드합니다.
2. **릴리즈 자동화 템플릿 (`workflow_template_publish_uhd_release.yml`)**: 필요 시 `.github/workflows/publish_uhd_release.yml`로 복사하면 자체 `GITHUB_TOKEN`만으로 `staging/` 에셋을 즉시 Public Release로 발행합니다.
3. **외부 자동화 워크플로우 연동**: 위 Release 직결 URL을 외부 게시 파이프라인의 미디어 URL 파라미터에 주입하면 원본 화질 그대로 게시됩니다.
