.PHONY: launch audit missing youtube epub kit backup panic_on panic_off

launch:
	zsh install_and_launch.zsh

audit:
	zsh tools/audit/run_two_pass_audit.zsh

missing:
	zsh scripts/first_run/fill_missing_info.zsh

youtube:
	zsh tools/automation/youtube/yt_prepare_and_upload.zsh artifacts/staging/draft_youtube.txt

epub:
	zsh tools/exporters/book_epub/build_epub.zsh 'artifacts/staging/*.txt' artifacts/published/book.epub

kit:
	zsh tools/exporters/digital_kit/build_kit.zsh

backup:
	zsh tools/snapshots/backup_now.zsh

panic_on:
	zsh scripts/panic_on.zsh

panic_off:
	zsh scripts/panic_off.zsh
