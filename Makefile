run:
	./_mp_integration/scripts/run_api.sh

ingest:
	python3 ./_mp_integration/merge/ingest_and_stage.py

merge:
	bash ./_mp_integration/merge/merge_into_current.sh

verify:
	curl -s http://127.0.0.1:8000/api/health

run-app:
	uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
