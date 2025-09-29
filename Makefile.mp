# Monkey Paw Integration Makefile

.PHONY: mp-copy mp-merge mp-full mp-clean

mp-copy:
	@echo "Running copy ingestion..."
	python3 _mp_integration/merge/copy_ingestion.py

mp-merge:
	@echo "Merging to project..."
	python3 _mp_integration/merge_to_project.py

mp-full: mp-copy mp-merge
	@echo "Full integration complete!"

mp-clean:
	@echo "Cleaning staging area..."
	rm -rf _mp_integration/staging/*
	@echo "Staging area cleaned."

mp-status:
	@echo "Integration Status:"
	@echo "Staging files:"
	@find _mp_integration/staging -type f 2>/dev/null | wc -l || echo "0"
	@echo "Imported files:"
	@find _mp_integration/imports -type f 2>/dev/null | wc -l || echo "0"
