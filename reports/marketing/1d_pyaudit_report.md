# PyAudit Report
- Scanned: 69287
- Errors: 4513

| # | File | Line | Col | Message | Snippet |
|---|------|------|-----|---------|---------|
| 1 | ai_debug_assistant.failed.py | 1 | 69 | unmatched ')' | `Run with trae -' to read from stdin eg. ps aux ¦ grep code ¦ trae -').'` |
| 2 | extract_files_from_paste.py | 61 | 47 | unterminated string literal (detected at line 61) | `""Categorize files by type and priority""""` |
| 3 | go_live_checklist.py | 41 | 48 | unterminated string literal (detected at line 41) | `""Comprehensive golive validation report""""` |
| 4 | monitoring_dashboard.py | 17 | 4 | unterminated string literal (detected at line 17) | `""""` |
| 5 | api_security_compliance.py | 245 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 237 | `}` |
| 6 | real_mcp_ai_assistant.py | 487 | 27 | unterminated string literal (detected at line 487) | `report += f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S',` |
| 7 | fastapi_performance_baseline.py | 273 | 13 | unterminated string literal (detected at line 273) | `f"Successful:         {results.get('successful_requests',` |
| 8 | fix_common_syntax_errors.py | 16 | 15 | unterminated string literal (detected at line 16) | `pattern = r'f"([^"]*{[^}]*\n[^}]*})([^"]*)"` |
| 9 | startup_orchestrator.py | 156 | 29 | unterminated string literal (detected at line 156) | `command=f"python -m uvicorn {service_data.get('module', 'unified_api_router:app')} --host 0.0.0.0 --port {service_data.get('port',` |
| 10 | api_deployment_orchestrator.py | 47 | 1 | invalid syntax | `class DeploymentStage:` |
| 11 | content_automation_pipeline.py | 460 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 446 | `}` |
| 12 | python_syntax_error_fixer.py | 61 | 1 | invalid syntax | `class PythonSyntaxFixer:` |
| 13 | monitoring_system.py | 322 | 25 | unterminated string literal (detected at line 322) | `f"📊 Monitoring Report: {json.dumps(report,` |
| 14 | capabilities_example.py | 45 | 5 | invalid syntax | `def capabilities(self) -> dict:` |
| 15 | database_validator.py | 189 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 180 | `}` |
| 16 | comprehensive_syntax_fixer.py | 44 | 9 | cannot assign to attribute here. Maybe you meant '==' instead of '='? | `self.bracket_pairs = {'(': ')', '[': ']', '{': '}'}` |
| 17 | news_driven_content_trigger.py | 91 | 9 | invalid syntax. Perhaps you forgot a comma? | `self._init_trigger_database()` |
| 18 | create_real_video.py | 37 | 34 | invalid syntax. Perhaps you forgot a comma? | `level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"` |
| 19 | simple_automation_test.py | 23 | 34 | invalid syntax. Perhaps you forgot a comma? | `level = logging.INFO, format="%(asctime)s ¦ %(levelname)s ¦ %(message)s"` |
| 20 | test_avatar_generation.py | 97 | 13 | unterminated string literal (detected at line 97) | `f"📊 Result keys: {result.keys() if isinstance(result,` |
| 21 | api_manager.py | 103 | 21 | unterminated string literal (detected at line 103) | `f"✅ Successfully discovered {result.get('apis_integrated',` |
| 22 | run_api_discovery.py | 520 | 17 | unterminated string literal (detected at line 520) | `f"   • Free APIs: {summary.get('free_apis',` |
| 23 | main_app.py | 703 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 692 | `},` |
| 24 | ai_debug_assistant.py | 52 | 8 | unexpected indent | `error_msg = "sqlite3.OperationalError: no such column: search_keywords"` |
| 25 | api_deployment_orchestrator.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 26 | copy_of_code/launch_live.py | 503 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 496 | `}` |
| 27 | copy_of_code/base_agents.py | 664 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 656 | `}` |
| 28 | copy_of_code/dashboard.py | 2027 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 2020 | `),` |
| 29 | copy_of_code/secrets_cli.py | 101 | 9 | invalid syntax | `except SecretStoreError as e:` |
| 30 | copy_of_code/doctor_creative_env.py | 34 | 16 | closing parenthesis ')' does not match opening parenthesis '[' on line 29 | `text = True).returncode` |
| 31 | copy_of_code/agents/niche_domination_agent.py | 203 | 21 | unterminated string literal (detected at line 203) | `"CREATE INDEX IF NOT EXISTS idx_growth_metrics_channel_niche ON growth_metrics(channel,` |
| 32 | copy_of_code/agents/research_tools.py | 1028 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 1023 | `},` |
| 33 | copy_of_code/agents/strategic_advisor_agent.py | 962 | 29 | unterminated string literal (detected at line 962) | `f"{brief.year}-{self._quarter_to_month(brief.quarter,` |
| 34 | copy_of_code/agents/base_agents.py | 264 | 16 | unterminated string literal (detected at line 264) | `return f"{self.__class__.__name__}(agent_id='{self.agent_id}',` |
| 35 | copy_of_code/agents/content_evolution_agent.py | 226 | 21 | unterminated string literal (detected at line 226) | `"CREATE INDEX IF NOT EXISTS idx_trends_platform_format ON format_trends(platform,` |
| 36 | copy_of_code/agents/specialized_agents.py | 787 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 772 | `}` |
| 37 | copy_of_code/agents/web_automation_tools.py | 1073 | 42 | unterminated string literal (detected at line 1073) | `self.logger.info(f"Retrying action {i + 1},` |
| 38 | copy_of_code/agents/stealth_automation_agent.py | 523 | 17 | unterminated string literal (detected at line 523) | `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,` |
| 39 | copy_of_code/agents/financial_management_agent.py | 1083 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 1061 | `}` |
| 40 | copy_of_code/content/audio_postprod.py | 204 | 13 | did you forget parentheses around the comprehension target? | `"/usr/local/bin/ffmpeg",` |
| 41 | copy_of_code/content/animate_avatar.py | 164 | 56 | invalid syntax. Perhaps you forgot a comma? | `source_image, audio_file, output_path, config` |
| 42 | copy_of_code/content/ai_video_editing.py | 329 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 321 | `}` |
| 43 | copy_of_code/content/blender_compositor.py | 365 | 17 | unterminated string literal (detected at line 365) | `"            start_frame = checkpoint.get('last_frame',` |
| 44 | copy_of_code/content/ai_video_editor.py | 364 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 356 | `}` |
| 45 | copy_of_code/content/audio_post_production.py | 941 | 25 | unterminated string literal (detected at line 941) | `f"Analyzed track '{track.name}': {track_analysis.get('duration',` |
| 46 | tasks/business_automation.py | 645 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 637 | `}` |
| 47 | rewritten/trae_ai_main.py | 35 | 4 | unterminated string literal (detected at line 35) | `""""` |
| 48 | rewritten/extract_files_from_paste.py | 4 | 4 | unterminated string literal (detected at line 4) | `""""` |
| 49 | rewritten/go_live_checklist.py | 6 | 4 | unterminated string literal (detected at line 6) | `""""` |
| 50 | rewritten/environment_config_manager.py | 15 | 4 | unterminated string literal (detected at line 15) | `""""` |
| 51 | rewritten/monitoring_dashboard.py | 17 | 4 | unterminated string literal (detected at line 17) | `""""` |
| 52 | rewritten/api_security_compliance.py | 245 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 237 | `}` |
| 53 | rewritten/test_automation_integration.py | 46 | 1 | invalid syntax | `from tools.basic_video_generator import create_basic_video` |
| 54 | rewritten/real_mcp_ai_assistant.py | 487 | 27 | unterminated string literal (detected at line 487) | `report += f"**Timestamp:** {time.strftime('%Y-%m-%d %H:%M:%S',` |
| 55 | rewritten/fastapi_performance_baseline.py | 273 | 13 | unterminated string literal (detected at line 273) | `f"Successful:         {results.get('successful_requests',` |
| 56 | rewritten/fix_common_syntax_errors.py | 16 | 15 | unterminated string literal (detected at line 16) | `pattern = r'f"([^"]*{[^}]*\n[^}]*})([^"]*)"` |
| 57 | rewritten/startup_orchestrator.py | 156 | 29 | unterminated string literal (detected at line 156) | `command=f"python -m uvicorn {service_data.get('module', 'unified_api_router:app')} --host 0.0.0.0 --port {service_data.get('port',` |
| 58 | rewritten/api_deployment_orchestrator.py | 47 | 1 | invalid syntax | `class DeploymentStage:` |
| 59 | rewritten/content_automation_pipeline.py | 460 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 446 | `}` |
| 60 | rewritten/python_syntax_error_fixer.py | 61 | 1 | invalid syntax | `class PythonSyntaxFixer:` |
| 61 | rewritten/monitoring_system.py | 322 | 25 | unterminated string literal (detected at line 322) | `f"📊 Monitoring Report: {json.dumps(report,` |
| 62 | rewritten/capabilities_example.py | 45 | 5 | invalid syntax | `def capabilities(self) -> dict:` |
| 63 | rewritten/database_validator.py | 189 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 180 | `}` |
| 64 | rewritten/comprehensive_syntax_fixer.py | 46 | 9 | cannot assign to attribute here. Maybe you meant '==' instead of '='? | `self.bracket_pairs = {'(': ')', '[': ']', '{': '}'}` |
| 65 | rewritten/news_driven_content_trigger.py | 91 | 9 | invalid syntax. Perhaps you forgot a comma? | `self._init_trigger_database()` |
| 66 | rewritten/create_real_video.py | 37 | 34 | invalid syntax. Perhaps you forgot a comma? | `level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"` |
| 67 | rewritten/simple_automation_test.py | 23 | 34 | invalid syntax. Perhaps you forgot a comma? | `level = logging.INFO, format="%(asctime)s ¦ %(levelname)s ¦ %(message)s"` |
| 68 | rewritten/test_avatar_generation.py | 97 | 13 | unterminated string literal (detected at line 97) | `f"📊 Result keys: {result.keys() if isinstance(result,` |
| 69 | rewritten/api_manager.py | 103 | 21 | unterminated string literal (detected at line 103) | `f"✅ Successfully discovered {result.get('apis_integrated',` |
| 70 | rewritten/run_api_discovery.py | 520 | 17 | unterminated string literal (detected at line 520) | `f"   • Free APIs: {summary.get('free_apis',` |
| 71 | rewritten/main_app.py | 703 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 692 | `},` |
| 72 | rewritten/ai_debug_assistant.py | 52 | 8 | unexpected indent | `error_msg = "sqlite3.OperationalError: no such column: search_keywords"` |
| 73 | rewritten/tasks/document_processing.py | 111 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 103 | `}` |
| 74 | rewritten/tasks/business_automation.py | 645 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 637 | `}` |
| 75 | rewritten/tools/basic_video_generator.py | 79 | 5 | invalid syntax | `else:` |
| 76 | rewritten/tools/cleanup/unused_scan.py | 36 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `logger = logging.getLogger(__name__)` |
| 77 | rewritten/monetization_bundle/main.py | 70 | 1 | invalid syntax | `from sqlalchemy.ext.declarative import declarative_base` |
| 78 | rewritten/app/dashboard_integration.py | 194 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 182 | `}` |
| 79 | rewritten/app/bridge_to_system.py | 237 | 21 | unterminated string literal (detected at line 237) | `f"Loaded {` |
| 80 | rewritten/app/dashboard.py | 378 | 17 | unterminated string literal (detected at line 378) | `f"[actions] manifest updated after agent registration: {` |
| 81 | rewritten/app/system_smoke_test_agent.py | 185 | 17 | unterminated string literal (detected at line 185) | `f"Checking {` |
| 82 | rewritten/app/ai_integrated_dashboard.py | 90 | 21 | unterminated string literal (detected at line 91) | `logger.info("Using browser automation for ChatGPT, Gemini, \` |
| 83 | rewritten/app/websocket_manager.py | 28 | 13 | unterminated string literal (detected at line 28) | `f"WebSocket connected: {` |
| 84 | rewritten/frontend/media_dashboard.py | 670 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 640 | `}` |
| 85 | rewritten/master_orchestrator/business_generators.py | 232 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 211 | `}` |
| 86 | rewritten/deploy/production_config.py | 83 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `missing_vars = []` |
| 87 | rewritten/agents/strategic_advisor_agent.py | 944 | 25 | unterminated string literal (detected at line 944) | `f"{brief.year}-{self._quarter_to_month(brief.quarter,` |
| 88 | rewritten/agents/specialized_agents.py | 789 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 774 | `}` |
| 89 | rewritten/agents/web_automation_tools.py | 1073 | 42 | unterminated string literal (detected at line 1073) | `self.logger.info(f"Retrying action {i + 1},` |
| 90 | rewritten/agents/stealth_automation_agent.py | 523 | 17 | unterminated string literal (detected at line 523) | `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,` |
| 91 | rewritten/backend/zero_cost_stack.py | 201 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 191 | `),` |
| 92 | rewritten/backend/youtube_scheduler.py | 211 | 5 | invalid syntax | `def _load_config(self) -> Dict[str, Any]:` |
| 93 | rewritten/backend/payment_processor.py | 866 | 22 | unterminated string literal (detected at line 866) | `attempt_id = f"att_{int(time.time() * 1000000)}_{hash(payment_id) % 10000}_{random.randint(1000,` |
| 94 | rewritten/backend/youtube_engagement_automation.py | 586 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 579 | `}` |
| 95 | rewritten/backend/m1_optimizer.py | 150 | 24 | invalid syntax. Perhaps you forgot a comma? | `thread_name_prefix="M1 - Perf"` |
| 96 | rewritten/backend/rule1_scanner.py | 159 | 17 | invalid syntax. Perhaps you forgot a comma? | `"""` |
| 97 | rewritten/backend/revenue_streams_api.py | 326 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 313 | `},` |
| 98 | rewritten/backend/routers/chat.py | 255 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 244 | `},` |
| 99 | rewritten/backend/core/database_production.py | 32 | 8 | unexpected indent | `from psycopg2.pool import ThreadedConnectionPool` |
| 100 | rewritten/backend/security/security_scanner.py | 99 | 80 | closing parenthesis ']' does not match opening parenthesis '{' on line 98 | `"pattern": r'(?i)(database[_-]?url¦db[_-]?url)\\s*[=:]\\s*["\\']?(postgresql¦mysql¦mongodb)://[^\\s"\\'>]+["\\']?',` |
| 101 | rewritten/backend/security/compliance_validator.py | 92 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 78 | `}` |
| 102 | rewritten/backend/integration/master_control_system.py | 386 | 42 | unterminated string literal (detected at line 386) | `logging.getLogger(__name__).info(f"Received signal {signum},` |
| 103 | rewritten/backend/agents/strategic_advisor_agent.py | 961 | 25 | unterminated string literal (detected at line 961) | `f"{brief.year}-{self._quarter_to_month(brief.quarter,` |
| 104 | rewritten/backend/agents/system_agent.py | 39 | 5 | invalid syntax | `from app.actions import dashboard_action` |
| 105 | rewritten/backend/content/evidence_based_scripting.py | 48 | 5 | invalid syntax | `def _validate_protected_channel(self):` |
| 106 | rewritten/backend/content/audio_postprod.py | 204 | 13 | did you forget parentheses around the comprehension target? | `"/usr/local/bin/ffmpeg",` |
| 107 | rewritten/backend/content/blender_compositor.py | 864 | 17 | unterminated string literal (detected at line 864) | `"            start_frame = checkpoint.get('last_frame',` |
| 108 | rewritten/backend/content/ai_video_editor.py | 364 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 356 | `}` |
| 109 | rewritten/backend/content/automated_author.py | 293 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 286 | `),` |
| 110 | rewritten/backend/content/vidscript_pro.py | 311 | 34 | unterminated string literal (detected at line 311) | `live_briefing += f"• {trend.get('topic', 'Unknown')}: {trend.get('momentum_score',` |
| 111 | rewritten/backend/content/relentless_optimization.py | 1094 | 17 | unterminated string literal (detected at line 1094) | `f"Generated optimization report with {report.get('active_tests',` |
| 112 | rewritten/backend/content/audio_post_production.py | 926 | 25 | unterminated string literal (detected at line 926) | `f"Analyzed track '{track.name}': {track_analysis.get('duration',` |
| 113 | rewritten/backend/pipelines/blender_scripts/avatar_creator.py | 28 | 28 | invalid syntax. Perhaps you forgot a comma? | `size = 1, location=(location[0], location[1], location[2] + 1)` |
| 114 | rewritten/backend/dashboard/actions_bus.py | 40 | 29 | unterminated string literal (detected at line 40) | `"endpoint": f"/api/action/{getattr(fn, '_agent_pretty',` |
| 115 | rewritten/backend/integrations/reddit_integration.py | 32 | 5 | invalid syntax | `def ready(self) -> bool:` |
| 116 | rewritten/backend/integrations/obs_automation.py | 171 | 8 | unexpected indent | `start_time: Optional[str] = None` |
| 117 | rewritten/backend/integrations/pinterest_integration.py | 17 | 19 | '(' was never closed | `return cls(` |
| 118 | rewritten/backend/integrations/audacity_automation.py | 55 | 9 | invalid syntax. Perhaps you forgot a comma? | `"Warning: Audio processing libraries not available. Install with: pip install librosa soundfile numpy"` |
| 119 | rewritten/backend/integrations/twitter_integration.py | 248 | 23 | unterminated string literal (detected at line 248) | `base_string = f"{method.upper()}&{urllib.parse.quote(url,` |
| 120 | rewritten/backend/monitoring/alert_manager.py | 275 | 29 | closing parenthesis '}' does not match opening parenthesis '[' on line 269 | `}` |
| 121 | rewritten/backend/services/web_search_service.py | 112 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 104 | `}` |
| 122 | rewritten/backend/services/stress_tester.py | 50 | 1 | invalid syntax | `from .health_monitor import HealthMonitor, get_health_monitor` |
| 123 | rewritten/backend/services/auto_discovery_service.py | 780 | 17 | unterminated string literal (detected at line 780) | `f"Estimated Monthly Cost: ${result.cost_analysis.get('estimated_monthly_cost',` |
| 124 | rewritten/backend/services/performance_monitor.py | 720 | 17 | unterminated string literal (detected at line 720) | `"CREATE INDEX IF NOT EXISTS idx_metrics_name_timestamp ON performance_metrics(name,` |
| 125 | rewritten/backend/services/health_monitor.py | 1033 | 33 | closing parenthesis '}' does not match opening parenthesis '(' on line 1020 | `}` |
| 126 | rewritten/backend/services/automated_model_generator.py | 155 | 12 | unexpected indent | `elif self.state == "half - open":` |
| 127 | rewritten/backend/services/api_integration_service.py | 242 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 227 | `),` |
| 128 | rewritten/backend/services/redundancy_manager.py | 633 | 17 | unterminated string literal (detected at line 633) | `f"Hybrid backend '{self.config.name}' initialized (local: {local_ok},` |
| 129 | rewritten/models/linly_talker/webui.py | 1275 | 47 | unterminated string literal (detected at line 1275) | `label="Still Mode (fewer head motion,` |
| 130 | rewritten/models/linly_talker/app_multi.py | 41 | 4 | unexpected indent | `maximum = 45,` |
| 131 | rewritten/models/linly_talker/one_button_test.py | 85 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 67 | `}` |
| 132 | rewritten/models/linly_talker/app_musetalk.py | 57 | 5 | invalid syntax | `except Exception:` |
| 133 | rewritten/models/linly_talker/app.py | 48 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `exp_weight = 1` |
| 134 | rewritten/models/linly_talker/png_avatar_processor.py | 112 | 52 | invalid syntax. Perhaps you forgot a comma? | `processed_image, enhance = True` |
| 135 | rewritten/models/linly_talker/app_img.py | 317 | 47 | unterminated string literal (detected at line 317) | `label="Still Mode (fewer head motion,` |
| 136 | rewritten/models/linly_talker/app_vits.py | 50 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `exp_weight = 1` |
| 137 | rewritten/models/linly_talker/NeRF/data_utils/wav2mel_hparams.py | 35 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 138 | rewritten/models/linly_talker/NeRF/data_utils/process.py | 58 | 5 | invalid syntax | `except Exception:` |
| 139 | rewritten/models/linly_talker/NeRF/data_utils/hubert.py | 26 | 54 | invalid syntax. Perhaps you forgot a comma? | `speech, return_tensors="pt", sampling_rate = 16000` |
| 140 | rewritten/models/linly_talker/NeRF/data_utils/face_tracking/render_3dmm.py | 66 | 19 | unterminated string literal (detected at line 66) | `msg = "Cameras must be specified either at initialization \\` |
| 141 | rewritten/models/linly_talker/NeRF/data_utils/face_tracking/face_tracker.py | 25 | 58 | invalid syntax. Perhaps you forgot a comma? | `"--path", type = str, default="obama/ori_imgs", help="idname of target person"` |
| 142 | rewritten/models/linly_talker/NeRF/nerf_triplane/provider.py | 24 | 1 | invalid syntax | `def nerf_matrix_to_ngp(pose, scale = 0.33, offset=[0, 0, 0]):` |
| 143 | rewritten/models/linly_talker/NeRF/nerf_triplane/renderer.py | 871 | 48 | invalid decimal literal | `max={self.density_grid_torso.max().item():.4f},` |
| 144 | rewritten/models/linly_talker/NeRF/nerf_triplane/asr.py | 68 | 47 | invalid decimal literal | `latency should be (ctx + stride_right) * 20ms` |
| 145 | rewritten/models/linly_talker/NeRF/nerf_triplane/utils.py | 1449 | 19 | closing parenthesis '}' does not match opening parenthesis '(' on line 1375 | `f"{name}.mp4")} -i {self.opt.aud} -strict -2 {os.path.join(save_path,` |
| 146 | rewritten/models/linly_talker/NeRF/nerf_triplane/network.py | 397 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 387 | `),` |
| 147 | rewritten/models/linly_talker/NeRF/nerf_triplane/wav2vec.py | 68 | 47 | invalid decimal literal | `latency should be (ctx + stride_right) * 20ms` |
| 148 | rewritten/models/linly_talker/NeRF/nerf_triplane/gui.py | 25 | 6 | unmatched ']' | `0], [0, -1,` |
| 149 | rewritten/models/linly_talker/NeRF/gridencoder/grid.py | 70 | 9 | invalid syntax | `else:` |
| 150 | rewritten/models/linly_talker/VITS/GPT_SoVITS.py | 607 | 15 | closing parenthesis ')' does not match opening parenthesis '[' on line 582 | `0) * 32768).astype(` |
| 151 | rewritten/models/linly_talker/VITS/XTTS.py | 27 | 39 | invalid syntax. Perhaps you forgot a comma? | `get_user_data_dir("tts"), model_name.replace("/", "--")` |
| 152 | rewritten/models/linly_talker/Musetalk/musetalk/utils/preprocessing.py | 99 | 18 | unterminated string literal (detected at line 99) | `text_range = f"Total frame:「{len(frames)}」 Manually adjust range : [ -{int(sum(average_range_minus)/len(average_range_minus))}~{int(sum(average_range_plus)/len(average_range_plus))} ] ,` |
| 153 | rewritten/models/linly_talker/Musetalk/musetalk/utils/face_detection/api.py | 93 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.face_detector = face_detector_module.FaceDetector(` |
| 154 | rewritten/models/linly_talker/Musetalk/musetalk/utils/face_detection/detection/sfd/sfd_detector.py | 28 | 12 | unexpected indent | `if not os.path.isfile(path_to_detector):` |
| 155 | rewritten/models/linly_talker/Musetalk/musetalk/models/vae.py | 41 | 12 | unexpected indent | `self.transform = transforms.Normalize(mean=[0.5,` |
| 156 | rewritten/models/linly_talker/Musetalk/musetalk/whisper/whisper/decoding.py | 45 | 13 | invalid syntax. Perhaps you forgot a comma? | `f"This model doesn't have language tokens so it can't perform lang id"` |
| 157 | rewritten/models/linly_talker/Musetalk/musetalk/whisper/whisper/model.py | 49 | 1 | invalid syntax | `class Conv1d(nn.Conv1d):` |
| 158 | rewritten/models/linly_talker/Musetalk/musetalk/whisper/whisper/tokenizer.py | 290 | 75 | invalid character '♪' (U+266A) | `"<< >> <<< >>> -- --- -( -[ (' (\\" (( )) ((( ))) [[ ]] {{ }} ♪♪ ♪♪♪".split()` |
| 159 | rewritten/models/linly_talker/Musetalk/musetalk/whisper/whisper/utils.py | 92 | 13 | unterminated string literal (detected at line 92) | `f"{format_timestamp(segment['start'],` |
| 160 | rewritten/models/linly_talker/Musetalk/musetalk/whisper/whisper/transcribe.py | 258 | 18 | unterminated string literal (detected at line 258) | `help="optional patience value to use in beam decoding,` |
| 161 | rewritten/models/linly_talker/Musetalk/musetalk/whisper/whisper/normalizers/english.py | 58 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 31 | `}` |
| 162 | rewritten/models/linly_talker/Musetalk/scripts/realtime_inference.py | 175 | 21 | unterminated string literal (detected at line 175) | `f" 【bbox_shift】 is changed,` |
| 163 | rewritten/models/linly_talker/LLM/Llama2Chinese.py | 51 | 28 | invalid syntax. Perhaps you forgot a comma? | `model_vocab_size = base_model.get_input_embeddings().weight.size(0)` |
| 164 | rewritten/models/linly_talker/LLM/Qwen2.py | 31 | 78 | invalid syntax. Perhaps you forgot a comma? | `path, device_map="auto", torch_dtype="auto", trust_remote_code = True` |
| 165 | rewritten/models/linly_talker/Qwen/Qwen-1_8B-Chat/cpp_kernels.py | 13 | 14 | invalid syntax. Perhaps you forgot a comma? | `output = raw_output.split()` |
| 166 | rewritten/models/linly_talker/Qwen/Qwen-1_8B-Chat/tokenization_qwen.py | 96 | 33 | unterminated string literal (detected at line 96) | `logger.info(f'the index {index} for extra token {token} exists,` |
| 167 | rewritten/models/linly_talker/Qwen/Qwen-1_8B-Chat/modeling_qwen.py | 31 | 1 | invalid syntax | `from transformers.modeling_utils import PreTrainedModel` |
| 168 | rewritten/models/linly_talker/TFG/MuseTalk.py | 35 | 1 | invalid syntax | `from musetalk.utils.preprocessing import (coord_placeholder, get_bbox_range,` |
| 169 | rewritten/models/linly_talker/TFG/SadTalker.py | 51 | 60 | invalid syntax. Perhaps you forgot a comma? | `checkpoint_path, self.config_path, 256, False, "crop"` |
| 170 | rewritten/models/linly_talker/TFG/Wav2Lipv2.py | 46 | 6 | invalid syntax | `torch.manual_seed(1234)` |
| 171 | rewritten/models/linly_talker/TFG/Wav2Lip.py | 43 | 70 | invalid syntax. Perhaps you forgot a comma? | `checkpoint_path, map_location = lambda storage, loc: storage` |
| 172 | rewritten/models/linly_talker/TFG/MuseV.py | 53 | 50 | unexpected character after line continuation character | `from musev.models.ip_adapter_face_loader import \\` |
| 173 | rewritten/models/linly_talker/TTS/XTTS.py | 20 | 44 | '(' was never closed | `tempf = tempfile.NamedTemporaryFile(` |
| 174 | rewritten/models/linly_talker/GPT_SoVITS/s1_train.py | 94 | 1 | invalid syntax | `def main(args):` |
| 175 | rewritten/models/linly_talker/GPT_SoVITS/inference_webui.py | 38 | 1 | invalid syntax | `if os.path.exists("./sweight.txt"):` |
| 176 | rewritten/models/linly_talker/GPT_SoVITS/utils.py | 331 | 13 | unterminated string literal (detected at line 331) | `"{} is not a git repository,` |
| 177 | rewritten/models/linly_talker/GPT_SoVITS/s2_train.py | 728 | 21 | closing parenthesis '}' does not match opening parenthesis '(' on line 723 | `}` |
| 178 | rewritten/models/linly_talker/GPT_SoVITS/prepare_datasets/3-get-semantic.py | 64 | 23 | invalid syntax | `if is_half is True:` |
| 179 | rewritten/models/linly_talker/GPT_SoVITS/module/models.py | 43 | 17 | invalid syntax. Perhaps you forgot a comma? | `modules.ConvFlow(2, filter_channels, kernel_size, n_layers = 3)` |
| 180 | rewritten/models/linly_talker/GPT_SoVITS/module/models_onnx.py | 44 | 17 | invalid syntax. Perhaps you forgot a comma? | `modules.ConvFlow(2, filter_channels, kernel_size, n_layers = 3)` |
| 181 | rewritten/models/linly_talker/GPT_SoVITS/module/quantize.py | 22 | 8 | unexpected indent | `codes: torch.Tensor` |
| 182 | rewritten/models/linly_talker/GPT_SoVITS/AR/models/t2s_model.py | 10 | 1 | invalid syntax | `from AR.modules.embedding import SinePositionalEmbedding, TokenEmbedding` |
| 183 | rewritten/models/linly_talker/GPT_SoVITS/AR/modules/scaling.py | 71 | 38 | invalid syntax | `if __name__ == "__main__":` |
| 184 | rewritten/models/linly_talker/GPT_SoVITS/AR/modules/patched_mha_with_cache.py | 390 | 5 | unterminated string literal (detected at line 390) | `f"expecting static_k.size(0) of {bsz * num_heads},` |
| 185 | rewritten/models/linly_talker/GPT_SoVITS/AR/modules/activation_onnx.py | 61 | 21 | invalid syntax. Perhaps you forgot a comma? | `torch.empty((embed_dim, embed_dim), **factory_kwargs)` |
| 186 | rewritten/models/linly_talker/GPT_SoVITS/AR/modules/activation.py | 403 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 397 | `):` |
| 187 | rewritten/models/linly_talker/GPT_SoVITS/AR/modules/optim.py | 500 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 493 | `}` |
| 188 | rewritten/models/linly_talker/GPT_SoVITS/AR/data/dataset.py | 36 | 13 | invalid syntax. Perhaps you forgot a comma? | `[(0, 0)] * axis + [(0, max_length - length)] + [(0, 0)] * (ndim - axis - 1)` |
| 189 | rewritten/models/linly_talker/GPT_SoVITS/feature_extractor/cnhubert.py | 32 | 5 | invalid syntax | `def forward(self, x):` |
| 190 | rewritten/models/linly_talker/face_detection/detection/sfd/sfd_detector.py | 28 | 12 | unexpected indent | `if not os.path.isfile(path_to_detector):` |
| 191 | rewritten/models/linly_talker/src/hparams.py | 35 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 192 | rewritten/models/linly_talker/src/test_audio2coeff.py | 53 | 13 | invalid syntax | `else:` |
| 193 | rewritten/models/linly_talker/src/facerender/animate.py | 321 | 56 | closing parenthesis ')' does not match opening parenthesis '[' on line 309 | `int(img_size * original_size[1]/original_size[0]) )),` |
| 194 | rewritten/models/linly_talker/src/facerender/pirender_animate.py | 42 | 66 | invalid syntax. Perhaps you forgot a comma? | `checkpoint_path, map_location = lambda storage, loc: storage` |
| 195 | rewritten/models/linly_talker/src/facerender/modules/keypoint_detector.py | 9 | 1 | invalid syntax | `from src.facerender.sync_batchnorm import SynchronizedBatchNorm2d as BatchNorm2d` |
| 196 | rewritten/models/linly_talker/src/facerender/modules/make_animation.py | 34 | 41 | invalid syntax. Perhaps you forgot a comma? | `kp_driving["jacobian"], torch.inverse(kp_driving_initial["jacobian"])` |
| 197 | rewritten/models/linly_talker/src/facerender/modules/util.py | 77 | 85 | invalid syntax. Perhaps you forgot a comma? | `in_channels = in_features, out_channels = in_features//4, kernel_size = 1` |
| 198 | rewritten/models/linly_talker/src/facerender/modules/dense_motion.py | 33 | 8 | unexpected indent | `self.hourglass = Hourglass(` |
| 199 | rewritten/models/linly_talker/src/facerender/modules/generator.py | 10 | 1 | invalid syntax | `from torch import nn` |
| 200 | rewritten/models/linly_talker/src/utils/croper.py | 77 | 10 | invalid syntax | `x/= np.hypot(` |
| 201 | rewritten/models/linly_talker/src/utils/hparams.py | 39 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 202 | rewritten/models/linly_talker/src/utils/face_enhancer.py | 32 | 5 | invalid syntax | `return list(gen)` |
| 203 | rewritten/models/linly_talker/src/utils/model2safetensor.py | 21 | 1 | invalid syntax | `from src.facerender.modules.keypoint_detector import HEEstimator, KPDetector` |
| 204 | rewritten/models/linly_talker/src/utils/utils.py | 15 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dtype = np.float32,` |
| 205 | rewritten/models/linly_talker/src/utils/hparamsv2.py | 35 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 206 | rewritten/models/linly_talker/src/models/wav2lip.py | 264 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 161 | `)  # 96,96` |
| 207 | rewritten/models/linly_talker/src/face3d/util/nvdiffrast.py | 42 | 14 | unmatched ')' | `f = zfar)).matmul(` |
| 208 | rewritten/models/linly_talker/src/face3d/models/bfm.py | 24 | 1 | invalid syntax | `class SH:` |
| 209 | rewritten/models/linly_talker/src/face3d/models/base_model.py | 49 | 13 | unmatched ')' | `opt.name)  # save all the checkpoints to save_dir` |
| 210 | rewritten/models/linly_talker/src/face3d/models/facerecon_model.py | 16 | 1 | invalid syntax | `from src.face3d.util import util` |
| 211 | rewritten/models/linly_talker/src/face3d/models/arcface_torch/eval_ijbc.py | 40 | 50 | invalid syntax. Perhaps you forgot a comma? | `"--target", default="IJBC", type = str, help="target, set to IJBC or IJBB"` |
| 212 | rewritten/models/linly_talker/src/face3d/models/arcface_torch/dataset.py | 20 | 12 | unexpected indent | `self.local_rank = local_rank` |
| 213 | rewritten/models/linly_talker/src/face3d/models/arcface_torch/onnx_ijbc.py | 26 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dtype = np.float32,` |
| 214 | rewritten/models/linly_talker/src/face3d/models/arcface_torch/partial_fc.py | 74 | 13 | invalid syntax. Perhaps you forgot a comma? | `rank < num_classes % world_size` |
| 215 | rewritten/models/linly_talker/src/face3d/models/arcface_torch/utils/utils_amp.py | 25 | 12 | unexpected indent | `self._per_device_tensors: Dict[torch.device, torch.Tensor] = {}` |
| 216 | rewritten/models/linly_talker/src/face3d/models/arcface_torch/eval/verification.py | 92 | 45 | invalid syntax. Perhaps you forgot a comma? | `threshold, dist[train_set], actual_issame[train_set]` |
| 217 | rewritten/models/linly_talker/src/face3d/data/template_dataset.py | 69 | 26 | unmatched ')' | `opt.max_dataset_size)) to get all the image paths under the directory self.root` |
| 218 | rewritten/models/linly_talker/src/audio2pose_models/discriminator.py | 39 | 13 | invalid syntax | `if norm == "BN":` |
| 219 | rewritten/models/linly_talker/src/audio2pose_models/audio_encoder.py | 14 | 65 | invalid syntax. Perhaps you forgot a comma? | `nn.Conv2d(cin, cout, kernel_size, stride, padding), nn.BatchNorm2d(cout)` |
| 220 | rewritten/scripts/environment_validator.py | 109 | 27 | unterminated string literal (detected at line 109) | `version_str = f"{` |
| 221 | rewritten/scripts/system_orchestrator.py | 200 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 190 | `},` |
| 222 | rewritten/scripts/generate_realistic_avatar.py | 100 | 25 | unterminated string literal (detected at line 100) | `f"Unusual aspect ratio {` |
| 223 | rewritten/scripts/repair-model-generation.py | 92 | 21 | unterminated string literal (detected at line 92) | `f"Only {` |
| 224 | rewritten/scripts/load-test.py | 634 | 17 | unterminated string literal (detected at line 634) | `f"  Avg Response Time: {` |
| 225 | rewritten/scripts/go_live_preparation.py | 31 | 13 | invalid syntax. Perhaps you forgot a comma? | `logging.StreamHandler()` |
| 226 | rewritten/scripts/security_audit.py | 82 | 77 | closing parenthesis ']' does not match opening parenthesis '{' on line 74 | `"generic_secret": r'(secret¦password¦token¦key)\\s*[=:]\\s*["\\'][a-zA-Z0-9_\\-\\.]{8,}["\\']',` |
| 227 | rewritten/scripts/synthesize_release_v3.py | 177 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 169 | `}` |
| 228 | rewritten/scripts/production_deployment.py | 53 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `logger = logging.getLogger(__name__)` |
| 229 | rewritten/scripts/security_scanner.py | 102 | 71 | closing parenthesis ']' does not match opening parenthesis '{' on line 101 | `"pattern": r'(?i)(api[_-]?key¦apikey)\\s*[=:]\\s*["\\']?([a - zA - Z0 - 9_\\-]{20,})["\\']?',` |
| 230 | rewritten/scripts/start_distributed_system.py | 39 | 1 | invalid syntax | `class DistributedSystemOrchestrator:` |
| 231 | rewritten/scripts/deployment_orchestrator.py | 812 | 21 | unterminated string literal (detected at line 812) | `f"High response time detected: {` |
| 232 | rewritten/scripts/secrets_cli.py | 183 | 84 | invalid syntax. Perhaps you forgot a comma? | `secret["created_at"][:19] if secret["created_at"] else "N/A"` |
| 233 | rewritten/scripts/doctor_creative_env.py | 134 | 13 | unterminated string literal (detected at line 134) | `f"Failed to install dependencies. pip exited with status {` |
| 234 | data_persistence/world_bible.py | 209 | 17 | unterminated string literal (detected at line 209) | `"CREATE INDEX IF NOT EXISTS idx_trends_niche_source ON trends (niche_id,` |
| 235 | app/dashboard_integration.py | 194 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 182 | `}` |
| 236 | app/dashboard.py | 714 | 29 | closing parenthesis '}' does not match opening parenthesis '[' on line 706 | `}` |
| 237 | app/system_smoke_test_agent.py | 185 | 17 | unterminated string literal (detected at line 185) | `f"Checking {` |
| 238 | app/ai_integrated_dashboard.py | 90 | 21 | unterminated string literal (detected at line 91) | `logger.info("Using browser automation for ChatGPT, Gemini, \` |
| 239 | app/websocket_manager.py | 28 | 13 | unterminated string literal (detected at line 28) | `f"WebSocket connected: {` |
| 240 | frontend/media_dashboard.py | 670 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 640 | `}` |
| 241 | master_orchestrator/business_generators.py | 232 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 211 | `}` |
| 242 | deploy/production_config.py | 83 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `missing_vars = []` |
| 243 | tests/test_ai_benchmark_integration.py | 29 | 1 | invalid syntax | `class TestAIBenchmarkIntegration:` |
| 244 | tests/end_to_end_verification.py | 773 | 72 | unterminated string literal (detected at line 773) | `r'api[_-]?key[\\s]*[=:][\\s]*["\\'][a-zA-Z0-9+/=]{10,}["\\']',` |
| 245 | agents/specialized_agents.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 246 | agents/research_tools.py | 1028 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 1023 | `},` |
| 247 | agents/strategic_advisor_agent.py | 944 | 25 | unterminated string literal (detected at line 944) | `f"{brief.year}-{self._quarter_to_month(brief.quarter,` |
| 248 | agents/research_tools.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 249 | agents/specialized_agents.py | 789 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 774 | `}` |
| 250 | agents/stealth_automation_agent.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 251 | agents/web_automation_tools.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 252 | agents/web_automation_tools.py | 1073 | 42 | unterminated string literal (detected at line 1073) | `self.logger.info(f"Retrying action {i + 1},` |
| 253 | agents/stealth_automation_agent.py | 523 | 17 | unterminated string literal (detected at line 523) | `"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,` |
| 254 | backend/zero_cost_stack.py | 201 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 191 | `),` |
| 255 | backend/youtube_scheduler.py | 211 | 5 | invalid syntax | `def _load_config(self) -> Dict[str, Any]:` |
| 256 | backend/youtube_engagement_automation.py | 586 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 579 | `}` |
| 257 | backend/rule1_scanner.py | 312 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 299 | `}` |
| 258 | backend/revenue_streams_api.py | 326 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 313 | `},` |
| 259 | backend/core/database_production.py | 32 | 8 | unexpected indent | `from psycopg2.pool import ThreadedConnectionPool` |
| 260 | backend/security/security_scanner.py | 99 | 80 | closing parenthesis ']' does not match opening parenthesis '{' on line 98 | `"pattern": r'(?i)(database[_-]?url¦db[_-]?url)\\s*[=:]\\s*["\\']?(postgresql¦mysql¦mongodb)://[^\\s"\\'>]+["\\']?',` |
| 261 | backend/security/compliance_validator.py | 92 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 78 | `}` |
| 262 | backend/integration/master_control_system.py | 386 | 42 | unterminated string literal (detected at line 386) | `logging.getLogger(__name__).info(f"Received signal {signum},` |
| 263 | backend/agents/strategic_advisor_agent.py | 961 | 25 | unterminated string literal (detected at line 961) | `f"{brief.year}-{self._quarter_to_month(brief.quarter,` |
| 264 | backend/content/evidence_based_scripting.py | 48 | 5 | invalid syntax | `def _validate_protected_channel(self):` |
| 265 | backend/content/audio_postprod.py | 204 | 13 | did you forget parentheses around the comprehension target? | `"/usr/local/bin/ffmpeg",` |
| 266 | backend/content/blender_compositor.py | 864 | 17 | unterminated string literal (detected at line 864) | `"            start_frame = checkpoint.get('last_frame',` |
| 267 | backend/content/ai_video_editor.py | 364 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 356 | `}` |
| 268 | backend/content/automated_author.py | 293 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 286 | `),` |
| 269 | backend/content/relentless_optimization.py | 1094 | 17 | unterminated string literal (detected at line 1094) | `f"Generated optimization report with {report.get('active_tests',` |
| 270 | backend/content/audio_post_production.py | 926 | 25 | unterminated string literal (detected at line 926) | `f"Analyzed track '{track.name}': {track_analysis.get('duration',` |
| 271 | backend/pipelines/blender_scripts/avatar_creator.py | 28 | 28 | invalid syntax. Perhaps you forgot a comma? | `size = 1, location=(location[0], location[1], location[2] + 1)` |
| 272 | backend/dashboard/actions_bus.py | 40 | 29 | unterminated string literal (detected at line 40) | `"endpoint": f"/api/action/{getattr(fn, '_agent_pretty',` |
| 273 | backend/integrations/obs_automation.py | 171 | 8 | unexpected indent | `start_time: Optional[str] = None` |
| 274 | backend/integrations/audacity_automation.py | 55 | 9 | invalid syntax. Perhaps you forgot a comma? | `"Warning: Audio processing libraries not available. Install with: pip install librosa soundfile numpy"` |
| 275 | backend/integrations/twitter_integration.py | 248 | 23 | unterminated string literal (detected at line 248) | `base_string = f"{method.upper()}&{urllib.parse.quote(url,` |
| 276 | backend/scrapers/news_scraper.py | 37 | 33 | unterminated string literal (detected at line 37) | `"User - Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML,` |
| 277 | backend/scrapers/youtube_scraper.py | 35 | 33 | unterminated string literal (detected at line 35) | `"User - Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML,` |
| 278 | backend/monitoring/alert_manager.py | 275 | 29 | closing parenthesis '}' does not match opening parenthesis '[' on line 269 | `}` |
| 279 | backend/services/web_search_service.py | 112 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 104 | `}` |
| 280 | backend/services/stress_tester.py | 50 | 1 | invalid syntax | `from .health_monitor import HealthMonitor, get_health_monitor` |
| 281 | backend/services/auto_discovery_service.py | 780 | 17 | unterminated string literal (detected at line 780) | `f"Estimated Monthly Cost: ${result.cost_analysis.get('estimated_monthly_cost',` |
| 282 | backend/services/performance_monitor.py | 720 | 17 | unterminated string literal (detected at line 720) | `"CREATE INDEX IF NOT EXISTS idx_metrics_name_timestamp ON performance_metrics(name,` |
| 283 | backend/services/health_monitor.py | 1033 | 33 | closing parenthesis '}' does not match opening parenthesis '(' on line 1020 | `}` |
| 284 | backend/services/automated_model_generator.py | 155 | 12 | unexpected indent | `elif self.state == "half - open":` |
| 285 | backend/services/api_integration_service.py | 242 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 227 | `),` |
| 286 | backend/services/redundancy_manager.py | 633 | 17 | unterminated string literal (detected at line 633) | `f"Hybrid backend '{self.config.name}' initialized (local: {local_ok},` |
| 287 | models/linly_talker/webui.py | 1275 | 47 | unterminated string literal (detected at line 1275) | `label="Still Mode (fewer head motion,` |
| 288 | models/linly_talker/app_multi.py | 41 | 4 | unexpected indent | `maximum = 45,` |
| 289 | models/linly_talker/one_button_test.py | 85 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 67 | `}` |
| 290 | models/linly_talker/app_musetalk.py | 57 | 5 | invalid syntax | `except Exception:` |
| 291 | models/linly_talker/app.py | 48 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `exp_weight = 1` |
| 292 | models/linly_talker/png_avatar_processor.py | 112 | 52 | invalid syntax. Perhaps you forgot a comma? | `processed_image, enhance = True` |
| 293 | models/linly_talker/app_img.py | 317 | 47 | unterminated string literal (detected at line 317) | `label="Still Mode (fewer head motion,` |
| 294 | models/linly_talker/app_vits.py | 50 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `exp_weight = 1` |
| 295 | models/linly_talker/NeRF/data_utils/wav2mel_hparams.py | 35 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 296 | models/linly_talker/NeRF/data_utils/process.py | 58 | 5 | invalid syntax | `except Exception:` |
| 297 | models/linly_talker/NeRF/data_utils/hubert.py | 26 | 54 | invalid syntax. Perhaps you forgot a comma? | `speech, return_tensors="pt", sampling_rate = 16000` |
| 298 | models/linly_talker/NeRF/data_utils/face_tracking/render_3dmm.py | 66 | 19 | unterminated string literal (detected at line 66) | `msg = "Cameras must be specified either at initialization \\` |
| 299 | models/linly_talker/NeRF/data_utils/face_tracking/face_tracker.py | 25 | 58 | invalid syntax. Perhaps you forgot a comma? | `"--path", type = str, default="obama/ori_imgs", help="idname of target person"` |
| 300 | models/linly_talker/NeRF/nerf_triplane/provider.py | 24 | 1 | invalid syntax | `def nerf_matrix_to_ngp(pose, scale = 0.33, offset=[0, 0, 0]):` |
| 301 | models/linly_talker/NeRF/nerf_triplane/renderer.py | 871 | 48 | invalid decimal literal | `max={self.density_grid_torso.max().item():.4f},` |
| 302 | models/linly_talker/NeRF/nerf_triplane/asr.py | 68 | 47 | invalid decimal literal | `latency should be (ctx + stride_right) * 20ms` |
| 303 | models/linly_talker/NeRF/nerf_triplane/utils.py | 1449 | 19 | closing parenthesis '}' does not match opening parenthesis '(' on line 1375 | `f"{name}.mp4")} -i {self.opt.aud} -strict -2 {os.path.join(save_path,` |
| 304 | models/linly_talker/NeRF/nerf_triplane/network.py | 397 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 387 | `),` |
| 305 | models/linly_talker/NeRF/nerf_triplane/wav2vec.py | 68 | 47 | invalid decimal literal | `latency should be (ctx + stride_right) * 20ms` |
| 306 | models/linly_talker/NeRF/nerf_triplane/gui.py | 25 | 6 | unmatched ']' | `0], [0, -1,` |
| 307 | models/linly_talker/NeRF/gridencoder/grid.py | 70 | 9 | invalid syntax | `else:` |
| 308 | models/linly_talker/VITS/GPT_SoVITS.py | 607 | 15 | closing parenthesis ')' does not match opening parenthesis '[' on line 582 | `0) * 32768).astype(` |
| 309 | models/linly_talker/VITS/XTTS.py | 27 | 39 | invalid syntax. Perhaps you forgot a comma? | `get_user_data_dir("tts"), model_name.replace("/", "--")` |
| 310 | models/linly_talker/Musetalk/musetalk/utils/preprocessing.py | 99 | 18 | unterminated string literal (detected at line 99) | `text_range = f"Total frame:「{len(frames)}」 Manually adjust range : [ -{int(sum(average_range_minus)/len(average_range_minus))}~{int(sum(average_range_plus)/len(average_range_plus))} ] ,` |
| 311 | models/linly_talker/Musetalk/musetalk/utils/face_detection/api.py | 93 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.face_detector = face_detector_module.FaceDetector(` |
| 312 | models/linly_talker/Musetalk/musetalk/utils/face_detection/api.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 313 | models/linly_talker/Musetalk/musetalk/utils/face_detection/detection/sfd/sfd_detector.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 314 | models/linly_talker/Musetalk/musetalk/utils/face_detection/detection/sfd/sfd_detector.py | 28 | 12 | unexpected indent | `if not os.path.isfile(path_to_detector):` |
| 315 | models/linly_talker/Musetalk/musetalk/models/vae.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 316 | models/linly_talker/Musetalk/musetalk/models/vae.py | 41 | 12 | unexpected indent | `self.transform = transforms.Normalize(mean=[0.5,` |
| 317 | models/linly_talker/Musetalk/musetalk/whisper/whisper/decoding.py | 45 | 13 | invalid syntax. Perhaps you forgot a comma? | `f"This model doesn't have language tokens so it can't perform lang id"` |
| 318 | models/linly_talker/Musetalk/musetalk/whisper/whisper/model.py | 49 | 1 | invalid syntax | `class Conv1d(nn.Conv1d):` |
| 319 | models/linly_talker/Musetalk/musetalk/whisper/whisper/tokenizer.py | 290 | 75 | invalid character '♪' (U+266A) | `"<< >> <<< >>> -- --- -( -[ (' (\\" (( )) ((( ))) [[ ]] {{ }} ♪♪ ♪♪♪".split()` |
| 320 | models/linly_talker/Musetalk/musetalk/whisper/whisper/utils.py | 92 | 13 | unterminated string literal (detected at line 92) | `f"{format_timestamp(segment['start'],` |
| 321 | models/linly_talker/Musetalk/musetalk/whisper/whisper/transcribe.py | 258 | 18 | unterminated string literal (detected at line 258) | `help="optional patience value to use in beam decoding,` |
| 322 | models/linly_talker/Musetalk/musetalk/whisper/whisper/normalizers/english.py | 58 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 31 | `}` |
| 323 | models/linly_talker/Musetalk/scripts/realtime_inference.py | 175 | 21 | unterminated string literal (detected at line 175) | `f" 【bbox_shift】 is changed,` |
| 324 | models/linly_talker/LLM/Llama2Chinese.py | 51 | 28 | invalid syntax. Perhaps you forgot a comma? | `model_vocab_size = base_model.get_input_embeddings().weight.size(0)` |
| 325 | models/linly_talker/LLM/Qwen2.py | 31 | 78 | invalid syntax. Perhaps you forgot a comma? | `path, device_map="auto", torch_dtype="auto", trust_remote_code = True` |
| 326 | models/linly_talker/Qwen/Qwen-1_8B-Chat/cpp_kernels.py | 13 | 14 | invalid syntax. Perhaps you forgot a comma? | `output = raw_output.split()` |
| 327 | models/linly_talker/Qwen/Qwen-1_8B-Chat/tokenization_qwen.py | 96 | 33 | unterminated string literal (detected at line 96) | `logger.info(f'the index {index} for extra token {token} exists,` |
| 328 | models/linly_talker/Qwen/Qwen-1_8B-Chat/modeling_qwen.py | 31 | 1 | invalid syntax | `from transformers.modeling_utils import PreTrainedModel` |
| 329 | models/linly_talker/TFG/MuseTalk.py | 35 | 1 | invalid syntax | `from musetalk.utils.preprocessing import (coord_placeholder, get_bbox_range,` |
| 330 | models/linly_talker/TFG/SadTalker.py | 51 | 60 | invalid syntax. Perhaps you forgot a comma? | `checkpoint_path, self.config_path, 256, False, "crop"` |
| 331 | models/linly_talker/TFG/Wav2Lipv2.py | 46 | 6 | invalid syntax | `torch.manual_seed(1234)` |
| 332 | models/linly_talker/TFG/Wav2Lip.py | 43 | 70 | invalid syntax. Perhaps you forgot a comma? | `checkpoint_path, map_location = lambda storage, loc: storage` |
| 333 | models/linly_talker/TFG/MuseV.py | 53 | 50 | unexpected character after line continuation character | `from musev.models.ip_adapter_face_loader import \\` |
| 334 | models/linly_talker/TTS/XTTS.py | 20 | 44 | '(' was never closed | `tempf = tempfile.NamedTemporaryFile(` |
| 335 | models/linly_talker/GPT_SoVITS/s1_train.py | 94 | 1 | invalid syntax | `def main(args):` |
| 336 | models/linly_talker/GPT_SoVITS/inference_webui.py | 38 | 1 | invalid syntax | `if os.path.exists("./sweight.txt"):` |
| 337 | models/linly_talker/GPT_SoVITS/utils.py | 331 | 13 | unterminated string literal (detected at line 331) | `"{} is not a git repository,` |
| 338 | models/linly_talker/GPT_SoVITS/s2_train.py | 728 | 21 | closing parenthesis '}' does not match opening parenthesis '(' on line 723 | `}` |
| 339 | models/linly_talker/GPT_SoVITS/prepare_datasets/3-get-semantic.py | 64 | 23 | invalid syntax | `if is_half is True:` |
| 340 | models/linly_talker/GPT_SoVITS/module/models.py | 43 | 17 | invalid syntax. Perhaps you forgot a comma? | `modules.ConvFlow(2, filter_channels, kernel_size, n_layers = 3)` |
| 341 | models/linly_talker/GPT_SoVITS/module/models_onnx.py | 44 | 17 | invalid syntax. Perhaps you forgot a comma? | `modules.ConvFlow(2, filter_channels, kernel_size, n_layers = 3)` |
| 342 | models/linly_talker/GPT_SoVITS/module/quantize.py | 22 | 8 | unexpected indent | `codes: torch.Tensor` |
| 343 | models/linly_talker/GPT_SoVITS/AR/models/t2s_model.py | 10 | 1 | invalid syntax | `from AR.modules.embedding import SinePositionalEmbedding, TokenEmbedding` |
| 344 | models/linly_talker/GPT_SoVITS/AR/modules/scaling.py | 71 | 38 | invalid syntax | `if __name__ == "__main__":` |
| 345 | models/linly_talker/GPT_SoVITS/AR/modules/patched_mha_with_cache.py | 390 | 5 | unterminated string literal (detected at line 390) | `f"expecting static_k.size(0) of {bsz * num_heads},` |
| 346 | models/linly_talker/GPT_SoVITS/AR/modules/activation_onnx.py | 61 | 21 | invalid syntax. Perhaps you forgot a comma? | `torch.empty((embed_dim, embed_dim), **factory_kwargs)` |
| 347 | models/linly_talker/GPT_SoVITS/AR/modules/activation.py | 403 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 397 | `):` |
| 348 | models/linly_talker/GPT_SoVITS/AR/modules/optim.py | 500 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 493 | `}` |
| 349 | models/linly_talker/GPT_SoVITS/AR/data/dataset.py | 36 | 13 | invalid syntax. Perhaps you forgot a comma? | `[(0, 0)] * axis + [(0, max_length - length)] + [(0, 0)] * (ndim - axis - 1)` |
| 350 | models/linly_talker/GPT_SoVITS/feature_extractor/cnhubert.py | 32 | 5 | invalid syntax | `def forward(self, x):` |
| 351 | models/linly_talker/face_detection/detection/sfd/sfd_detector.py | 28 | 12 | unexpected indent | `if not os.path.isfile(path_to_detector):` |
| 352 | models/linly_talker/src/hparams.py | 35 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 353 | models/linly_talker/src/test_audio2coeff.py | 53 | 13 | invalid syntax | `else:` |
| 354 | models/linly_talker/src/facerender/animate.py | 321 | 56 | closing parenthesis ')' does not match opening parenthesis '[' on line 309 | `int(img_size * original_size[1]/original_size[0]) )),` |
| 355 | models/linly_talker/src/facerender/pirender_animate.py | 42 | 66 | invalid syntax. Perhaps you forgot a comma? | `checkpoint_path, map_location = lambda storage, loc: storage` |
| 356 | models/linly_talker/src/facerender/modules/keypoint_detector.py | 9 | 1 | invalid syntax | `from src.facerender.sync_batchnorm import SynchronizedBatchNorm2d as BatchNorm2d` |
| 357 | models/linly_talker/src/facerender/modules/make_animation.py | 34 | 41 | invalid syntax. Perhaps you forgot a comma? | `kp_driving["jacobian"], torch.inverse(kp_driving_initial["jacobian"])` |
| 358 | models/linly_talker/src/facerender/modules/util.py | 77 | 85 | invalid syntax. Perhaps you forgot a comma? | `in_channels = in_features, out_channels = in_features//4, kernel_size = 1` |
| 359 | models/linly_talker/src/facerender/modules/dense_motion.py | 33 | 8 | unexpected indent | `self.hourglass = Hourglass(` |
| 360 | models/linly_talker/src/facerender/modules/generator.py | 10 | 1 | invalid syntax | `from torch import nn` |
| 361 | models/linly_talker/src/utils/croper.py | 77 | 10 | invalid syntax | `x/= np.hypot(` |
| 362 | models/linly_talker/src/utils/hparams.py | 39 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 363 | models/linly_talker/src/utils/face_enhancer.py | 32 | 5 | invalid syntax | `return list(gen)` |
| 364 | models/linly_talker/src/utils/model2safetensor.py | 21 | 1 | invalid syntax | `from src.facerender.modules.keypoint_detector import HEEstimator, KPDetector` |
| 365 | models/linly_talker/src/utils/utils.py | 15 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dtype = np.float32,` |
| 366 | models/linly_talker/src/utils/hparamsv2.py | 35 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 367 | models/linly_talker/src/models/wav2lip.py | 264 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 161 | `)  # 96,96` |
| 368 | models/linly_talker/src/face3d/util/util.py | 56 | 9 | unterminated string literal (detected at line 56) | `"In %s,` |
| 369 | models/linly_talker/src/face3d/util/nvdiffrast.py | 42 | 14 | unmatched ')' | `f = zfar)).matmul(` |
| 370 | models/linly_talker/src/face3d/models/bfm.py | 24 | 1 | invalid syntax | `class SH:` |
| 371 | models/linly_talker/src/face3d/models/base_model.py | 49 | 13 | unmatched ')' | `opt.name)  # save all the checkpoints to save_dir` |
| 372 | models/linly_talker/src/face3d/models/facerecon_model.py | 16 | 1 | invalid syntax | `from src.face3d.util import util` |
| 373 | models/linly_talker/src/face3d/models/arcface_torch/eval_ijbc.py | 40 | 50 | invalid syntax. Perhaps you forgot a comma? | `"--target", default="IJBC", type = str, help="target, set to IJBC or IJBB"` |
| 374 | models/linly_talker/src/face3d/models/arcface_torch/dataset.py | 20 | 12 | unexpected indent | `self.local_rank = local_rank` |
| 375 | models/linly_talker/src/face3d/models/arcface_torch/onnx_ijbc.py | 26 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dtype = np.float32,` |
| 376 | models/linly_talker/src/face3d/models/arcface_torch/partial_fc.py | 74 | 13 | invalid syntax. Perhaps you forgot a comma? | `rank < num_classes % world_size` |
| 377 | models/linly_talker/src/face3d/models/arcface_torch/utils/utils_amp.py | 25 | 12 | unexpected indent | `self._per_device_tensors: Dict[torch.device, torch.Tensor] = {}` |
| 378 | models/linly_talker/src/face3d/models/arcface_torch/eval/verification.py | 92 | 45 | invalid syntax. Perhaps you forgot a comma? | `threshold, dist[train_set], actual_issame[train_set]` |
| 379 | models/linly_talker/src/face3d/data/template_dataset.py | 69 | 26 | unmatched ')' | `opt.max_dataset_size)) to get all the image paths under the directory self.root` |
| 380 | models/linly_talker/src/audio2pose_models/discriminator.py | 39 | 13 | invalid syntax | `if norm == "BN":` |
| 381 | models/linly_talker/src/audio2pose_models/audio_encoder.py | 14 | 65 | invalid syntax. Perhaps you forgot a comma? | `nn.Conv2d(cin, cout, kernel_size, stride, padding), nn.BatchNorm2d(cout)` |
| 382 | url_fix_backups/fix_all_linting_issues.py | 158 | 38 | closing parenthesis ']' does not match opening parenthesis '(' | `content = re.sub(r'(["\\'])([^"\\']*)\\\\;([^"\\']*)\\1',` |
| 383 | url_fix_backups/system_monitor.py | 300 | 33 | unterminated string literal (detected at line 300) | `condition = f"memory_percent > {thresholds.get('memory_percent',` |
| 384 | url_fix_backups/environment_config_manager.py | 332 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 323 | `},` |
| 385 | url_fix_backups/api_opportunity_finder.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 386 | url_fix_backups/api_security_compliance.py | 260 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 252 | `}` |
| 387 | url_fix_backups/deploy_live.py | 178 | 17 | unterminated string literal (detected at line 178) | `'Configure GitHub repository secrets (NETLIFY_AUTH_TOKEN,` |
| 388 | url_fix_backups/test_automation_integration.py | 48 | 1 | invalid syntax | `from tools.basic_video_generator import create_basic_video` |
| 389 | url_fix_backups/run_simple.py | 123 | 25 | unterminated string literal (detected at line 123) | `f"import uvicorn; from main import app; uvicorn.run(app,` |
| 390 | url_fix_backups/api_opportunity_finder.py | 487 | 41 | unterminated string literal (detected at line 487) | `"User - Agent": "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36 (KHTML,` |
| 391 | url_fix_backups/api_integration_validator.py | 76 | 9 | cannot assign to attribute here. Maybe you meant '==' instead of '='? | `self.validation_registry = {` |
| 392 | url_fix_backups/launch_live.py | 62 | 1 | invalid syntax | `class IDEProbeFilter(logging.Filter):` |
| 393 | url_fix_backups/paste_app.py | 445 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 424 | `}` |
| 394 | url_fix_backups/real_mcp_ai_assistant.py | 45 | 35 | unterminated string literal (detected at line 45) | `"submit": 'button[type="submit"], .send - button, .submit - btn,` |
| 395 | url_fix_backups/content_sources.py | 321 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 288 | `},` |
| 396 | url_fix_backups/fastapi_performance_baseline.py | 112 | 25 | closing parenthesis '}' does not match opening parenthesis '(' on line 106 | `}` |
| 397 | url_fix_backups/demonstrate_research_capabilities.py | 16 | 60 | '(' was never closed | `from backend.agents.predictive_analytics_engine import (ContentFeatures,` |
| 398 | url_fix_backups/automation_controller.py | 310 | 21 | unterminated string literal (detected at line 310) | `"INSERT INTO system_metrics (component,` |
| 399 | url_fix_backups/startup_orchestrator.py | 163 | 35 | unterminated string literal (detected at line 163) | `command = f"python -m uvicorn {service_data.get('module', 'unified_api_router:app')} --host 0.0.0.0 --port {service_data.get('port',` |
| 400 | url_fix_backups/minimal_api_discovery.py | 219 | 25 | unterminated string literal (detected at line 219) | `f"Discovered via minimal_api_discovery - Auth: {api.get('Auth', 'none')},` |
| 401 | url_fix_backups/davinci_resolve_integration.py | 24 | 34 | invalid syntax. Perhaps you forgot a comma? | `level = logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"` |
| 402 | url_fix_backups/api_deployment_orchestrator.py | 47 | 1 | invalid syntax | `class DeploymentStage:` |
| 403 | url_fix_backups/content_automation_pipeline.py | 460 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 446 | `}` |
| 404 | url_fix_backups/ultimate_lint_fixer_v2.py | 71 | 13 | invalid syntax | `except subprocess.CalledProcessError:` |
| 405 | url_fix_backups/master_integration.py | 46 | 8 | unexpected indent | `from backend.content_agent import AutomatedStudio` |
| 406 | url_fix_backups/test_automation_systems.py | 27 | 20 | '(' was never closed | `logging.basicConfig(` |
| 407 | url_fix_backups/monitoring_system.py | 338 | 33 | unterminated string literal (detected at line 338) | `logger.info(f"📊 Monitoring Report: {json.dumps(report,` |
| 408 | url_fix_backups/breaking_news_watcher.py | 332 | 33 | unterminated string literal (detected at line 332) | `"User - Agent": "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36 (KHTML,` |
| 409 | url_fix_backups/database_validator.py | 336 | 23 | unterminated string literal (detected at line 336) | `report.append(f"Missing Recommended Indexes: {integrity.get('missing_recommended_indexes',` |
| 410 | url_fix_backups/unified_api_router.py | 162 | 26 | unterminated string literal (detected at line 162) | `self.logger.info("AI Integration (ChatGPT,` |
| 411 | url_fix_backups/news_driven_content_trigger.py | 91 | 9 | invalid syntax. Perhaps you forgot a comma? | `self._init_trigger_database()` |
| 412 | url_fix_backups/autonomous_decision_engine.py | 192 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 182 | `}` |
| 413 | url_fix_backups/create_real_video.py | 37 | 34 | invalid syntax. Perhaps you forgot a comma? | `level = logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"` |
| 414 | url_fix_backups/check_deployment_readiness.py | 169 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 165 | `},` |
| 415 | url_fix_backups/simple_automation_test.py | 23 | 34 | invalid syntax. Perhaps you forgot a comma? | `level = logging.INFO, format="%(asctime)s ¦ %(levelname)s ¦ %(message)s"` |
| 416 | url_fix_backups/test_3d_pipeline.py | 21 | 17 | unterminated string literal (detected at line 21) | `"import bpy; print('Blender API Version:',` |
| 417 | url_fix_backups/core_ai_integration.py | 442 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 438 | `}` |
| 418 | url_fix_backups/test_avatar_generation.py | 97 | 13 | unterminated string literal (detected at line 97) | `f"📊 Result keys: {result.keys() if isinstance(result,` |
| 419 | url_fix_backups/api_integration_validator.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 420 | url_fix_backups/fix_agents.py | 56 | 93 | unexpected character after line continuation character | `r"class\\s + RightPerspectiveFirewall\\s*(?:\\([^)]*\\))?\\s*:\\s*(?:\\n\\s+\\"\\"\\".*?\\"\\"\\"\\s*)?",` |
| 421 | url_fix_backups/api_manager.py | 106 | 21 | unterminated string literal (detected at line 106) | `f"✅ Successfully discovered {result.get('apis_integrated',` |
| 422 | url_fix_backups/api_security_compliance.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 423 | url_fix_backups/run_api_discovery.py | 471 | 19 | unterminated string literal (detected at line 471) | `print(f"   • Free APIs: {summary.get('free_apis',` |
| 424 | url_fix_backups/main_app.py | 699 | 21 | closing parenthesis '}' does not match opening parenthesis '(' on line 688 | `},` |
| 425 | url_fix_backups/api_deployment_orchestrator.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 426 | url_fix_backups/routers/comprehensive_dashboard.py | 19 | 8 | unexpected indent | `from system_monitor import SystemMonitor` |
| 427 | url_fix_backups/copy_of_code/launch_live.py | 503 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 496 | `}` |
| 428 | url_fix_backups/copy_of_code/base_agents.py | 664 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 656 | `}` |
| 429 | url_fix_backups/copy_of_code/dashboard.py | 2107 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 2100 | `),` |
| 430 | url_fix_backups/copy_of_code/secrets_cli.py | 101 | 9 | invalid syntax | `except SecretStoreError as e:` |
| 431 | url_fix_backups/copy_of_code/doctor_creative_env.py | 34 | 16 | closing parenthesis ')' does not match opening parenthesis '[' on line 29 | `text = True).returncode` |
| 432 | url_fix_backups/copy_of_code/agents/self_repair_agent.py | 580 | 32 | unterminated string literal (detected at line 580) | `creative_context = " Note: This component uses an isolated Python virtual environment (venv_creative) with creative dependencies (torch,` |
| 433 | url_fix_backups/copy_of_code/agents/niche_domination_agent.py | 203 | 21 | unterminated string literal (detected at line 203) | `"CREATE INDEX IF NOT EXISTS idx_growth_metrics_channel_niche ON growth_metrics(channel,` |
| 434 | url_fix_backups/copy_of_code/agents/research_tools.py | 1028 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 1023 | `},` |
| 435 | url_fix_backups/copy_of_code/agents/strategic_advisor_agent.py | 971 | 29 | unterminated string literal (detected at line 971) | `f"{brief.year}-{self._quarter_to_month(brief.quarter,` |
| 436 | url_fix_backups/copy_of_code/agents/base_agents.py | 264 | 16 | unterminated string literal (detected at line 264) | `return f"{self.__class__.__name__}(agent_id='{self.agent_id}',` |
| 437 | url_fix_backups/copy_of_code/agents/content_evolution_agent.py | 226 | 21 | unterminated string literal (detected at line 226) | `"CREATE INDEX IF NOT EXISTS idx_trends_platform_format ON format_trends(platform,` |
| 438 | url_fix_backups/copy_of_code/agents/specialized_agents.py | 789 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 774 | `}` |
| 439 | url_fix_backups/copy_of_code/agents/web_automation_tools.py | 160 | 13 | unterminated string literal (detected at line 160) | `"Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36 (KHTML,` |
| 440 | url_fix_backups/copy_of_code/agents/stealth_automation_agent.py | 523 | 17 | unterminated string literal (detected at line 523) | `"Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML,` |
| 441 | url_fix_backups/copy_of_code/agents/financial_management_agent.py | 1083 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 1061 | `}` |
| 442 | url_fix_backups/copy_of_code/content/audio_postprod.py | 204 | 13 | did you forget parentheses around the comprehension target? | `"/usr / local / bin / ffmpeg",` |
| 443 | url_fix_backups/copy_of_code/content/animate_avatar.py | 164 | 56 | invalid syntax. Perhaps you forgot a comma? | `source_image, audio_file, output_path, config` |
| 444 | url_fix_backups/copy_of_code/content/ai_video_editing.py | 329 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 321 | `}` |
| 445 | url_fix_backups/copy_of_code/content/blender_compositor.py | 365 | 17 | unterminated string literal (detected at line 365) | `"            start_frame = checkpoint.get('last_frame',` |
| 446 | url_fix_backups/copy_of_code/content/ai_video_editor.py | 364 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 356 | `}` |
| 447 | url_fix_backups/copy_of_code/content/audio_post_production.py | 941 | 25 | unterminated string literal (detected at line 941) | `f"Analyzed track '{track.name}': {track_analysis.get('duration',` |
| 448 | url_fix_backups/tasks/document_processing.py | 111 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 103 | `}` |
| 449 | url_fix_backups/tasks/business_automation.py | 645 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 637 | `}` |
| 450 | url_fix_backups/tools/basic_video_generator.py | 79 | 5 | invalid syntax | `else:` |
| 451 | url_fix_backups/tools/cleanup/unused_scan.py | 36 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `logger = logging.getLogger(__name__)` |
| 452 | url_fix_backups/tools/cleanup/rule1_rewrite_suggester.py | 34 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `logger = logging.getLogger(__name__)` |
| 453 | url_fix_backups/monetization_bundle/main.py | 70 | 1 | invalid syntax | `from sqlalchemy.ext.declarative import declarative_base` |
| 454 | url_fix_backups/app/dashboard_integration.py | 205 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 192 | `}` |
| 455 | url_fix_backups/app/bridge_to_system.py | 239 | 21 | unterminated string literal (detected at line 239) | `f"Loaded {` |
| 456 | url_fix_backups/app/actions.py | 112 | 40 | unterminated string literal (detected at line 112) | `name = f"action:{` |
| 457 | url_fix_backups/app/dashboard.py | 377 | 17 | unterminated string literal (detected at line 377) | `f"[actions] manifest updated after agent registration: {` |
| 458 | url_fix_backups/app/dashboard.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 459 | url_fix_backups/app/ai_integrated_dashboard.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 460 | url_fix_backups/app/system_smoke_test_agent.py | 196 | 21 | unterminated string literal (detected at line 196) | `f"Checking {` |
| 461 | url_fix_backups/app/ai_integrated_dashboard.py | 90 | 21 | unterminated string literal (detected at line 91) | `logger.info("Using browser automation for ChatGPT, Gemini, \` |
| 462 | url_fix_backups/app/websocket_manager.py | 30 | 13 | unterminated string literal (detected at line 30) | `f"WebSocket connected: {` |
| 463 | url_fix_backups/app/routers/content.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 464 | url_fix_backups/app/routers/places.py | 165 | 49 | unterminated string literal (detected at line 165) | `logging.getLogger(__name__).warning(f"Provider error: {provider_error},` |
| 465 | url_fix_backups/app/routers/avatar_api.py | 107 | 26 | unterminated string literal (detected at line 107) | `detail = f"Avatar generation failed: {` |
| 466 | url_fix_backups/app/routers/avatar.py | 205 | 30 | unterminated string literal (detected at line 205) | `detail = f"Engine {` |
| 467 | url_fix_backups/app/routers/dashboard.py | 414 | 20 | unterminated string literal (detected at line 414) | `paste_id = f"paste_{` |
| 468 | url_fix_backups/app/routers/content.py | 20 | 36 | '(' was never closed | `from content_agent.main import (ContentAgent, ContentConfig, ContentRequest,` |
| 469 | url_fix_backups/app/routers/oauth.py | 147 | 21 | unterminated string literal (detected at line 147) | `f"TikTok OAuth successful for user: {` |
| 470 | url_fix_backups/app/integrations/monitor.py | 94 | 30 | unterminated string literal (detected at line 94) | `"nominatim_osm": f"{` |
| 471 | url_fix_backups/app/integrations/monitor.failed.py | 1 | 5 | invalid syntax | `Run with 'trae -' to read from stdin (e.g. 'ps aux ¦ grep code ¦ trae -').` |
| 472 | url_fix_backups/frontend/media_dashboard.py | 670 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 640 | `}` |
| 473 | url_fix_backups/master_orchestrator/business_generators.py | 247 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 226 | `}` |
| 474 | url_fix_backups/deploy/production_config.py | 83 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `missing_vars = []` |
| 475 | url_fix_backups/tests/test_manifest_contract.py | 52 | 21 | unterminated string literal (detected at line 52) | `f"❌ Version field '{field}' should be string,` |
| 476 | url_fix_backups/tests/test_vidscript_debug.py | 27 | 13 | unterminated string literal (detected at line 28) | `f"📊 Available methods: {[attr for attr in dir(script_gen) if not attr.startswith('_') \` |
| 477 | url_fix_backups/tests/test_avatar_failsafe.py | 63 | 21 | unterminated string literal (detected at line 63) | `f"   Failover Triggered: {orch_info.get('failover_triggered',` |
| 478 | url_fix_backups/tests/test_ai_benchmark_integration.py | 30 | 1 | invalid syntax | `class TestAIBenchmarkIntegration:` |
| 479 | url_fix_backups/tests/end_to_end_verification.py | 44 | 8 | unexpected indent | `from backend.zero_cost_stack import ZeroCostStackManager` |
| 480 | url_fix_backups/utils/credit_optimizer.py | 516 | 13 | unterminated string literal (detected at line 516) | `f"Credit optimizer cleanup completed,` |
| 481 | url_fix_backups/backend/api_orchestrator.py | 431 | 25 | unterminated string literal (detected at line 431) | `f"No available API endpoint,` |
| 482 | url_fix_backups/backend/zero_cost_stack.py | 201 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 191 | `),` |
| 483 | url_fix_backups/backend/ai_benchmark_integration.py | 506 | 36 | unterminated string literal (detected at line 507) | `recommendations.append("Enhance clarity with better structure \` |
| 484 | url_fix_backups/backend/youtube_scheduler.py | 211 | 5 | invalid syntax | `def _load_config(self) -> Dict[str, Any]:` |
| 485 | url_fix_backups/backend/autonomous_diagnosis_repair.py | 204 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 197 | `},` |
| 486 | url_fix_backups/backend/payment_processor.py | 899 | 22 | unterminated string literal (detected at line 899) | `attempt_id = f"att_{int(time.time() * 1000000)}_{hash(payment_id) % 10000}_{random.randint(1000,` |
| 487 | url_fix_backups/backend/ecommerce_marketing_layer.py | 219 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 210 | `},` |
| 488 | url_fix_backups/backend/secure_secret_store.py | 394 | 21 | unterminated string literal (detected at line 394) | `"INSERT INTO access_log (secret_id,` |
| 489 | url_fix_backups/backend/youtube_engagement_automation.py | 586 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 579 | `}` |
| 490 | url_fix_backups/backend/orchestrator.py | 100 | 1 | invalid syntax | `except ImportError:` |
| 491 | url_fix_backups/backend/m1_optimizer.py | 150 | 24 | invalid syntax. Perhaps you forgot a comma? | `thread_name_prefix="M1 - Perf"` |
| 492 | url_fix_backups/backend/app.py | 341 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 333 | `},` |
| 493 | url_fix_backups/backend/rule1_scanner.py | 159 | 17 | invalid syntax. Perhaps you forgot a comma? | `"""` |
| 494 | url_fix_backups/backend/youtube_analytics_automation.py | 908 | 39 | unterminated string literal (detected at line 908) | `description = f"Top performing videos have titles averaging {optimal_length} characters,` |
| 495 | url_fix_backups/backend/youtube_automation_orchestrator.py | 57 | 1 | invalid syntax | `from backend.pipelines.hollywood_pipeline import HollywoodPipeline` |
| 496 | url_fix_backups/backend/api_monetization.py | 427 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 420 | `},` |
| 497 | url_fix_backups/backend/revenue_streams_api.py | 334 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 321 | `},` |
| 498 | url_fix_backups/backend/agentic_protocol.py | 251 | 25 | unterminated string literal (detected at line 251) | `"INSERT OR REPLACE INTO agents (id,` |
| 499 | url_fix_backups/backend/ai_intelligent_router.py | 183 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 156 | `}` |
| 500 | url_fix_backups/backend/production_init.py | 106 | 60 | unexpected character after line continuation character | `from backend.agents.specialized_agents import \\` |
| 501 | url_fix_backups/backend/routers/chat.py | 249 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 238 | `},` |
| 502 | url_fix_backups/backend/enhancement/pipeline_enhancement_system.py | 395 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 385 | `}` |
| 503 | url_fix_backups/backend/core/database_production.py | 32 | 8 | unexpected indent | `from psycopg2.pool import ThreadedConnectionPool` |
| 504 | url_fix_backups/backend/security/security_scanner.py | 69 | 71 | closing parenthesis ']' does not match opening parenthesis '{' on line 68 | `"pattern": r'(?i)(api[_-]?key¦apikey)\\s*[=:]\\s*["\\']?([a - zA - Z0 - 9_\\-]{20,})["\\']?',` |
| 505 | url_fix_backups/backend/security/compliance_validator.py | 92 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 78 | `}` |
| 506 | url_fix_backups/backend/integration/master_control_system.py | 386 | 42 | unterminated string literal (detected at line 386) | `logging.getLogger(__name__).info(f"Received signal {signum},` |
| 507 | url_fix_backups/backend/runner/channel_executor.py | 413 | 21 | closing parenthesis '}' does not match opening parenthesis '(' on line 403 | `},` |
| 508 | url_fix_backups/backend/agents/enhanced_web_scraping_tools.py | 254 | 13 | unterminated string literal (detected at line 254) | `"Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36 (KHTML,` |
| 509 | url_fix_backups/backend/agents/marketing_tools.py | 2849 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 2835 | `}` |
| 510 | url_fix_backups/backend/agents/self_repair_agent.py | 580 | 32 | unterminated string literal (detected at line 580) | `creative_context = " Note: This component uses an isolated Python virtual environment (venv_creative) with creative dependencies (torch,` |
| 511 | url_fix_backups/backend/agents/niche_domination_agent.py | 230 | 21 | unterminated string literal (detected at line 230) | `"CREATE INDEX IF NOT EXISTS idx_growth_metrics_channel_niche ON growth_metrics(channel,` |
| 512 | url_fix_backups/backend/agents/research_tools.py | 676 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 669 | `),` |
| 513 | url_fix_backups/backend/agents/planner_agent.py | 195 | 21 | unterminated string literal (detected at line 195) | `f"Performance below threshold ({metrics.overall_score():.2f}),` |
| 514 | url_fix_backups/backend/agents/community_engagement_agent.py | 132 | 17 | unterminated string literal (detected at line 132) | `"INSERT OR IGNORE INTO community_keywords (keyword,` |
| 515 | url_fix_backups/backend/agents/monetization_services_agent.py | 36 | 8 | unexpected indent | `from reportlab.lib.pagesizes import A4, letter` |
| 516 | url_fix_backups/backend/agents/strategic_advisor_agent.py | 978 | 29 | unterminated string literal (detected at line 978) | `f"{brief.year}-{self._quarter_to_month(brief.quarter,` |
| 517 | url_fix_backups/backend/agents/base_agents.py | 449 | 16 | unterminated string literal (detected at line 449) | `return f"{self.__class__.__name__}(agent_id='{self.agent_id}',` |
| 518 | url_fix_backups/backend/agents/predictive_analytics_engine.py | 28 | 8 | unexpected indent | `from sklearn.linear_model import LinearRegression` |
| 519 | url_fix_backups/backend/agents/research_agent.py | 1106 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 1097 | `}` |
| 520 | url_fix_backups/backend/agents/content_evolution_agent.py | 226 | 21 | unterminated string literal (detected at line 226) | `"CREATE INDEX IF NOT EXISTS idx_trends_platform_format ON format_trends(platform,` |
| 521 | url_fix_backups/backend/agents/collaboration_outreach_agent.py | 874 | 29 | closing parenthesis ')' does not match opening parenthesis '[' on line 867 | `),` |
| 522 | url_fix_backups/backend/agents/system_agent.py | 1226 | 13 | unterminated string literal (detected at line 1226) | `f"Watchdog monitor started (threshold: {self.watchdog_threshold}s,` |
| 523 | url_fix_backups/backend/agents/specialized_agents.py | 689 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 678 | `}` |
| 524 | url_fix_backups/backend/agents/marketing_agent.py | 158 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 151 | `},` |
| 525 | url_fix_backups/backend/agents/conservative_research_agent.py | 285 | 29 | unterminated string literal (detected at line 285) | `"User - Agent": "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36 (KHTML,` |
| 526 | url_fix_backups/backend/agents/web_automation_tools.py | 160 | 13 | unterminated string literal (detected at line 160) | `"Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36 (KHTML,` |
| 527 | url_fix_backups/backend/agents/stealth_automation_agent.py | 529 | 17 | unterminated string literal (detected at line 529) | `"Mozilla / 5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36 (KHTML,` |
| 528 | url_fix_backups/backend/agents/financial_management_agent.py | 1103 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 1081 | `}` |
| 529 | url_fix_backups/backend/content/evidence_based_scripting.py | 48 | 5 | invalid syntax | `def _validate_protected_channel(self):` |
| 530 | url_fix_backups/backend/content/audio_postprod.py | 204 | 13 | did you forget parentheses around the comprehension target? | `"/usr / local / bin / ffmpeg",` |
| 531 | url_fix_backups/backend/content/ai_video_editing.py | 330 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 322 | `}` |
| 532 | url_fix_backups/backend/content/blender_compositor.py | 864 | 17 | unterminated string literal (detected at line 864) | `"            start_frame = checkpoint.get('last_frame',` |
| 533 | url_fix_backups/backend/content/ai_video_editor.py | 364 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 356 | `}` |
| 534 | url_fix_backups/backend/content/automated_author.py | 302 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 295 | `),` |
| 535 | url_fix_backups/backend/content/vidscript_pro.py | 323 | 34 | unterminated string literal (detected at line 323) | `live_briefing += f"• {trend.get('topic', 'Unknown')}: {trend.get('momentum_score',` |
| 536 | url_fix_backups/backend/content/relentless_optimization.py | 1095 | 17 | unterminated string literal (detected at line 1095) | `f"Generated optimization report with {report.get('active_tests',` |
| 537 | url_fix_backups/backend/content/audio_post_production.py | 926 | 25 | unterminated string literal (detected at line 926) | `f"Analyzed track '{track.name}': {track_analysis.get('duration',` |
| 538 | url_fix_backups/backend/pipelines/blender_scripts/avatar_creator.py | 28 | 28 | invalid syntax. Perhaps you forgot a comma? | `size = 1, location=(location[0], location[1], location[2] + 1)` |
| 539 | url_fix_backups/backend/dashboard/actions_bus.py | 41 | 33 | unterminated string literal (detected at line 41) | `"endpoint": f"/api / action/{getattr(fn, '_agent_pretty',` |
| 540 | url_fix_backups/backend/integrations/reddit_integration.py | 32 | 5 | invalid syntax | `def ready(self) -> bool:` |
| 541 | url_fix_backups/backend/integrations/obs_automation.py | 171 | 8 | unexpected indent | `start_time: Optional[str] = None` |
| 542 | url_fix_backups/backend/integrations/crewai_integration.py | 223 | 17 | invalid syntax. Perhaps you forgot a comma? | `"CrewAI not installed. Install with: pip install crewai"` |
| 543 | url_fix_backups/backend/integrations/supabase_integration.py | 48 | 8 | unexpected indent | `from storage3 import StorageException` |
| 544 | url_fix_backups/backend/integrations/gimp_automation.py | 55 | 9 | invalid syntax. Perhaps you forgot a comma? | `"Warning: Image processing libraries not available. Install with: pip install Pillow numpy"` |
| 545 | url_fix_backups/backend/integrations/research_validation_service.py | 393 | 29 | closing parenthesis '}' does not match opening parenthesis '(' on line 388 | `}` |
| 546 | url_fix_backups/backend/integrations/worker_manager.py | 104 | 21 | invalid syntax. Perhaps you forgot a comma? | `worker_id = f"worker_{self.platform}_{int(time.time())}"` |
| 547 | url_fix_backups/backend/integrations/audacity_automation.py | 55 | 9 | invalid syntax. Perhaps you forgot a comma? | `"Warning: Audio processing libraries not available. Install with: pip install librosa soundfile numpy"` |
| 548 | url_fix_backups/backend/integrations/twitter_integration.py | 239 | 23 | unterminated string literal (detected at line 239) | `base_string = f"{method.upper()}&{urllib.parse.quote(url,` |
| 549 | url_fix_backups/backend/testing/automated_test_suite.py | 1704 | 28 | unterminated string literal (detected at line 1704) | `"message": f"Weekly content: {successful_content}/{len(content_types)} types successful,` |
| 550 | url_fix_backups/backend/scrapers/news_scraper.py | 37 | 33 | unterminated string literal (detected at line 37) | `"User - Agent": "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36 (KHTML,` |
| 551 | url_fix_backups/backend/scrapers/youtube_scraper.py | 35 | 33 | unterminated string literal (detected at line 35) | `"User - Agent": "Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36 (KHTML,` |
| 552 | url_fix_backups/backend/automation/self_healing_pipeline.py | 308 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 298 | `}` |
| 553 | url_fix_backups/backend/monitoring/alert_manager.py | 275 | 29 | closing parenthesis '}' does not match opening parenthesis '[' on line 269 | `}` |
| 554 | url_fix_backups/backend/monitoring/zero_cost_monitoring_stack.py | 692 | 17 | unterminated string literal (detected at line 692) | `f"ALERT FIRING: {rule.name} - {rule.description} (value: {value},` |
| 555 | url_fix_backups/backend/monitoring/health_monitor.py | 175 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 163 | `}` |
| 556 | url_fix_backups/backend/revenue/revenue_optimization_system.py | 555 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 536 | `}` |
| 557 | url_fix_backups/backend/services/web_search_service.py | 112 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 104 | `}` |
| 558 | url_fix_backups/backend/services/stress_tester.py | 50 | 1 | invalid syntax | `from .health_monitor import HealthMonitor, get_health_monitor` |
| 559 | url_fix_backups/backend/services/auto_discovery_service.py | 799 | 17 | unterminated string literal (detected at line 799) | `f"Estimated Monthly Cost: ${result.cost_analysis.get('estimated_monthly_cost',` |
| 560 | url_fix_backups/backend/services/performance_monitor.py | 722 | 17 | unterminated string literal (detected at line 722) | `"CREATE INDEX IF NOT EXISTS idx_metrics_name_timestamp ON performance_metrics(name,` |
| 561 | url_fix_backups/backend/services/rss_watcher.py | 529 | 13 | unterminated string literal (detected at line 529) | `f"RSS monitoring started (interval: {self.monitoring_interval}s,` |
| 562 | url_fix_backups/backend/services/health_monitor.py | 1033 | 33 | closing parenthesis '}' does not match opening parenthesis '(' on line 1020 | `}` |
| 563 | url_fix_backups/backend/services/automated_model_generator.py | 147 | 12 | unexpected indent | `elif self.state == "open":` |
| 564 | url_fix_backups/backend/services/api_integration_service.py | 247 | 25 | closing parenthesis ')' does not match opening parenthesis '[' on line 232 | `),` |
| 565 | url_fix_backups/backend/services/redundancy_manager.py | 642 | 17 | unterminated string literal (detected at line 642) | `f"Hybrid backend '{self.config.name}' initialized (local: {local_ok},` |
| 566 | url_fix_backups/backend/services/reliable_model_generator.py | 39 | 1 | invalid syntax | `from backup_generator import BackupGenerator, BackupStrategy, GenerationMode` |
| 567 | url_fix_backups/backend/media/workflow_engine.py | 285 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 277 | `},` |
| 568 | url_fix_backups/models/linly_talker/webui.py | 1275 | 47 | unterminated string literal (detected at line 1275) | `label="Still Mode (fewer head motion,` |
| 569 | url_fix_backups/models/linly_talker/app_multi.py | 41 | 4 | unexpected indent | `maximum = 45,` |
| 570 | url_fix_backups/models/linly_talker/one_button_test.py | 85 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 67 | `}` |
| 571 | url_fix_backups/models/linly_talker/app_musetalk.py | 57 | 5 | invalid syntax | `except Exception:` |
| 572 | url_fix_backups/models/linly_talker/app.py | 48 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `exp_weight = 1` |
| 573 | url_fix_backups/models/linly_talker/png_avatar_processor.py | 112 | 52 | invalid syntax. Perhaps you forgot a comma? | `processed_image, enhance = True` |
| 574 | url_fix_backups/models/linly_talker/app_img.py | 317 | 47 | unterminated string literal (detected at line 317) | `label="Still Mode (fewer head motion,` |
| 575 | url_fix_backups/models/linly_talker/app_vits.py | 50 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `exp_weight = 1` |
| 576 | url_fix_backups/models/linly_talker/NeRF/data_utils/wav2mel_hparams.py | 35 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 577 | url_fix_backups/models/linly_talker/NeRF/data_utils/process.py | 58 | 5 | invalid syntax | `except Exception:` |
| 578 | url_fix_backups/models/linly_talker/NeRF/data_utils/hubert.py | 26 | 54 | invalid syntax. Perhaps you forgot a comma? | `speech, return_tensors="pt", sampling_rate = 16000` |
| 579 | url_fix_backups/models/linly_talker/NeRF/data_utils/face_tracking/render_3dmm.py | 66 | 19 | unterminated string literal (detected at line 66) | `msg = "Cameras must be specified either at initialization \\` |
| 580 | url_fix_backups/models/linly_talker/NeRF/data_utils/face_tracking/face_tracker.py | 25 | 60 | invalid syntax. Perhaps you forgot a comma? | `"--path", type = str, default="obama / ori_imgs", help="idname of target person"` |
| 581 | url_fix_backups/models/linly_talker/NeRF/nerf_triplane/provider.py | 24 | 1 | invalid syntax | `def nerf_matrix_to_ngp(pose, scale = 0.33, offset=[0, 0, 0]):` |
| 582 | url_fix_backups/models/linly_talker/NeRF/nerf_triplane/renderer.py | 871 | 48 | invalid decimal literal | `max={self.density_grid_torso.max().item():.4f},` |
| 583 | url_fix_backups/models/linly_talker/NeRF/nerf_triplane/asr.py | 68 | 47 | invalid decimal literal | `latency should be (ctx + stride_right) * 20ms` |
| 584 | url_fix_backups/models/linly_talker/NeRF/nerf_triplane/utils.py | 1449 | 19 | closing parenthesis '}' does not match opening parenthesis '(' on line 1375 | `f"{name}.mp4")} -i {self.opt.aud} -strict -2 {os.path.join(save_path,` |
| 585 | url_fix_backups/models/linly_talker/NeRF/nerf_triplane/network.py | 397 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 387 | `),` |
| 586 | url_fix_backups/models/linly_talker/NeRF/nerf_triplane/wav2vec.py | 68 | 47 | invalid decimal literal | `latency should be (ctx + stride_right) * 20ms` |
| 587 | url_fix_backups/models/linly_talker/NeRF/nerf_triplane/gui.py | 25 | 6 | unmatched ']' | `0], [0, -1,` |
| 588 | url_fix_backups/models/linly_talker/NeRF/gridencoder/grid.py | 70 | 9 | invalid syntax | `else:` |
| 589 | url_fix_backups/models/linly_talker/VITS/GPT_SoVITS.py | 607 | 15 | closing parenthesis ')' does not match opening parenthesis '[' on line 582 | `0) * 32768).astype(` |
| 590 | url_fix_backups/models/linly_talker/VITS/XTTS.py | 27 | 39 | invalid syntax. Perhaps you forgot a comma? | `get_user_data_dir("tts"), model_name.replace("/", "--")` |
| 591 | url_fix_backups/models/linly_talker/Musetalk/musetalk/utils/preprocessing.py | 99 | 18 | unterminated string literal (detected at line 99) | `text_range = f"Total frame:「{len(frames)}」 Manually adjust range : [ -{int(sum(average_range_minus)/len(average_range_minus))}~{int(sum(average_range_plus)/len(average_range_plus))} ] ,` |
| 592 | url_fix_backups/models/linly_talker/Musetalk/musetalk/utils/face_detection/api.py | 93 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.face_detector = face_detector_module.FaceDetector(` |
| 593 | url_fix_backups/models/linly_talker/Musetalk/musetalk/utils/face_detection/detection/sfd/sfd_detector.py | 28 | 12 | unexpected indent | `if not os.path.isfile(path_to_detector):` |
| 594 | url_fix_backups/models/linly_talker/Musetalk/musetalk/models/vae.py | 41 | 12 | unexpected indent | `self.transform = transforms.Normalize(mean=[0.5,` |
| 595 | url_fix_backups/models/linly_talker/Musetalk/musetalk/whisper/whisper/decoding.py | 45 | 13 | invalid syntax. Perhaps you forgot a comma? | `f"This model doesn't have language tokens so it can't perform lang id"` |
| 596 | url_fix_backups/models/linly_talker/Musetalk/musetalk/whisper/whisper/model.py | 49 | 1 | invalid syntax | `class Conv1d(nn.Conv1d):` |
| 597 | url_fix_backups/models/linly_talker/Musetalk/musetalk/whisper/whisper/utils.py | 92 | 13 | unterminated string literal (detected at line 92) | `f"{format_timestamp(segment['start'],` |
| 598 | url_fix_backups/models/linly_talker/Musetalk/musetalk/whisper/whisper/transcribe.py | 258 | 18 | unterminated string literal (detected at line 258) | `help="optional patience value to use in beam decoding,` |
| 599 | url_fix_backups/models/linly_talker/Musetalk/musetalk/whisper/whisper/normalizers/english.py | 58 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 31 | `}` |
| 600 | url_fix_backups/models/linly_talker/Musetalk/scripts/realtime_inference.py | 175 | 21 | unterminated string literal (detected at line 175) | `f" 【bbox_shift】 is changed,` |
| 601 | url_fix_backups/models/linly_talker/LLM/Qwen2.py | 31 | 78 | invalid syntax. Perhaps you forgot a comma? | `path, device_map="auto", torch_dtype="auto", trust_remote_code = True` |
| 602 | url_fix_backups/models/linly_talker/Qwen/Qwen-1_8B-Chat/cpp_kernels.py | 13 | 14 | invalid syntax. Perhaps you forgot a comma? | `output = raw_output.split()` |
| 603 | url_fix_backups/models/linly_talker/Qwen/Qwen-1_8B-Chat/tokenization_qwen.py | 96 | 33 | unterminated string literal (detected at line 96) | `logger.info(f'the index {index} for extra token {token} exists,` |
| 604 | url_fix_backups/models/linly_talker/Qwen/Qwen-1_8B-Chat/modeling_qwen.py | 31 | 1 | invalid syntax | `from transformers.modeling_utils import PreTrainedModel` |
| 605 | url_fix_backups/models/linly_talker/TFG/MuseTalk.py | 35 | 1 | invalid syntax | `from musetalk.utils.preprocessing import (coord_placeholder, get_bbox_range,` |
| 606 | url_fix_backups/models/linly_talker/TFG/SadTalker.py | 51 | 60 | invalid syntax. Perhaps you forgot a comma? | `checkpoint_path, self.config_path, 256, False, "crop"` |
| 607 | url_fix_backups/models/linly_talker/TFG/Wav2Lipv2.py | 46 | 6 | invalid syntax | `torch.manual_seed(1234)` |
| 608 | url_fix_backups/models/linly_talker/TFG/Wav2Lip.py | 43 | 70 | invalid syntax. Perhaps you forgot a comma? | `checkpoint_path, map_location = lambda storage, loc: storage` |
| 609 | url_fix_backups/models/linly_talker/TFG/MuseV.py | 53 | 50 | unexpected character after line continuation character | `from musev.models.ip_adapter_face_loader import \\` |
| 610 | url_fix_backups/models/linly_talker/TTS/XTTS.py | 20 | 44 | '(' was never closed | `tempf = tempfile.NamedTemporaryFile(` |
| 611 | url_fix_backups/models/linly_talker/GPT_SoVITS/s1_train.py | 94 | 1 | invalid syntax | `def main(args):` |
| 612 | url_fix_backups/models/linly_talker/GPT_SoVITS/inference_webui.py | 38 | 1 | invalid syntax | `if os.path.exists("./sweight.txt"):` |
| 613 | url_fix_backups/models/linly_talker/GPT_SoVITS/utils.py | 331 | 13 | unterminated string literal (detected at line 331) | `"{} is not a git repository,` |
| 614 | url_fix_backups/models/linly_talker/GPT_SoVITS/s2_train.py | 728 | 21 | closing parenthesis '}' does not match opening parenthesis '(' on line 723 | `}` |
| 615 | url_fix_backups/models/linly_talker/GPT_SoVITS/prepare_datasets/3-get-semantic.py | 64 | 23 | invalid syntax | `if is_half is True:` |
| 616 | url_fix_backups/models/linly_talker/GPT_SoVITS/module/models.py | 43 | 17 | invalid syntax. Perhaps you forgot a comma? | `modules.ConvFlow(2, filter_channels, kernel_size, n_layers = 3)` |
| 617 | url_fix_backups/models/linly_talker/GPT_SoVITS/module/models_onnx.py | 44 | 17 | invalid syntax. Perhaps you forgot a comma? | `modules.ConvFlow(2, filter_channels, kernel_size, n_layers = 3)` |
| 618 | url_fix_backups/models/linly_talker/GPT_SoVITS/module/quantize.py | 22 | 8 | unexpected indent | `codes: torch.Tensor` |
| 619 | url_fix_backups/models/linly_talker/GPT_SoVITS/AR/models/t2s_model.py | 10 | 1 | invalid syntax | `from AR.modules.embedding import SinePositionalEmbedding, TokenEmbedding` |
| 620 | url_fix_backups/models/linly_talker/GPT_SoVITS/AR/modules/scaling.py | 71 | 38 | invalid syntax | `if __name__ == "__main__":` |
| 621 | url_fix_backups/models/linly_talker/GPT_SoVITS/AR/modules/patched_mha_with_cache.py | 390 | 5 | unterminated string literal (detected at line 390) | `f"expecting static_k.size(0) of {bsz * num_heads},` |
| 622 | url_fix_backups/models/linly_talker/GPT_SoVITS/AR/modules/activation_onnx.py | 61 | 21 | invalid syntax. Perhaps you forgot a comma? | `torch.empty((embed_dim, embed_dim), **factory_kwargs)` |
| 623 | url_fix_backups/models/linly_talker/GPT_SoVITS/AR/modules/activation.py | 403 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 397 | `):` |
| 624 | url_fix_backups/models/linly_talker/GPT_SoVITS/AR/modules/optim.py | 500 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 493 | `}` |
| 625 | url_fix_backups/models/linly_talker/GPT_SoVITS/AR/data/dataset.py | 36 | 13 | invalid syntax. Perhaps you forgot a comma? | `[(0, 0)] * axis + [(0, max_length - length)] + [(0, 0)] * (ndim - axis - 1)` |
| 626 | url_fix_backups/models/linly_talker/GPT_SoVITS/feature_extractor/cnhubert.py | 32 | 5 | invalid syntax | `def forward(self, x):` |
| 627 | url_fix_backups/models/linly_talker/face_detection/detection/sfd/sfd_detector.py | 28 | 12 | unexpected indent | `if not os.path.isfile(path_to_detector):` |
| 628 | url_fix_backups/models/linly_talker/src/hparams.py | 35 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 629 | url_fix_backups/models/linly_talker/src/test_audio2coeff.py | 53 | 13 | invalid syntax | `else:` |
| 630 | url_fix_backups/models/linly_talker/src/facerender/animate.py | 321 | 56 | closing parenthesis ')' does not match opening parenthesis '[' on line 309 | `int(img_size * original_size[1]/original_size[0]) )),` |
| 631 | url_fix_backups/models/linly_talker/src/facerender/pirender_animate.py | 42 | 66 | invalid syntax. Perhaps you forgot a comma? | `checkpoint_path, map_location = lambda storage, loc: storage` |
| 632 | url_fix_backups/models/linly_talker/src/facerender/modules/keypoint_detector.py | 9 | 1 | invalid syntax | `from src.facerender.sync_batchnorm import SynchronizedBatchNorm2d as BatchNorm2d` |
| 633 | url_fix_backups/models/linly_talker/src/facerender/modules/make_animation.py | 34 | 41 | invalid syntax. Perhaps you forgot a comma? | `kp_driving["jacobian"], torch.inverse(kp_driving_initial["jacobian"])` |
| 634 | url_fix_backups/models/linly_talker/src/facerender/modules/util.py | 77 | 87 | invalid syntax. Perhaps you forgot a comma? | `in_channels = in_features, out_channels = in_features // 4, kernel_size = 1` |
| 635 | url_fix_backups/models/linly_talker/src/utils/croper.py | 77 | 11 | invalid syntax | `x /= np.hypot(` |
| 636 | url_fix_backups/models/linly_talker/src/utils/hparams.py | 39 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 637 | url_fix_backups/models/linly_talker/src/utils/face_enhancer.py | 32 | 5 | invalid syntax | `return list(gen)` |
| 638 | url_fix_backups/models/linly_talker/src/utils/model2safetensor.py | 21 | 1 | invalid syntax | `from src.facerender.modules.keypoint_detector import HEEstimator, KPDetector` |
| 639 | url_fix_backups/models/linly_talker/src/utils/utils.py | 15 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dtype = np.float32,` |
| 640 | url_fix_backups/models/linly_talker/src/utils/hparamsv2.py | 35 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `800 = 50 ms (If None,` |
| 641 | url_fix_backups/models/linly_talker/src/models/wav2lip.py | 264 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 161 | `)  # 96,96` |
| 642 | url_fix_backups/models/linly_talker/src/face3d/util/util.py | 56 | 9 | unterminated string literal (detected at line 56) | `"In %s,` |
| 643 | url_fix_backups/models/linly_talker/src/face3d/util/nvdiffrast.py | 42 | 14 | unmatched ')' | `f = zfar)).matmul(` |
| 644 | url_fix_backups/models/linly_talker/src/face3d/models/bfm.py | 24 | 1 | invalid syntax | `class SH:` |
| 645 | url_fix_backups/models/linly_talker/src/face3d/models/base_model.py | 49 | 13 | unmatched ')' | `opt.name)  # save all the checkpoints to save_dir` |
| 646 | url_fix_backups/models/linly_talker/src/face3d/models/facerecon_model.py | 16 | 1 | invalid syntax | `from src.face3d.util import util` |
| 647 | url_fix_backups/models/linly_talker/src/face3d/models/arcface_torch/eval_ijbc.py | 40 | 50 | invalid syntax. Perhaps you forgot a comma? | `"--target", default="IJBC", type = str, help="target, set to IJBC or IJBB"` |
| 648 | url_fix_backups/models/linly_talker/src/face3d/models/arcface_torch/dataset.py | 20 | 12 | unexpected indent | `self.local_rank = local_rank` |
| 649 | url_fix_backups/models/linly_talker/src/face3d/models/arcface_torch/onnx_ijbc.py | 26 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dtype = np.float32,` |
| 650 | url_fix_backups/models/linly_talker/src/face3d/models/arcface_torch/partial_fc.py | 74 | 13 | invalid syntax. Perhaps you forgot a comma? | `rank < num_classes % world_size` |
| 651 | url_fix_backups/models/linly_talker/src/face3d/models/arcface_torch/eval/verification.py | 92 | 45 | invalid syntax. Perhaps you forgot a comma? | `threshold, dist[train_set], actual_issame[train_set]` |
| 652 | url_fix_backups/integrations/puppeteer_service.py | 58 | 25 | unterminated string literal (detected at line 58) | `"--user - agent = Mozilla / 5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit / 537.36 (KHTML,` |
| 653 | url_fix_backups/scripts/environment_validator.py | 109 | 27 | unterminated string literal (detected at line 109) | `version_str = f"{` |
| 654 | url_fix_backups/scripts/system_orchestrator.py | 200 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 190 | `},` |
| 655 | url_fix_backups/scripts/generate_realistic_avatar.py | 103 | 25 | unterminated string literal (detected at line 103) | `f"Unusual aspect ratio {` |
| 656 | url_fix_backups/scripts/repair-model-generation.py | 95 | 21 | unterminated string literal (detected at line 95) | `f"Only {` |
| 657 | url_fix_backups/scripts/setup_creative_environment.py | 82 | 21 | unterminated string literal (detected at line 82) | `f"Creative environment already exists at {` |
| 658 | url_fix_backups/scripts/load-test.py | 147 | 13 | unterminated string literal (detected at line 147) | `f"Starting load test with {` |
| 659 | url_fix_backups/scripts/go_live_preparation.py | 31 | 13 | invalid syntax. Perhaps you forgot a comma? | `logging.StreamHandler()` |
| 660 | url_fix_backups/scripts/security_audit.py | 82 | 81 | closing parenthesis ']' does not match opening parenthesis '{' on line 74 | `"generic_secret": r'(secret¦password¦token¦key)\\s*[=:]\\s*["\\'][a - zA - Z0 - 9_\\-\\.]{8,}["\\']',` |
| 661 | url_fix_backups/scripts/synthesize_release_v3.py | 184 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 176 | `}` |
| 662 | url_fix_backups/scripts/production_deployment.py | 53 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `logger = logging.getLogger(__name__)` |
| 663 | url_fix_backups/scripts/security_scanner.py | 102 | 71 | closing parenthesis ']' does not match opening parenthesis '{' on line 101 | `"pattern": r'(?i)(api[_-]?key¦apikey)\\s*[=:]\\s*["\\']?([a - zA - Z0 - 9_\\-]{20,})["\\']?',` |
| 664 | url_fix_backups/scripts/start_distributed_system.py | 39 | 1 | invalid syntax | `class DistributedSystemOrchestrator:` |
| 665 | url_fix_backups/scripts/deployment_orchestrator.py | 812 | 21 | unterminated string literal (detected at line 812) | `f"High response time detected: {` |
| 666 | url_fix_backups/scripts/register_avatar_engines.py | 185 | 13 | unterminated string literal (detected at line 185) | `"  • Primary Engine: Linly - Talker (Priority 1) - High quality,` |
| 667 | url_fix_backups/scripts/secrets_cli.py | 101 | 9 | invalid syntax | `except SecretStoreError as e:` |
| 668 | url_fix_backups/scripts/doctor_creative_env.py | 34 | 16 | closing parenthesis ')' does not match opening parenthesis '[' on line 29 | `text = True).returncode` |
| 669 | url_fix_backups/ops/watchdog.py | 134 | 25 | unterminated string literal (detected at line 134) | `"ℹ️ Service monitoring_system marked non - critical,` |
| 670 | url_fix_backups/monitoring/scaling-policies.py | 422 | 43 | unterminated string literal (detected at line 422) | `MetricType.RESPONSE_TIME: f'histogram_quantile(0.95,` |
| 671 | url_fix_backups/monitoring/prometheus_integration.py | 30 | 31 | '(' was never closed | `from prometheus_client import (CONTENT_TYPE_LATEST, CollectorRegistry, Counter, Gauge,` |
| 672 | url_fix_backups/orchestrator/main.py | 143 | 17 | unterminated string literal (detected at line 143) | `description="Task priority (1 - 10,` |
| 673 | integrations/puppeteer_service.py | 58 | 25 | unterminated string literal (detected at line 58) | `"--user - agent = Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML,` |
| 674 | scripts/environment_validator.py | 109 | 27 | unterminated string literal (detected at line 109) | `version_str = f"{` |
| 675 | scripts/system_orchestrator.py | 200 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 190 | `},` |
| 676 | scripts/generate_realistic_avatar.py | 100 | 25 | unterminated string literal (detected at line 100) | `f"Unusual aspect ratio {` |
| 677 | scripts/repair-model-generation.py | 92 | 21 | unterminated string literal (detected at line 92) | `f"Only {` |
| 678 | scripts/load-test.py | 634 | 17 | unterminated string literal (detected at line 634) | `f"  Avg Response Time: {` |
| 679 | scripts/go_live_preparation.py | 31 | 13 | invalid syntax. Perhaps you forgot a comma? | `logging.StreamHandler()` |
| 680 | scripts/synthesize_release_v3.py | 177 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 169 | `}` |
| 681 | scripts/production_deployment.py | 53 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `logger = logging.getLogger(__name__)` |
| 682 | scripts/start_distributed_system.py | 39 | 1 | invalid syntax | `class DistributedSystemOrchestrator:` |
| 683 | scripts/deployment_orchestrator.py | 812 | 21 | unterminated string literal (detected at line 812) | `f"High response time detected: {` |
| 684 | scripts/doctor_creative_env.py | 134 | 13 | unterminated string literal (detected at line 134) | `f"Failed to install dependencies. pip exited with status {` |
| 685 | .venv311/lib/python3.11/site-packages/pycodestyle.py | 66 | 9 | invalid syntax. Perhaps you forgot a comma? | `sys.version_info < (3, 10) and` |
| 686 | .venv311/lib/python3.11/site-packages/autopep8.py | 112 | 5 | invalid syntax. Perhaps you forgot a comma? | `r'^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)'` |
| 687 | .venv311/lib/python3.11/site-packages/sympy/core/add.py | 31 | 5 | invalid syntax | `positive_args = len(expr.args) - negative_args` |
| 688 | .venv311/lib/python3.11/site-packages/sympy/core/exprtools.py | 25 | 1 | invalid syntax | `from collections import defaultdict` |
| 689 | .venv311/lib/python3.11/site-packages/sympy/core/mul.py | 397 | 41 | unindent does not match any outer indentation level | `return [S.NaN], [], None` |
| 690 | .venv311/lib/python3.11/site-packages/sympy/core/function.py | 60 | 1 | invalid syntax | `from sympy.utilities.iterables import (has_dups, sift, iterable,` |
| 691 | .venv311/lib/python3.11/site-packages/sympy/core/expr.py | 184 | 16 | invalid syntax. Perhaps you forgot a comma? | `args = (len(args), tuple(args))` |
| 692 | .venv311/lib/python3.11/site-packages/sympy/concrete/expr_with_limits.py | 14 | 1 | invalid syntax | `from sympy.logic.boolalg import BooleanFunction` |
| 693 | .venv311/lib/python3.11/site-packages/sympy/printing/str.py | 102 | 5 | invalid syntax | `def _print_Basic(self, expr):` |
| 694 | .venv311/lib/python3.11/site-packages/sympy/printing/latex.py | 48 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `tex_greek_dictionary = {` |
| 695 | .venv311/lib/python3.11/site-packages/sympy/printing/pretty/pretty.py | 380 | 44 | invalid syntax | `if (count_total_deriv > 1) != False:` |
| 696 | .venv311/lib/python3.11/site-packages/sympy/logic/boolalg.py | 218 | 5 | invalid syntax | `def binary_symbols(self):` |
| 697 | .venv311/lib/python3.11/site-packages/sympy/logic/algorithms/lra_theory.py | 473 | 23 | unindent does not match any outer indentation level | `M = self.A` |
| 698 | .venv311/lib/python3.11/site-packages/sympy/solvers/bivariate.py | 79 | 5 | invalid syntax | `if len(fterms) == 1:` |
| 699 | .venv311/lib/python3.11/site-packages/sympy/solvers/solvers.py | 25 | 1 | invalid syntax | `from sympy.core.logic import fuzzy_not, fuzzy_and` |
| 700 | .venv311/lib/python3.11/site-packages/sympy/solvers/simplex.py | 149 | 9 | invalid syntax. Perhaps you forgot a comma? | `A = M - Mj * (Mi / Mij)` |
| 701 | .venv311/lib/python3.11/site-packages/sympy/solvers/solveset.py | 18 | 1 | invalid syntax | `from sympy.core.containers import Tuple` |
| 702 | .venv311/lib/python3.11/site-packages/sympy/solvers/ode/subscheck.py | 130 | 13 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `funcs = set().union(*funcs)` |
| 703 | .venv311/lib/python3.11/site-packages/sympy/solvers/ode/systems.py | 12 | 1 | invalid syntax | `from sympy.functions import (exp, im, cos, sin, re, Piecewise,` |
| 704 | .venv311/lib/python3.11/site-packages/sympy/solvers/ode/ode.py | 238 | 1 | invalid syntax | `from sympy.core.multidimensional import vectorize` |
| 705 | .venv311/lib/python3.11/site-packages/sympy/testing/tests/test_code_quality.py | 84 | 25 | unindent does not match any outer indentation level | `continue` |
| 706 | .venv311/lib/python3.11/site-packages/sympy/integrals/meijerint.py | 43 | 1 | invalid syntax | `from sympy.core.mul import Mul` |
| 707 | .venv311/lib/python3.11/site-packages/sympy/integrals/transforms.py | 10 | 1 | invalid syntax | `from sympy.core.mul import Mul` |
| 708 | .venv311/lib/python3.11/site-packages/sympy/integrals/integrals.py | 102 | 9 | invalid syntax | `return obj` |
| 709 | .venv311/lib/python3.11/site-packages/sympy/assumptions/handlers/matrices.py | 16 | 1 | invalid syntax | `from sympy.matrices.expressions.blockmatrix import reblock_2x2` |
| 710 | .venv311/lib/python3.11/site-packages/sympy/assumptions/handlers/order.py | 26 | 1 | invalid syntax | `def _NegativePredicate_number(expr, assumptions):` |
| 711 | .venv311/lib/python3.11/site-packages/sympy/plotting/series.py | 15 | 1 | invalid syntax | `from sympy.core.sympify import sympify` |
| 712 | .venv311/lib/python3.11/site-packages/sympy/sets/sets.py | 2331 | 33 | unterminated string literal (detected at line 2332) | `raise TypeError("Invalid input: '%s', input args \` |
| 713 | .venv311/lib/python3.11/site-packages/sympy/interactive/printing.py | 72 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dvioptions = dvi.split()` |
| 714 | .venv311/lib/python3.11/site-packages/sympy/functions/special/hyper.py | 22 | 1 | invalid syntax | `from sympy.functions import factorial, RisingFactorial` |
| 715 | .venv311/lib/python3.11/site-packages/sympy/functions/combinatorial/numbers.py | 28 | 1 | invalid syntax | `from sympy.functions.elementary.exponential import log` |
| 716 | .venv311/lib/python3.11/site-packages/sympy/functions/elementary/integers.py | 49 | 9 | invalid syntax | `for t in Add.make_args(arg):` |
| 717 | .venv311/lib/python3.11/site-packages/sympy/functions/elementary/complexes.py | 10 | 1 | invalid syntax | `from sympy.core.logic import fuzzy_not, fuzzy_or` |
| 718 | .venv311/lib/python3.11/site-packages/sympy/functions/elementary/trigonometric.py | 24 | 1 | invalid syntax | `from sympy.logic.boolalg import And` |
| 719 | .venv311/lib/python3.11/site-packages/sympy/tensor/array/array_comprehension.py | 38 | 30 | invalid syntax. Perhaps you forgot a comma? | `raise ValueError('ArrayComprehension requires values lower and upper bound'` |
| 720 | .venv311/lib/python3.11/site-packages/sympy/physics/control/lti.py | 36 | 1 | invalid syntax | `def _roots(poly, var):` |
| 721 | .venv311/lib/python3.11/site-packages/sympy/physics/optics/gaussopt.py | 46 | 1 | invalid syntax | `from sympy.core.expr import Expr` |
| 722 | .venv311/lib/python3.11/site-packages/sympy/physics/quantum/gate.py | 39 | 1 | invalid syntax | `from sympy.physics.quantum.matrixutils import matrix_tensor_product, matrix_eye` |
| 723 | .venv311/lib/python3.11/site-packages/sympy/parsing/autolev/_listener_autolev_antlr.py | 19 | 17 | invalid syntax. Perhaps you forgot a comma? | `AutolevParser = getattr(autolevparser, 'AutolevParser', None)` |
| 724 | .venv311/lib/python3.11/site-packages/sympy/simplify/combsimp.py | 54 | 31 | unindent does not match any outer indentation level | `return gammasimp(expr)` |
| 725 | .venv311/lib/python3.11/site-packages/sympy/simplify/hyperexpand.py | 71 | 1 | invalid syntax | `from sympy.core.mod import Mod` |
| 726 | .venv311/lib/python3.11/site-packages/sympy/vector/coordsysrect.py | 27 | 1 | invalid syntax | `class CoordSys3D(Basic):` |
| 727 | .venv311/lib/python3.11/site-packages/sympy/diffgeom/diffgeom.py | 14 | 1 | invalid syntax | `from sympy.core.cache import cacheit` |
| 728 | .venv311/lib/python3.11/site-packages/sympy/stats/stochastic_process_types.py | 49 | 1 | invalid syntax | `from sympy.stats.stochastic_process import StochasticPSpace` |
| 729 | .venv311/lib/python3.11/site-packages/sympy/matrices/matrixbase.py | 53 | 1 | invalid syntax | `from .utilities import _iszero, _is_zero_after_expand_mul` |
| 730 | .venv311/lib/python3.11/site-packages/sympy/matrices/expressions/matmul.py | 12 | 1 | invalid syntax | `from sympy.matrices.exceptions import NonInvertibleMatrixError` |
| 731 | .venv311/lib/python3.11/site-packages/pygments/lexers/_postgres_builtins.py | 572 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `PSEUDO_TYPES = tuple(sorted(set(PSEUDO_TYPES) - set(map(str.lower, KEYWORDS))))` |
| 732 | .venv311/lib/python3.11/site-packages/pygments/lexers/objective.py | 197 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 191 | `}` |
| 733 | .venv311/lib/python3.11/site-packages/pygments/lexers/modula2.py | 355 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 338 | `}` |
| 734 | .venv311/lib/python3.11/site-packages/pygments/lexers/sql.py | 225 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 218 | `}` |
| 735 | .venv311/lib/python3.11/site-packages/kombu/serialization.py | 17 | 1 | invalid syntax | `from .utils.compat import entrypoints` |
| 736 | .venv311/lib/python3.11/site-packages/kombu/transport/redis.py | 127 | 1 | invalid syntax | `def get_redis_error_classes():` |
| 737 | .venv311/lib/python3.11/site-packages/kombu/transport/virtual/exchange.py | 59 | 1 | invalid syntax | `class DirectExchange(ExchangeType):` |
| 738 | .venv311/lib/python3.11/site-packages/flask_cors/core.py | 45 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `FLASK_CORS_EVALUATED = '_FLASK_CORS_EVALUATED'` |
| 739 | .venv311/lib/python3.11/site-packages/docutils/nodes.py | 157 | 9 | invalid syntax | `try:` |
| 740 | .venv311/lib/python3.11/site-packages/docutils/parsers/rst/tableparser.py | 83 | 17 | invalid syntax | `else:` |
| 741 | .venv311/lib/python3.11/site-packages/docutils/utils/__init__.py | 82 | 5 | invalid syntax | `def __init__(self, source, report_level, halt_level, stream=None,` |
| 742 | .venv311/lib/python3.11/site-packages/docutils/transforms/frontmatter.py | 127 | 9 | invalid syntax | `return True` |
| 743 | .venv311/lib/python3.11/site-packages/docutils/transforms/references.py | 88 | 13 | expression cannot contain assignment, perhaps you meant "=="? | `target['refid'] = target['ids'][0]` |
| 744 | .venv311/lib/python3.11/site-packages/docutils/transforms/universal.py | 68 | 1 | expected ':' | `#                or settings.source_url:` |
| 745 | .venv311/lib/python3.11/site-packages/mpmath/libmp/gammazeta.py | 40 | 1 | invalid syntax | `from .libelefun import (\` |
| 746 | .venv311/lib/python3.11/site-packages/mpmath/functions/hypergeometric.py | 47 | 1 | expected ':' | `#             and not have_singular_nongamma_weight:` |
| 747 | .venv311/lib/python3.11/site-packages/pyppeteer/launcher.py | 62 | 17 | invalid syntax | `AUTOMATION_ARGS = [` |
| 748 | .venv311/lib/python3.11/site-packages/IPython/core/prefilter.py | 25 | 1 | invalid syntax | `from .macro import Macro` |
| 749 | .venv311/lib/python3.11/site-packages/IPython/core/completerlib.py | 55 | 24 | expression cannot contain assignment, perhaps you meant "=="? | `import_re = re.compile(r'(?P<name>[^\W\d]\w*?)'` |
| 750 | .venv311/lib/python3.11/site-packages/IPython/core/inputtransformer2.py | 89 | 16 | invalid syntax. Perhaps you forgot a comma? | `initial_re=re.compile(r'^>>>( ¦$)')` |
| 751 | .venv311/lib/python3.11/site-packages/IPython/core/magics/namespace.py | 63 | 5 | invalid syntax | `@line_magic` |
| 752 | .venv311/lib/python3.11/site-packages/IPython/terminal/interactiveshell.py | 633 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 623 | `),` |
| 753 | .venv311/lib/python3.11/site-packages/IPython/terminal/pt_inputhooks/qt.py | 31 | 1 | expected ':' | `#                     and not os.environ.get('WAYLAND_DISPLAY'):` |
| 754 | .venv311/lib/python3.11/site-packages/IPython/utils/wildcard.py | 91 | 1 | invalid syntax | `def list_namespace(namespace, type_pattern, filter, ignore_case=False, show_all=False):` |
| 755 | .venv311/lib/python3.11/site-packages/markdown/treeprocessors.py | 141 | 31 | invalid syntax | `if not matched:` |
| 756 | .venv311/lib/python3.11/site-packages/gast/gast.py | 41 | 9 | invalid syntax | `for i in range(len(args)):` |
| 757 | .venv311/lib/python3.11/site-packages/jedi/parser_utils.py | 23 | 1 | invalid syntax | `def get_executable_nodes(node, last_added=False):` |
| 758 | .venv311/lib/python3.11/site-packages/jedi/plugins/django.py | 46 | 1 | invalid syntax | `@inference_state_function_cache()` |
| 759 | .venv311/lib/python3.11/site-packages/jedi/plugins/pytest.py | 23 | 1 | invalid syntax | `def execute(callback):` |
| 760 | .venv311/lib/python3.11/site-packages/jedi/plugins/stdlib.py | 162 | 13 | invalid syntax | `except ParamIssue:` |
| 761 | .venv311/lib/python3.11/site-packages/jedi/api/completion.py | 42 | 1 | expected ':' | `#                     and p.name not in used_kwargs:` |
| 762 | .venv311/lib/python3.11/site-packages/jedi/api/__init__.py | 120 | 59 | invalid syntax. Perhaps you forgot a comma? | `project, environment=environment, script_path=self.path` |
| 763 | .venv311/lib/python3.11/site-packages/jedi/api/classes.py | 85 | 5 | invalid syntax | `def __init__(self, inference_state, name):` |
| 764 | .venv311/lib/python3.11/site-packages/jedi/api/helpers.py | 55 | 1 | invalid syntax | `def get_on_completion_name(module_node, lines, position):` |
| 765 | .venv311/lib/python3.11/site-packages/jedi/api/project.py | 97 | 5 | invalid syntax | `def save(self):` |
| 766 | .venv311/lib/python3.11/site-packages/jedi/api/file_name.py | 53 | 37 | '(' was never closed | `yield classes.Completion(` |
| 767 | .venv311/lib/python3.11/site-packages/jedi/api/refactoring/__init__.py | 122 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 116 | `}` |
| 768 | .venv311/lib/python3.11/site-packages/jedi/api/refactoring/extract.py | 20 | 1 | invalid syntax | `def extract_variable(inference_state, path, module_node, name, pos, until_pos):` |
| 769 | .venv311/lib/python3.11/site-packages/jedi/inference/finder.py | 73 | 26 | '[' was never closed | `names = reversed([` |
| 770 | .venv311/lib/python3.11/site-packages/jedi/inference/analysis.py | 58 | 5 | invalid syntax | `def __eq__(self, other):` |
| 771 | .venv311/lib/python3.11/site-packages/jedi/inference/sys_path.py | 111 | 1 | expected ':' | `#                         and c[1].type == 'trailer':` |
| 772 | .venv311/lib/python3.11/site-packages/jedi/inference/references.py | 54 | 1 | invalid syntax | `def _find_defining_names(module_context, tree_name):` |
| 773 | .venv311/lib/python3.11/site-packages/jedi/inference/flow_analysis.py | 49 | 1 | expected ':' | `#             or not context.inference_state.flow_analysis_enabled:` |
| 774 | .venv311/lib/python3.11/site-packages/jedi/inference/docstrings.py | 45 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `REST_ROLE_PATTERN = re.compile(r':[^`]+:`([^`]+)`')` |
| 775 | .venv311/lib/python3.11/site-packages/jedi/inference/dynamic_params.py | 94 | 29 | Generator expression must be parenthesized | `function_value, arguments` |
| 776 | .venv311/lib/python3.11/site-packages/jedi/inference/syntax_tree.py | 71 | 1 | expected ':' | `#                     and context.get_value() is inference_state.builtins_module:` |
| 777 | .venv311/lib/python3.11/site-packages/jedi/inference/star_args.py | 40 | 1 | expected ':' | `#                     and argument.children[0] == '*' * param_name.star_count:` |
| 778 | .venv311/lib/python3.11/site-packages/jedi/inference/value/instance.py | 32 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self._instance = instance` |
| 779 | .venv311/lib/python3.11/site-packages/jedi/inference/value/dynamic_arrays.py | 99 | 1 | expected ':' | `#                             or execution_trailer.children[0] != '(' \` |
| 780 | .venv311/lib/python3.11/site-packages/jedi/inference/value/klass.py | 72 | 9 | invalid syntax | `for result_value in inferred:` |
| 781 | .venv311/lib/python3.11/site-packages/jedi/inference/value/function.py | 78 | 5 | invalid syntax | `def name(self):` |
| 782 | .venv311/lib/python3.11/site-packages/jedi/inference/compiled/access.py | 42 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `MethodDescriptorType = type(str.replace)` |
| 783 | .venv311/lib/python3.11/site-packages/jedi/inference/compiled/value.py | 61 | 9 | invalid syntax | `try:` |
| 784 | .venv311/lib/python3.11/site-packages/jedi/inference/compiled/getattr_static.py | 102 | 1 | expected ':' | `#                 and _safe_is_data_descriptor(klass_result):` |
| 785 | .venv311/lib/python3.11/site-packages/pyquery/pyquery.py | 47 | 1 | invalid syntax | `def with_camel_case_alias(func):` |
| 786 | .venv311/lib/python3.11/site-packages/Cython/Distutils/old_build_ext.py | 63 | 9 | cannot assign to attribute here. Maybe you meant '==' instead of '='? | `self.state = sysconfig.get_config_vars(*self.flags)` |
| 787 | .venv311/lib/python3.11/site-packages/Cython/Compiler/Optimize.py | 1190 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 1184 | `)),` |
| 788 | .venv311/lib/python3.11/site-packages/Cython/Compiler/Symtab.py | 22 | 1 | invalid syntax | `from . import DebugFlags` |
| 789 | .venv311/lib/python3.11/site-packages/Cython/Compiler/ParseTreeTransforms.py | 1802 | 33 | closing parenthesis ')' does not match opening parenthesis '[' on line 1789 | `else_clause=None),` |
| 790 | .venv311/lib/python3.11/site-packages/Cython/Compiler/ExprNodes.py | 5797 | 40 | too many nested parentheses | `start=copy.deepcopy(self.start or none_node),` |
| 791 | .venv311/lib/python3.11/site-packages/engineio/server.py | 214 | 25 | invalid syntax. Perhaps you forgot a comma? | `r = self._bad_request('Not an accepted origin.')` |
| 792 | .venv311/lib/python3.11/site-packages/engineio/async_server.py | 204 | 17 | invalid syntax | `for client in self.sockets.values()` |
| 793 | .venv311/lib/python3.11/site-packages/numpy/ctypeslib.py | 57 | 1 | invalid syntax | `import os` |
| 794 | .venv311/lib/python3.11/site-packages/numpy/distutils/ccompiler.py | 17 | 1 | invalid syntax | `from distutils.errors import (` |
| 795 | .venv311/lib/python3.11/site-packages/numpy/distutils/misc_util.py | 50 | 1 | invalid syntax | `class InstallableLib:` |
| 796 | .venv311/lib/python3.11/site-packages/numpy/distutils/system_info.py | 3071 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 3064 | `}` |
| 797 | .venv311/lib/python3.11/site-packages/numpy/distutils/core.py | 152 | 33 | invalid syntax. Perhaps you forgot a comma? | `raise TypeError("invalid description of extension module "` |
| 798 | .venv311/lib/python3.11/site-packages/numpy/distutils/fcompiler/__init__.py | 21 | 1 | invalid syntax | `import os` |
| 799 | .venv311/lib/python3.11/site-packages/numpy/distutils/command/build_src.py | 24 | 1 | invalid syntax | `from numpy.distutils.from_template import process_file as process_f_file` |
| 800 | .venv311/lib/python3.11/site-packages/numpy/f2py/cfuncs.py | 96 | 1 | cannot assign to subscript here. Maybe you meant '==' instead of '='? | `typedefs['complex_float'] = 'typedef struct {float r,i;} complex_float;'` |
| 801 | .venv311/lib/python3.11/site-packages/numpy/f2py/crackfortran.py | 273 | 5 | cannot assign to subscript here. Maybe you meant '==' instead of '='? | `badnames[n] = n + '_bn'` |
| 802 | .venv311/lib/python3.11/site-packages/numpy/testing/_private/utils.py | 26 | 1 | invalid syntax | `from numpy import isfinite, isnan, isinf` |
| 803 | .venv311/lib/python3.11/site-packages/numpy/lib/_arraypad_impl.py | 115 | 5 | invalid syntax | `order = 'F' if array.flags.fnc else 'C'  # Fortran and not also C-order` |
| 804 | .venv311/lib/python3.11/site-packages/numpy/lib/_function_base_impl.py | 17 | 1 | invalid syntax | `from numpy._core.umath import (` |
| 805 | .venv311/lib/python3.11/site-packages/pasta/base/codegen.py | 126 | 20 | unindent does not match any outer indentation level | `val = default` |
| 806 | .venv311/lib/python3.11/site-packages/safety/alerts/requirements.py | 35 | 5 | invalid syntax | `def is_valid(self):` |
| 807 | .venv311/lib/python3.11/site-packages/babel/messages/extract.py | 35 | 1 | invalid syntax | `from functools import lru_cache` |
| 808 | .venv311/lib/python3.11/site-packages/socketio/server.py | 174 | 5 | invalid syntax | `def send(self, data, to=None, room=None, skip_sid=None, namespace=None,` |
| 809 | .venv311/lib/python3.11/site-packages/socketio/async_server.py | 124 | 5 | invalid syntax | `def is_asyncio_based(self):` |
| 810 | .venv311/lib/python3.11/site-packages/sphinx/directives/__init__.py | 225 | 13 | invalid syntax. Perhaps you forgot a comma? | `'no-index' in self.options` |
| 811 | .venv311/lib/python3.11/site-packages/sphinx/ext/intersphinx.py | 144 | 5 | invalid syntax. Perhaps you forgot a comma? | `r.raise_for_status()` |
| 812 | .venv311/lib/python3.11/site-packages/tensorflow/python/autograph/impl/conversion.py | 76 | 9 | invalid syntax. Perhaps you forgot a comma? | `'{} appears to be decorated by wrapt, which is not yet supported'` |
| 813 | .venv311/lib/python3.11/site-packages/tensorflow/python/keras/metrics.py | 155 | 22 | expected 'else' after 'if' expression | `self._dtype = (backend.floatx() if dtype is None` |
| 814 | .venv311/lib/python3.11/site-packages/tensorflow/python/keras/layers/core.py | 127 | 15 | invalid syntax. Perhaps you forgot a comma? | `outputs = inputs * math_ops.cast(boolean_mask, inputs.dtype)` |
| 815 | .venv311/lib/python3.11/site-packages/tensorflow/python/keras/engine/base_layer_utils.py | 144 | 1 | invalid syntax | `def collect_previous_mask(input_tensors):` |
| 816 | .venv311/lib/python3.11/site-packages/tensorflow/python/keras/engine/training_eager_v1.py | 64 | 7 | invalid syntax | `targets = new_targets` |
| 817 | .venv311/lib/python3.11/site-packages/tensorflow/python/keras/engine/training.py | 101 | 5 | invalid syntax | `return method(self, *args, **kwargs)` |
| 818 | .venv311/lib/python3.11/site-packages/tensorflow/python/tools/api/generator/create_python_api.py | 100 | 3 | invalid syntax | `return import_list[0][0]` |
| 819 | .venv311/lib/python3.11/site-packages/tensorflow/python/checkpoint/functional_saver.py | 478 | 79 | closing parenthesis '}' does not match opening parenthesis '[' on line 473 | `for task, shardable_tensors in self._shardable_tensors_by_task.items()}` |
| 820 | .venv311/lib/python3.11/site-packages/tensorflow/python/checkpoint/restore.py | 104 | 7 | invalid syntax | `return False  # Not a new assignment` |
| 821 | .venv311/lib/python3.11/site-packages/tensorflow/python/saved_model/tracing_utils.py | 46 | 35 | unindent does not match any outer indentation level | `raise NotImplementedError(` |
| 822 | .venv311/lib/python3.11/site-packages/tensorflow/python/framework/type_spec.py | 177 | 9 | invalid syntax | `if attribute_supertype is None:` |
| 823 | .venv311/lib/python3.11/site-packages/tensorflow/python/kernel_tests/nn_ops/depthwise_conv_op_base.py | 63 | 13 | invalid syntax. Perhaps you forgot a comma? | `x1[:, start_height:end_height, start_width:end_width, k, np.newaxis]` |
| 824 | .venv311/lib/python3.11/site-packages/tensorflow/python/training/queue_runner_impl.py | 35 | 1 | invalid syntax | `@tf_export(v1=["train.queue_runner.QueueRunner", "train.QueueRunner"])` |
| 825 | .venv311/lib/python3.11/site-packages/tensorflow/python/training/saving/saveable_object_util.py | 580 | 5 | closing parenthesis '}' does not match opening parenthesis '(' on line 574 | `}` |
| 826 | .venv311/lib/python3.11/site-packages/tensorflow/python/distribute/mirrored_strategy.py | 87 | 40 | invalid syntax | `if num_workers == 1 and not all_local:` |
| 827 | .venv311/lib/python3.11/site-packages/tensorflow/python/distribute/ps_values.py | 52 | 1 | invalid syntax | `class AggregatingVariable(resource_variable_ops.BaseResourceVariable,` |
| 828 | .venv311/lib/python3.11/site-packages/tensorflow/python/distribute/single_loss_example.py | 49 | 3 | invalid syntax | `return single_loss_step, layer` |
| 829 | .venv311/lib/python3.11/site-packages/tensorflow/python/distribute/cross_device_ops.py | 82 | 42 | invalid syntax | `if not check_destinations(destinations):` |
| 830 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/special_math_ops.py | 612 | 1 | invalid syntax | `def _enclosing_tpu_context():` |
| 831 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/sparse_ops.py | 142 | 14 | invalid syntax. Perhaps you forgot a comma? | `values = array_ops.gather_nd(tensor, indices)` |
| 832 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/parsing_ops.py | 50 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_construct_sparse_tensors_for_sparse_features = \` |
| 833 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/cond_v2.py | 110 | 5 | positional argument follows keyword argument | `return _build_cond(` |
| 834 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/control_flow_ops.py | 87 | 1 | invalid syntax | `def _NextIteration(tensor, name=None):` |
| 835 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/gradients_util.py | 130 | 3 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `pending_count = collections.defaultdict(int)` |
| 836 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/math_ops.py | 194 | 13 | invalid syntax. Perhaps you forgot a comma? | `start = array_ops.broadcast_to(start, broadcast_shape)` |
| 837 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/embedding_ops.py | 79 | 13 | expected 'else' after 'if' expression | `axes=(list(range(ids_rank, params_rank)) if ids_static and params_static` |
| 838 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/linalg/linear_operator_util.py | 116 | 5 | invalid syntax | `return value` |
| 839 | .venv311/lib/python3.11/site-packages/tensorflow/python/ops/distributions/student_t.py | 44 | 1 | invalid syntax | `@tf_export(v1=["distributions.StudentT"])` |
| 840 | .venv311/lib/python3.11/site-packages/tensorflow/python/tpu/device_assignment.py | 96 | 23 | invalid syntax. Perhaps you forgot a comma? | `core_assignment = numpy_compat.np_asarray(core_assignment, dtype=np.int32)` |
| 841 | .venv311/lib/python3.11/site-packages/tensorflow/python/data/experimental/ops/parsing_ops.py | 37 | 23 | invalid syntax. Perhaps you forgot a comma? | `raise TypeError("Input dataset should be a dataset of vectors of "` |
| 842 | .venv311/lib/python3.11/site-packages/tensorflow/python/data/ops/from_generator_op.py | 125 | 33 | invalid syntax | `if output_shapes is not None:` |
| 843 | .venv311/lib/python3.11/site-packages/tensorflow/python/eager/backprop_util.py | 50 | 26 | unindent does not match any outer indentation level | `return first_type` |
| 844 | .venv311/lib/python3.11/site-packages/tensorflow/python/eager/polymorphic_function/concrete_function.py | 99 | 3 | invalid syntax. Perhaps you forgot a comma? | `backward_function_attr.update(common_attributes)` |
| 845 | .venv311/lib/python3.11/site-packages/tensorflow/python/eager/polymorphic_function/polymorphic_function.py | 124 | 1 | invalid syntax | `class _FrequentTracingDetector(object):` |
| 846 | .venv311/lib/python3.11/site-packages/tensorflow/python/debug/cli/command_parser.py | 56 | 1 | invalid syntax | `def parse_command(command):` |
| 847 | .venv311/lib/python3.11/site-packages/tensorflow/python/debug/lib/debug_data.py | 237 | 1 | invalid syntax | `def extract_core_metadata_from_event_proto(event):` |
| 848 | .venv311/lib/python3.11/site-packages/tensorboard/_vendor/bleach/_vendor/html5lib/html5parser.py | 28 | 1 | invalid syntax | `def parse(doc, treebuilder="etree", namespaceHTMLElements=True, **kwargs):` |
| 849 | .venv311/lib/python3.11/site-packages/tensorboard/_vendor/bleach/_vendor/html5lib/_tokenizer.py | 1498 | 55 | too many nested parentheses | `self.tokenQueue.append({"type": tokenTypes["ParseError"], "data":` |
| 850 | .venv311/lib/python3.11/site-packages/tensorboard/_vendor/bleach/_vendor/html5lib/filters/whitespace.py | 21 | 1 | expected ':' | `#                     and (preserve or token["name"] in self.spacePreserveElements):` |
| 851 | .venv311/lib/python3.11/site-packages/yaml/scanner.py | 268 | 5 | invalid syntax | `def next_possible_simple_key(self):` |
| 852 | .venv311/lib/python3.11/site-packages/yaml/error.py | 66 | 76 | unmatched ')' | `or self.context_mark.column != self.problem_mark.column):` |
| 853 | .venv311/lib/python3.11/site-packages/yaml/representer.py | 7 | 1 | invalid syntax | `from .error import *` |
| 854 | .venv311/lib/python3.11/site-packages/yaml/reader.py | 41 | 9 | invalid syntax | `else:` |
| 855 | .venv311/lib/python3.11/site-packages/yaml/resolver.py | 73 | 1 | expected ':' | `#                     and not isinstance(node_check, str) \` |
| 856 | .venv311/lib/python3.11/site-packages/yaml/emitter.py | 172 | 5 | invalid syntax | `def expect_nothing(self):` |
| 857 | .venv311/lib/python3.11/site-packages/mesonbuild/interpreter/interpreter.py | 810 | 54 | closing parenthesis ')' does not match opening parenthesis '[' on line 806 | `kwargs: 'kwtypes.RunCommand') -> RunProcess:` |
| 858 | .venv311/lib/python3.11/site-packages/mesonbuild/linkers/linkers.py | 246 | 5 | invalid syntax | `def get_allow_undefined_args(self) -> T.List[str]:` |
| 859 | .venv311/lib/python3.11/site-packages/mesonbuild/dependencies/ui.py | 20 | 1 | invalid syntax | `from ..environment import detect_cpu_family` |
| 860 | .venv311/lib/python3.11/site-packages/mesonbuild/dependencies/mpi.py | 84 | 5 | invalid syntax | `if DependencyMethods.SYSTEM in methods and env.machines[for_machine].is_windows():` |
| 861 | .venv311/lib/python3.11/site-packages/flasgger/utils.py | 59 | 11 | invalid syntax. Perhaps you forgot a comma? | `= swagger.config.get('optional_fields') or OPTIONAL_FIELDS` |
| 862 | .venv311/lib/python3.11/site-packages/celery/platforms.py | 51 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `EX_OK = getattr(os, 'EX_OK', 0)` |
| 863 | .venv311/lib/python3.11/site-packages/celery/backends/mongodb.py | 265 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 259 | `}` |
| 864 | .venv311/lib/python3.11/site-packages/feedparser/api.py | 114 | 1 | expected ':' | `#        and urllib.parse.urlparse(url_file_stream_or_string)[0] in ('http', 'https', 'ftp', 'file', 'feed'):` |
| 865 | .venv311/lib/python3.11/site-packages/parso/python/tree.py | 60 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_RETURN_STMT_CONTAINERS = set(['suite', 'simple_stmt']) ¦ _FLOW_CONTAINERS` |
| 866 | .venv311/lib/python3.11/site-packages/parso/python/pep8.py | 15 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_NON_STAR_TYPES = ('term', 'import_from', 'power')` |
| 867 | .venv311/lib/python3.11/site-packages/parso/python/diff.py | 110 | 1 | expected ':' | `#                     and node.get_start_pos_of_prefix() == (1, 0):` |
| 868 | .venv311/lib/python3.11/site-packages/parso/python/errors.py | 22 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_COMP_FOR_TYPES = ('comp_for', 'sync_comp_for')` |
| 869 | .venv311/lib/python3.11/site-packages/parso/python/tokenize.py | 116 | 5 | invalid syntax. Perhaps you forgot a comma? | `r'(?:\{\{¦\}\}¦\\N\{' + unicode_character_name` |
| 870 | .venv311/lib/python3.11/site-packages/parso/pgen2/grammar_parser.py | 45 | 26 | invalid syntax. Perhaps you forgot a comma? | `version_info=parse_version_string('3.9')` |
| 871 | .venv311/lib/python3.11/site-packages/reportlab/lib/testutils.py | 106 | 1 | invalid syntax | `def mockUrlRead(name):` |
| 872 | .venv311/lib/python3.11/site-packages/reportlab/graphics/barcode/lto.py | 46 | 1 | expected ':' | `#             or (subtype not in ascii_uppercase + string_digits) :` |
| 873 | .venv311/lib/python3.11/site-packages/reportlab/graphics/barcode/code128.py | 272 | 1 | expected ':' | `#                     and l[i+1] in digits:` |
| 874 | .venv311/lib/python3.11/site-packages/billiard/pool.py | 34 | 1 | invalid syntax | `from .compat import get_errno, mem_rss, send_offset` |
| 875 | .venv311/lib/python3.11/site-packages/future/backports/email/_header_value_parser.py | 210 | 5 | invalid syntax | `@property` |
| 876 | .venv311/lib/python3.11/site-packages/future/backports/email/feedparser.py | 193 | 1 | expected ':' | `#                and not root.is_multipart():` |
| 877 | .venv311/lib/python3.11/site-packages/future/standard_library/__init__.py | 244 | 1 | invalid syntax | `class RenameImport(object):` |
| 878 | .venv311/lib/python3.11/site-packages/scipy/odr/_odrpack.py | 51 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `odr = __odrpack.odr` |
| 879 | .venv311/lib/python3.11/site-packages/scipy/optimize/_shgo.py | 489 | 30 | invalid syntax. Perhaps you forgot a comma? | `shc.fail_routine(mes="Failed to find a feasible minimizer point. "` |
| 880 | .venv311/lib/python3.11/site-packages/scipy/optimize/_linprog_simplex.py | 237 | 13 | invalid syntax. Perhaps you forgot a comma? | `f"The pivot operation produces a pivot value of:{pivval: .1e}, "` |
| 881 | .venv311/lib/python3.11/site-packages/scipy/optimize/_minimize.py | 26 | 1 | invalid syntax | `from ._trustregion_dogleg import _minimize_dogleg` |
| 882 | .venv311/lib/python3.11/site-packages/scipy/optimize/_trustregion_constr/qp_subproblem.py | 22 | 1 | invalid syntax | `def eqp_kktfact(H, c, A, b):` |
| 883 | .venv311/lib/python3.11/site-packages/scipy/interpolate/_polyint.py | 11 | 9 | invalid syntax | `__all__ = ["KroghInterpolator", "krogh_interpolate",` |
| 884 | .venv311/lib/python3.11/site-packages/scipy/interpolate/_interpolate.py | 173 | 1 | invalid syntax | `def _do_extrapolate(fill_value):` |
| 885 | .venv311/lib/python3.11/site-packages/scipy/sparse/_coo.py | 19 | 1 | invalid syntax | `from ._base import issparse, SparseEfficiencyWarning, _spbase, sparray` |
| 886 | .venv311/lib/python3.11/site-packages/scipy/signal/_signaltools.py | 119 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 115 | `):` |
| 887 | .venv311/lib/python3.11/site-packages/email_validator/validate_email.py | 93 | 22 | expected 'else' after 'if' expression | `ret.original = ((local_part if not is_quoted_local_part` |
| 888 | .venv311/lib/python3.11/site-packages/dateutil/parser/_parser.py | 69 | 29 | invalid syntax. Perhaps you forgot a comma? | `raise TypeError('Parser must be a string or character stream, not '` |
| 889 | .venv311/lib/python3.11/site-packages/pyflakes/checker.py | 50 | 1 | invalid syntax | `def _is_tuple_constant(node):  # type: (ast.AST) -> bool` |
| 890 | .venv311/lib/python3.11/site-packages/passlib/tests/test_ext_django_source.py | 21 | 1 | invalid syntax | `if has_min_django:` |
| 891 | venv_creative/lib/python3.13/site-packages/soundfile.py | 175 | 5 | invalid syntax | `elif _sys.platform == 'linux':` |
| 892 | venv_creative/lib/python3.13/site-packages/socks.py | 109 | 1 | closing parenthesis '}' does not match opening parenthesis '(' on line 105 | `}` |
| 893 | venv_creative/lib/python3.13/site-packages/six.py | 41 | 8 | unexpected indent | `integer_types = int,` |
| 894 | venv_creative/lib/python3.13/site-packages/librosa/sequence.py | 63 | 1 | invalid syntax | `@overload` |
| 895 | venv_creative/lib/python3.13/site-packages/librosa/display.py | 84 | 1 | invalid syntax | `class TimeFormatter(mplticker.Formatter):` |
| 896 | venv_creative/lib/python3.13/site-packages/librosa/core/notation.py | 131 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 51 | `}` |
| 897 | venv_creative/lib/python3.13/site-packages/librosa/core/spectrum.py | 2817 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 2812 | `) -> np.ndarray:` |
| 898 | venv_creative/lib/python3.13/site-packages/librosa/core/audio.py | 71 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 59 | `) -> Tuple[np.ndarray, Union[int, float]]:` |
| 899 | venv_creative/lib/python3.13/site-packages/librosa/util/matching.py | 100 | 16 | unexpected indent | `else:` |
| 900 | venv_creative/lib/python3.13/site-packages/flask/helpers.py | 123 | 17 | invalid syntax. Perhaps you forgot a comma? | `"'stream_with_context' can only be used when a request"` |
| 901 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/bidi/common.py | 39 | 8 | unexpected indent | `return cmd` |
| 902 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/overlay.py | 47 | 1 | invalid syntax | `@dataclass` |
| 903 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/audits.py | 50 | 1 | invalid syntax | `@dataclass` |
| 904 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/media.py | 91 | 1 | invalid syntax | `@dataclass` |
| 905 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/input_.py | 99 | 1 | invalid syntax | `class GestureSourceType(enum.Enum):` |
| 906 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/security.py | 163 | 16 | unexpected indent | `return json` |
| 907 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/system_info.py | 54 | 12 | unexpected indent | `json['driverVersion'] = self.driver_version` |
| 908 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/emulation.py | 82 | 1 | invalid syntax | `@dataclass` |
| 909 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/page.py | 101 | 1 | invalid syntax | `@dataclass` |
| 910 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/browser.py | 122 | 1 | invalid syntax | `class PermissionType(enum.Enum):` |
| 911 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/css.py | 92 | 1 | invalid syntax | `@dataclass` |
| 912 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/network.py | 419 | 1 | invalid syntax | `class ResourcePriority(enum.Enum):` |
| 913 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v138/dom.py | 93 | 1 | invalid syntax | `class PseudoType(enum.Enum):` |
| 914 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/overlay.py | 47 | 1 | invalid syntax | `@dataclass` |
| 915 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/audits.py | 50 | 1 | invalid syntax | `@dataclass` |
| 916 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/media.py | 91 | 1 | invalid syntax | `@dataclass` |
| 917 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/input_.py | 99 | 1 | invalid syntax | `class GestureSourceType(enum.Enum):` |
| 918 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/security.py | 163 | 16 | unexpected indent | `return json` |
| 919 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/system_info.py | 54 | 12 | unexpected indent | `json['driverVersion'] = self.driver_version` |
| 920 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/emulation.py | 82 | 1 | invalid syntax | `@dataclass` |
| 921 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/page.py | 101 | 1 | invalid syntax | `@dataclass` |
| 922 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/browser.py | 122 | 1 | invalid syntax | `class PermissionType(enum.Enum):` |
| 923 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/css.py | 92 | 1 | invalid syntax | `@dataclass` |
| 924 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/network.py | 419 | 1 | invalid syntax | `class ResourcePriority(enum.Enum):` |
| 925 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v139/dom.py | 93 | 1 | invalid syntax | `class PseudoType(enum.Enum):` |
| 926 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/overlay.py | 47 | 1 | invalid syntax | `@dataclass` |
| 927 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/audits.py | 50 | 1 | invalid syntax | `@dataclass` |
| 928 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/media.py | 91 | 1 | invalid syntax | `@dataclass` |
| 929 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/input_.py | 99 | 1 | invalid syntax | `class GestureSourceType(enum.Enum):` |
| 930 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/security.py | 163 | 16 | unexpected indent | `return json` |
| 931 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/system_info.py | 54 | 12 | unexpected indent | `json['driverVersion'] = self.driver_version` |
| 932 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/emulation.py | 82 | 1 | invalid syntax | `@dataclass` |
| 933 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/page.py | 101 | 1 | invalid syntax | `@dataclass` |
| 934 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/browser.py | 122 | 1 | invalid syntax | `class PermissionType(enum.Enum):` |
| 935 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/css.py | 92 | 1 | invalid syntax | `@dataclass` |
| 936 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/network.py | 418 | 1 | invalid syntax | `class ResourcePriority(enum.Enum):` |
| 937 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/common/devtools/v137/dom.py | 93 | 1 | invalid syntax | `class PseudoType(enum.Enum):` |
| 938 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/support/expected_conditions.py | 22 | 40 | '(' was never closed | `from selenium.common.exceptions import (NoAlertPresentException, NoSuchElementException,` |
| 939 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/remote/command.py | 112 | 8 | unexpected indent | `ADD_VIRTUAL_AUTHENTICATOR: str = "addVirtualAuthenticator"` |
| 940 | venv_creative/lib/python3.13/site-packages/selenium/webdriver/remote/webdriver.py | 39 | 1 | invalid syntax | `from selenium.webdriver.common.bidi.browser import Browser` |
| 941 | venv_creative/lib/python3.13/site-packages/packaging/_manylinux.py | 48 | 1 | invalid syntax | `def _is_linux_i686(executable: str) -> bool:` |
| 942 | venv_creative/lib/python3.13/site-packages/packaging/specifiers.py | 249 | 5 | invalid syntax | `def __init__(self, spec: str = "", prereleases: bool ¦ None = None) -> None:` |
| 943 | venv_creative/lib/python3.13/site-packages/aiohttp/test_utils.py | 106 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 100 | `) -> None:` |
| 944 | venv_creative/lib/python3.13/site-packages/aiohttp/compression_utils.py | 182 | 12 | unexpected indent | `self._max_sync_chunk_size = max_sync_chunk_size` |
| 945 | venv_creative/lib/python3.13/site-packages/aiohttp/client.py | 271 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 253 | `) -> None:` |
| 946 | venv_creative/lib/python3.13/site-packages/aiohttp/web_urldispatcher.py | 22 | 1 | invalid syntax | `from yarl import URL` |
| 947 | venv_creative/lib/python3.13/site-packages/aiohttp/payload.py | 165 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 156 | `) -> None:` |
| 948 | venv_creative/lib/python3.13/site-packages/aiohttp/connector.py | 20 | 1 | invalid syntax | `import aiohappyeyeballs` |
| 949 | venv_creative/lib/python3.13/site-packages/aiohttp/client_exceptions.py | 63 | 1 | invalid syntax | `class ClientError(Exception):` |
| 950 | venv_creative/lib/python3.13/site-packages/aiohttp/helpers.py | 30 | 1 | invalid syntax | `from urllib.parse import quote` |
| 951 | venv_creative/lib/python3.13/site-packages/aiohttp/pytest_plugin.py | 10 | 1 | invalid syntax | `import pytest` |
| 952 | venv_creative/lib/python3.13/site-packages/ffmpeg/_view.py | 11 | 1 | invalid syntax | `from ._run import topo_sort` |
| 953 | venv_creative/lib/python3.13/site-packages/httpcore/_synchronization.py | 27 | 9 | expected 'except' or 'finally' block | `import sniffio` |
| 954 | venv_creative/lib/python3.13/site-packages/msgpack/fallback.py | 97 | 12 | unexpected indent | `if unpacker._got_extradata():` |
| 955 | venv_creative/lib/python3.13/site-packages/networkx/convert.py | 36 | 1 | invalid syntax | `def to_networkx_graph(data, create_using = None, multigraph_input = False):` |
| 956 | venv_creative/lib/python3.13/site-packages/networkx/readwrite/gexf.py | 191 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 185 | `),` |
| 957 | venv_creative/lib/python3.13/site-packages/networkx/readwrite/json_graph/node_link.py | 136 | 8 | unexpected indent | `if link is not None:` |
| 958 | venv_creative/lib/python3.13/site-packages/networkx/drawing/layout.py | 44 | 1 | invalid syntax | `def _process_params(G, center, dim):` |
| 959 | venv_creative/lib/python3.13/site-packages/networkx/drawing/nx_pylab.py | 49 | 1 | invalid syntax | `def apply_matplotlib_colors(` |
| 960 | venv_creative/lib/python3.13/site-packages/networkx/drawing/tests/test_layout.py | 34 | 12 | unexpected indent | `assert all(np.array_equal(out[n], pos[n]) for n in (0, 2))` |
| 961 | venv_creative/lib/python3.13/site-packages/networkx/classes/digraph.py | 14 | 1 | invalid syntax | `from networkx.exception import NetworkXError` |
| 962 | venv_creative/lib/python3.13/site-packages/networkx/classes/tests/historical_tests.py | 75 | 9 | invalid syntax | `assert sorted(G, key = str) == [1, 2, 3, 4, "A", "B", "C", "D", "E", "F", "G"]` |
| 963 | venv_creative/lib/python3.13/site-packages/networkx/classes/tests/test_multigraph.py | 150 | 9 | invalid syntax | `assert edges_equal(` |
| 964 | venv_creative/lib/python3.13/site-packages/networkx/classes/tests/test_graph.py | 47 | 9 | invalid syntax | `assert sorted(G.nodes()) == self.k3nodes` |
| 965 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/sparsifiers.py | 106 | 45 | invalid syntax. Perhaps you forgot a comma? | `residual_graph, clustering, v` |
| 966 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/lowest_common_ancestors.py | 18 | 1 | invalid syntax | `@not_implemented_for("undirected")` |
| 967 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/threshold.py | 558 | 20 | unexpected indent | `rdi.pop(0)` |
| 968 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/simple_paths.py | 17 | 1 | invalid syntax | `@nx._dispatchable` |
| 969 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/d_separation.py | 233 | 1 | invalid syntax | `@not_implemented_for("undirected")` |
| 970 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/tree/mst.py | 32 | 1 | invalid syntax | `class EdgePartition(Enum):` |
| 971 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/isomorphism/ismags.py | 208 | 16 | unexpected indent | `return colors` |
| 972 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/isomorphism/tests/test_vf2pp.py | 28 | 1 | invalid syntax | `class TestPreCheck:` |
| 973 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/isomorphism/tests/test_vf2pp_helpers.py | 612 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 607 | `}` |
| 974 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/isomorphism/tests/test_tree_isomorphism.py | 117 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `t1 = nx.Graph()` |
| 975 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/link_analysis/pagerank_alg.py | 117 | 1 | invalid syntax | `def _pagerank_python(` |
| 976 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/link_analysis/hits_alg.py | 111 | 12 | unexpected indent | `s = 1.0 / sum(h.values())` |
| 977 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/connectivity/edge_kcomponents.py | 18 | 11 | '[' was never closed | `__all__ = [` |
| 978 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/approximation/density.py | 15 | 13 | invalid syntax. Perhaps you forgot a comma? | `f"The number of iterations must be an integer >= 1. Provided: {iterations}"` |
| 979 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/centrality/current_flow_betweenness_subset.py | 7 | 11 | '[' was never closed | `__all__ = [` |
| 980 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/centrality/current_flow_betweenness.py | 10 | 1 | invalid syntax | `from networkx.utils import (not_implemented_for, py_random_state,` |
| 981 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/centrality/katz.py | 188 | 21 | expected 'except' or 'finally' block | `s = 1.0 / math.hypot(*x.values())` |
| 982 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/centrality/tests/test_trophic.py | 55 | 5 | invalid syntax | `assert np.array_equal(q.todense(), expected_q)` |
| 983 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/tests/test_dag.py | 88 | 9 | invalid syntax | `assert nx.dag_longest_path(G) == [1, 3]` |
| 984 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/tests/test_lowest_common_ancestors.py | 29 | 13 | invalid syntax. Perhaps you forgot a comma? | `{` |
| 985 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/tests/test_swap.py | 42 | 9 | invalid syntax. Perhaps you forgot a comma? | `"Maximum number of swap attempts \\(11\\) exceeded "` |
| 986 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/bipartite/tests/test_project.py | 178 | 31 | unindent does not match any outer indentation level | `cls.G.add_edge("A", 1)` |
| 987 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/shortest_paths/weighted.py | 43 | 1 | invalid syntax | `def _weight_function(G, weight):` |
| 988 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/shortest_paths/unweighted.py | 7 | 11 | '[' was never closed | `__all__ = [` |
| 989 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/shortest_paths/tests/test_dense.py | 33 | 15 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `path, dist = nx.floyd_warshall_predecessor_and_distance(XG)` |
| 990 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/community/lukes.py | 109 | 28 | '(' was never closed | `raise TypeError(` |
| 991 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/coloring/equitable_coloring.py | 109 | 8 | unexpected indent | `while X != dst_color:` |
| 992 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/coloring/greedy_coloring.py | 26 | 1 | invalid syntax | `def strategy_largest_first(G, colors):` |
| 993 | venv_creative/lib/python3.13/site-packages/networkx/algorithms/coloring/tests/test_coloring.py | 918 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 905 | `}` |
| 994 | venv_creative/lib/python3.13/site-packages/networkx/utils/misc.py | 46 | 1 | invalid syntax | `def flatten(obj, result = None):` |
| 995 | venv_creative/lib/python3.13/site-packages/networkx/utils/backends.py | 78 | 9 | invalid syntax | `elif load_and_call:` |
| 996 | venv_creative/lib/python3.13/site-packages/networkx/utils/decorators.py | 26 | 1 | invalid syntax | `def not_implemented_for(*graph_types):` |
| 997 | venv_creative/lib/python3.13/site-packages/networkx/utils/tests/test_decorators.py | 12 | 1 | invalid syntax | `from networkx.utils.misc import PythonRandomInterface, PythonRandomViaNumpyBits` |
| 998 | venv_creative/lib/python3.13/site-packages/networkx/utils/tests/test_misc.py | 13 | 1 | invalid syntax | `from networkx.utils.misc import _dict_to_numpy_array1, _dict_to_numpy_array2` |
| 999 | venv_creative/lib/python3.13/site-packages/networkx/generators/nonisomorphic_trees.py | 65 | 12 | unexpected indent | `return _unlabeled_trees(order)` |
| 1000 | venv_creative/lib/python3.13/site-packages/networkx/generators/directed.py | 17 | 9 | invalid syntax | `__all__ = [` |
| 1001 | venv_creative/lib/python3.13/site-packages/networkx/generators/tests/test_time_series.py | 48 | 8 | unexpected indent | `expected_node_count = len(series)` |
| 1002 | venv_creative/lib/python3.13/site-packages/zhconv/zhconv.py | 42 | 11 | invalid syntax. Perhaps you forgot a comma? | `Locales = {` |
| 1003 | venv_creative/lib/python3.13/site-packages/websocket/_http.py | 28 | 1 | invalid syntax | `from ._logging import debug, dump, trace` |
| 1004 | venv_creative/lib/python3.13/site-packages/websocket/_app.py | 631 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 621 | `) -> bool:` |
| 1005 | venv_creative/lib/python3.13/site-packages/h11/_connection.py | 8 | 1 | invalid syntax | `from ._events import (ConnectionClosed, Data, EndOfMessage, Event,` |
| 1006 | venv_creative/lib/python3.13/site-packages/accelerate/local_sgd.py | 73 | 48 | '[' was never closed | `if accelerator.distributed_type not in [` |
| 1007 | venv_creative/lib/python3.13/site-packages/accelerate/data_loader.py | 34 | 8 | invalid syntax | `logger = get_logger(__name__)` |
| 1008 | venv_creative/lib/python3.13/site-packages/accelerate/optimizer.py | 25 | 1 | invalid syntax | `if is_torch_xla_available():` |
| 1009 | venv_creative/lib/python3.13/site-packages/accelerate/test_utils/scripts/test_script.py | 37 | 1 | invalid syntax | `from torch.utils.data import DataLoader, Dataset` |
| 1010 | venv_creative/lib/python3.13/site-packages/accelerate/test_utils/scripts/external_deps/test_peak_memory_usage.py | 25 | 1 | invalid syntax | `from accelerate.utils.deepspeed import DummyOptim, DummyScheduler` |
| 1011 | venv_creative/lib/python3.13/site-packages/accelerate/test_utils/scripts/external_deps/test_ds_multiple_model.py | 38 | 20 | invalid syntax | `MAX_GPU_BATCH_SIZE = 16` |
| 1012 | venv_creative/lib/python3.13/site-packages/accelerate/test_utils/scripts/external_deps/test_checkpointing.py | 30 | 20 | invalid syntax | `MAX_GPU_BATCH_SIZE = 16` |
| 1013 | venv_creative/lib/python3.13/site-packages/accelerate/utils/deepspeed.py | 116 | 53 | invalid syntax | `if not isinstance(state.deepspeed_plugins, dict):` |
| 1014 | venv_creative/lib/python3.13/site-packages/accelerate/utils/memory.py | 34 | 1 | invalid syntax | `from .versions import compare_versions` |
| 1015 | venv_creative/lib/python3.13/site-packages/accelerate/utils/other.py | 39 | 1 | invalid syntax | `from .modeling import id_tensor_storage` |
| 1016 | venv_creative/lib/python3.13/site-packages/accelerate/utils/operations.py | 129 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 123 | `}` |
| 1017 | venv_creative/lib/python3.13/site-packages/accelerate/utils/environment.py | 123 | 104 | invalid syntax. Perhaps you forgot a comma? | `[_nvidia_smi(), "--query - gpu = count,name", "--format = csv,noheader"], universal_newlines = True` |
| 1018 | venv_creative/lib/python3.13/site-packages/accelerate/utils/megatron_lm.py | 42 | 5 | invalid syntax | `from megatron.core.pipeline_parallel import get_forward_backward_func` |
| 1019 | venv_creative/lib/python3.13/site-packages/accelerate/commands/tpu.py | 25 | 1 | invalid syntax | `from packaging.version import Version, parse` |
| 1020 | venv_creative/lib/python3.13/site-packages/trio/_ssl.py | 226 | 1 | invalid syntax | `class NeedHandshakeError(Exception):` |
| 1021 | venv_creative/lib/python3.13/site-packages/trio/_highlevel_open_tcp_listeners.py | 112 | 8 | unexpected indent | `if not isinstance(port, int):` |
| 1022 | venv_creative/lib/python3.13/site-packages/trio/_subprocess.py | 20 | 1 | invalid syntax | `from ._sync import Lock` |
| 1023 | venv_creative/lib/python3.13/site-packages/trio/_channel.py | 22 | 1 | invalid syntax | `if sys.version_info < (3, 11):` |
| 1024 | venv_creative/lib/python3.13/site-packages/trio/_repl.py | 42 | 20 | unexpected indent | `else:` |
| 1025 | venv_creative/lib/python3.13/site-packages/trio/_dtls.py | 30 | 8 | unexpected indent | `from types import TracebackType` |
| 1026 | venv_creative/lib/python3.13/site-packages/trio/_highlevel_socket.py | 92 | 9 | invalid syntax | `with suppress(OSError):` |
| 1027 | venv_creative/lib/python3.13/site-packages/trio/_tests/test_highlevel_open_unix_stream.py | 13 | 38 | '(' was never closed | `skip_if_not_unix = pytest.mark.skipif(` |
| 1028 | venv_creative/lib/python3.13/site-packages/trio/_tests/test_testing_raisesgroup.py | 878 | 25 | closing parenthesis ')' does not match opening parenthesis '[' on line 872 | `),` |
| 1029 | venv_creative/lib/python3.13/site-packages/trio/_tests/test_highlevel_open_tcp_stream.py | 16 | 1 | invalid syntax | `from trio.socket import AF_INET, AF_INET6, IPPROTO_TCP, SOCK_STREAM, SocketType` |
| 1030 | venv_creative/lib/python3.13/site-packages/trio/_tests/test_socket.py | 71 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 65 | `) -> None:` |
| 1031 | venv_creative/lib/python3.13/site-packages/trio/_tests/test_util.py | 19 | 1 | invalid syntax | `from .._util import (ConflictDetector, MultipleExceptionError, NoPublicConstructor,` |
| 1032 | venv_creative/lib/python3.13/site-packages/trio/_tests/test_highlevel_socket.py | 17 | 1 | invalid syntax | `from .test_socket import setsockopt_tests` |
| 1033 | venv_creative/lib/python3.13/site-packages/trio/_tests/test_channel.py | 163 | 9 | expected an indented block after function definition on line 162 | `with pytest.raises(trio.ClosedResourceError):` |
| 1034 | venv_creative/lib/python3.13/site-packages/trio/_tests/test_subprocess.py | 25 | 1 | invalid syntax | `from .._core._tests.tutil import skip_if_fbsd_pipes_broken, slow` |
| 1035 | venv_creative/lib/python3.13/site-packages/trio/_tests/test_threads.py | 20 | 1 | invalid syntax | `from .._core._tests.test_ki import ki_self` |
| 1036 | venv_creative/lib/python3.13/site-packages/trio/_core/_io_windows.py | 23 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 1037 | venv_creative/lib/python3.13/site-packages/trio/_core/_run.py | 43 | 1 | invalid syntax | `if sys.version_info < (3, 11):` |
| 1038 | venv_creative/lib/python3.13/site-packages/trio/_core/_tests/test_run.py | 27 | 1 | invalid syntax | `from .._run import DEADLINE_HEAP_MIN_PRUNE_THRESHOLD, _count_context_run_tb_frames` |
| 1039 | venv_creative/lib/python3.13/site-packages/trio/_core/_tests/test_ki.py | 35 | 5 | invalid syntax | `from ..._core import Abort, RaiseCancelT` |
| 1040 | venv_creative/lib/python3.13/site-packages/trio/_core/_tests/test_instrumentation.py | 98 | 5 | invalid syntax | `assert r1.record == r2.record + r3.record` |
| 1041 | venv_creative/lib/python3.13/site-packages/trio/_core/_tests/test_asyncgen.py | 120 | 8 | unexpected indent | `assert str(exc_value) == "oops"` |
| 1042 | venv_creative/lib/python3.13/site-packages/trio/_core/_tests/test_windows.py | 26 | 8 | unexpected indent | `from io import BufferedWriter` |
| 1043 | venv_creative/lib/python3.13/site-packages/trio/_subprocess_platform/waitid.py | 25 | 28 | unindent does not match any outer indentation level | `waitid_ffi = cffi.FFI()` |
| 1044 | venv_creative/lib/python3.13/site-packages/trio/testing/_check_streams.py | 196 | 9 | invalid syntax | `async def expect_broken_stream_on_send() -> None:` |
| 1045 | venv_creative/lib/python3.13/site-packages/trio/testing/_memory_streams.py | 44 | 5 | invalid syntax | `def close(self) -> None:` |
| 1046 | venv_creative/lib/python3.13/site-packages/huggingface_hub/hub_mixin.py | 220 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 212 | `) -> None:` |
| 1047 | venv_creative/lib/python3.13/site-packages/huggingface_hub/file_download.py | 24 | 1 | invalid syntax | `from .constants import \` |
| 1048 | venv_creative/lib/python3.13/site-packages/huggingface_hub/_oauth.py | 230 | 13 | invalid syntax | `for org in orgs_data` |
| 1049 | venv_creative/lib/python3.13/site-packages/huggingface_hub/hf_api.py | 6263 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 6254 | `},` |
| 1050 | venv_creative/lib/python3.13/site-packages/huggingface_hub/dataclasses.py | 9 | 1 | invalid syntax | `from .errors import (StrictDataclassClassValidationError,` |
| 1051 | venv_creative/lib/python3.13/site-packages/huggingface_hub/_snapshot_download.py | 14 | 1 | invalid syntax | `from .file_download import REGEX_COMMIT_HASH, hf_hub_download, repo_folder_name` |
| 1052 | venv_creative/lib/python3.13/site-packages/huggingface_hub/repository.py | 21 | 1 | invalid syntax | `from .utils._deprecation import _deprecate_method` |
| 1053 | venv_creative/lib/python3.13/site-packages/huggingface_hub/serialization/_base.py | 137 | 12 | unexpected indent | `current_shard_size += tensor_size` |
| 1054 | venv_creative/lib/python3.13/site-packages/huggingface_hub/utils/_fixes.py | 78 | 9 | expected 'except' or 'finally' block | `tmpdir.cleanup()` |
| 1055 | venv_creative/lib/python3.13/site-packages/huggingface_hub/utils/_http.py | 40 | 1 | invalid syntax | `from . import logging` |
| 1056 | venv_creative/lib/python3.13/site-packages/huggingface_hub/cli/auth.py | 63 | 88 | unindent does not match any outer indentation level | `auth_subparsers = auth_parser.add_subparsers(help="Authentication subcommands")` |
| 1057 | venv_creative/lib/python3.13/site-packages/huggingface_hub/cli/cache.py | 28 | 1 | invalid syntax | `from . import BaseHuggingfaceCLICommand` |
| 1058 | venv_creative/lib/python3.13/site-packages/huggingface_hub/cli/jobs.py | 92 | 9 | invalid syntax. Perhaps you forgot a comma? | `run_parser.add_argument("--env - file", type = str, help="Read in a file of environment variables.")` |
| 1059 | venv_creative/lib/python3.13/site-packages/huggingface_hub/inference/_common.py | 31 | 1 | invalid syntax | `from huggingface_hub.errors import (GenerationError, IncompleteGenerationError,` |
| 1060 | venv_creative/lib/python3.13/site-packages/huggingface_hub/inference/_providers/_common.py | 94 | 12 | unexpected indent | `api_key = self._prepare_api_key(api_key)` |
| 1061 | venv_creative/lib/python3.13/site-packages/huggingface_hub/inference/_generated/_async_client.py | 31 | 1 | invalid syntax | `from huggingface_hub import constants` |
| 1062 | venv_creative/lib/python3.13/site-packages/huggingface_hub/commands/delete_cache.py | 98 | 9 | invalid syntax | `return fn(*args, **kwargs)` |
| 1063 | venv_creative/lib/python3.13/site-packages/ecdsa/test_keys.py | 22 | 1 | invalid syntax | `from .ecdsa import generator_brainpoolp160r1` |
| 1064 | venv_creative/lib/python3.13/site-packages/ecdsa/keys.py | 23 | 9 | invalid syntax | `__all__ = [` |
| 1065 | venv_creative/lib/python3.13/site-packages/ecdsa/ellipticcurve.py | 119 | 9 | invalid syntax | `return NotImplemented` |
| 1066 | venv_creative/lib/python3.13/site-packages/ecdsa/ecdsa.py | 119 | 13 | invalid syntax. Perhaps you forgot a comma? | `pow(x, 3, curve.p()) + (curve.a() * x) + curve.b()` |
| 1067 | venv_creative/lib/python3.13/site-packages/ecdsa/numbertheory.py | 75 | 5 | invalid syntax | `if exponent < 0:` |
| 1068 | venv_creative/lib/python3.13/site-packages/ecdsa/curves.py | 50 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `PRIME_FIELD_OID = (1, 2, 840, 10045, 1, 1)` |
| 1069 | venv_creative/lib/python3.13/site-packages/ecdsa/test_pyecdsa.py | 30 | 1 | invalid syntax | `from .ecdsa import (curve_brainpoolp224r1, curve_brainpoolp256r1, curve_brainpoolp384r1,` |
| 1070 | venv_creative/lib/python3.13/site-packages/ecdsa/eddsa.py | 10 | 1 | invalid syntax | `from ._sha3 import shake_256` |
| 1071 | venv_creative/lib/python3.13/site-packages/tifffile/numcodecs.py | 56 | 1 | invalid syntax | `class Tiff(Codec):  # type: ignore[misc]` |
| 1072 | venv_creative/lib/python3.13/site-packages/tifffile/tifffile.py | 6433 | 40 | too many nested parentheses | `axes = ''.join(reversed(attr['DimensionOrder']))` |
| 1073 | venv_creative/lib/python3.13/site-packages/tifffile/zarr.py | 400 | 33 | closing parenthesis '}' does not match opening parenthesis '[' on line 391 | `}` |
| 1074 | venv_creative/lib/python3.13/site-packages/sympy/series/limits.py | 165 | 32 | invalid syntax | `if isinstance(dir, str):` |
| 1075 | venv_creative/lib/python3.13/site-packages/sympy/series/gruntz.py | 320 | 39 | invalid syntax. Perhaps you forgot a comma? | `raise NotImplementedError("MRV set computation for functions in"` |
| 1076 | venv_creative/lib/python3.13/site-packages/sympy/core/facts.py | 130 | 5 | invalid syntax | `return res` |
| 1077 | venv_creative/lib/python3.13/site-packages/sympy/core/backend.py | 15 | 5 | invalid syntax | `from symengine import sympify as sympify_symengine` |
| 1078 | venv_creative/lib/python3.13/site-packages/sympy/core/add.py | 32 | 5 | invalid syntax | `positive_args = len(expr.args) - negative_args` |
| 1079 | venv_creative/lib/python3.13/site-packages/sympy/core/exprtools.py | 13 | 1 | invalid syntax | `from .add import Add` |
| 1080 | venv_creative/lib/python3.13/site-packages/sympy/core/relational.py | 27 | 1 | invalid syntax | `from sympy.multipledispatch import dispatch` |
| 1081 | venv_creative/lib/python3.13/site-packages/sympy/core/mul.py | 408 | 41 | unindent does not match any outer indentation level | `return [S.NaN], [], None` |
| 1082 | venv_creative/lib/python3.13/site-packages/sympy/core/sympify.py | 42 | 10 | invalid syntax | `converter: dict[type[Any], Callable[[Any], Basic]] = {}` |
| 1083 | venv_creative/lib/python3.13/site-packages/sympy/core/evalf.py | 21 | 1 | invalid syntax | `from mpmath.libmp.backend import MPZ` |
| 1084 | venv_creative/lib/python3.13/site-packages/sympy/core/mod.py | 181 | 12 | unexpected indent | `from sympy.polys.polytools import gcd` |
| 1085 | venv_creative/lib/python3.13/site-packages/sympy/core/power.py | 18 | 1 | invalid syntax | `from .kind import NumberKind, UndefinedKind` |
| 1086 | venv_creative/lib/python3.13/site-packages/sympy/core/function.py | 47 | 1 | invalid syntax | `from sympy.utilities.iterables import (has_dups, is_sequence, iterable, sift,` |
| 1087 | venv_creative/lib/python3.13/site-packages/sympy/core/assumptions.py | 297 | 5 | invalid syntax | `return _assume_rules` |
| 1088 | venv_creative/lib/python3.13/site-packages/sympy/core/expr.py | 205 | 16 | invalid syntax. Perhaps you forgot a comma? | `args = (len(args), tuple(args))` |
| 1089 | venv_creative/lib/python3.13/site-packages/sympy/core/tests/test_subs.py | 50 | 8 | unexpected indent | `assert Add(Matrix([[3]]), x).subs(x, 2.0) == Add(Matrix([[3]]), 2.0)` |
| 1090 | venv_creative/lib/python3.13/site-packages/sympy/core/tests/test_numbers.py | 15 | 1 | invalid syntax | `from sympy.core.logic import fuzzy_not` |
| 1091 | venv_creative/lib/python3.13/site-packages/sympy/core/tests/test_power.py | 6 | 1 | invalid syntax | `from sympy.core.function import expand_multinomial` |
| 1092 | venv_creative/lib/python3.13/site-packages/sympy/core/tests/test_exprtools.py | 8 | 34 | '(' was never closed | `from sympy.core.exprtools import (Factors, Term, _gcd_terms, _mask_nc, _monotonic_sign,` |
| 1093 | venv_creative/lib/python3.13/site-packages/sympy/core/tests/test_args.py | 33 | 1 | invalid syntax | `def test_all_classes_are_tested():` |
| 1094 | venv_creative/lib/python3.13/site-packages/sympy/core/tests/test_facts.py | 5 | 1 | invalid syntax | `from sympy.core.logic import And, Not` |
| 1095 | venv_creative/lib/python3.13/site-packages/sympy/core/tests/test_function.py | 12 | 1 | invalid syntax | `from sympy.core.numbers import E, Float, I, Rational, nan, oo, pi, zoo` |
| 1096 | venv_creative/lib/python3.13/site-packages/sympy/core/tests/test_expr.py | 12 | 1 | invalid syntax | `from sympy.core.mul import Mul, _unevaluated_Mul` |
| 1097 | venv_creative/lib/python3.13/site-packages/sympy/core/tests/test_sympify.py | 18 | 1 | invalid syntax | `from sympy.external import import_module` |
| 1098 | venv_creative/lib/python3.13/site-packages/sympy/unify/tests/test_sympy.py | 15 | 1 | invalid syntax | `def test_deconstruct():` |
| 1099 | venv_creative/lib/python3.13/site-packages/sympy/polys/rootoftools.py | 11 | 1 | invalid syntax | `from sympy.core.basic import Basic` |
| 1100 | venv_creative/lib/python3.13/site-packages/sympy/polys/ring_series.py | 54 | 1 | invalid syntax | `from sympy.polys.domains import EX, QQ` |
| 1101 | venv_creative/lib/python3.13/site-packages/sympy/polys/fields.py | 265 | 23 | '(' was never closed | `powers = tuple((gen, gen.as_base_exp()) for gen in mapping.keys()` |
| 1102 | venv_creative/lib/python3.13/site-packages/sympy/polys/polyutils.py | 39 | 12 | unexpected indent | `if not len(roots):` |
| 1103 | venv_creative/lib/python3.13/site-packages/sympy/polys/solvers.py | 34 | 34 | '(' was never closed | `sympy_deprecation_warning(` |
| 1104 | venv_creative/lib/python3.13/site-packages/sympy/polys/polytools.py | 21 | 1 | invalid syntax | `from sympy.core.exprtools import Factors, factor_nc, factor_terms` |
| 1105 | venv_creative/lib/python3.13/site-packages/sympy/polys/puiseux.py | 32 | 8 | unexpected indent | `from typing import Any, Unpack` |
| 1106 | venv_creative/lib/python3.13/site-packages/sympy/polys/partfrac.py | 129 | 20 | invalid syntax. Perhaps you forgot a comma? | `common, P, Q = P.cancel(Q)` |
| 1107 | venv_creative/lib/python3.13/site-packages/sympy/polys/densearith.py | 8 | 1 | invalid syntax | `from sympy.polys.polyerrors import ExactQuotientFailed, PolynomialDivisionFailed` |
| 1108 | venv_creative/lib/python3.13/site-packages/sympy/polys/subresultants_qq_zz.py | 1557 | 12 | unexpected indent | `for u in u_list:` |
| 1109 | venv_creative/lib/python3.13/site-packages/sympy/polys/rings.py | 29 | 1 | invalid syntax | `from sympy.polys.polyoptions import Domain as DomainOpt` |
| 1110 | venv_creative/lib/python3.13/site-packages/sympy/polys/domains/mpelements.py | 8 | 26 | '(' was never closed | `from mpmath.libmp import (MPZ_ONE, finf, fnan, fninf, fone, from_float, from_int,` |
| 1111 | venv_creative/lib/python3.13/site-packages/sympy/polys/domains/realfield.py | 48 | 12 | unexpected indent | `else:` |
| 1112 | venv_creative/lib/python3.13/site-packages/sympy/polys/domains/tests/test_domains.py | 1121 | 15 | invalid decimal literal | `assert CC(1e - 13j).imag > 1e-50` |
| 1113 | venv_creative/lib/python3.13/site-packages/sympy/polys/tests/test_dispersion.py | 88 | 8 | unexpected indent | `f = (x + 1)*(x + 2)` |
| 1114 | venv_creative/lib/python3.13/site-packages/sympy/polys/tests/test_rootoftools.py | 19 | 1 | invalid syntax | `from sympy.polys.polytools import Poly` |
| 1115 | venv_creative/lib/python3.13/site-packages/sympy/polys/numberfields/minpoly.py | 26 | 1 | invalid syntax | `from sympy.polys.polyutils import dict_from_expr, expr_from_dict` |
| 1116 | venv_creative/lib/python3.13/site-packages/sympy/polys/numberfields/modules.py | 1212 | 9 | invalid syntax | `elif isinstance(other, ModuleElement) and other.module == self.parent:` |
| 1117 | venv_creative/lib/python3.13/site-packages/sympy/polys/agca/modules.py | 239 | 5 | invalid syntax | `def __sub__(self, om):` |
| 1118 | venv_creative/lib/python3.13/site-packages/sympy/polys/agca/ideals.py | 135 | 5 | invalid syntax | `def contains(self, elem):` |
| 1119 | venv_creative/lib/python3.13/site-packages/sympy/polys/agca/tests/test_extensions.py | 18 | 8 | unexpected indent | `assert i.parent() is A` |
| 1120 | venv_creative/lib/python3.13/site-packages/sympy/polys/matrices/dense.py | 44 | 25 | '(' was never closed | `from .exceptions import (DMDomainError, DMNonInvertibleMatrixError,` |
| 1121 | venv_creative/lib/python3.13/site-packages/sympy/polys/matrices/domainmatrix.py | 25 | 1 | invalid syntax | `from sympy.polys.domains import EXRAW, QQ, ZZ` |
| 1122 | venv_creative/lib/python3.13/site-packages/sympy/polys/matrices/sdm.py | 864 | 16 | unexpected indent | `m, n = A.shape` |
| 1123 | venv_creative/lib/python3.13/site-packages/sympy/polys/matrices/_dfm.py | 53 | 1 | invalid syntax | `if GROUND_TYPES != 'flint':` |
| 1124 | venv_creative/lib/python3.13/site-packages/sympy/polys/matrices/tests/test_ddm.py | 8 | 1 | invalid syntax | `from sympy.testing.pytest import raises` |
| 1125 | venv_creative/lib/python3.13/site-packages/sympy/concrete/summations.py | 307 | 5 | invalid syntax | `def _eval_derivative(self, x):` |
| 1126 | venv_creative/lib/python3.13/site-packages/sympy/concrete/expr_with_limits.py | 49 | 15 | invalid syntax. Perhaps you forgot a comma? | `lhs = function.lhs` |
| 1127 | venv_creative/lib/python3.13/site-packages/sympy/concrete/tests/test_products.py | 147 | 14 | unindent does not match any outer indentation level | `a = l` |
| 1128 | venv_creative/lib/python3.13/site-packages/sympy/concrete/tests/test_sums_products.py | 10 | 1 | invalid syntax | `from sympy.core import Catalan, EulerGamma` |
| 1129 | venv_creative/lib/python3.13/site-packages/sympy/holonomic/holonomic.py | 11 | 1 | invalid syntax | `from sympy.core.singleton import S` |
| 1130 | venv_creative/lib/python3.13/site-packages/sympy/holonomic/numerical.py | 15 | 8 | unexpected indent | `a = ann.order` |
| 1131 | venv_creative/lib/python3.13/site-packages/sympy/holonomic/tests/test_holonomic.py | 19 | 1 | invalid syntax | `from sympy.holonomic.recurrence import HolonomicSequence, RecurrenceOperators` |
| 1132 | venv_creative/lib/python3.13/site-packages/sympy/ntheory/ecm.py | 261 | 12 | unexpected indent | `if g != 1 and g != n:` |
| 1133 | venv_creative/lib/python3.13/site-packages/sympy/ntheory/qs.py | 451 | 16 | unexpected indent | `while N_copy % factor == 0:` |
| 1134 | venv_creative/lib/python3.13/site-packages/sympy/ntheory/continued_fraction.py | 74 | 21 | '(' was never closed | `raise ValueError(` |
| 1135 | venv_creative/lib/python3.13/site-packages/sympy/printing/preview.py | 76 | 22 | invalid syntax. Perhaps you forgot a comma? | `config = config` |
| 1136 | venv_creative/lib/python3.13/site-packages/sympy/printing/str.py | 116 | 5 | invalid syntax | `def _print_Basic(self, expr):` |
| 1137 | venv_creative/lib/python3.13/site-packages/sympy/printing/aesaracode.py | 18 | 8 | unexpected indent | `from aesara.tensor import nlinalg` |
| 1138 | venv_creative/lib/python3.13/site-packages/sympy/printing/mathml.py | 20 | 1 | invalid syntax | `from sympy.printing.pretty.pretty_symbology import greek_unicode` |
| 1139 | venv_creative/lib/python3.13/site-packages/sympy/printing/codeprinter.py | 286 | 46 | unterminated string literal (detected at line 287) | `raise ValueError("FIXME: lhs present in rhs,\` |
| 1140 | venv_creative/lib/python3.13/site-packages/sympy/printing/numpy.py | 11 | 15 | invalid syntax | `_not_in_numpy = 'erf erfc factorial gamma loggamma'.split()` |
| 1141 | venv_creative/lib/python3.13/site-packages/sympy/printing/lambdarepr.py | 19 | 1 | invalid syntax | `class LambdaPrinter(PythonCodePrinter):` |
| 1142 | venv_creative/lib/python3.13/site-packages/sympy/printing/theanocode.py | 29 | 8 | unexpected indent | `from theano.sandbox import linalg as tlinalg` |
| 1143 | venv_creative/lib/python3.13/site-packages/sympy/printing/latex.py | 43 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `tex_greek_dictionary = {` |
| 1144 | venv_creative/lib/python3.13/site-packages/sympy/printing/julia.py | 40 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `known_fcns_src2 = {` |
| 1145 | venv_creative/lib/python3.13/site-packages/sympy/printing/octave.py | 40 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `known_fcns_src2 = {` |
| 1146 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_theanocode.py | 24 | 8 | unexpected indent | `xt, yt, zt = [tt.scalar(name, 'floatX') for name in 'xyz']` |
| 1147 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_c.py | 9 | 1 | invalid syntax | `from sympy.codegen.cfunctions import (Cbrt, Sqrt, exp2, expm1, fma, hypot, isinf, isnan,` |
| 1148 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_glsl.py | 7 | 1 | invalid syntax | `from sympy.functions import Abs, Piecewise, ceiling, cos, exp, sin, sqrt` |
| 1149 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_latex.py | 25 | 1 | invalid syntax | `from sympy.functions.combinatorial.numbers import (bell, bernoulli, catalan,` |
| 1150 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_julia.py | 6 | 1 | invalid syntax | `from sympy.functions import Piecewise, ceiling, cos, exp, sin, sinc, sqrt` |
| 1151 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_octave.py | 7 | 1 | invalid syntax | `from sympy.functions import (DiracDelta, Heaviside, LambertW, Max, Min, Piecewise,` |
| 1152 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_aesaracode.py | 24 | 8 | unexpected indent | `from aesara.graph.basic import Variable` |
| 1153 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_maple.py | 6 | 1 | invalid syntax | `from sympy.functions import Piecewise, ceiling, cos, exp, lucas, sin, sinc, sqrt` |
| 1154 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_rust.py | 5 | 1 | invalid syntax | `from sympy.functions import Abs, Piecewise, ceiling, cos, exp, floor, sign, sin, sqrt` |
| 1155 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_jscode.py | 5 | 1 | invalid syntax | `from sympy.functions import (Abs, Max, Min, Piecewise, acos, acosh, asin, ceiling, cos,` |
| 1156 | venv_creative/lib/python3.13/site-packages/sympy/printing/tests/test_fortran.py | 7 | 1 | invalid syntax | `from sympy.core import Catalan, EulerGamma, GoldenRatio` |
| 1157 | venv_creative/lib/python3.13/site-packages/sympy/printing/pretty/pretty.py | 23 | 1 | invalid syntax | `from sympy.printing.pretty.pretty_symbology import root as nth_root` |
| 1158 | venv_creative/lib/python3.13/site-packages/sympy/algebras/quaternion.py | 40 | 26 | invalid syntax. Perhaps you forgot a comma? | `raise ValueError("seq must either be fully uppercase (for extrinsic "` |
| 1159 | venv_creative/lib/python3.13/site-packages/sympy/logic/boolalg.py | 251 | 5 | invalid syntax | `def binary_symbols(self):` |
| 1160 | venv_creative/lib/python3.13/site-packages/sympy/logic/algorithms/lra_theory.py | 478 | 23 | unindent does not match any outer indentation level | `M = self.A` |
| 1161 | venv_creative/lib/python3.13/site-packages/sympy/logic/algorithms/minisat22_wrapper.py | 49 | 23 | unindent does not match any outer indentation level | `return _gen(r)` |
| 1162 | venv_creative/lib/python3.13/site-packages/sympy/solvers/bivariate.py | 78 | 5 | invalid syntax | `if len(fterms) == 1:` |
| 1163 | venv_creative/lib/python3.13/site-packages/sympy/solvers/solvers.py | 30 | 1 | invalid syntax | `from sympy.core.intfunc import ilcm, integer_log` |
| 1164 | venv_creative/lib/python3.13/site-packages/sympy/solvers/simplex.py | 149 | 9 | invalid syntax. Perhaps you forgot a comma? | `A = M - Mj * (Mi / Mij)` |
| 1165 | venv_creative/lib/python3.13/site-packages/sympy/solvers/inequalities.py | 48 | 5 | invalid syntax | `if poly.as_expr().is_number:` |
| 1166 | venv_creative/lib/python3.13/site-packages/sympy/solvers/solveset.py | 22 | 1 | invalid syntax | `from sympy.core.intfunc import integer_log` |
| 1167 | venv_creative/lib/python3.13/site-packages/sympy/solvers/deutils.py | 85 | 30 | invalid syntax. Perhaps you forgot a comma? | `raise ValueError('The function cannot be '` |
| 1168 | venv_creative/lib/python3.13/site-packages/sympy/solvers/diophantine/diophantine.py | 35 | 1 | invalid syntax | `from sympy.utilities.misc import as_int, filldedent` |
| 1169 | venv_creative/lib/python3.13/site-packages/sympy/solvers/diophantine/tests/test_diophantine.py | 43 | 1 | invalid syntax | `from sympy.testing.pytest import XFAIL, raises, slow` |
| 1170 | venv_creative/lib/python3.13/site-packages/sympy/solvers/tests/test_solvers.py | 2687 | 20 | too many nested parentheses | `sfun = solve([c[4 * i]*x + c[4 * i + 1]*y + c[4 * i + 2]*z + c[4 * i + 3]` |
| 1171 | venv_creative/lib/python3.13/site-packages/sympy/solvers/tests/test_numeric.py | 52 | 44 | invalid decimal literal | `x = nsolve(f, (x1, x2), x0, tol = 1.e - 8)` |
| 1172 | venv_creative/lib/python3.13/site-packages/sympy/solvers/tests/test_solveset.py | 1307 | 32 | too many nested parentheses | `ImageSet(Lambda(n, sqrt(3)*(2 * n*pi - 4 - asec(I))/3), S.Integers),` |
| 1173 | venv_creative/lib/python3.13/site-packages/sympy/solvers/ode/subscheck.py | 129 | 13 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `funcs = set().union(*funcs)` |
| 1174 | venv_creative/lib/python3.13/site-packages/sympy/solvers/ode/systems.py | 8 | 1 | invalid syntax | `from sympy.core.numbers import I` |
| 1175 | venv_creative/lib/python3.13/site-packages/sympy/solvers/ode/single.py | 17 | 1 | invalid syntax | `from sympy.core.mul import Mul` |
| 1176 | venv_creative/lib/python3.13/site-packages/sympy/solvers/ode/hypergeometric.py | 46 | 16 | '(' was never closed | `r = collect(eq,` |
| 1177 | venv_creative/lib/python3.13/site-packages/sympy/solvers/ode/ode.py | 238 | 1 | invalid syntax | `from sympy.core.multidimensional import vectorize` |
| 1178 | venv_creative/lib/python3.13/site-packages/sympy/solvers/ode/riccati.py | 366 | 8 | unexpected indent | `pwr = val_at_inf(num, den, x)` |
| 1179 | venv_creative/lib/python3.13/site-packages/sympy/solvers/ode/tests/test_lie_group.py | 36 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `i1 = infinitesimals(eq1, hint='abaco1_simple')` |
| 1180 | venv_creative/lib/python3.13/site-packages/sympy/solvers/ode/tests/test_ode.py | 500 | 75 | closing parenthesis '}' does not match opening parenthesis '[' on line 496 | `(1, x(t), 0): 0, (0, x(t), 0): 0, (1, y(t), 0): 0, (0, x(t), 1): 1}, 'order': {y(t): 1, x(t): 1}, 'no_of_equation': 2}` |
| 1181 | venv_creative/lib/python3.13/site-packages/sympy/solvers/ode/tests/test_single.py | 911 | 5 | closing parenthesis '}' does not match opening parenthesis '(' on line 907 | `},` |
| 1182 | venv_creative/lib/python3.13/site-packages/sympy/codegen/matrix_nodes.py | 75 | 12 | unexpected indent | `return MatrixSolve(A, b.diff(x) - A.diff(x) * MatrixSolve(A, b))` |
| 1183 | venv_creative/lib/python3.13/site-packages/sympy/codegen/ast.py | 585 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 579 | `}` |
| 1184 | venv_creative/lib/python3.13/site-packages/sympy/codegen/tests/test_approximations.py | 34 | 12 | unexpected indent | `bnds1 = {x: (-1, 1)}` |
| 1185 | venv_creative/lib/python3.13/site-packages/sympy/codegen/tests/test_cfunctions.py | 1 | 38 | '(' was never closed | `from sympy.codegen.cfunctions import (Cbrt, Sqrt, exp2, expm1, fma, hypot, isinf, isnan,` |
| 1186 | venv_creative/lib/python3.13/site-packages/sympy/codegen/tests/test_ast.py | 591 | 48 | invalid decimal literal | `dcm21 = Float('0.123456789012345670499') + 1e - 20j  # 21 decimals` |
| 1187 | venv_creative/lib/python3.13/site-packages/sympy/multipledispatch/tests/test_dispatcher.py | 1 | 47 | '(' was never closed | `from sympy.multipledispatch.dispatcher import (Dispatcher, MDNotImplementedError,` |
| 1188 | venv_creative/lib/python3.13/site-packages/sympy/utilities/misc.py | 305 | 5 | invalid syntax | `if path is None:` |
| 1189 | venv_creative/lib/python3.13/site-packages/sympy/utilities/lambdify.py | 146 | 5 | invalid syntax | `except KeyError:` |
| 1190 | venv_creative/lib/python3.13/site-packages/sympy/utilities/autowrap.py | 103 | 1 | invalid syntax | `from sympy.utilities.decorator import doctest_depends_on` |
| 1191 | venv_creative/lib/python3.13/site-packages/sympy/utilities/codegen.py | 92 | 1 | invalid syntax | `from sympy.printing.c import c_code_printers` |
| 1192 | venv_creative/lib/python3.13/site-packages/sympy/utilities/iterables.py | 8 | 1 | invalid syntax | `from operator import gt` |
| 1193 | venv_creative/lib/python3.13/site-packages/sympy/utilities/mathml/__init__.py | 27 | 62 | unindent does not match any outer indentation level | `return files(pkgname).joinpath(filename).read_bytes()` |
| 1194 | venv_creative/lib/python3.13/site-packages/sympy/utilities/tests/test_lambdify.py | 2080 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 2071 | `),` |
| 1195 | venv_creative/lib/python3.13/site-packages/sympy/utilities/tests/test_wester.py | 612 | 31 | unterminated string literal (detected at line 613) | `raise NotImplementedError("evaluate (b + c)**4 assuming b**3 == 2, c**2 == 3. \` |
| 1196 | venv_creative/lib/python3.13/site-packages/sympy/utilities/tests/test_codegen.py | 16 | 1 | invalid syntax | `from sympy.utilities.lambdify import implemented_function` |
| 1197 | venv_creative/lib/python3.13/site-packages/sympy/testing/pytest.py | 138 | 9 | invalid syntax | `else:` |
| 1198 | venv_creative/lib/python3.13/site-packages/sympy/testing/runtests.py | 88 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `SPLIT_DENSITY_SLOW = [0.0086, 0.0004, 0.0568, 0.0003, 0.0032, 0.0005, 0.0004, 0.0013, 0.0016, 0.0648, 0.0198, 0.1285, 0.098, 0.0005, 0.0064, 0.0003, 0.0004, 0.0026, 0.0007, 0.0051, 0.0089, 0.0024, 0.0033, 0.0057, 0.0005, 0.0003, 0.001, 0.0045, 0.0091, 0.0006, 0.0005, 0.0321, 0.0059, 0.1105, 0.216, 0.1489, 0.0004, 0.0003, 0.0006, 0.0483]` |
| 1199 | venv_creative/lib/python3.13/site-packages/sympy/testing/tests/test_code_quality.py | 84 | 25 | unindent does not match any outer indentation level | `continue` |
| 1200 | venv_creative/lib/python3.13/site-packages/sympy/integrals/laplace.py | 13 | 1 | invalid syntax | `from sympy.core.mul import Mul, prod` |
| 1201 | venv_creative/lib/python3.13/site-packages/sympy/integrals/meijerint.py | 44 | 1 | invalid syntax | `from sympy.core.intfunc import ilcm` |
| 1202 | venv_creative/lib/python3.13/site-packages/sympy/integrals/transforms.py | 60 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.function = function` |
| 1203 | venv_creative/lib/python3.13/site-packages/sympy/integrals/intpoly.py | 71 | 33 | invalid syntax | `if isinstance(poly, Polygon):` |
| 1204 | venv_creative/lib/python3.13/site-packages/sympy/integrals/heurisch.py | 21 | 1 | invalid syntax | `from sympy.functions.elementary.complexes import Abs, arg, im, re, sign` |
| 1205 | venv_creative/lib/python3.13/site-packages/sympy/integrals/integrals.py | 104 | 9 | invalid syntax | `return obj` |
| 1206 | venv_creative/lib/python3.13/site-packages/sympy/integrals/manualintegrate.py | 50 | 1 | invalid syntax | `from sympy.functions.elementary.miscellaneous import sqrt` |
| 1207 | venv_creative/lib/python3.13/site-packages/sympy/integrals/tests/test_meijerint.py | 23 | 1 | invalid syntax | `from sympy.simplify.hyperexpand import hyperexpand` |
| 1208 | venv_creative/lib/python3.13/site-packages/sympy/integrals/tests/test_transforms.py | 31 | 1 | invalid syntax | `from sympy.simplify.gammasimp import gammasimp` |
| 1209 | venv_creative/lib/python3.13/site-packages/sympy/assumptions/handlers/matrices.py | 19 | 1 | invalid syntax | `from sympy.matrices.expressions.blockmatrix import reblock_2x2` |
| 1210 | venv_creative/lib/python3.13/site-packages/sympy/assumptions/handlers/order.py | 25 | 1 | invalid syntax | `def _NegativePredicate_number(expr, assumptions):` |
| 1211 | venv_creative/lib/python3.13/site-packages/sympy/assumptions/handlers/ntheory.py | 11 | 1 | invalid syntax | `from sympy.functions import Abs, im, re` |
| 1212 | venv_creative/lib/python3.13/site-packages/sympy/assumptions/handlers/sets.py | 14 | 1 | invalid syntax | `from sympy.core.relational import Eq` |
| 1213 | venv_creative/lib/python3.13/site-packages/sympy/plotting/series.py | 44 | 5 | invalid syntax | `def _print_Or(self, expr):` |
| 1214 | venv_creative/lib/python3.13/site-packages/sympy/plotting/pygletplot/plot_surface.py | 21 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `evaluate = self._get_evaluator()` |
| 1215 | venv_creative/lib/python3.13/site-packages/sympy/plotting/pygletplot/color_scheme.py | 79 | 5 | invalid syntax | `def _interpret_args(self, args):` |
| 1216 | venv_creative/lib/python3.13/site-packages/sympy/plotting/pygletplot/plot_axes.py | 10 | 1 | invalid syntax | `from sympy.utilities.iterables import is_sequence` |
| 1217 | venv_creative/lib/python3.13/site-packages/sympy/plotting/intervalmath/lib_interval.py | 182 | 5 | invalid syntax | `else:` |
| 1218 | venv_creative/lib/python3.13/site-packages/sympy/plotting/tests/test_series.py | 5 | 1 | invalid syntax | `from sympy.external import import_module` |
| 1219 | venv_creative/lib/python3.13/site-packages/sympy/sets/fancysets.py | 669 | 25 | invalid syntax | `if slc.step == 0:` |
| 1220 | venv_creative/lib/python3.13/site-packages/sympy/sets/sets.py | 2589 | 33 | unterminated string literal (detected at line 2590) | `raise TypeError("Invalid input: '%s', input args \` |
| 1221 | venv_creative/lib/python3.13/site-packages/sympy/sets/tests/test_sets.py | 30 | 1 | invalid syntax | `from sympy.testing.pytest import XFAIL, raises, warns_deprecated_sympy` |
| 1222 | venv_creative/lib/python3.13/site-packages/sympy/combinatorics/tensor_can.py | 8 | 1 | invalid syntax | `"""` |
| 1223 | venv_creative/lib/python3.13/site-packages/sympy/combinatorics/free_groups.py | 109 | 22 | invalid syntax. Perhaps you forgot a comma? | `raise ValueError("The type of `symbols` must be one of the following: "` |
| 1224 | venv_creative/lib/python3.13/site-packages/sympy/combinatorics/pc_groups.py | 502 | 24 | unexpected indent | `gens = conj**-1 * collected_gens[j]*conj` |
| 1225 | venv_creative/lib/python3.13/site-packages/sympy/combinatorics/perm_groups.py | 10 | 1 | invalid syntax | `from sympy.combinatorics.util import (_base_ordering, _check_cycles_alt_sym,` |
| 1226 | venv_creative/lib/python3.13/site-packages/sympy/combinatorics/fp_groups.py | 10 | 1 | invalid syntax | `from sympy.combinatorics.free_groups import FreeGroup, FreeGroupElement, free_group` |
| 1227 | venv_creative/lib/python3.13/site-packages/sympy/combinatorics/tests/test_pc_groups.py | 5 | 1 | invalid syntax | `from sympy.combinatorics.permutations import Permutation` |
| 1228 | venv_creative/lib/python3.13/site-packages/sympy/combinatorics/tests/test_perm_groups.py | 8 | 1 | invalid syntax | `from sympy.combinatorics.perm_groups import (Coset, PermutationGroup,` |
| 1229 | venv_creative/lib/python3.13/site-packages/sympy/combinatorics/tests/test_permutations.py | 8 | 1 | invalid syntax | `from sympy.core.expr import unchanged` |
| 1230 | venv_creative/lib/python3.13/site-packages/sympy/interactive/printing.py | 63 | 12 | unexpected indent | `else:` |
| 1231 | venv_creative/lib/python3.13/site-packages/sympy/functions/special/hyper.py | 21 | 1 | invalid syntax | `from sympy.functions.elementary.complexes import Abs, re, unpolarify` |
| 1232 | venv_creative/lib/python3.13/site-packages/sympy/functions/special/polynomials.py | 17 | 1 | invalid syntax | `from sympy.functions.elementary.complexes import re` |
| 1233 | venv_creative/lib/python3.13/site-packages/sympy/functions/special/elliptic_integrals.py | 89 | 12 | unexpected indent | `return hyperexpand(self.rewrite(hyper)._eval_nseries(x, n = n, logx = logx))` |
| 1234 | venv_creative/lib/python3.13/site-packages/sympy/functions/special/bessel.py | 81 | 5 | invalid syntax | `def _eval_conjugate(self):` |
| 1235 | venv_creative/lib/python3.13/site-packages/sympy/functions/special/tests/test_hyper.py | 55 | 5 | invalid syntax | `assert td(h, z)` |
| 1236 | venv_creative/lib/python3.13/site-packages/sympy/functions/combinatorial/numbers.py | 35 | 1 | invalid syntax | `from sympy.ntheory.generate import _primepi` |
| 1237 | venv_creative/lib/python3.13/site-packages/sympy/functions/combinatorial/factorials.py | 100 | 63 | invalid syntax. Perhaps you forgot a comma? | `35102025, 5014575, 145422675, 9694845, 300540195, 300540195` |
| 1238 | venv_creative/lib/python3.13/site-packages/sympy/functions/combinatorial/tests/test_comb_numbers.py | 21 | 1 | invalid syntax | `from sympy.functions.combinatorial.numbers import _nT, carmichael` |
| 1239 | venv_creative/lib/python3.13/site-packages/sympy/functions/elementary/integers.py | 50 | 9 | invalid syntax | `for t in Add.make_args(arg):` |
| 1240 | venv_creative/lib/python3.13/site-packages/sympy/functions/elementary/complexes.py | 10 | 1 | invalid syntax | `from sympy.core.logic import fuzzy_not, fuzzy_or` |
| 1241 | venv_creative/lib/python3.13/site-packages/sympy/functions/elementary/trigonometric.py | 10 | 1 | invalid syntax | `from sympy.core.logic import FuzzyBool, fuzzy_and, fuzzy_not, fuzzy_or` |
| 1242 | venv_creative/lib/python3.13/site-packages/sympy/functions/elementary/exponential.py | 13 | 1 | invalid syntax | `from sympy.core.logic import fuzzy_and, fuzzy_not, fuzzy_or` |
| 1243 | venv_creative/lib/python3.13/site-packages/sympy/functions/elementary/tests/test_miscellaneous.py | 16 | 1 | invalid syntax | `from sympy.functions.elementary.trigonometric import cos, sin` |
| 1244 | venv_creative/lib/python3.13/site-packages/sympy/functions/elementary/tests/test_complexes.py | 33 | 32 | invalid decimal literal | `return comp(a.n(), b.n(), 1.e - 6)` |
| 1245 | venv_creative/lib/python3.13/site-packages/sympy/tensor/index_methods.py | 303 | 1 | invalid syntax | `def get_contraction_structure(expr):` |
| 1246 | venv_creative/lib/python3.13/site-packages/sympy/tensor/tensor.py | 47 | 1 | invalid syntax | `from sympy.core import Add, Basic, Expr, Mul, S, sympify` |
| 1247 | venv_creative/lib/python3.13/site-packages/sympy/tensor/array/array_comprehension.py | 42 | 30 | invalid syntax. Perhaps you forgot a comma? | `raise ValueError('ArrayComprehension requires values lower and upper bound'` |
| 1248 | venv_creative/lib/python3.13/site-packages/sympy/tensor/array/expressions/from_array_to_matrix.py | 42 | 1 | invalid syntax | `from sympy.tensor.array.expressions.utils import _get_mapping_from_subranks` |
| 1249 | venv_creative/lib/python3.13/site-packages/sympy/tensor/array/expressions/from_indexed_to_array.py | 24 | 1 | invalid syntax | `from sympy.tensor.array.expressions.utils import _get_argindex, _get_diagonal_indices` |
| 1250 | venv_creative/lib/python3.13/site-packages/sympy/tensor/array/expressions/array_expressions.py | 33 | 1 | invalid syntax | `from sympy.tensor.array.dense_ndim_array import ImmutableDenseNDimArray` |
| 1251 | venv_creative/lib/python3.13/site-packages/sympy/tensor/tests/test_tensor.py | 23 | 1 | invalid syntax | `from sympy.testing.pytest import XFAIL, raises, warns_deprecated_sympy` |
| 1252 | venv_creative/lib/python3.13/site-packages/sympy/geometry/line.py | 85 | 9 | invalid syntax | `if len(p1) != len(p2):` |
| 1253 | venv_creative/lib/python3.13/site-packages/sympy/geometry/polygon.py | 19 | 1 | invalid syntax | `from sympy.utilities.misc import as_int, func_name` |
| 1254 | venv_creative/lib/python3.13/site-packages/sympy/geometry/entity.py | 62 | 9 | invalid syntax. Perhaps you forgot a comma? | `"Parabola"` |
| 1255 | venv_creative/lib/python3.13/site-packages/sympy/geometry/ellipse.py | 126 | 5 | invalid syntax | `def __hash__(self):` |
| 1256 | venv_creative/lib/python3.13/site-packages/sympy/geometry/plane.py | 26 | 1 | invalid syntax | `from .point import Point, Point3D` |
| 1257 | venv_creative/lib/python3.13/site-packages/sympy/geometry/tests/test_point.py | 198 | 5 | invalid syntax | `assert Point3D.midpoint(p2, p2) == p2` |
| 1258 | venv_creative/lib/python3.13/site-packages/sympy/geometry/tests/test_plane.py | 10 | 1 | invalid syntax | `from sympy.geometry.util import are_coplanar` |
| 1259 | venv_creative/lib/python3.13/site-packages/sympy/geometry/tests/test_ellipse.py | 14 | 1 | invalid syntax | `from sympy.geometry.line import Segment2D` |
| 1260 | venv_creative/lib/python3.13/site-packages/sympy/physics/secondquant.py | 72 | 1 | invalid syntax | `class SecondQuantizationError(Exception):` |
| 1261 | venv_creative/lib/python3.13/site-packages/sympy/physics/tests/test_qho_1d.py | 50 | 27 | unindent does not match any outer indentation level | `for i in range(n + 1):` |
| 1262 | venv_creative/lib/python3.13/site-packages/sympy/physics/tests/test_secondquant.py | 23 | 1 | invalid syntax | `from sympy.printing.latex import latex` |
| 1263 | venv_creative/lib/python3.13/site-packages/sympy/physics/mechanics/functions.py | 13 | 1 | invalid syntax | `from sympy.simplify.simplify import simplify` |
| 1264 | venv_creative/lib/python3.13/site-packages/sympy/physics/mechanics/linearize.py | 110 | 76 | invalid syntax. Perhaps you forgot a comma? | `self._qd_dup = Matrix([var if var not in dup_vars else Dummy() for var` |
| 1265 | venv_creative/lib/python3.13/site-packages/sympy/physics/mechanics/tests/test_joint.py | 1476 | 32 | too many nested parentheses | `assert A.dcm(N) == Matrix([[-1, 0, 0],` |
| 1266 | venv_creative/lib/python3.13/site-packages/sympy/physics/mechanics/tests/test_linearize.py | 8 | 1 | invalid syntax | `from sympy.simplify.simplify import simplify` |
| 1267 | venv_creative/lib/python3.13/site-packages/sympy/physics/mechanics/tests/test_kane2.py | 7 | 1 | invalid syntax | `from sympy.simplify.simplify import simplify` |
| 1268 | venv_creative/lib/python3.13/site-packages/sympy/physics/mechanics/tests/test_kane3.py | 327 | 12 | invalid decimal literal | `eps = 1.e - 12` |
| 1269 | venv_creative/lib/python3.13/site-packages/sympy/physics/units/unitsystem.py | 63 | 5 | invalid syntax | `def __repr__(self):` |
| 1270 | venv_creative/lib/python3.13/site-packages/sympy/physics/units/util.py | 109 | 29 | invalid syntax | `if isinstance(expr, Add):` |
| 1271 | venv_creative/lib/python3.13/site-packages/sympy/physics/units/tests/test_quantities.py | 19 | 1 | invalid syntax | `from sympy.physics.units.definitions import (amu, au, bit, byte, centimeter, coulomb,` |
| 1272 | venv_creative/lib/python3.13/site-packages/sympy/physics/continuum_mechanics/beam.py | 535 | 9 | invalid syntax | `else:` |
| 1273 | venv_creative/lib/python3.13/site-packages/sympy/physics/vector/functions.py | 7 | 1 | invalid syntax | `from sympy.integrals.integrals import integrate` |
| 1274 | venv_creative/lib/python3.13/site-packages/sympy/physics/vector/frame.py | 216 | 13 | cannot assign to attribute here. Maybe you meant '==' instead of '='? | `self.indices = indices` |
| 1275 | venv_creative/lib/python3.13/site-packages/sympy/physics/vector/fieldfunctions.py | 8 | 11 | '[' was never closed | `__all__ = ['curl', 'divergence', 'gradient', 'is_conservative',` |
| 1276 | venv_creative/lib/python3.13/site-packages/sympy/physics/vector/dyadic.py | 52 | 21 | invalid syntax. Perhaps you forgot a comma? | `inlist.remove(inlist[0])` |
| 1277 | venv_creative/lib/python3.13/site-packages/sympy/physics/control/lti.py | 24 | 1 | invalid syntax | `from sympy.matrices.expressions import MatAdd, MatMul` |
| 1278 | venv_creative/lib/python3.13/site-packages/sympy/physics/control/tests/test_lti.py | 28 | 55 | unterminated string literal (detected at line 29) | `a, x, b, c, s, g, d, p, k, tau, zeta, wn, T = symbols('a, x, b, c, s, g, d, p, k,\` |
| 1279 | venv_creative/lib/python3.13/site-packages/sympy/physics/optics/gaussopt.py | 45 | 1 | invalid syntax | `from sympy.core.expr import Expr` |
| 1280 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/matrixutils.py | 10 | 11 | '[' was never closed | `__all__ = [` |
| 1281 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/spin.py | 61 | 1 | invalid syntax | `def m_values(j):` |
| 1282 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/sho1d.py | 122 | 5 | invalid syntax | `def _eval_adjoint(self):` |
| 1283 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/hilbert.py | 94 | 30 | unterminated string literal (detected at line 95) | `raise ValueError('The third argument to __pow__ is not supported \` |
| 1284 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/tensorproduct.py | 16 | 1 | invalid syntax | `from sympy.physics.quantum.matrixutils import (matrix_tensor_product, numpy_ndarray,` |
| 1285 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/gate.py | 78 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_normalized = True` |
| 1286 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/anticommutator.py | 23 | 1 | invalid syntax | `class AntiCommutator(Expr):` |
| 1287 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/commutator.py | 24 | 1 | invalid syntax | `class Commutator(Expr):` |
| 1288 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/state.py | 29 | 9 | invalid syntax. Perhaps you forgot a comma? | `'Wavefunction'` |
| 1289 | venv_creative/lib/python3.13/site-packages/sympy/physics/quantum/tests/test_sho1d.py | 25 | 1 | invalid syntax | `from sympy.simplify import simplify` |
| 1290 | venv_creative/lib/python3.13/site-packages/sympy/external/pythonmpq.py | 68 | 20 | unexpected indent | `denominator //= divisor` |
| 1291 | venv_creative/lib/python3.13/site-packages/sympy/external/tests/test_codegen.py | 87 | 9 | invalid syntax. Perhaps you forgot a comma? | `"cc main.o codegen.o -lm -o test.exe"` |
| 1292 | venv_creative/lib/python3.13/site-packages/sympy/parsing/mathematica.py | 19 | 1 | invalid syntax | `from sympy.core.sympify import _sympify, sympify` |
| 1293 | venv_creative/lib/python3.13/site-packages/sympy/parsing/sympy_parser.py | 15 | 1 | invalid syntax | `from typing import Any, Callable` |
| 1294 | venv_creative/lib/python3.13/site-packages/sympy/parsing/tests/test_fortran_parser.py | 13 | 5 | invalid syntax | `from sympy.core import Add, Float, Integer` |
| 1295 | venv_creative/lib/python3.13/site-packages/sympy/parsing/tests/test_sympy_parser.py | 11 | 1 | invalid syntax | `from sympy.functions import Max, Min, exp, factorial, factorial2, sin` |
| 1296 | venv_creative/lib/python3.13/site-packages/sympy/parsing/tests/test_custom_latex.py | 7 | 38 | '(' was never closed | `from sympy.parsing.latex.lark import (LarkLaTeXParser, TransformToSymPyExpr,` |
| 1297 | venv_creative/lib/python3.13/site-packages/sympy/parsing/autolev/_listener_autolev_antlr.py | 19 | 17 | invalid syntax. Perhaps you forgot a comma? | `AutolevParser = getattr(autolevparser, 'AutolevParser', None)` |
| 1298 | venv_creative/lib/python3.13/site-packages/sympy/parsing/c/c_parser.py | 56 | 5 | invalid syntax | `from sympy.codegen.cnodes import (PostDecrement, PostIncrement, PreDecrement,` |
| 1299 | venv_creative/lib/python3.13/site-packages/sympy/calculus/singularities.py | 27 | 1 | invalid syntax | `from sympy.functions.elementary.trigonometric import cos, cot, csc, sec, tan` |
| 1300 | venv_creative/lib/python3.13/site-packages/sympy/calculus/tests/test_finite_diff.py | 7 | 1 | invalid syntax | `from sympy.core.function import Function, diff` |
| 1301 | venv_creative/lib/python3.13/site-packages/sympy/simplify/simplify.py | 13 | 1 | invalid syntax | `from sympy.core.exprtools import factor_nc` |
| 1302 | venv_creative/lib/python3.13/site-packages/sympy/simplify/combsimp.py | 54 | 31 | unindent does not match any outer indentation level | `return gammasimp(expr)` |
| 1303 | venv_creative/lib/python3.13/site-packages/sympy/simplify/trigsimp.py | 820 | 20 | closing parenthesis '}' does not match opening parenthesis '(' on line 815 | `}[method]` |
| 1304 | venv_creative/lib/python3.13/site-packages/sympy/simplify/hyperexpand.py | 71 | 1 | invalid syntax | `from sympy.core.mod import Mod` |
| 1305 | venv_creative/lib/python3.13/site-packages/sympy/simplify/tests/test_simplify.py | 11 | 1 | invalid syntax | `from sympy.core.mul import Mul, _keep_coeff` |
| 1306 | venv_creative/lib/python3.13/site-packages/sympy/simplify/tests/test_cse.py | 25 | 1 | invalid syntax | `from sympy.matrices.dense import Matrix` |
| 1307 | venv_creative/lib/python3.13/site-packages/sympy/simplify/tests/test_hyperexpand.py | 31 | 1 | invalid syntax | `from sympy.testing.pytest import XFAIL, raises, slow, tooslow` |
| 1308 | venv_creative/lib/python3.13/site-packages/sympy/vector/functions.py | 65 | 25 | unterminated string literal (detected at line 66) | `raise TypeError("system should be a CoordSys3D \` |
| 1309 | venv_creative/lib/python3.13/site-packages/sympy/vector/coordsysrect.py | 23 | 1 | invalid syntax | `from sympy.vector.scalar import BaseScalar` |
| 1310 | venv_creative/lib/python3.13/site-packages/sympy/vector/point.py | 24 | 9 | invalid syntax | `if (not isinstance(parent_point, Point) and` |
| 1311 | venv_creative/lib/python3.13/site-packages/sympy/vector/integrals.py | 13 | 1 | invalid syntax | `from sympy.vector.operators import _get_coord_systems` |
| 1312 | venv_creative/lib/python3.13/site-packages/sympy/vector/dyadic.py | 13 | 1 | invalid syntax | `class Dyadic(BasisDependent):` |
| 1313 | venv_creative/lib/python3.13/site-packages/sympy/diffgeom/diffgeom.py | 12 | 1 | invalid syntax | `from sympy.core.cache import cacheit` |
| 1314 | venv_creative/lib/python3.13/site-packages/sympy/stats/symbolic_probability.py | 22 | 9 | invalid syntax | `__all__ = ['Probability', 'Expectation', 'Variance', 'Covariance']` |
| 1315 | venv_creative/lib/python3.13/site-packages/sympy/stats/stochastic_process_types.py | 49 | 1 | invalid syntax | `from sympy.stats.stochastic_process import StochasticPSpace` |
| 1316 | venv_creative/lib/python3.13/site-packages/sympy/stats/tests/test_continuous_rv.py | 45 | 1 | invalid syntax | `from sympy.stats.compound_rv import CompoundPSpace` |
| 1317 | venv_creative/lib/python3.13/site-packages/sympy/matrices/sparsetools.py | 218 | 16 | unexpected indent | `if not isinstance(args[-1], (dict, Dict)):` |
| 1318 | venv_creative/lib/python3.13/site-packages/sympy/matrices/matrixbase.py | 44 | 1 | invalid syntax | `from .determinant import (_adjugate, _charpoly, _cofactor, _cofactor_matrix, _det,` |
| 1319 | venv_creative/lib/python3.13/site-packages/sympy/matrices/common.py | 43 | 1 | invalid syntax | `from .utilities import _dotprodsimp, _get_intermediate_simp_bool, _simplify` |
| 1320 | venv_creative/lib/python3.13/site-packages/sympy/matrices/tests/test_sparse.py | 10 | 1 | invalid syntax | `from sympy.polys.polytools import PurePoly` |
| 1321 | venv_creative/lib/python3.13/site-packages/sympy/matrices/tests/test_determinant.py | 30 | 1 | invalid syntax | `def test_eval_determinant(method, M, sol):` |
| 1322 | venv_creative/lib/python3.13/site-packages/sympy/matrices/tests/test_eigen.py | 30 | 5 | invalid syntax | `assert M.left_eigenvects() == (` |
| 1323 | venv_creative/lib/python3.13/site-packages/sympy/matrices/tests/test_matrices.py | 2225 | 40 | too many nested parentheses | `raises(ValueError, lambda: Matrix([[1, 2], [3, 4]]).minor(4, 5))` |
| 1324 | venv_creative/lib/python3.13/site-packages/sympy/matrices/tests/test_matrixbase.py | 2258 | 17 | too many nested parentheses | `M = Matrix([[1,2,3],` |
| 1325 | venv_creative/lib/python3.13/site-packages/sympy/matrices/expressions/matmul.py | 63 | 9 | invalid syntax | `if check is not False:` |
| 1326 | venv_creative/lib/python3.13/site-packages/sympy/matrices/expressions/trace.py | 63 | 16 | unexpected indent | `return expr._eval_derivative(v)` |
| 1327 | venv_creative/lib/python3.13/site-packages/sympy/matrices/expressions/diagonal.py | 181 | 12 | unexpected indent | `return obj` |
| 1328 | venv_creative/lib/python3.13/site-packages/pygments/style.py | 137 | 16 | unexpected indent | `color = _ansimap[color]` |
| 1329 | venv_creative/lib/python3.13/site-packages/pygments/filters/__init__.py | 20 | 1 | invalid syntax | `from pygments.util import (ClassNotFound, OptionError, get_bool_opt, get_choice_opt,` |
| 1330 | venv_creative/lib/python3.13/site-packages/pygments/lexers/_postgres_builtins.py | 572 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `PSEUDO_TYPES = tuple(sorted(set(PSEUDO_TYPES) - set(map(str.lower, KEYWORDS))))` |
| 1331 | venv_creative/lib/python3.13/site-packages/pygments/lexers/objective.py | 201 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 195 | `}` |
| 1332 | venv_creative/lib/python3.13/site-packages/pygments/lexers/robotframework.py | 151 | 5 | invalid syntax | `def _start_table(self, header):` |
| 1333 | venv_creative/lib/python3.13/site-packages/pygments/lexers/textfmts.py | 97 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 91 | `}` |
| 1334 | venv_creative/lib/python3.13/site-packages/pygments/lexers/scripting.py | 180 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 174 | `}` |
| 1335 | venv_creative/lib/python3.13/site-packages/pygments/lexers/ruby.py | 445 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 440 | `}` |
| 1336 | venv_creative/lib/python3.13/site-packages/pygments/lexers/tnt.py | 19 | 9 | invalid syntax | `__all__ = ['TNTLexer']` |
| 1337 | venv_creative/lib/python3.13/site-packages/pygments/lexers/freefem.py | 50 | 8 | unexpected indent | `preprocessor = {'ENDIFMACRO', 'include', 'IFMACRO', 'load'}` |
| 1338 | venv_creative/lib/python3.13/site-packages/pygments/lexers/ml.py | 406 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 398 | `}` |
| 1339 | venv_creative/lib/python3.13/site-packages/pygments/lexers/templates.py | 203 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 187 | `}` |
| 1340 | venv_creative/lib/python3.13/site-packages/pygments/lexers/pascal.py | 275 | 5 | closing parenthesis '}' does not match opening parenthesis '(' on line 252 | `}` |
| 1341 | venv_creative/lib/python3.13/site-packages/pygments/lexers/textedit.py | 85 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 57 | `}` |
| 1342 | venv_creative/lib/python3.13/site-packages/pygments/lexers/modula2.py | 354 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 337 | `}` |
| 1343 | venv_creative/lib/python3.13/site-packages/pygments/lexers/sql.py | 228 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 221 | `}` |
| 1344 | venv_creative/lib/python3.13/site-packages/pygments/lexers/haskell.py | 181 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 170 | `}` |
| 1345 | venv_creative/lib/python3.13/site-packages/pygments/lexers/special.py | 78 | 39 | '(' was never closed | `self.compress = get_choice_opt(options, 'compress',` |
| 1346 | venv_creative/lib/python3.13/site-packages/pygments/lexers/data.py | 498 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 480 | `}` |
| 1347 | venv_creative/lib/python3.13/site-packages/pygments/formatters/html.py | 45 | 12 | unexpected indent | `else:` |
| 1348 | venv_creative/lib/python3.13/site-packages/pygments/formatters/img.py | 38 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `STYLES = {` |
| 1349 | venv_creative/lib/python3.13/site-packages/pygments/formatters/terminal256.py | 218 | 16 | unexpected indent | `self.best_match[color] = index` |
| 1350 | venv_creative/lib/python3.13/site-packages/pygments/formatters/rtf.py | 126 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.lineno_padding = get_int_opt(options, 'lineno_padding', 2)` |
| 1351 | venv_creative/lib/python3.13/site-packages/semantic_version/__init__.py | 12 | 46 | unindent does not match any outer indentation level | `__version__ = version("semantic_version")` |
| 1352 | venv_creative/lib/python3.13/site-packages/semantic_version/base.py | 19 | 1 | invalid syntax | `class MaxIdentifier(object):` |
| 1353 | venv_creative/lib/python3.13/site-packages/chunk/__init__.py | 54 | 14 | '(' was never closed | `warnings.warn(` |
| 1354 | venv_creative/lib/python3.13/site-packages/aiofiles/base.py | 13 | 12 | unexpected indent | `self._ref_loop = loop` |
| 1355 | venv_creative/lib/python3.13/site-packages/pycparser/c_ast.py | 46 | 16 | unexpected indent | `result += indent` |
| 1356 | venv_creative/lib/python3.13/site-packages/pycparser/c_generator.py | 86 | 20 | unexpected indent | `elif n.op == 'p--':` |
| 1357 | venv_creative/lib/python3.13/site-packages/pycparser/ply/yacc.py | 487 | 13 | invalid syntax | `if t is not None:` |
| 1358 | venv_creative/lib/python3.13/site-packages/pycparser/ply/cpp.py | 24 | 10 | '(' was never closed | `tokens = (` |
| 1359 | venv_creative/lib/python3.13/site-packages/typer/models.py | 222 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 177 | `):` |
| 1360 | venv_creative/lib/python3.13/site-packages/typer/_completion_shared.py | 103 | 1 | invalid syntax | `def install_bash(*, prog_name: str, complete_var: str, shell: str) -> Path:` |
| 1361 | venv_creative/lib/python3.13/site-packages/typer/main.py | 26 | 1 | invalid syntax | `from .models import (AnyType, ArgumentInfo, CommandFunctionType, CommandInfo, Default,` |
| 1362 | venv_creative/lib/python3.13/site-packages/mpmath/rational.py | 243 | 16 | unexpected indent | `return NotImplemented` |
| 1363 | venv_creative/lib/python3.13/site-packages/mpmath/ctx_mp_python.py | 21 | 1 | invalid syntax | `from .libmp.backend import basestring, exec_` |
| 1364 | venv_creative/lib/python3.13/site-packages/mpmath/visualization.py | 65 | 32 | unexpected indent | `v = func(x[i])` |
| 1365 | venv_creative/lib/python3.13/site-packages/mpmath/ctx_iv.py | 4 | 20 | '(' was never closed | `from .libmp import (MPZ_ONE, ComplexResult, dps_to_prec, finf, fnan, fninf, from_float,` |
| 1366 | venv_creative/lib/python3.13/site-packages/mpmath/ctx_mp.py | 29 | 1 | invalid syntax | `from .libmp.backend import BACKEND, basestring` |
| 1367 | venv_creative/lib/python3.13/site-packages/mpmath/math2.py | 125 | 1 | invalid syntax | `def nthroot(x, n):` |
| 1368 | venv_creative/lib/python3.13/site-packages/mpmath/ctx_base.py | 271 | 30 | invalid syntax | `if not len(args) >= 1:` |
| 1369 | venv_creative/lib/python3.13/site-packages/mpmath/libmp/backend.py | 77 | 20 | unexpected indent | `if gmpy.version() >= '1.03':` |
| 1370 | venv_creative/lib/python3.13/site-packages/mpmath/libmp/libintmath.py | 61 | 8 | unexpected indent | `rshift = operator.rshift` |
| 1371 | venv_creative/lib/python3.13/site-packages/mpmath/libmp/libhyper.py | 29 | 1 | invalid syntax | `from .libelefun import (agm_fixed, mpf_cos, mpf_cos_sin, mpf_exp, mpf_log, mpf_pi,` |
| 1372 | venv_creative/lib/python3.13/site-packages/mpmath/libmp/gammazeta.py | 39 | 1 | invalid syntax | `from .libelefun import constant_memo, def_mpf_constant` |
| 1373 | venv_creative/lib/python3.13/site-packages/mpmath/libmp/libmpf.py | 19 | 1 | invalid syntax | `from .libintmath import (bctable, bin_to_radix, bitcount, giant_steps, isqrt,` |
| 1374 | venv_creative/lib/python3.13/site-packages/mpmath/libmp/libmpc.py | 26 | 1 | invalid syntax | `from .libelefun import (mpf_cos_sin, mpf_cosh_sinh, mpf_exp, mpf_log, mpf_log_hypot,` |
| 1375 | venv_creative/lib/python3.13/site-packages/mpmath/libmp/libmpi.py | 12 | 1 | invalid syntax | `from .libmpf import (MPZ_ONE, ComplexResult, bitcount, dps_to_prec, fhalf, finf, fnan,` |
| 1376 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_trig.py | 21 | 16 | invalid decimal literal | `assert sin(1e - 6j).ae(1.0000000000001666e - 006j, rel_eps = 2e-15, abs_eps = 0)` |
| 1377 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_linalg.py | 123 | 51 | invalid decimal literal | `assert mnorm(A * inv - eye(A.rows), 1) < 1.e - 14` |
| 1378 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_rootfinding.py | 88 | 69 | invalid decimal literal | `assert mnorm(jacobian(f, (1,-2)) - matrix([[6,8],[0,-2]]),1) < 1.e - 7` |
| 1379 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_elliptic.py | 91 | 14 | did you forget parentheses around the comprehension target? | `math1 = [(mpf(1)/10, mpf('0.006584651553858370274473060')),` |
| 1380 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_visualization.py | 17 | 16 | unexpected indent | `import pylab` |
| 1381 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_power.py | 141 | 12 | unexpected indent | `assert powr(pos10001, 5, r) == 1` |
| 1382 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_fp.py | 84 | 32 | invalid decimal literal | `assert ae(fp.sinpi(1e-10 + 1e - 10j), (3.141592653589793353e-10 + 3.1415926535897933528e - 10j))` |
| 1383 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_basic_ops.py | 134 | 20 | invalid decimal literal | `assert mpc(2 + 1e - 15j).ae(2)` |
| 1384 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_ode.py | 78 | 8 | unexpected indent | `f = odefun(lambda x, y: [-y[1], y[0]], 0, [1, 0])` |
| 1385 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_hp.py | 227 | 12 | unexpected indent | `n = int(round(b))` |
| 1386 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_functions.py | 188 | 21 | invalid decimal literal | `assert (log(1 + 1e - 8j).real * 10**16).ae(0.5)` |
| 1387 | venv_creative/lib/python3.13/site-packages/mpmath/tests/torture.py | 75 | 12 | unexpected indent | `exponents = range(-20,20)` |
| 1388 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_gammazeta.py | 368 | 25 | invalid decimal literal | `assert psi0(1e-10 + 1e - 10j).ae(-5000000000.577215 + 5000000000.000000j)` |
| 1389 | venv_creative/lib/python3.13/site-packages/mpmath/tests/test_functions2.py | 321 | 97 | invalid decimal literal | `assert e1(fmul(10**20, j, exact = True)).ae(6.4525128526578084421e-21 - 7.6397040444172830039e - 21j, abs_eps = 0, rel_eps = 8 * eps)` |
| 1390 | venv_creative/lib/python3.13/site-packages/mpmath/functions/zeta.py | 165 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `comb3 = ctx.sum_accurately(terms, 1)` |
| 1391 | venv_creative/lib/python3.13/site-packages/mpmath/functions/functions.py | 46 | 30 | '{' was never closed | `self._aliases.update({` |
| 1392 | venv_creative/lib/python3.13/site-packages/mpmath/functions/qfunctions.py | 286 | 24 | unexpected indent | `t /= p` |
| 1393 | venv_creative/lib/python3.13/site-packages/mpmath/functions/elliptic.py | 353 | 25 | '(' was never closed | `raise ValueError("First argument must be a two - character string "` |
| 1394 | venv_creative/lib/python3.13/site-packages/mpmath/functions/hypergeometric.py | 33 | 40 | unindent does not match any outer indentation level | `if data_index == 2:` |
| 1395 | venv_creative/lib/python3.13/site-packages/mpmath/functions/orthogonal.py | 33 | 12 | unexpected indent | `can_use_2f0 = ctx.isnpint(-n) or ctx.re(z) > 0 or \` |
| 1396 | venv_creative/lib/python3.13/site-packages/mpmath/functions/theta.py | 1001 | 16 | unexpected indent | `finally:` |
| 1397 | venv_creative/lib/python3.13/site-packages/mpmath/functions/rszeta.py | 1202 | 8 | unexpected indent | `ctx.prec = 53` |
| 1398 | venv_creative/lib/python3.13/site-packages/mpmath/functions/bessel.py | 47 | 13 | invalid syntax | `finally:` |
| 1399 | venv_creative/lib/python3.13/site-packages/mpmath/calculus/inverselaplace.py | 200 | 12 | unexpected indent | `self.t = self.ctx.convert(t)` |
| 1400 | venv_creative/lib/python3.13/site-packages/mpmath/calculus/quadrature.py | 134 | 20 | unexpected indent | `else:` |
| 1401 | venv_creative/lib/python3.13/site-packages/mpmath/calculus/optimization.py | 277 | 30 | invalid syntax. Perhaps you forgot a comma? | `raise ValueError('expected 1, 2 or 3 starting points, got %i'` |
| 1402 | venv_creative/lib/python3.13/site-packages/mpmath/calculus/approximation.py | 138 | 12 | unexpected indent | `err = ctx.zero` |
| 1403 | venv_creative/lib/python3.13/site-packages/mpmath/calculus/odes.py | 262 | 16 | unexpected indent | `n = bisect(series_boundaries, x)` |
| 1404 | venv_creative/lib/python3.13/site-packages/mpmath/calculus/extrapolation.py | 1198 | 16 | unexpected indent | `best = partial[-1]` |
| 1405 | venv_creative/lib/python3.13/site-packages/mpmath/matrices/matrices.py | 343 | 46 | invalid syntax | `if isinstance(args[0], (list, tuple)):` |
| 1406 | venv_creative/lib/python3.13/site-packages/mpmath/matrices/linalg.py | 508 | 29 | '(' was never closed | `s = c - ctx.fsum((L[j,k] for k in xrange(j)),` |
| 1407 | venv_creative/lib/python3.13/site-packages/mpmath/matrices/eigen_symmetric.py | 1100 | 16 | unexpected indent | `nm = k - 1` |
| 1408 | venv_creative/lib/python3.13/site-packages/pyparsing/core.py | 2234 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 2229 | `) -> tuple[bool, list[tuple[str, Union[ParseResults, Exception]]]]:` |
| 1409 | venv_creative/lib/python3.13/site-packages/resampy/interpn.py | 37 | 12 | unexpected indent | `eta = index_frac - offset` |
| 1410 | venv_creative/lib/python3.13/site-packages/past/translation/__init__.py | 73 | 19 | invalid syntax | `py2_detect_fixers = [` |
| 1411 | venv_creative/lib/python3.13/site-packages/jinja2/runtime.py | 24 | 3 | invalid syntax | `V = t.TypeVar("V")` |
| 1412 | venv_creative/lib/python3.13/site-packages/jinja2/lexer.py | 681 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 671 | `}` |
| 1413 | venv_creative/lib/python3.13/site-packages/jinja2/nativetypes.py | 43 | 5 | invalid syntax | `except (ValueError, SyntaxError, MemoryError):` |
| 1414 | venv_creative/lib/python3.13/site-packages/cryptography/hazmat/primitives/ciphers/modes.py | 15 | 1 | invalid syntax | `from cryptography.hazmat.primitives.ciphers import algorithms` |
| 1415 | venv_creative/lib/python3.13/site-packages/cryptography/x509/name.py | 129 | 1 | invalid syntax | `class NameAttribute(typing.Generic[NameAttributeValueType]):` |
| 1416 | venv_creative/lib/python3.13/site-packages/soupsieve/css_parser.py | 242 | 1 | invalid syntax | `def _purge_cache() -> None:` |
| 1417 | venv_creative/lib/python3.13/site-packages/soupsieve/css_match.py | 49 | 5 | invalid syntax. Perhaps you forgot a comma? | `r'^(?P < year>[0 - 9]{4,})-(?P < month>[0 - 9]{2})-(?P < day>[0 - 9]{2})T(?P < hour>[0 - 9]{2}):(?P < minutes>[0 - 9]{2})$'` |
| 1418 | venv_creative/lib/python3.13/site-packages/fsspec/generic.py | 106 | 5 | invalid syntax | `logger.debug(f"{len(dirs)} directories to create")` |
| 1419 | venv_creative/lib/python3.13/site-packages/fsspec/asyn.py | 165 | 12 | unexpected indent | `else:` |
| 1420 | venv_creative/lib/python3.13/site-packages/fsspec/core.py | 15 | 1 | invalid syntax | `from fsspec.compression import compr` |
| 1421 | venv_creative/lib/python3.13/site-packages/fsspec/spec.py | 689 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 682 | `}` |
| 1422 | venv_creative/lib/python3.13/site-packages/fsspec/utils.py | 123 | 21 | invalid syntax. Perhaps you forgot a comma? | `f"Collision between inferred and specified storage "` |
| 1423 | venv_creative/lib/python3.13/site-packages/fsspec/tests/abstract/mv.py | 47 | 8 | unexpected indent | `with pytest.raises(PermissionError):` |
| 1424 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/libarchive.py | 7 | 1 | invalid syntax | `import libarchive` |
| 1425 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/memory.py | 53 | 17 | invalid syntax. Perhaps you forgot a comma? | `{` |
| 1426 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/local.py | 249 | 47 | '(' was never closed | `return datetime.datetime.fromtimestamp(` |
| 1427 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/smb.py | 142 | 17 | invalid syntax. Perhaps you forgot a comma? | `"register_session_retry_wait must be a non - negative integer"` |
| 1428 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/http_sync.py | 81 | 9 | invalid syntax | `return self._headers` |
| 1429 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/dbfs.py | 60 | 9 | invalid syntax. Perhaps you forgot a comma? | `self.session.mount("https://", HTTPAdapter(max_retries = self.retries))` |
| 1430 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/cached.py | 129 | 56 | invalid syntax | `if not (fs is None) ^ (target_protocol is None):` |
| 1431 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/cache_metadata.py | 18 | 8 | unexpected indent | `from typing import Any, Literal` |
| 1432 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/http.py | 20 | 1 | invalid syntax | `from ..caching import AllBytes` |
| 1433 | venv_creative/lib/python3.13/site-packages/fsspec/implementations/reference.py | 270 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 262 | `}` |
| 1434 | venv_creative/lib/python3.13/site-packages/markdown/treeprocessors.py | 148 | 31 | invalid syntax | `if not matched:` |
| 1435 | venv_creative/lib/python3.13/site-packages/markdown/htmlparser.py | 427 | 45 | unindent does not match any outer indentation level | `self.handle_starttag(tag, attrs)` |
| 1436 | venv_creative/lib/python3.13/site-packages/markdown/extensions/tables.py | 181 | 65 | unindent does not match any outer indentation level | `tic_points.append((m.start(2), m.end(2) - 1, 1))` |
| 1437 | venv_creative/lib/python3.13/site-packages/markdown/extensions/md_in_html.py | 50 | 13 | invalid syntax. Perhaps you forgot a comma? | `['address', 'dd', 'dt', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'legend', 'li', 'p', 'summary', 'td', 'th']` |
| 1438 | venv_creative/lib/python3.13/site-packages/markdown/extensions/footnotes.py | 87 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 82 | `}` |
| 1439 | venv_creative/lib/python3.13/site-packages/llvmlite/ir/builder.py | 42 | 34 | invalid syntax. Perhaps you forgot a comma? | `raise ValueError("Operands must be the same type, got (%s, %s)"` |
| 1440 | venv_creative/lib/python3.13/site-packages/llvmlite/tests/customize.py | 70 | 9 | positional argument follows keyword argument | `return parser` |
| 1441 | venv_creative/lib/python3.13/site-packages/llvmlite/tests/test_binding.py | 419 | 9 | invalid syntax. Perhaps you forgot a comma? | `'ret'` |
| 1442 | venv_creative/lib/python3.13/site-packages/llvmlite/binding/module.py | 6 | 1 | invalid syntax | `from llvmlite.binding import ffi` |
| 1443 | venv_creative/lib/python3.13/site-packages/diffusers/__init__.py | 54 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 34 | `}` |
| 1444 | venv_creative/lib/python3.13/site-packages/diffusers/modular_pipelines/components_manager.py | 94 | 28 | invalid syntax. Perhaps you forgot a comma? | `end_time = time.perf_counter()` |
| 1445 | venv_creative/lib/python3.13/site-packages/diffusers/modular_pipelines/modular_pipeline.py | 35 | 1 | invalid syntax | `from ..utils import PushToHubMixin, is_accelerate_available, logging` |
| 1446 | venv_creative/lib/python3.13/site-packages/diffusers/modular_pipelines/flux/decoders.py | 66 | 5 | invalid syntax | `@property` |
| 1447 | venv_creative/lib/python3.13/site-packages/diffusers/modular_pipelines/stable_diffusion_xl/before_denoise.py | 28 | 1 | invalid syntax | `from ...pipelines.controlnet.multicontrolnet import MultiControlNetModel` |
| 1448 | venv_creative/lib/python3.13/site-packages/diffusers/quantizers/base.py | 58 | 12 | unexpected indent | `self.modules_to_not_convert = kwargs.pop("modules_to_not_convert", [])` |
| 1449 | venv_creative/lib/python3.13/site-packages/diffusers/quantizers/quanto/quanto_quantizer.py | 10 | 1 | invalid syntax | `from ..base import DiffusersQuantizer` |
| 1450 | venv_creative/lib/python3.13/site-packages/diffusers/quantizers/torchao/torchao_quantizer.py | 31 | 1 | invalid syntax | `from ..base import DiffusersQuantizer` |
| 1451 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pipeline_loading_utils.py | 742 | 5 | closing parenthesis '}' does not match opening parenthesis '(' on line 732 | `}` |
| 1452 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/__init__.py | 13 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1453 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pipeline_utils.py | 34 | 1 | invalid syntax | `from huggingface_hub.utils import OfflineModeIsEnabled, validate_hf_hub_args` |
| 1454 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/free_noise_utils.py | 498 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 493 | `) -> None:` |
| 1455 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_gligen/pipeline_stable_diffusion_gligen.py | 33 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1456 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_gligen/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1457 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_gligen/pipeline_stable_diffusion_gligen_text_image.py | 26 | 1 | invalid syntax | `from ...image_processor import VaeImageProcessor` |
| 1458 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_video_diffusion/pipeline_stable_video_diffusion.py | 31 | 1 | invalid syntax | `from ...utils.torch_utils import is_compiled_module, randn_tensor` |
| 1459 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_video_diffusion/__init__.py | 28 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 22 | `}` |
| 1460 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pia/pipeline_pia.py | 206 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 193 | `):` |
| 1461 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/qwenimage/pipeline_qwenimage_img2img.py | 113 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"The current scheduler class {scheduler.__class__}'s `set_timesteps` does not support custom"` |
| 1462 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/qwenimage/pipeline_qwenimage.py | 109 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"The current scheduler class {scheduler.__class__}'s `set_timesteps` does not support custom"` |
| 1463 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/qwenimage/pipeline_qwenimage_inpaint.py | 116 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"The current scheduler class {scheduler.__class__}'s `set_timesteps` does not support custom"` |
| 1464 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/qwenimage/pipeline_qwenimage_edit.py | 26 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1465 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/mochi/pipeline_mochi.py | 74 | 5 | invalid syntax | `sigma_schedule = linear_sigma_schedule + quadratic_sigma_schedule` |
| 1466 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/mochi/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1467 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/kolors/pipeline_kolors_img2img.py | 953 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 946 | `):` |
| 1468 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/kolors/pipeline_kolors.py | 803 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 796 | `):` |
| 1469 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_attend_and_excite/pipeline_stable_diffusion_attend_and_excite.py | 34 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1470 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_attend_and_excite/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1471 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/omnigen/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1472 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/omnigen/pipeline_omnigen.py | 30 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1473 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/kandinsky/pipeline_kandinsky_prior.py | 26 | 1 | invalid syntax | `from ...models import PriorTransformer` |
| 1474 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet_sd3/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1475 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet_sd3/pipeline_stable_diffusion_3_controlnet.py | 215 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 208 | `):` |
| 1476 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet_sd3/pipeline_stable_diffusion_3_controlnet_inpainting.py | 240 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 233 | `):` |
| 1477 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/pipeline_controlnet_union_sd_xl.py | 259 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 249 | `):` |
| 1478 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/pipeline_controlnet_sd_xl.py | 1184 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1177 | `):` |
| 1479 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/pipeline_controlnet_inpaint.py | 1185 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1178 | `):` |
| 1480 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/pipeline_controlnet.py | 1072 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1065 | `):` |
| 1481 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/pipeline_controlnet_sd_xl_img2img.py | 1270 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1263 | `):` |
| 1482 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1483 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/pipeline_controlnet_img2img.py | 1072 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1065 | `):` |
| 1484 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/pipeline_controlnet_union_sd_xl_img2img.py | 277 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 266 | `):` |
| 1485 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/pipeline_controlnet_inpaint_sd_xl.py | 1389 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1382 | `):` |
| 1486 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet/pipeline_controlnet_union_inpaint_sd_xl.py | 248 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 237 | `):` |
| 1487 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/ltx/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1488 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/ledits_pp/pipeline_leditspp_stable_diffusion_xl.py | 27 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1489 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/ledits_pp/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1490 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/ledits_pp/pipeline_leditspp_stable_diffusion.py | 17 | 1 | invalid syntax | `from ...models import AutoencoderKL, UNet2DConditionModel` |
| 1491 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cogvideo/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1492 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cogvideo/pipeline_cogvideox.py | 606 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 599 | `) -> Union[CogVideoXPipelineOutput, Tuple]:` |
| 1493 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cogvideo/pipeline_cogvideox_fun_control.py | 666 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 659 | `) -> Union[CogVideoXPipelineOutput, Tuple]:` |
| 1494 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cogvideo/pipeline_cogvideox_image2video.py | 716 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 709 | `) -> Union[CogVideoXPipelineOutput, Tuple]:` |
| 1495 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cogvideo/pipeline_cogvideox_video2video.py | 691 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 684 | `) -> Union[CogVideoXPipelineOutput, Tuple]:` |
| 1496 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/latent_consistency_models/pipeline_latent_consistency_img2img.py | 28 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1497 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/latent_consistency_models/pipeline_latent_consistency_text2img.py | 27 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1498 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/latent_consistency_models/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1499 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/marigold/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1500 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/marigold/pipeline_marigold_intrinsics.py | 35 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1501 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/marigold/pipeline_marigold_depth.py | 36 | 1 | invalid syntax | `from ...utils.import_utils import is_scipy_available` |
| 1502 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/marigold/pipeline_marigold_normals.py | 35 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1503 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/unidiffuser/pipeline_unidiffuser.py | 13 | 1 | invalid syntax | `from ...image_processor import VaeImageProcessor` |
| 1504 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/unidiffuser/modeling_uvit.py | 36 | 5 | invalid syntax | `with torch.no_grad():` |
| 1505 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/chroma/pipeline_chroma_img2img.py | 25 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1506 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/chroma/pipeline_chroma.py | 25 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1507 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_sag/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1508 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_sag/pipeline_stable_diffusion_sag.py | 25 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1509 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/musicldm/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1510 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/musicldm/pipeline_musicldm.py | 25 | 1 | invalid syntax | `from ...models import AutoencoderKL, UNet2DConditionModel` |
| 1511 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/text_to_video_synthesis/pipeline_text_to_video_zero_sdxl.py | 17 | 1 | invalid syntax | `from ...image_processor import VaeImageProcessor` |
| 1512 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/text_to_video_synthesis/pipeline_text_to_video_zero.py | 18 | 1 | invalid syntax | `from ...models import AutoencoderKL, UNet2DConditionModel` |
| 1513 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/text_to_video_synthesis/pipeline_text_to_video_synth_img2img.py | 30 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1514 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/text_to_video_synthesis/pipeline_text_to_video_synth.py | 29 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1515 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_panorama/pipeline_stable_diffusion_panorama.py | 24 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1516 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_panorama/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1517 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/animatediff/pipeline_animatediff_video2video.py | 264 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 252 | `):` |
| 1518 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/animatediff/pipeline_animatediff_video2video_controlnet.py | 282 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 270 | `):` |
| 1519 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/animatediff/pipeline_animatediff_sdxl.py | 312 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 299 | `):` |
| 1520 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/animatediff/pipeline_animatediff.py | 139 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 127 | `):` |
| 1521 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/animatediff/pipeline_animatediff_sparsectrl.py | 27 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1522 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/animatediff/pipeline_animatediff_controlnet.py | 25 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput` |
| 1523 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/audioldm2/modeling_audioldm2.py | 31 | 1 | invalid syntax | `from ...models.embeddings import TimestepEmbedding, Timesteps` |
| 1524 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/audioldm2/pipeline_audioldm2.py | 27 | 1 | invalid syntax | `from ...models import AutoencoderKL` |
| 1525 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_control_inpaint.py | 27 | 1 | invalid syntax | `from ...models.autoencoders import AutoencoderKL` |
| 1526 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_controlnet_inpainting.py | 235 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 230 | `):` |
| 1527 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_controlnet.py | 233 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 226 | `):` |
| 1528 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_kontext_inpaint.py | 16 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1529 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_control_img2img.py | 27 | 1 | invalid syntax | `from ...models.autoencoders import AutoencoderKL` |
| 1530 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_output.py | 41 | 8 | unexpected indent | `pooled_prompt_embeds: torch.Tensor` |
| 1531 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_fill.py | 27 | 1 | invalid syntax | `from ...models.autoencoders import AutoencoderKL` |
| 1532 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_kontext.py | 26 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1533 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux.py | 26 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1534 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_inpaint.py | 27 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1535 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_img2img.py | 26 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1536 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_controlnet_image_to_image.py | 229 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 224 | `):` |
| 1537 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/flux/pipeline_flux_control.py | 27 | 1 | invalid syntax | `from ...models.autoencoders import AutoencoderKL` |
| 1538 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_audio/pipeline_stable_audio.py | 123 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.rotary_embed_dim = self.transformer.config.attention_head_dim // 2` |
| 1539 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/kandinsky2_2/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1540 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/kandinsky2_2/pipeline_kandinsky2_2_prior.py | 10 | 1 | invalid syntax | `from ...models import PriorTransformer` |
| 1541 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/shap_e/renderer.py | 214 | 13 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dim=-1,` |
| 1542 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/shap_e/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1543 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/semantic_stable_diffusion/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1544 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/semantic_stable_diffusion/pipeline_semantic_stable_diffusion.py | 18 | 1 | invalid syntax | `from .pipeline_output import SemanticStableDiffusionPipelineOutput` |
| 1545 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/t2i_adapter/pipeline_stable_diffusion_adapter.py | 29 | 1 | invalid syntax | `from ...models import AutoencoderKL, MultiAdapter, T2IAdapter, UNet2DConditionModel` |
| 1546 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/t2i_adapter/pipeline_stable_diffusion_xl_adapter.py | 27 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1547 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_ldm3d/pipeline_stable_diffusion_ldm3d.py | 27 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessorLDM3D` |
| 1548 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_ldm3d/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1549 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/aura_flow/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1550 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/aura_flow/pipeline_aura_flow.py | 517 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 511 | `) -> Union[ImagePipelineOutput, Tuple]:` |
| 1551 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/wuerstchen/modeling_wuerstchen_diffnext.py | 30 | 1 | invalid syntax | `class WuerstchenDiffNeXt(ModelMixin, ConfigMixin):` |
| 1552 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/wuerstchen/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1553 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cosmos/pipeline_cosmos_video2world.py | 601 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 594 | `):` |
| 1554 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cosmos/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1555 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_safe/__init__.py | 15 | 1 | invalid syntax | `@dataclass` |
| 1556 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_safe/pipeline_stable_diffusion_safe.py | 13 | 1 | invalid syntax | `from ...configuration_utils import FrozenDict` |
| 1557 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/sana/pipeline_sana_sprint_img2img.py | 760 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 748 | `) -> Union[SanaPipelineOutput, Tuple]:` |
| 1558 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/sana/pipeline_sana_sprint.py | 675 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 663 | `) -> Union[SanaPipelineOutput, Tuple]:` |
| 1559 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/sana/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1560 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/sana/pipeline_sana.py | 799 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 787 | `) -> Union[SanaPipelineOutput, Tuple]:` |
| 1561 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/sana/pipeline_sana_controlnet.py | 857 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 845 | `) -> Union[SanaPipelineOutput, Tuple]:` |
| 1562 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/audioldm/pipeline_audioldm.py | 26 | 1 | invalid syntax | `from ...models import AutoencoderKL, UNet2DConditionModel` |
| 1563 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/consisid/pipeline_consisid.py | 781 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 771 | `) -> Union[ConsisIDPipelineOutput, Tuple]:` |
| 1564 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/consisid/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1565 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_diffedit/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1566 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_diffedit/pipeline_stable_diffusion_diffedit.py | 36 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1567 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/amused/pipeline_amused_inpaint.py | 29 | 1 | invalid syntax | `if is_torch_xla_available():` |
| 1568 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/amused/pipeline_amused_img2img.py | 29 | 1 | invalid syntax | `if is_torch_xla_available():` |
| 1569 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/amused/pipeline_amused.py | 29 | 1 | invalid syntax | `if is_torch_xla_available():` |
| 1570 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/lumina/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1571 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/lumina/pipeline_lumina.py | 731 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 725 | `) -> Union[ImagePipelineOutput, Tuple]:` |
| 1572 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cogview3/pipeline_cogview3plus.py | 490 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 483 | `) -> Union[CogView3PipelineOutput, Tuple]:` |
| 1573 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cogview4/pipeline_cogview4.py | 485 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 478 | `) -> Union[CogView4PipelineOutput, Tuple]:` |
| 1574 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/cogview4/pipeline_cogview4_control.py | 523 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 516 | `) -> Union[CogView4PipelineOutput, Tuple]:` |
| 1575 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/easyanimate/pipeline_easyanimate.py | 624 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 617 | `):` |
| 1576 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/easyanimate/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1577 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/easyanimate/pipeline_easyanimate_inpaint.py | 919 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 909 | `):` |
| 1578 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/easyanimate/pipeline_easyanimate_control.py | 787 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 779 | `):` |
| 1579 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/hidream_image/pipeline_hidream_image.py | 25 | 1 | invalid syntax | `from ...image_processor import VaeImageProcessor` |
| 1580 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/blip_diffusion/blip_image_processing.py | 26 | 1 | invalid syntax | `from transformers.image_transforms import (convert_to_rgb, resize,` |
| 1581 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/blip_diffusion/__init__.py | 8 | 22 | '(' was never closed | `from ...utils import (OptionalDependencyNotAvailable, is_torch_available,` |
| 1582 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/latte/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1583 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/latte/pipeline_latte.py | 700 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 690 | `) -> Union[LattePipelineOutput, Tuple]:` |
| 1584 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/latent_diffusion/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1585 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/latent_diffusion/pipeline_latent_diffusion.py | 145 | 12 | unexpected indent | `width = width or self.unet.config.sample_size * self.vae_scale_factor` |
| 1586 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/hunyuan_video/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1587 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/hunyuan_video/pipeline_hunyuan_skyreels_image2video.py | 613 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 605 | `):` |
| 1588 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/hunyuan_video/pipeline_hunyuan_video.py | 560 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 552 | `):` |
| 1589 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/hunyuan_video/pipeline_hunyuan_video_image2video.py | 768 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 759 | `):` |
| 1590 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/hunyuan_video/pipeline_hunyuan_video_framepack.py | 743 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 734 | `):` |
| 1591 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/skyreels_v2/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1592 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/skyreels_v2/pipeline_skyreels_v2_diffusion_forcing_i2v.py | 757 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 744 | `):` |
| 1593 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/skyreels_v2/pipeline_skyreels_v2_diffusion_forcing.py | 700 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 687 | `):` |
| 1594 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/dance_diffusion/pipeline_dance_diffusion.py | 28 | 1 | invalid syntax | `if is_torch_xla_available():` |
| 1595 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/kandinsky3/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1596 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/kandinsky3/pipeline_kandinsky3_img2img.py | 17 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1597 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/wan/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1598 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion_image_variation.py | 103 | 68 | invalid syntax | `if safety_checker is not None and feature_extractor is None:` |
| 1599 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_flax_stable_diffusion.py | 123 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 115 | `):` |
| 1600 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_flax_stable_diffusion_inpaint.py | 150 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 142 | `):` |
| 1601 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/safety_checker_flax.py | 42 | 62 | invalid syntax. Perhaps you forgot a comma? | `"special_care_embeds", jax.nn.initializers.ones, (3, self.config.projection_dim)` |
| 1602 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_flax_stable_diffusion_img2img.py | 147 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 139 | `):` |
| 1603 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_unclip.py | 32 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1604 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/__init__.py | 11 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1605 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion_depth2img.py | 28 | 1 | invalid syntax | `from ...configuration_utils import FrozenDict` |
| 1606 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion.py | 912 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 905 | `):` |
| 1607 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion_img2img.py | 1000 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 993 | `):` |
| 1608 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion_upscale.py | 29 | 1 | invalid syntax | `from ...models import AutoencoderKL, UNet2DConditionModel` |
| 1609 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion_instruct_pix2pix.py | 215 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 207 | `):` |
| 1610 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/convert_from_ckpt.py | 32 | 1 | invalid syntax | `from ...models import (AutoencoderKL, ControlNetModel, PriorTransformer,` |
| 1611 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_onnx_stable_diffusion_upscale.py | 88 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"The configuration file of this scheduler: {scheduler} is outdated. `steps_offset`"` |
| 1612 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_unclip_img2img.py | 25 | 1 | invalid syntax | `from ...image_processor import VaeImageProcessor` |
| 1613 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion/pipeline_stable_diffusion_inpaint.py | 1044 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1037 | `):` |
| 1614 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/i2vgen_xl/pipeline_i2vgen_xl.py | 27 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1615 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/visualcloze/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1616 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/visualcloze/pipeline_visualcloze_generation.py | 25 | 1 | invalid syntax | `from ...models.autoencoders import AutoencoderKL` |
| 1617 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deepfloyd_if/pipeline_if_img2img_superresolution.py | 841 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 818 | `):` |
| 1618 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deepfloyd_if/pipeline_if_inpainting_superresolution.py | 940 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 917 | `):` |
| 1619 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deepfloyd_if/__init__.py | 23 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 11 | `}` |
| 1620 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deepfloyd_if/pipeline_if.py | 17 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1621 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deepfloyd_if/pipeline_if_img2img.py | 746 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 725 | `):` |
| 1622 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deepfloyd_if/pipeline_if_superresolution.py | 20 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1623 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deepfloyd_if/pipeline_if_inpainting.py | 850 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 829 | `):` |
| 1624 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet_hunyuandit/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1625 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet_hunyuandit/pipeline_hunyuandit_controlnet.py | 265 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 254 | `):` |
| 1626 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_3/pipeline_stable_diffusion_3.py | 25 | 1 | invalid syntax | `from ...callbacks import MultiPipelineCallbacks, PipelineCallback` |
| 1627 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_3/pipeline_stable_diffusion_3_img2img.py | 26 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1628 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_3/pipeline_stable_diffusion_3_inpaint.py | 25 | 1 | invalid syntax | `from ...callbacks import MultiPipelineCallbacks, PipelineCallback` |
| 1629 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_xl/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1630 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_xl/pipeline_flax_stable_diffusion_xl.py | 55 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 49 | `):` |
| 1631 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_xl/pipeline_stable_diffusion_xl_inpaint.py | 1277 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1270 | `):` |
| 1632 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_xl/pipeline_stable_diffusion_xl.py | 982 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 975 | `):` |
| 1633 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_xl/pipeline_stable_diffusion_xl_img2img.py | 1150 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1143 | `):` |
| 1634 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_xl/pipeline_stable_diffusion_xl_instruct_pix2pix.py | 27 | 1 | invalid syntax | `from ...models import AutoencoderKL, UNet2DConditionModel` |
| 1635 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/lumina2/pipeline_lumina2.py | 31 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1636 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/lumina2/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1637 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/hunyuandit/pipeline_hunyuandit.py | 687 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 676 | `):` |
| 1638 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/hunyuandit/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1639 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pixart_alpha/pipeline_pixart_alpha.py | 31 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1640 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pixart_alpha/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1641 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pixart_alpha/pipeline_pixart_sigma.py | 31 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1642 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_k_diffusion/__init__.py | 10 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1643 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_k_diffusion/pipeline_stable_diffusion_k_diffusion.py | 27 | 1 | invalid syntax | `from ...image_processor import VaeImageProcessor` |
| 1644 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/stable_diffusion_k_diffusion/pipeline_stable_diffusion_xl_k_diffusion.py | 29 | 1 | invalid syntax | `from ...models import AutoencoderKL, UNet2DConditionModel` |
| 1645 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/unclip/pipeline_unclip_image_variation.py | 26 | 1 | invalid syntax | `from ...models import UNet2DConditionModel, UNet2DModel` |
| 1646 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/allegro/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1647 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/allegro/pipeline_allegro.py | 793 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 785 | `) -> Union[AllegroPipelineOutput, Tuple]:` |
| 1648 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_kolors.py | 827 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 818 | `):` |
| 1649 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_controlnet_sd_xl_img2img.py | 1272 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1264 | `):` |
| 1650 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_hunyuandit.py | 709 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 696 | `):` |
| 1651 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_controlnet_sd.py | 1019 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1011 | `):` |
| 1652 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sd_3.py | 24 | 1 | invalid syntax | `from ...image_processor import VaeImageProcessor` |
| 1653 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sd.py | 24 | 1 | invalid syntax | `from ...configuration_utils import FrozenDict` |
| 1654 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1655 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sd_animatediff.py | 24 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput` |
| 1656 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sd_3_img2img.py | 25 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1657 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_controlnet_sd_inpaint.py | 1152 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1144 | `):` |
| 1658 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_controlnet_sd_xl.py | 1187 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1179 | `):` |
| 1659 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sd_xl_inpaint.py | 1282 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1274 | `):` |
| 1660 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sd_inpaint.py | 25 | 1 | invalid syntax | `from ...configuration_utils import FrozenDict` |
| 1661 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sana.py | 728 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 714 | `) -> Union[ImagePipelineOutput, Tuple]:` |
| 1662 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sd_img2img.py | 922 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 914 | `):` |
| 1663 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_pixart_sigma.py | 31 | 1 | invalid syntax | `from ...utils.torch_utils import randn_tensor` |
| 1664 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sd_xl.py | 25 | 1 | invalid syntax | `from ...image_processor import PipelineImageInput, VaeImageProcessor` |
| 1665 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/pag/pipeline_pag_sd_xl_img2img.py | 1169 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1161 | `):` |
| 1666 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet_xs/pipeline_controlnet_xs_sd_xl.py | 860 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 854 | `):` |
| 1667 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet_xs/__init__.py | 9 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1668 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/controlnet_xs/pipeline_controlnet_xs.py | 764 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 758 | `):` |
| 1669 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/paint_by_example/__init__.py | 14 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1670 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/paint_by_example/pipeline_paint_by_example.py | 32 | 1 | invalid syntax | `from ..stable_diffusion import StableDiffusionPipelineOutput` |
| 1671 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/__init__.py | 10 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1672 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/repaint/pipeline_repaint.py | 199 | 29 | '(' was never closed | `raise ValueError(` |
| 1673 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/alt_diffusion/pipeline_alt_diffusion_img2img.py | 27 | 1 | invalid syntax | `from ....configuration_utils import FrozenDict` |
| 1674 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/alt_diffusion/pipeline_alt_diffusion.py | 25 | 1 | invalid syntax | `from ....configuration_utils import FrozenDict` |
| 1675 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/spectrogram_diffusion/__init__.py | 10 | 16 | invalid syntax | `_dummy_objects = {}` |
| 1676 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/stable_diffusion_variants/pipeline_stable_diffusion_pix2pix_zero.py | 28 | 1 | invalid syntax | `from ....image_processor import PipelineImageInput, VaeImageProcessor` |
| 1677 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/stable_diffusion_variants/pipeline_cycle_diffusion.py | 34 | 1 | invalid syntax | `from ....utils.torch_utils import randn_tensor` |
| 1678 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/stable_diffusion_variants/pipeline_stable_diffusion_paradigms.py | 26 | 1 | invalid syntax | `from ....models import AutoencoderKL, UNet2DConditionModel` |
| 1679 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/stable_diffusion_variants/pipeline_stable_diffusion_inpaint_legacy.py | 30 | 1 | invalid syntax | `from ....models import AutoencoderKL, UNet2DConditionModel` |
| 1680 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/stable_diffusion_variants/pipeline_stable_diffusion_model_editing.py | 31 | 1 | invalid syntax | `from ....utils.torch_utils import randn_tensor` |
| 1681 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/versatile_diffusion/pipeline_versatile_diffusion_dual_guided.py | 27 | 1 | invalid syntax | `from ....image_processor import VaeImageProcessor` |
| 1682 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/versatile_diffusion/pipeline_versatile_diffusion_image_variation.py | 58 | 8 | unexpected indent | `image_encoder: CLIPVisionModelWithProjection` |
| 1683 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/versatile_diffusion/pipeline_versatile_diffusion_text_to_image.py | 58 | 8 | unexpected indent | `text_encoder: CLIPTextModelWithProjection` |
| 1684 | venv_creative/lib/python3.13/site-packages/diffusers/pipelines/deprecated/versatile_diffusion/pipeline_versatile_diffusion.py | 11 | 1 | invalid syntax | `from ....models import AutoencoderKL, UNet2DConditionModel` |
| 1685 | venv_creative/lib/python3.13/site-packages/diffusers/utils/remote_utils.py | 29 | 8 | unexpected indent | `from ..video_processor import VideoProcessor` |
| 1686 | venv_creative/lib/python3.13/site-packages/diffusers/utils/testing_utils.py | 1018 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 1005 | `}` |
| 1687 | venv_creative/lib/python3.13/site-packages/diffusers/models/upsampling.py | 136 | 9 | invalid syntax | `elif use_conv:` |
| 1688 | venv_creative/lib/python3.13/site-packages/diffusers/models/downsampling.py | 124 | 9 | invalid syntax | `else:` |
| 1689 | venv_creative/lib/python3.13/site-packages/diffusers/models/attention_processor.py | 28 | 1 | invalid syntax | `from ..utils.torch_utils import is_torch_version, maybe_allow_in_graph` |
| 1690 | venv_creative/lib/python3.13/site-packages/diffusers/models/modeling_flax_pytorch_utils.py | 72 | 12 | unexpected indent | `elif pt_tuple_key[-1] in ["weight", "gamma"] and pt_tuple_key[:-1] + ("scale",) in random_flax_state_dict:` |
| 1691 | venv_creative/lib/python3.13/site-packages/diffusers/models/adapter.py | 59 | 12 | unexpected indent | `first_adapter_downscale_factor = adapters[0].downscale_factor` |
| 1692 | venv_creative/lib/python3.13/site-packages/diffusers/models/modeling_pytorch_flax_utils.py | 51 | 17 | invalid syntax | `else:` |
| 1693 | venv_creative/lib/python3.13/site-packages/diffusers/models/embeddings.py | 58 | 68 | invalid syntax. Perhaps you forgot a comma? | `start = 0, end = half_dim, dtype = torch.float32, device = timesteps.device` |
| 1694 | venv_creative/lib/python3.13/site-packages/diffusers/models/resnet.py | 30 | 1 | invalid syntax | `from .normalization import AdaGroupNorm` |
| 1695 | venv_creative/lib/python3.13/site-packages/diffusers/models/modeling_utils.py | 35 | 1 | invalid syntax | `import safetensors` |
| 1696 | venv_creative/lib/python3.13/site-packages/diffusers/models/controlnets/controlnet_xs.py | 31 | 1 | invalid syntax | `from ..embeddings import TimestepEmbedding, Timesteps` |
| 1697 | venv_creative/lib/python3.13/site-packages/diffusers/models/transformers/transformer_omnigen.py | 67 | 103 | invalid syntax. Perhaps you forgot a comma? | `in_channels, embed_dim, kernel_size=(patch_size, patch_size), stride = patch_size, bias = bias` |
| 1698 | venv_creative/lib/python3.13/site-packages/diffusers/models/transformers/transformer_ltx.py | 29 | 1 | invalid syntax | `from ...utils.torch_utils import maybe_allow_in_graph` |
| 1699 | venv_creative/lib/python3.13/site-packages/diffusers/models/transformers/transformer_cogview4.py | 246 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 240 | `) -> Tuple[torch.Tensor, torch.Tensor]:` |
| 1700 | venv_creative/lib/python3.13/site-packages/diffusers/models/transformers/transformer_flux.py | 28 | 1 | invalid syntax | `from ...utils import (USE_PEFT_BACKEND, deprecate, logging, scale_lora_layers,` |
| 1701 | venv_creative/lib/python3.13/site-packages/diffusers/models/transformers/transformer_wan.py | 28 | 1 | invalid syntax | `from ...utils.torch_utils import maybe_allow_in_graph` |
| 1702 | venv_creative/lib/python3.13/site-packages/diffusers/models/transformers/transformer_cosmos.py | 52 | 97 | invalid syntax. Perhaps you forgot a comma? | `batch_size, num_channels, num_frames // p_t, p_t, height // p_h, p_h, width // p_w, p_w` |
| 1703 | venv_creative/lib/python3.13/site-packages/diffusers/models/autoencoders/autoencoder_oobleck.py | 94 | 12 | unexpected indent | `return output_tensor` |
| 1704 | venv_creative/lib/python3.13/site-packages/diffusers/models/autoencoders/autoencoder_kl_ltx.py | 73 | 5 | invalid syntax | `def forward(self, hidden_states: torch.Tensor) -> torch.Tensor:` |
| 1705 | venv_creative/lib/python3.13/site-packages/diffusers/models/autoencoders/autoencoder_kl_cosmos.py | 73 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.pad_mode = pad_mode` |
| 1706 | venv_creative/lib/python3.13/site-packages/diffusers/models/autoencoders/autoencoder_kl_magvit.py | 789 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 776 | `):` |
| 1707 | venv_creative/lib/python3.13/site-packages/diffusers/models/autoencoders/vae.py | 30 | 1 | invalid syntax | `@dataclass` |
| 1708 | venv_creative/lib/python3.13/site-packages/diffusers/models/autoencoders/autoencoder_tiny.py | 137 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.decoder = DecoderTiny(` |
| 1709 | venv_creative/lib/python3.13/site-packages/diffusers/models/autoencoders/autoencoder_kl_allegro.py | 67 | 9 | invalid syntax | `elif up_sample:` |
| 1710 | venv_creative/lib/python3.13/site-packages/diffusers/hooks/_helpers.py | 125 | 8 | unexpected indent | `from ..models.transformers.transformer_flux import FluxAttnProcessor` |
| 1711 | venv_creative/lib/python3.13/site-packages/diffusers/loaders/lora_conversion_utils.py | 108 | 17 | invalid syntax. Perhaps you forgot a comma? | `key.split(delimiter)[: block_slice_pos - 1]` |
| 1712 | venv_creative/lib/python3.13/site-packages/diffusers/loaders/unet.py | 583 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 573 | `}` |
| 1713 | venv_creative/lib/python3.13/site-packages/diffusers/loaders/textual_inversion.py | 27 | 1 | invalid syntax | `if is_transformers_available():` |
| 1714 | venv_creative/lib/python3.13/site-packages/diffusers/loaders/transformer_flux.py | 50 | 77 | invalid syntax | `if low_cpu_mem_usage is True and not is_torch_version(">=", "1.9.0"):` |
| 1715 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_euler_discrete.py | 50 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1716 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_cosine_dpmsolver_multistep.py | 246 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"`final_sigmas_type` must be one of 'zero', or 'sigma_min', but got {self.config.final_sigmas_type}"` |
| 1717 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_lcm.py | 49 | 8 | unexpected indent | `denoised: Optional[torch.Tensor] = None` |
| 1718 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_ddpm.py | 46 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1719 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_heun_discrete.py | 47 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1720 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_k_dpm_2_discrete.py | 47 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1721 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_dpm_cogvideox.py | 49 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1722 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_dpmsolver_sde.py | 48 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1723 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_ddim_inverse.py | 45 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1724 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_scm.py | 49 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1725 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_k_dpm_2_ancestral_discrete.py | 48 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1726 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_lms_discrete.py | 46 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1727 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_ddim_cogvideox.py | 48 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1728 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_tcd.py | 48 | 8 | unexpected indent | `pred_noised_sample: Optional[torch.Tensor] = None` |
| 1729 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_euler_ancestral_discrete.py | 47 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1730 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_edm_euler.py | 46 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1731 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_ddpm_parallel.py | 47 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1732 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_ddim_parallel.py | 48 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1733 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_sde_ve.py | 44 | 8 | unexpected indent | `prev_sample_mean: torch.Tensor` |
| 1734 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_unclip.py | 45 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1735 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_amused.py | 42 | 8 | unexpected indent | `pred_original_sample: torch.Tensor = None` |
| 1736 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_repaint.py | 44 | 8 | unexpected indent | `pred_original_sample: torch.Tensor` |
| 1737 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_ddim.py | 48 | 8 | unexpected indent | `pred_original_sample: Optional[torch.Tensor] = None` |
| 1738 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/scheduling_unipc_multistep.py | 237 | 37 | invalid syntax | `if trained_betas is not None:` |
| 1739 | venv_creative/lib/python3.13/site-packages/diffusers/schedulers/deprecated/scheduling_karras_ve.py | 45 | 8 | unexpected indent | `derivative: torch.Tensor` |
| 1740 | venv_creative/lib/python3.13/site-packages/google/protobuf/message.py | 474 | 8 | unexpected indent | `return (_InternalConstructMessage, (container.full_name,),` |
| 1741 | venv_creative/lib/python3.13/site-packages/google/protobuf/descriptor_pool.py | 80 | 24 | invalid syntax | `_edition_defaults_lock = threading.Lock()` |
| 1742 | venv_creative/lib/python3.13/site-packages/google/protobuf/internal/decoder.py | 469 | 7 | invalid syntax | `if pos > endpoint:` |
| 1743 | venv_creative/lib/python3.13/site-packages/google/protobuf/internal/containers.py | 28 | 4 | invalid syntax | `_T = TypeVar('_T')` |
| 1744 | venv_creative/lib/python3.13/site-packages/colorama/winterm.py | 150 | 16 | unexpected indent | `elif mode == 1:` |
| 1745 | venv_creative/lib/python3.13/site-packages/cffi/backend_ctypes.py | 42 | 5 | invalid syntax | `def _to_ctypes(value):` |
| 1746 | venv_creative/lib/python3.13/site-packages/cffi/setuptools_ext.py | 14 | 8 | unexpected indent | `raise DistutilsSetupError(msg)` |
| 1747 | venv_creative/lib/python3.13/site-packages/cffi/_shimmed_dist_utils.py | 30 | 8 | unexpected indent | `from distutils.log import set_threshold, set_verbosity` |
| 1748 | venv_creative/lib/python3.13/site-packages/cffi/model.py | 35 | 12 | unexpected indent | `replace_with = replace_with.strip()` |
| 1749 | venv_creative/lib/python3.13/site-packages/cffi/ffiplatform.py | 12 | 1 | invalid syntax | `def get_extension(srcfilename, modname, sources=(), **kwds):` |
| 1750 | venv_creative/lib/python3.13/site-packages/cffi/recompiler.py | 37 | 5 | invalid syntax | `def as_python_expr(self):` |
| 1751 | venv_creative/lib/python3.13/site-packages/sunau/__init__.py | 118 | 42 | invalid syntax. Perhaps you forgot a comma? | `DeprecationWarning, stacklevel = 2` |
| 1752 | venv_creative/lib/python3.13/site-packages/torchvision/datasets/svhn.py | 58 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 51 | `}` |
| 1753 | venv_creative/lib/python3.13/site-packages/torchvision/io/_video_opt.py | 35 | 12 | unexpected indent | `self.denominator = denominator` |
| 1754 | venv_creative/lib/python3.13/site-packages/torchvision/io/video.py | 32 | 5 | invalid syntax | `try:` |
| 1755 | venv_creative/lib/python3.13/site-packages/torchvision/models/mnasnet.py | 31 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_BN_MOMENTUM = 1 - 0.9997` |
| 1756 | venv_creative/lib/python3.13/site-packages/torchvision/models/vision_transformer.py | 33 | 1 | invalid syntax | `class ConvStemConfig(NamedTuple):` |
| 1757 | venv_creative/lib/python3.13/site-packages/torchvision/models/feature_extraction.py | 19 | 9 | invalid syntax | `__all__ = ["create_feature_extractor", "get_graph_node_names"]` |
| 1758 | venv_creative/lib/python3.13/site-packages/torchvision/models/efficientnet.py | 47 | 1 | invalid syntax | `@dataclass` |
| 1759 | venv_creative/lib/python3.13/site-packages/torchvision/models/mobilenetv3.py | 27 | 1 | invalid syntax | `class InvertedResidualConfig:` |
| 1760 | venv_creative/lib/python3.13/site-packages/torchvision/models/maxvit.py | 28 | 1 | invalid syntax | `def _get_conv_output_shape(input_size: tuple[int, int], kernel_size: int, stride: int, padding: int) -> tuple[int, int]:` |
| 1761 | venv_creative/lib/python3.13/site-packages/torchvision/models/_utils.py | 91 | 12 | unexpected indent | `new_v = max(min_value, int(v + divisor / 2) // divisor * divisor)` |
| 1762 | venv_creative/lib/python3.13/site-packages/torchvision/models/video/swin_transformer.py | 31 | 1 | invalid syntax | `def _get_window_and_shift_size(` |
| 1763 | venv_creative/lib/python3.13/site-packages/torchvision/models/detection/rpn.py | 76 | 5 | invalid syntax | `def forward(self, x: list[Tensor]) -> tuple[list[Tensor], list[Tensor]]:` |
| 1764 | venv_creative/lib/python3.13/site-packages/torchvision/models/detection/fcos.py | 35 | 1 | invalid syntax | `class FCOSHead(nn.Module):` |
| 1765 | venv_creative/lib/python3.13/site-packages/torchvision/models/detection/retinanet.py | 37 | 1 | invalid syntax | `def _sum(x: list[Tensor]) -> Tensor:` |
| 1766 | venv_creative/lib/python3.13/site-packages/torchvision/models/detection/roi_heads.py | 56 | 5 | invalid syntax | `return classification_loss, box_loss` |
| 1767 | venv_creative/lib/python3.13/site-packages/torchvision/transforms/transforms.py | 62 | 1 | invalid syntax | `class Compose:` |
| 1768 | venv_creative/lib/python3.13/site-packages/torchvision/transforms/_functional_tensor.py | 147 | 9 | invalid syntax | `return pad(img[..., max(top, 0) : bottom, max(left, 0) : right], padding_ltrb, fill = 0)` |
| 1769 | venv_creative/lib/python3.13/site-packages/torchvision/transforms/v2/functional/_geometry.py | 23 | 1 | invalid syntax | `from torchvision.tv_tensors._bounding_boxes import CLAMPING_MODE_TYPE` |
| 1770 | venv_creative/lib/python3.13/site-packages/torchvision/tv_tensors/_video.py | 35 | 16 | unexpected indent | `return tensor.as_subclass(cls)` |
| 1771 | venv_creative/lib/python3.13/site-packages/markdown_it/rules_block/list.py | 53 | 8 | unexpected indent | `if ch_ord < 0x30 or ch_ord > 0x39:` |
| 1772 | venv_creative/lib/python3.13/site-packages/markdown_it/rules_block/lheading.py | 44 | 24 | unexpected indent | `if pos >= maximum:` |
| 1773 | venv_creative/lib/python3.13/site-packages/markdown_it/rules_block/blockquote.py | 14 | 75 | invalid syntax. Perhaps you forgot a comma? | `"entering blockquote: %s, %s, %s, %s", state, startLine, endLine, silent` |
| 1774 | venv_creative/lib/python3.13/site-packages/markdown_it/rules_core/replacements.py | 96 | 16 | unexpected indent | `token.content = COMMA_RE.sub(",", token.content)` |
| 1775 | venv_creative/lib/python3.13/site-packages/markdown_it/rules_inline/html_inline.py | 10 | 8 | unexpected indent | `return (lc >= 0x61) and (lc <= 0x7A)` |
| 1776 | venv_creative/lib/python3.13/site-packages/markdown_it/rules_inline/emphasis.py | 39 | 15 | positional argument follows keyword argument | `state.pos += scanned.length` |
| 1777 | venv_creative/lib/python3.13/site-packages/markdown_it/helpers/parse_link_title.py | 48 | 12 | unexpected indent | `if marker != 0x22 and marker != 0x27 and marker != 0x28:` |
| 1778 | venv_creative/lib/python3.13/site-packages/fontTools/qu2cu/qu2cu.py | 46 | 1 | invalid syntax | `@cython.locals(mid = cython.complex, deriv3 = cython.complex)` |
| 1779 | venv_creative/lib/python3.13/site-packages/fontTools/misc/arrayTools.py | 108 | 8 | unexpected indent | `return math.sqrt(x**2 + y**2)` |
| 1780 | venv_creative/lib/python3.13/site-packages/fontTools/misc/timeTools.py | 31 | 1 | invalid syntax | `def asctime(t = None):` |
| 1781 | venv_creative/lib/python3.13/site-packages/fontTools/misc/roundTools.py | 11 | 11 | '[' was never closed | `__all__ = [` |
| 1782 | venv_creative/lib/python3.13/site-packages/fontTools/misc/psCharStrings.py | 12 | 1 | invalid syntax | `from fontTools.misc.textTools import bytechr, byteord, bytesjoin, strjoin` |
| 1783 | venv_creative/lib/python3.13/site-packages/fontTools/misc/etree.py | 45 | 1 | invalid syntax | `try:` |
| 1784 | venv_creative/lib/python3.13/site-packages/fontTools/subset/__init__.py | 646 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 638 | `}` |
| 1785 | venv_creative/lib/python3.13/site-packages/fontTools/svgLib/path/shapes.py | 30 | 12 | unexpected indent | `matrix = tuple(float(p) for p in re.split(r"\s+¦,", match.group(1)))` |
| 1786 | venv_creative/lib/python3.13/site-packages/fontTools/svgLib/path/parser.py | 23 | 5 | invalid syntax. Perhaps you forgot a comma? | `r"[-+]?"  # optional sign` |
| 1787 | venv_creative/lib/python3.13/site-packages/fontTools/svgLib/path/arc.py | 91 | 12 | unexpected indent | `center_point = (point1 + point2) * 0.5` |
| 1788 | venv_creative/lib/python3.13/site-packages/fontTools/varLib/cff.py | 12 | 1 | invalid syntax | `from fontTools.cffLib.specializer import commandsToProgram, specializeCommands` |
| 1789 | venv_creative/lib/python3.13/site-packages/fontTools/varLib/interpolatablePlot.py | 15 | 1 | invalid syntax | `from fontTools.pens.recordingPen import (DecomposingRecordingPen, RecordingPen,` |
| 1790 | venv_creative/lib/python3.13/site-packages/fontTools/varLib/interpolatableHelpers.py | 64 | 1 | invalid syntax | `def rot_list(l, k):` |
| 1791 | venv_creative/lib/python3.13/site-packages/fontTools/varLib/varStore.py | 12 | 1 | invalid syntax | `from fontTools.varLib.models import supportScalar` |
| 1792 | venv_creative/lib/python3.13/site-packages/fontTools/varLib/merger.py | 36 | 1 | invalid syntax | `class Merger(object):` |
| 1793 | venv_creative/lib/python3.13/site-packages/fontTools/mtiLib/__init__.py | 90 | 17 | invalid syntax | `return` |
| 1794 | venv_creative/lib/python3.13/site-packages/fontTools/pens/pointPen.py | 36 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `Point = Tuple[float, float]` |
| 1795 | venv_creative/lib/python3.13/site-packages/fontTools/pens/areaPen.py | 59 | 16 | unexpected indent | `del self._p0, self._startPoint` |
| 1796 | venv_creative/lib/python3.13/site-packages/fontTools/pens/statisticsPen.py | 55 | 74 | invalid syntax. Perhaps you forgot a comma? | `self.covariance / self.varianceY if self.varianceY != 0 else float("NaN")` |
| 1797 | venv_creative/lib/python3.13/site-packages/fontTools/otlLib/builder.py | 22 | 1 | invalid syntax | `from fontTools.ttLib.ttFont import TTFont` |
| 1798 | venv_creative/lib/python3.13/site-packages/fontTools/ufoLib/__init__.py | 74 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `__version__ = "3.0.0"` |
| 1799 | venv_creative/lib/python3.13/site-packages/fontTools/ufoLib/glifLib.py | 35 | 9 | invalid syntax | `__all__ = [` |
| 1800 | venv_creative/lib/python3.13/site-packages/fontTools/designspaceLib/__init__.py | 3370 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 3362 | `}` |
| 1801 | venv_creative/lib/python3.13/site-packages/fontTools/ttLib/sfnt.py | 67 | 21 | invalid syntax. Perhaps you forgot a comma? | `"specify a font number between 0 and %d (inclusive)"` |
| 1802 | venv_creative/lib/python3.13/site-packages/fontTools/ttLib/ttFont.py | 18 | 5 | invalid syntax | `log = logging.getLogger(__name__)` |
| 1803 | venv_creative/lib/python3.13/site-packages/fontTools/ttLib/woff2.py | 15 | 1 | invalid syntax | `from fontTools.ttLib.sfnt import (DirectoryEntry, SFNTDirectoryEntry, SFNTReader,` |
| 1804 | venv_creative/lib/python3.13/site-packages/fontTools/ttLib/__main__.py | 55 | 5 | invalid syntax. Perhaps you forgot a comma? | `parser.add_argument("font", metavar="font", nargs="*", help="Font file.")` |
| 1805 | venv_creative/lib/python3.13/site-packages/fontTools/ttLib/tables/otConverters.py | 25 | 1 | invalid syntax | `from .otTables import NO_VARIATION_INDEX, AATAction, AATState, AATStateTable` |
| 1806 | venv_creative/lib/python3.13/site-packages/fontTools/ttLib/tables/sbixStrike.py | 43 | 16 | unexpected indent | `if len(self.data) < sbixStrikeHeaderFormatSize:` |
| 1807 | venv_creative/lib/python3.13/site-packages/fontTools/ttLib/tables/otBase.py | 61 | 1 | invalid syntax | `class OTLOffsetOverflowError(Exception):` |
| 1808 | venv_creative/lib/python3.13/site-packages/fontTools/cffLib/transforms.py | 7 | 1 | invalid syntax | `def _uniq_sort(l):` |
| 1809 | venv_creative/lib/python3.13/site-packages/fontTools/cffLib/__init__.py | 25 | 1 | invalid syntax | `from fontTools.ttLib import TTFont` |
| 1810 | venv_creative/lib/python3.13/site-packages/fontTools/colorLib/builder.py | 16 | 1 | invalid syntax | `from fontTools.misc.arrayTools import intRect` |
| 1811 | venv_creative/lib/python3.13/site-packages/werkzeug/middleware/proxy_fix.py | 99 | 12 | unexpected indent | `self.x_proto = x_proto` |
| 1812 | venv_creative/lib/python3.13/site-packages/werkzeug/middleware/lint.py | 50 | 1 | invalid syntax | `class InputStream:` |
| 1813 | venv_creative/lib/python3.13/site-packages/werkzeug/sansio/response.py | 11 | 1 | invalid syntax | `from ..http import (COEP, COOP, HTTP_STATUS_CODES, dump_age, dump_cookie, dump_header,` |
| 1814 | venv_creative/lib/python3.13/site-packages/werkzeug/routing/exceptions.py | 118 | 9 | invalid syntax | `if adapter and adapter.map._rules:` |
| 1815 | venv_creative/lib/python3.13/site-packages/werkzeug/debug/__init__.py | 85 | 80 | invalid syntax. Perhaps you forgot a comma? | `["ioreg", "-c", "IOPlatformExpertDevice", "-d", "2"], stdout = PIPE` |
| 1816 | venv_creative/lib/python3.13/site-packages/wheel/_bdist_wheel.py | 113 | 9 | invalid syntax | `return fallback` |
| 1817 | venv_creative/lib/python3.13/site-packages/wheel/vendored/packaging/_manylinux.py | 46 | 1 | invalid syntax | `def _is_linux_i686(executable: str) -> bool:` |
| 1818 | venv_creative/lib/python3.13/site-packages/wheel/vendored/packaging/specifiers.py | 247 | 5 | invalid syntax | `def __init__(self, spec: str = "", prereleases: Optional[bool] = None) -> None:` |
| 1819 | venv_creative/lib/python3.13/site-packages/click/core.py | 2242 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 2235 | `) -> None:` |
| 1820 | venv_creative/lib/python3.13/site-packages/click/termui.py | 158 | 27 | invalid syntax | `if confirmation_prompt:` |
| 1821 | venv_creative/lib/python3.13/site-packages/click/exceptions.py | 59 | 1 | invalid syntax | `class UsageError(ClickException):` |
| 1822 | venv_creative/lib/python3.13/site-packages/click/_termui_impl.py | 27 | 1 | invalid syntax | `from .exceptions import ClickException` |
| 1823 | venv_creative/lib/python3.13/site-packages/click/testing.py | 229 | 5 | invalid syntax | `def stdout(self) -> str:` |
| 1824 | venv_creative/lib/python3.13/site-packages/torch/_meta_registrations.py | 3807 | 17 | too many nested parentheses | `torch._check(` |
| 1825 | venv_creative/lib/python3.13/site-packages/torch/_ops.py | 134 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 126 | `) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:` |
| 1826 | venv_creative/lib/python3.13/site-packages/torch/quasirandom.py | 57 | 17 | invalid syntax. Perhaps you forgot a comma? | `"Supported range of dimensionality "` |
| 1827 | venv_creative/lib/python3.13/site-packages/torch/_weights_only_unpickler.py | 335 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 328 | `):` |
| 1828 | venv_creative/lib/python3.13/site-packages/torch/__init__.py | 2634 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 2628 | `) -> _Callable[_InputT, _RetT]: ...` |
| 1829 | venv_creative/lib/python3.13/site-packages/torch/overrides.py | 43 | 1 | invalid syntax | `from typing_extensions import ParamSpec` |
| 1830 | venv_creative/lib/python3.13/site-packages/torch/_tensor.py | 18 | 1 | invalid syntax | `from torch.overrides import (get_default_nowrap_functions, handle_torch_function,` |
| 1831 | venv_creative/lib/python3.13/site-packages/torch/_tensor_str.py | 129 | 9 | invalid syntax | `else torch.double` |
| 1832 | venv_creative/lib/python3.13/site-packages/torch/functional.py | 19 | 9 | invalid syntax | `__all__ = [` |
| 1833 | venv_creative/lib/python3.13/site-packages/torch/_appdirs.py | 175 | 30 | invalid syntax. Perhaps you forgot a comma? | `"XDG_DATA_DIRS", os.pathsep.join(["/usr / local / share", "/usr / share"])` |
| 1834 | venv_creative/lib/python3.13/site-packages/torch/_guards.py | 23 | 1 | invalid syntax | `import torch` |
| 1835 | venv_creative/lib/python3.13/site-packages/torch/serialization.py | 59 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `DEFAULT_PROTOCOL = 2` |
| 1836 | venv_creative/lib/python3.13/site-packages/torch/_higher_order_ops/effects.py | 20 | 1 | invalid syntax | `class _EffectType(Enum):` |
| 1837 | venv_creative/lib/python3.13/site-packages/torch/_higher_order_ops/invoke_subgraph.py | 23 | 1 | invalid syntax | `from torch._ops import HigherOrderOperator` |
| 1838 | venv_creative/lib/python3.13/site-packages/torch/_higher_order_ops/utils.py | 20 | 1 | invalid syntax | `from torch.fx.experimental.proxy_tensor import (` |
| 1839 | venv_creative/lib/python3.13/site-packages/torch/_higher_order_ops/scan.py | 121 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 111 | `) -> tuple[pytree.PyTree, pytree.PyTree]:` |
| 1840 | venv_creative/lib/python3.13/site-packages/torch/_higher_order_ops/triton_kernel_wrap.py | 1526 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1520 | `) -> Any:` |
| 1841 | venv_creative/lib/python3.13/site-packages/torch/_prims/__init__.py | 22 | 1 | invalid syntax | `from torch._prims_common.wrappers import backwards_not_supported` |
| 1842 | venv_creative/lib/python3.13/site-packages/torch/_functorch/pyfunctorch.py | 15 | 1 | invalid syntax | `from torch.autograd.forward_ad import _set_fwd_grad_enabled` |
| 1843 | venv_creative/lib/python3.13/site-packages/torch/_functorch/eager_transforms.py | 27 | 1 | invalid syntax | `from torch._functorch.utils import argnums_t, exposed_in` |
| 1844 | venv_creative/lib/python3.13/site-packages/torch/_functorch/_activation_checkpointing/knapsack_evaluator.py | 199 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 193 | `),` |
| 1845 | venv_creative/lib/python3.13/site-packages/torch/_functorch/_aot_autograd/runtime_wrappers.py | 2252 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 2239 | `):` |
| 1846 | venv_creative/lib/python3.13/site-packages/torch/_functorch/_aot_autograd/functional_utils.py | 27 | 15 | invalid syntax | `aot_joint_log = getArtifactLogger(__name__, "aot_joint_graph")` |
| 1847 | venv_creative/lib/python3.13/site-packages/torch/_functorch/_aot_autograd/utils.py | 37 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `original_zip = zip` |
| 1848 | venv_creative/lib/python3.13/site-packages/torch/_functorch/_aot_autograd/subclass_utils.py | 24 | 1 | invalid syntax | `from .utils import strict_zip` |
| 1849 | venv_creative/lib/python3.13/site-packages/torch/_functorch/_aot_autograd/subclass_parametrization.py | 39 | 20 | unexpected indent | `rebuilt = subclass_meta.class_type.__tensor_unflatten__(` |
| 1850 | venv_creative/lib/python3.13/site-packages/torch/_numpy/random.py | 38 | 1 | invalid syntax | `def use_numpy_random():` |
| 1851 | venv_creative/lib/python3.13/site-packages/torch/_numpy/_ndarray.py | 18 | 9 | invalid syntax | `newaxis = None` |
| 1852 | venv_creative/lib/python3.13/site-packages/torch/_numpy/_util.py | 168 | 24 | '(' was never closed | `raise TypeError(` |
| 1853 | venv_creative/lib/python3.13/site-packages/torch/_numpy/_normalizations.py | 112 | 34 | unindent does not match any outer indentation level | `from ._ndarray import ndarray` |
| 1854 | venv_creative/lib/python3.13/site-packages/torch/_numpy/_funcs_impl.py | 30 | 1 | invalid syntax | `def copy(` |
| 1855 | venv_creative/lib/python3.13/site-packages/torch/_numpy/testing/utils.py | 63 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `verbose = 0` |
| 1856 | venv_creative/lib/python3.13/site-packages/torch/_export/converter.py | 23 | 1 | invalid syntax | `from torch.fx import subgraph_rewriter` |
| 1857 | venv_creative/lib/python3.13/site-packages/torch/_export/pass_base.py | 22 | 1 | invalid syntax | `from torch.fx.graph import CodeGen` |
| 1858 | venv_creative/lib/python3.13/site-packages/torch/_export/utils.py | 34 | 1 | invalid syntax | `from torch.utils._pytree import (Context, FlattenFunc, FromDumpableContextFn,` |
| 1859 | venv_creative/lib/python3.13/site-packages/torch/_export/non_strict_utils.py | 19 | 1 | invalid syntax | `from torch._dynamo.variables.builder import TrackedFake` |
| 1860 | venv_creative/lib/python3.13/site-packages/torch/_export/passes/replace_with_hop_pass_util.py | 15 | 8 | unexpected indent | `from torch.export.graph_signature import ExportGraphSignature` |
| 1861 | venv_creative/lib/python3.13/site-packages/torch/_export/db/examples/decorator.py | 25 | 8 | unexpected indent | `def forward(self, x, y):` |
| 1862 | venv_creative/lib/python3.13/site-packages/torch/_export/serde/serialize.py | 408 | 5 | closing parenthesis '}' does not match opening parenthesis '(' on line 401 | `}` |
| 1863 | venv_creative/lib/python3.13/site-packages/torch/_subclasses/fake_impls.py | 20 | 1 | invalid syntax | `from torch._subclasses.fake_tensor import (DataDependentOutputException,` |
| 1864 | venv_creative/lib/python3.13/site-packages/torch/_subclasses/fake_tensor.py | 33 | 1 | invalid syntax | `from torch._utils import render_call` |
| 1865 | venv_creative/lib/python3.13/site-packages/torch/_subclasses/schema_check_mode.py | 96 | 16 | unexpected indent | `if (` |
| 1866 | venv_creative/lib/python3.13/site-packages/torch/_custom_op/autograd.py | 34 | 77 | invalid syntax. Perhaps you forgot a comma? | `"save_for_backward" if custom_op._has_impl("backward") else "backward"` |
| 1867 | venv_creative/lib/python3.13/site-packages/torch/nn/functional.py | 5205 | 17 | too many nested parentheses | `if input.dim() == 5 and mode == "trilinear":` |
| 1868 | venv_creative/lib/python3.13/site-packages/torch/nn/init.py | 45 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_R = TypeVar("_R")` |
| 1869 | venv_creative/lib/python3.13/site-packages/torch/nn/attention/flex_attention.py | 24 | 1 | invalid syntax | `from torch.nn.attention._utils import _validate_sdpa_input` |
| 1870 | venv_creative/lib/python3.13/site-packages/torch/nn/parallel/parallel_apply.py | 53 | 30 | invalid syntax | `if kwargs_tup is not None:` |
| 1871 | venv_creative/lib/python3.13/site-packages/torch/nn/utils/_named_member_accessor.py | 24 | 12 | unexpected indent | `else:` |
| 1872 | venv_creative/lib/python3.13/site-packages/torch/nn/utils/convert_parameters.py | 38 | 8 | unexpected indent | `if not isinstance(vec, torch.Tensor):` |
| 1873 | venv_creative/lib/python3.13/site-packages/torch/nn/utils/parametrize.py | 29 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_cache_enabled = 0` |
| 1874 | venv_creative/lib/python3.13/site-packages/torch/nn/utils/prune.py | 72 | 13 | invalid syntax. Perhaps you forgot a comma? | `f"Module {module} has to be pruned"` |
| 1875 | venv_creative/lib/python3.13/site-packages/torch/nn/utils/rnn.py | 22 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_T = TypeVar("_T")` |
| 1876 | venv_creative/lib/python3.13/site-packages/torch/nn/utils/_expanded_weights/expanded_weights_utils.py | 23 | 5 | invalid syntax | `return batch_first` |
| 1877 | venv_creative/lib/python3.13/site-packages/torch/nn/modules/transformer.py | 29 | 1 | invalid syntax | `def _generate_square_subsequent_mask(` |
| 1878 | venv_creative/lib/python3.13/site-packages/torch/nn/modules/sparse.py | 136 | 19 | invalid syntax | `num_embeddings: int` |
| 1879 | venv_creative/lib/python3.13/site-packages/torch/nn/modules/module.py | 1799 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1787 | `) -> RemovableHandle:` |
| 1880 | venv_creative/lib/python3.13/site-packages/torch/nn/modules/conv.py | 35 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `convolution_notes = {` |
| 1881 | venv_creative/lib/python3.13/site-packages/torch/nn/modules/rnn.py | 31 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_rnn_impls = {` |
| 1882 | venv_creative/lib/python3.13/site-packages/torch/mps/__init__.py | 22 | 8 | unexpected indent | `if _default_mps_generator is None:` |
| 1883 | venv_creative/lib/python3.13/site-packages/torch/onnx/symbolic_opset11.py | 89 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_onnx_symbolic = functools.partial(registration.onnx_symbolic, opset = 11)` |
| 1884 | venv_creative/lib/python3.13/site-packages/torch/onnx/symbolic_opset10.py | 69 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_onnx_symbolic = functools.partial(registration.onnx_symbolic, opset = 10)` |
| 1885 | venv_creative/lib/python3.13/site-packages/torch/onnx/symbolic_opset14.py | 40 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_onnx_symbolic = functools.partial(registration.onnx_symbolic, opset = 14)` |
| 1886 | venv_creative/lib/python3.13/site-packages/torch/onnx/symbolic_opset9.py | 3805 | 48 | too many nested parentheses | `decorate=[symbolic_helper._apply_params("aten::feature_alpha_dropout_")],` |
| 1887 | venv_creative/lib/python3.13/site-packages/torch/onnx/utils.py | 1392 | 5 | closing parenthesis '}' does not match opening parenthesis '(' on line 1386 | `}` |
| 1888 | venv_creative/lib/python3.13/site-packages/torch/onnx/symbolic_opset13.py | 32 | 5 | invalid syntax | `return softmax` |
| 1889 | venv_creative/lib/python3.13/site-packages/torch/onnx/symbolic_opset17.py | 55 | 16 | invalid syntax. Perhaps you forgot a comma? | `input, _type_utils.JitScalarType.FLOAT` |
| 1890 | venv_creative/lib/python3.13/site-packages/torch/onnx/_internal/_exporter_legacy.py | 13 | 1 | invalid syntax | `import abc` |
| 1891 | venv_creative/lib/python3.13/site-packages/torch/onnx/_internal/fx/onnxfunction_dispatcher.py | 78 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 72 | `) -> onnxscript.OnnxFunction ¦ onnxscript.TracedOnnxFunction:` |
| 1892 | venv_creative/lib/python3.13/site-packages/torch/onnx/_internal/fx/serialization.py | 28 | 5 | invalid syntax | `"""Create a TensorProto with external data from a PyTorch tensor.` |
| 1893 | venv_creative/lib/python3.13/site-packages/torch/onnx/_internal/exporter/_onnx_program.py | 399 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 394 | `) -> None:` |
| 1894 | venv_creative/lib/python3.13/site-packages/torch/onnx/_internal/exporter/_core.py | 34 | 1 | invalid syntax | `if typing.TYPE_CHECKING:` |
| 1895 | venv_creative/lib/python3.13/site-packages/torch/onnx/_internal/exporter/_torchlib/ops/nn.py | 67 | 1 | invalid syntax | `def aten_scaled_dot_product_attention_23(` |
| 1896 | venv_creative/lib/python3.13/site-packages/torch/distributed/_state_dict_utils.py | 18 | 8 | unexpected indent | `from torch.distributed.tensor import DTensor, Replicate, distribute_tensor` |
| 1897 | venv_creative/lib/python3.13/site-packages/torch/distributed/distributed_c10d.py | 34 | 1 | invalid syntax | `from torch._utils_internal import set_pytorch_distributed_envs_from_justknobs` |
| 1898 | venv_creative/lib/python3.13/site-packages/torch/distributed/_functional_collectives.py | 38 | 9 | invalid syntax | `def is_torchdynamo_compiling():` |
| 1899 | venv_creative/lib/python3.13/site-packages/torch/distributed/device_mesh.py | 41 | 1 | invalid syntax | `else:` |
| 1900 | venv_creative/lib/python3.13/site-packages/torch/distributed/checkpoint/format_utils.py | 16 | 1 | invalid syntax | `from torch.distributed.checkpoint.metadata import (STATE_DICT_TYPE, STORAGE_TYPES,` |
| 1901 | venv_creative/lib/python3.13/site-packages/torch/distributed/checkpoint/planner.py | 17 | 9 | invalid syntax | `__all__ = [` |
| 1902 | venv_creative/lib/python3.13/site-packages/torch/distributed/checkpoint/_sharded_tensor_utils.py | 48 | 12 | unexpected indent | `if not isinstance(inner_st, ShardedTensor):` |
| 1903 | venv_creative/lib/python3.13/site-packages/torch/distributed/checkpoint/utils.py | 23 | 1 | invalid syntax | `from .metadata import STATE_DICT_TYPE, MetadataIndex` |
| 1904 | venv_creative/lib/python3.13/site-packages/torch/distributed/checkpoint/planner_helpers.py | 18 | 1 | invalid syntax | `from .planner import (LoadItemType, ReadItem, SavePlan, TensorWriteData, WriteItem,` |
| 1905 | venv_creative/lib/python3.13/site-packages/torch/distributed/nn/functional.py | 206 | 1 | invalid syntax | `def all_reduce(tensor, op = ReduceOp.SUM, group = group.WORLD):` |
| 1906 | venv_creative/lib/python3.13/site-packages/torch/distributed/elastic/rendezvous/etcd_store.py | 112 | 13 | invalid syntax | `return int(self._decode(node.value))` |
| 1907 | venv_creative/lib/python3.13/site-packages/torch/distributed/elastic/rendezvous/etcd_rendezvous.py | 30 | 1 | invalid syntax | `from .etcd_store import EtcdStore, cas_delay` |
| 1908 | venv_creative/lib/python3.13/site-packages/torch/distributed/elastic/rendezvous/dynamic_rendezvous.py | 31 | 1 | invalid syntax | `from .utils import _delay, _PeriodicTimer` |
| 1909 | venv_creative/lib/python3.13/site-packages/torch/distributed/elastic/multiprocessing/api.py | 827 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 819 | `},` |
| 1910 | venv_creative/lib/python3.13/site-packages/torch/distributed/pipelining/_IR.py | 760 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 755 | `):` |
| 1911 | venv_creative/lib/python3.13/site-packages/torch/distributed/pipelining/_schedule_visualizer.py | 21 | 1 | invalid syntax | `from torch.distributed.pipelining.stage import PipelineStage` |
| 1912 | venv_creative/lib/python3.13/site-packages/torch/distributed/pipelining/microbatch.py | 19 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `logger = logging.getLogger(__name__)` |
| 1913 | venv_creative/lib/python3.13/site-packages/torch/distributed/pipelining/schedules.py | 39 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `logger = logging.getLogger(__name__)` |
| 1914 | venv_creative/lib/python3.13/site-packages/torch/distributed/algorithms/ddp_comm_hooks/ddp_zero_hook.py | 41 | 9 | invalid syntax. Perhaps you forgot a comma? | `"Overlapping DDP with ZeRO only supports a single parameter group"` |
| 1915 | venv_creative/lib/python3.13/site-packages/torch/distributed/algorithms/ddp_comm_hooks/powerSGD_hook.py | 45 | 1 | invalid syntax | `def _orthogonalize_gram_schmidt(matrices, epsilon = 0):` |
| 1916 | venv_creative/lib/python3.13/site-packages/torch/distributed/algorithms/_quantization/quantization.py | 38 | 32 | invalid syntax | `if qtype == DQuantType.FP16:` |
| 1917 | venv_creative/lib/python3.13/site-packages/torch/distributed/optim/zero_redundancy_optimizer.py | 65 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 59 | `}` |
| 1918 | venv_creative/lib/python3.13/site-packages/torch/distributed/_composable/checkpoint_activation.py | 13 | 1 | invalid syntax | `from .contract import _State, contract` |
| 1919 | venv_creative/lib/python3.13/site-packages/torch/distributed/_tools/sac_estimator.py | 20 | 1 | invalid syntax | `from torch.utils._python_dispatch import TorchDispatchMode` |
| 1920 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/sharded_grad_scaler.py | 32 | 1 | invalid syntax | `class _GeneralMultiDeviceReplicator(_MultiDeviceReplicator):` |
| 1921 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_state_dict_utils.py | 18 | 1 | invalid syntax | `from torch.distributed.device_mesh import _mesh_resources` |
| 1922 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_optim_utils.py | 961 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 950 | `) -> dict[str, Any]:` |
| 1923 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_runtime_utils.py | 24 | 1 | invalid syntax | `from torch.distributed.fsdp._flat_param import (RESHARD_AFTER_FORWARD_HANDLE_STRATEGIES,` |
| 1924 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_fsdp_extensions.py | 13 | 1 | invalid syntax | `from torch.distributed.tensor import DeviceMesh, DTensor` |
| 1925 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_flat_param.py | 24 | 1 | invalid syntax | `from torch.distributed.utils import (_alloc_storage, _data_ptr_allocated, _free_storage,` |
| 1926 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_fully_shard/_fsdp_common.py | 36 | 9 | invalid syntax | `global _compiled_autograd_enabled` |
| 1927 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_fully_shard/_fsdp_param_group.py | 21 | 1 | invalid syntax | `from ._fsdp_common import (FSDPMeshInfo, HSDPMeshInfo, TrainingState,` |
| 1928 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_fully_shard/_fsdp_param.py | 26 | 1 | invalid syntax | `"""` |
| 1929 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_fully_shard/_fsdp_init.py | 33 | 6 | invalid syntax | `):` |
| 1930 | venv_creative/lib/python3.13/site-packages/torch/distributed/fsdp/_fully_shard/_fsdp_collectives.py | 14 | 1 | invalid syntax | `from ._fsdp_param import FSDPParam, ShardedState` |
| 1931 | venv_creative/lib/python3.13/site-packages/torch/distributed/_shard/common_op_utils.py | 23 | 12 | unexpected indent | `if isinstance(e, ShardedTensor):` |
| 1932 | venv_creative/lib/python3.13/site-packages/torch/distributed/_shard/_utils.py | 18 | 8 | unexpected indent | `for idx, (offset, size) in enumerate(zip(offsets, sizes)):` |
| 1933 | venv_creative/lib/python3.13/site-packages/torch/distributed/_shard/sharded_tensor/metadata.py | 51 | 5 | invalid syntax | `def __setstate__(` |
| 1934 | venv_creative/lib/python3.13/site-packages/torch/distributed/_shard/sharded_tensor/api.py | 23 | 1 | invalid syntax | `from torch.distributed._shard.sharding_spec.api import (_dispatch_custom_op,` |
| 1935 | venv_creative/lib/python3.13/site-packages/torch/distributed/_shard/sharded_tensor/shard.py | 23 | 8 | unexpected indent | `metadata: ShardMetadata` |
| 1936 | venv_creative/lib/python3.13/site-packages/torch/distributed/_shard/sharded_tensor/utils.py | 16 | 1 | invalid syntax | `from .metadata import ShardedTensorMetadata, TensorProperties` |
| 1937 | venv_creative/lib/python3.13/site-packages/torch/distributed/_shard/sharding_spec/api.py | 18 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 1938 | venv_creative/lib/python3.13/site-packages/torch/distributed/_symmetric_memory/__init__.py | 42 | 5 | expression cannot contain assignment, perhaps you meant "=="? | `_group_name_to_store[group_name] = store` |
| 1939 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_shards_wrapper.py | 16 | 1 | invalid syntax | `from torch.distributed.checkpoint.planner import (TensorWriteData, WriteItem,` |
| 1940 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_redistribute.py | 17 | 8 | invalid syntax | `logger = logging.getLogger(__name__)` |
| 1941 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_collective_utils.py | 20 | 8 | invalid syntax | `logger = logging.getLogger(__name__)` |
| 1942 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_api.py | 21 | 1 | invalid syntax | `from torch.distributed.tensor._utils import (compute_global_tensor_info,` |
| 1943 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_dispatch.py | 24 | 1 | invalid syntax | `from torch.distributed.tensor._utils import try_find_mesh_from_args` |
| 1944 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/placement_types.py | 17 | 9 | invalid syntax | `__all__ = ["Placement", "Shard", "Replicate", "Partial"]` |
| 1945 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_tp_conv.py | 28 | 47 | invalid syntax | `if kernel_size[3] // 2 > input_size[3]:` |
| 1946 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/experimental/_attention.py | 144 | 22 | invalid syntax. Perhaps you forgot a comma? | `else self._lse` |
| 1947 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/parallel/fsdp.py | 14 | 1 | invalid syntax | `from torch.distributed._shard.sharding_spec import ShardMetadata` |
| 1948 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/parallel/style.py | 560 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 552 | `):` |
| 1949 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/parallel/loss.py | 19 | 1 | invalid syntax | `from torch.distributed.tensor._ops.utils import normalize_dim` |
| 1950 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_ops/_embedding_ops.py | 14 | 1 | invalid syntax | `from torch.distributed.tensor._ops.utils import (expand_to_full_mesh_op_strategy,` |
| 1951 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_ops/_tensor_ops.py | 989 | 25 | closing parenthesis ')' does not match opening parenthesis '[' on line 983 | `),` |
| 1952 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_ops/_matrix_ops.py | 13 | 1 | invalid syntax | `from torch.distributed.tensor._ops._einsum_strategy import gen_einsum_strategies` |
| 1953 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/_ops/_math_ops.py | 17 | 1 | invalid syntax | `from torch.distributed.tensor._ops.utils import (as_list,` |
| 1954 | venv_creative/lib/python3.13/site-packages/torch/distributed/tensor/debug/_visualize_sharding.py | 53 | 12 | unexpected indent | `r, g, b = (int(a * 255) for a in color)` |
| 1955 | venv_creative/lib/python3.13/site-packages/torch/distributed/rpc/__init__.py | 34 | 5 | invalid syntax | `import numbers` |
| 1956 | venv_creative/lib/python3.13/site-packages/torch/autograd/graph.py | 476 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 468 | `) -> RemovableHandle:` |
| 1957 | venv_creative/lib/python3.13/site-packages/torch/autograd/forward_ad.py | 21 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_current_level = -1` |
| 1958 | venv_creative/lib/python3.13/site-packages/torch/autograd/__init__.py | 28 | 1 | invalid syntax | `from .gradcheck import gradcheck, gradgradcheck` |
| 1959 | venv_creative/lib/python3.13/site-packages/torch/autograd/gradcheck.py | 31 | 1 | invalid syntax | `class GradcheckError(RuntimeError):` |
| 1960 | venv_creative/lib/python3.13/site-packages/torch/autograd/_functions/utils.py | 9 | 12 | unexpected indent | `return tensor.contiguous().view(size)` |
| 1961 | venv_creative/lib/python3.13/site-packages/torch/fx/proxy.py | 909 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 900 | `}` |
| 1962 | venv_creative/lib/python3.13/site-packages/torch/fx/experimental/validator.py | 104 | 13 | invalid syntax | `args = collect_str_args(e)` |
| 1963 | venv_creative/lib/python3.13/site-packages/torch/fx/experimental/symbolic_shapes.py | 3712 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 3706 | `}` |
| 1964 | venv_creative/lib/python3.13/site-packages/torch/fx/experimental/proxy_tensor.py | 1987 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 1979 | `}` |
| 1965 | venv_creative/lib/python3.13/site-packages/torch/fx/experimental/migrate_gradual_types/constraint_transformation.py | 324 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 318 | `),` |
| 1966 | venv_creative/lib/python3.13/site-packages/torch/fx/experimental/migrate_gradual_types/constraint_generator.py | 289 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 283 | `),` |
| 1967 | venv_creative/lib/python3.13/site-packages/torch/fx/passes/shape_prop.py | 96 | 1 | invalid syntax | `class ShapeProp(torch.fx.Interpreter):` |
| 1968 | venv_creative/lib/python3.13/site-packages/torch/fx/passes/_tensorify_python_scalars.py | 150 | 60 | invalid syntax | `if isinstance(expr, (Integer, Number, BooleanAtom)):` |
| 1969 | venv_creative/lib/python3.13/site-packages/torch/fx/passes/splitter_base.py | 24 | 9 | invalid syntax | `__all__ = [` |
| 1970 | venv_creative/lib/python3.13/site-packages/torch/fx/passes/utils/matcher_utils.py | 65 | 1 | invalid syntax | `@compatibility(is_backward_compatible = False)` |
| 1971 | venv_creative/lib/python3.13/site-packages/torch/cuda/nccl.py | 93 | 8 | unexpected indent | `if outputs is not None:` |
| 1972 | venv_creative/lib/python3.13/site-packages/torch/cuda/__init__.py | 34 | 1 | invalid syntax | `from .streams import Event, ExternalStream, Stream` |
| 1973 | venv_creative/lib/python3.13/site-packages/torch/backends/_nnapi/serializer.py | 408 | 17 | invalid syntax | `if nnapi_dtype in op_codes:` |
| 1974 | venv_creative/lib/python3.13/site-packages/torch/backends/cudnn/__init__.py | 42 | 20 | unexpected indent | `else:` |
| 1975 | venv_creative/lib/python3.13/site-packages/torch/_decomp/decompositions_for_jvp.py | 75 | 8 | unexpected indent | `decomp_fn = _maybe_remove_out_wrapper(decomp_fn)` |
| 1976 | venv_creative/lib/python3.13/site-packages/torch/_decomp/decompositions.py | 4725 | 31 | too many nested parentheses | `interpolation_mode in (0, 1, 2),` |
| 1977 | venv_creative/lib/python3.13/site-packages/torch/_decomp/__init__.py | 33 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_T = TypeVar("_T")` |
| 1978 | venv_creative/lib/python3.13/site-packages/torch/masked/_ops.py | 48 | 5 | invalid syntax | `else:` |
| 1979 | venv_creative/lib/python3.13/site-packages/torch/optim/lr_scheduler.py | 16 | 1 | invalid syntax | `from weakref import ref` |
| 1980 | venv_creative/lib/python3.13/site-packages/torch/optim/_adafactor.py | 14 | 9 | invalid syntax | `__all__ = ["Adafactor", "adafactor"]` |
| 1981 | venv_creative/lib/python3.13/site-packages/torch/optim/sgd.py | 16 | 9 | invalid syntax | `__all__ = ["SGD", "sgd"]` |
| 1982 | venv_creative/lib/python3.13/site-packages/torch/optim/adadelta.py | 16 | 9 | invalid syntax | `__all__ = ["Adadelta", "adadelta"]` |
| 1983 | venv_creative/lib/python3.13/site-packages/torch/_inductor/cudagraph_trees.py | 1345 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 1340 | `}` |
| 1984 | venv_creative/lib/python3.13/site-packages/torch/_inductor/select_algorithm.py | 1141 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 1128 | `}` |
| 1985 | venv_creative/lib/python3.13/site-packages/torch/_inductor/metrics.py | 34 | 54 | invalid syntax | `node_runtimes: list[tuple[BaseSchedulerNode, float]] = []` |
| 1986 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codecache.py | 1384 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1379 | `) -> tuple[Optional[CompiledFxGraph], dict[str, Any]]:` |
| 1987 | venv_creative/lib/python3.13/site-packages/torch/_inductor/cpp_builder.py | 39 | 5 | invalid syntax | `from triton.fb.build import _run_build_command, build_paths` |
| 1988 | venv_creative/lib/python3.13/site-packages/torch/_inductor/config.py | 43 | 1 | invalid syntax | `def static_cuda_launcher_default() -> bool:` |
| 1989 | venv_creative/lib/python3.13/site-packages/torch/_inductor/comms.py | 28 | 1 | invalid syntax | `from .virtualized import V` |
| 1990 | venv_creative/lib/python3.13/site-packages/torch/_inductor/mkldnn_lowerings.py | 18 | 1 | invalid syntax | `from .select_algorithm import (ChoiceCaller, ExternKernelChoice,` |
| 1991 | venv_creative/lib/python3.13/site-packages/torch/_inductor/aoti_eager.py | 62 | 26 | invalid syntax | `):` |
| 1992 | venv_creative/lib/python3.13/site-packages/torch/_inductor/graph.py | 300 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 286 | `) -> None:` |
| 1993 | venv_creative/lib/python3.13/site-packages/torch/_inductor/lowering.py | 480 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 473 | `) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:` |
| 1994 | venv_creative/lib/python3.13/site-packages/torch/_inductor/compile_fx.py | 41 | 1 | invalid syntax | `from torch._functorch import config as functorch_config` |
| 1995 | venv_creative/lib/python3.13/site-packages/torch/_inductor/sizevars.py | 155 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 149 | `}` |
| 1996 | venv_creative/lib/python3.13/site-packages/torch/_inductor/ir.py | 4650 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 4644 | `).data` |
| 1997 | venv_creative/lib/python3.13/site-packages/torch/_inductor/inductor_prims.py | 49 | 1 | invalid syntax | `def eager_force_stride(input_tensor: Tensor, stride) -> Tensor:` |
| 1998 | venv_creative/lib/python3.13/site-packages/torch/_inductor/utils.py | 206 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 201 | `) as p:` |
| 1999 | venv_creative/lib/python3.13/site-packages/torch/_inductor/debug.py | 38 | 1 | invalid syntax | `from .virtualized import V` |
| 2000 | venv_creative/lib/python3.13/site-packages/torch/_inductor/decomposition.py | 18 | 1 | invalid syntax | `from torch._decomp.decompositions import _grid_sampler_2d as decomp_grid_sampler_2d` |
| 2001 | venv_creative/lib/python3.13/site-packages/torch/_inductor/fx_utils.py | 16 | 1 | invalid syntax | `from torch.utils import _pytree as pytree` |
| 2002 | venv_creative/lib/python3.13/site-packages/torch/_inductor/choices.py | 19 | 1 | invalid syntax | `from .virtualized import V` |
| 2003 | venv_creative/lib/python3.13/site-packages/torch/_inductor/comm_analysis.py | 123 | 7 | invalid syntax | `hwLat = [` |
| 2004 | venv_creative/lib/python3.13/site-packages/torch/_inductor/output_code.py | 42 | 1 | invalid syntax | `from torch._inductor.freezing_utils import has_frozen_params, is_frozen_param` |
| 2005 | venv_creative/lib/python3.13/site-packages/torch/_inductor/loop_body.py | 24 | 1 | invalid syntax | `from .virtualized import V, ops` |
| 2006 | venv_creative/lib/python3.13/site-packages/torch/_inductor/runtime/triton_heuristics.py | 1800 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 1781 | `}` |
| 2007 | venv_creative/lib/python3.13/site-packages/torch/_inductor/runtime/triton_compat.py | 22 | 12 | unexpected indent | `except ImportError:` |
| 2008 | venv_creative/lib/python3.13/site-packages/torch/_inductor/runtime/hints.py | 57 | 45 | unindent does not match any outer indentation level | `res = AttrsDescriptor.from_dict(` |
| 2009 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/cpp_wrapper_gpu.py | 22 | 1 | invalid syntax | `from ..utils import GPU_ALIGN_BYTES, IndentedBuffer, cache_on_self, get_gpu_type` |
| 2010 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/triton_utils.py | 17 | 1 | invalid syntax | `def should_unwrap_unspec_arg(name: str):` |
| 2011 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/triton.py | 176 | 5 | closing parenthesis '}' does not match opening parenthesis '(' on line 170 | `}` |
| 2012 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/simd.py | 639 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 634 | `},` |
| 2013 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/wrapper_fxir.py | 16 | 1 | invalid syntax | `from torch._inductor.codecache import PyCodeCache` |
| 2014 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/cpp.py | 506 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 501 | `),` |
| 2015 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/cpp_wrapper_cpu.py | 34 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 2016 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/common.py | 664 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 649 | `},` |
| 2017 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/cpp_gemm_template.py | 22 | 1 | invalid syntax | `from ..virtualized import V, ops` |
| 2018 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/cuda/cutlass_utils.py | 57 | 5 | invalid syntax | `return content` |
| 2019 | venv_creative/lib/python3.13/site-packages/torch/_inductor/codegen/cuda/gemm_template.py | 24 | 1 | invalid syntax | `from ...utils import Placeholder, is_dynamic` |
| 2020 | venv_creative/lib/python3.13/site-packages/torch/_inductor/fx_passes/quantization.py | 1669 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 1662 | `):` |
| 2021 | venv_creative/lib/python3.13/site-packages/torch/_inductor/fx_passes/split_cat.py | 170 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 165 | `):` |
| 2022 | venv_creative/lib/python3.13/site-packages/torch/_inductor/fx_passes/group_batch_fusion.py | 20 | 1 | invalid syntax | `from ..utils import OPTIMUS_EXCLUDE_POST_GRAD` |
| 2023 | venv_creative/lib/python3.13/site-packages/torch/_inductor/fx_passes/pre_grad.py | 17 | 1 | invalid syntax | `from torch.fx.passes.graph_transform_observer import GraphTransformObserver` |
| 2024 | venv_creative/lib/python3.13/site-packages/torch/_inductor/kernel/flex_attention.py | 25 | 1 | invalid syntax | `from ..lowering import (_full, check_and_broadcast_indices, empty, empty_strided,` |
| 2025 | venv_creative/lib/python3.13/site-packages/torch/utils/dlpack.py | 8 | 11 | '[' was never closed | `__all__ = [` |
| 2026 | venv_creative/lib/python3.13/site-packages/torch/utils/_python_dispatch.py | 16 | 1 | invalid syntax | `from typing_extensions import TypeIs` |
| 2027 | venv_creative/lib/python3.13/site-packages/torch/utils/_config_module.py | 18 | 1 | invalid syntax | `from unittest import mock` |
| 2028 | venv_creative/lib/python3.13/site-packages/torch/utils/flop_counter.py | 58 | 39 | invalid syntax | `if target in flop_registry:` |
| 2029 | venv_creative/lib/python3.13/site-packages/torch/utils/_content_store.py | 78 | 62 | invalid syntax. Perhaps you forgot a comma? | `-(2**31), 2**31, x.shape, device = x.device, dtype = torch.int32` |
| 2030 | venv_creative/lib/python3.13/site-packages/torch/utils/benchmark/utils/fuzzer.py | 16 | 16 | invalid syntax | `_DISTRIBUTIONS = (` |
| 2031 | venv_creative/lib/python3.13/site-packages/torch/utils/benchmark/utils/valgrind_wrapper/timer_interface.py | 75 | 5 | invalid syntax | `def __repr__(self) -> str:` |
| 2032 | venv_creative/lib/python3.13/site-packages/torch/utils/_sympy/singleton_int.py | 45 | 4 | unexpected unindent | `def free_symbols(self):` |
| 2033 | venv_creative/lib/python3.13/site-packages/torch/utils/hipify/hipify_python.py | 79 | 1 | invalid syntax | `class InputError(Exception):` |
| 2034 | venv_creative/lib/python3.13/site-packages/torch/utils/tensorboard/summary.py | 914 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 908 | `),` |
| 2035 | venv_creative/lib/python3.13/site-packages/torch/utils/data/graph.py | 60 | 16 | unexpected indent | `else:` |
| 2036 | venv_creative/lib/python3.13/site-packages/torch/utils/data/dataloader.py | 30 | 1 | invalid syntax | `from torch.utils.data.dataset import Dataset, IterableDataset` |
| 2037 | venv_creative/lib/python3.13/site-packages/torch/utils/data/sampler.py | 19 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_T_co = TypeVar("_T_co", covariant = True)` |
| 2038 | venv_creative/lib/python3.13/site-packages/torch/utils/data/datapipes/_hook_iterator.py | 52 | 24 | invalid syntax | `if simplify_dp_name:` |
| 2039 | venv_creative/lib/python3.13/site-packages/torch/utils/data/datapipes/dataframe/dataframes.py | 37 | 1 | invalid syntax | `def disable_capture():` |
| 2040 | venv_creative/lib/python3.13/site-packages/torch/utils/_strobelight/cli_function_profiler.py | 19 | 5 | invalid syntax. Perhaps you forgot a comma? | `"%(name)s, line %(lineno)d, %(asctime)s, %(levelname)s: %(message)s"` |
| 2041 | venv_creative/lib/python3.13/site-packages/torch/quantization/_quantized_conversions.py | 34 | 1 | invalid syntax | `def quantized_weight_reorder_for_mixed_dtypes_linear_cutlass(` |
| 2042 | venv_creative/lib/python3.13/site-packages/torch/testing/_comparison.py | 29 | 13 | invalid syntax. Perhaps you forgot a comma? | `"If you are a user and see this message during normal operation "` |
| 2043 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/triton_utils.py | 110 | 13 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `key=[],` |
| 2044 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/common_nn.py | 29 | 1 | invalid syntax | `from torch.types import _TensorOrTensors` |
| 2045 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/custom_op_db.py | 14 | 1 | invalid syntax | `from torch.testing._internal.common_dtype import all_types_and` |
| 2046 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/autocast_test_lists.py | 173 | 77 | invalid decimal literal | `("poisson_nll_loss", mat0_fp16 + mat1_fp16 + (True, False, 1.e - 8, torch.nn._reduction.get_enum('mean'))),` |
| 2047 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/common_fsdp.py | 32 | 1 | invalid syntax | `from torch.distributed.fsdp._init_utils import NO_RESHARD_AFTER_FORWARD_STRATEGIES` |
| 2048 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/common_device_type.py | 25 | 1 | invalid syntax | `from torch.testing._internal.common_dtype import get_all_dtypes` |
| 2049 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/common_distributed.py | 44 | 1 | invalid syntax | `from torch.testing._internal.distributed.multi_threaded_pg import (` |
| 2050 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/common_methods_invocations.py | 2739 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 2733 | `),` |
| 2051 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/logging_tensor.py | 55 | 55 | invalid syntax. Perhaps you forgot a comma? | `device = elem.device, requires_grad = kwargs.get("requires_grad", False)` |
| 2052 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/common_quantization.py | 1172 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 1165 | `) -> None:` |
| 2053 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/common_jit.py | 26 | 1 | invalid syntax | `def check_output_types(self, func, ref_outputs, args, kwargs):` |
| 2054 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/common_utils.py | 74 | 1 | invalid syntax | `from torch.testing._internal.common_dtype import get_all_dtypes` |
| 2055 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/opinfo/core.py | 24 | 1 | invalid syntax | `from torch.testing._internal.common_dtype import (_dispatch_dtypes,` |
| 2056 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/opinfo/definitions/linalg.py | 1559 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1542 | `),` |
| 2057 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/opinfo/definitions/sparse.py | 16 | 1 | invalid syntax | `def _check_validate(op_info, sample):` |
| 2058 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/opinfo/definitions/fft.py | 277 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 253 | `),` |
| 2059 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/distributed/ddp_under_dist_autograd_test.py | 22 | 1 | invalid syntax | `from torch.testing._internal.dist_utils import INIT_METHOD_TEMPLATE, dist_init` |
| 2060 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/distributed/distributed_test.py | 3366 | 31 | too many nested parentheses | `2 + (10 * (len(group) - 1)),` |
| 2061 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/distributed/multi_threaded_pg.py | 19 | 1 | invalid syntax | `from torch.distributed.distributed_c10d import P2POp, _CollOp, _store_based_barrier` |
| 2062 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/distributed/rpc/rpc_test.py | 4749 | 62 | too many nested parentheses | `fut3 = rpc.rpc_async(dst, torch.add, args=(torch.ones(2, 2), 1)).then(callback)` |
| 2063 | venv_creative/lib/python3.13/site-packages/torch/testing/_internal/distributed/rpc/jit/rpc_test.py | 21 | 1 | invalid syntax | `from torch.testing._internal.distributed.rpc.rpc_agent_test_fixture import \` |
| 2064 | venv_creative/lib/python3.13/site-packages/torch/amp/grad_scaler.py | 27 | 12 | unexpected indent | `self._per_device_tensors: dict[torch.device, torch.Tensor] = {}` |
| 2065 | venv_creative/lib/python3.13/site-packages/torch/jit/_script.py | 30 | 1 | invalid syntax | `from torch.jit._recursive import (ScriptMethodStub, _compile_and_register_class,` |
| 2066 | venv_creative/lib/python3.13/site-packages/torch/jit/_shape_functions.py | 42 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"The size of tensor a {sizeA} must match the size of tensor b ({sizeB}) at non - singleton dimension {i}"` |
| 2067 | venv_creative/lib/python3.13/site-packages/torch/jit/frontend.py | 25 | 1 | invalid syntax | `from torch._jit_internal import (FunctionModifiers, _is_drop_fn,  # noqa: F401` |
| 2068 | venv_creative/lib/python3.13/site-packages/torch/jit/_trace.py | 27 | 1 | invalid syntax | `from torch.autograd import function` |
| 2069 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/guards.py | 3176 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 3169 | `):` |
| 2070 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/test_minifier_common.py | 86 | 13 | invalid syntax. Perhaps you forgot a comma? | `torch._dynamo.config.patch(debug_dir_root = cls.DEBUG_DIR)` |
| 2071 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/output_graph.py | 53 | 1 | invalid syntax | `from torch._subclasses.fake_tensor import FakeTensor` |
| 2072 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/utils.py | 59 | 1 | invalid syntax | `import torch` |
| 2073 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/side_effects.py | 42 | 1 | invalid syntax | `from .codegen import PyCodegen` |
| 2074 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/pgo.py | 35 | 1 | invalid syntax | `from torch._environment import is_fbcode` |
| 2075 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/symbolic_convert.py | 4713 | 18 | too many nested parentheses | `self.push(ConstantVariable.create(None))` |
| 2076 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/eval_frame.py | 895 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 889 | `) -> None:` |
| 2077 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/backends/debugging.py | 209 | 1 | invalid syntax. Perhaps you forgot a comma? | `register_backend(name="aot_eager", compiler_fn = aot_eager)` |
| 2078 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/backends/distributed.py | 102 | 5 | invalid syntax | `if len(rows):` |
| 2079 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/functions.py | 52 | 1 | invalid syntax | `from ..guards import GuardBuilder, install_guard` |
| 2080 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/iter.py | 29 | 1 | invalid syntax | `from .base import ValueMutationNew, VariableTracker` |
| 2081 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/misc.py | 1786 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1780 | `),` |
| 2082 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/lists.py | 919 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 913 | `),` |
| 2083 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/user_defined.py | 376 | 29 | closing parenthesis ')' does not match opening parenthesis '[' on line 363 | `),` |
| 2084 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/builder.py | 2483 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 2478 | `) or not config.assume_static_by_default:` |
| 2085 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/tensor.py | 40 | 1 | invalid syntax | `from torch.utils._python_dispatch import is_traceable_wrapper_subclass` |
| 2086 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/builtin.py | 508 | 25 | closing parenthesis ')' does not match opening parenthesis '[' on line 502 | `),` |
| 2087 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/constant.py | 70 | 13 | invalid syntax | `return variables.BaseListVariable.cls_for(type(value))(items, **kwargs)` |
| 2088 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/lazy.py | 28 | 12 | unexpected indent | `from . import builder` |
| 2089 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/variables/base.py | 107 | 1 | invalid syntax | `class ValueMutationNew(MutationType):` |
| 2090 | venv_creative/lib/python3.13/site-packages/torch/_dynamo/polyfills/__init__.py | 24 | 19 | '(' was never closed | `from . import (` |
| 2091 | venv_creative/lib/python3.13/site-packages/torch/_lazy/extract_compiled_graph.py | 100 | 20 | unexpected indent | `return duplicated_list` |
| 2092 | venv_creative/lib/python3.13/site-packages/torch/ao/nn/quantized/modules/__init__.py | 15 | 1 | invalid syntax | `from .batchnorm import BatchNorm2d, BatchNorm3d` |
| 2093 | venv_creative/lib/python3.13/site-packages/torch/ao/ns/fx/graph_passes.py | 21 | 1 | invalid syntax | `def _maybe_get_fqn(node: Node, gm: GraphModule) -> Optional[str]:` |
| 2094 | venv_creative/lib/python3.13/site-packages/torch/ao/ns/fx/graph_matcher.py | 19 | 5 | invalid syntax | `toq = torch.ops.quantized` |
| 2095 | venv_creative/lib/python3.13/site-packages/torch/ao/ns/fx/n_shadows_utils.py | 1319 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 1309 | `}` |
| 2096 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/observer.py | 26 | 1 | invalid syntax | `from torch.fx import Node` |
| 2097 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/_correct_bias.py | 18 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_supported_modules = {nn.Linear, nn.Conv2d}` |
| 2098 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/fake_quantize.py | 17 | 1 | invalid syntax | `from torch.nn import Module` |
| 2099 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/qconfig.py | 19 | 1 | invalid syntax | `from typing_extensions import deprecated` |
| 2100 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/utils.py | 33 | 86 | invalid syntax. Perhaps you forgot a comma? | `Callable, tuple[Callable, Callable], tuple[Callable, tuple[Callable, Callable]], Any` |
| 2101 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/pt2e/qat_utils.py | 17 | 1 | invalid syntax | `from torch.fx import Graph, GraphModule, Node` |
| 2102 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/pt2e/_numeric_debugger.py | 42 | 13 | invalid syntax. Perhaps you forgot a comma? | `f"Expected ep to be ExportedProgram, got {type(ExportedProgram)}"` |
| 2103 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/fx/convert.py | 14 | 1 | invalid syntax | `from torch.ao.quantization.backend_config.utils import (` |
| 2104 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/fx/utils.py | 425 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 406 | `}` |
| 2105 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/fx/_lower_to_native_backend.py | 39 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 31 | `}` |
| 2106 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/fx/_model_report/detector.py | 1780 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 1773 | `}` |
| 2107 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/fx/_model_report/model_report_visualizer.py | 138 | 21 | expected an indented block after 'if' statement on line 134 | `unique_feature_names.add(feature_name)` |
| 2108 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/fx/_model_report/model_report_observer.py | 47 | 8 | unexpected indent | `epoch_activation_max: torch.Tensor` |
| 2109 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/fx/_model_report/model_report.py | 15 | 1 | invalid syntax | `from torch.ao.quantization.fx._model_report.model_report_visualizer import \` |
| 2110 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/quantizer/xnnpack_quantizer.py | 86 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 80 | `}` |
| 2111 | venv_creative/lib/python3.13/site-packages/torch/ao/quantization/quantizer/quantizer.py | 26 | 1 | invalid syntax | `class QuantizationSpecBase(ABC):  # noqa: B024` |
| 2112 | venv_creative/lib/python3.13/site-packages/torch/ao/pruning/_experimental/data_sparsifier/data_norm_sparsifier.py | 75 | 9 | invalid syntax | `return mask` |
| 2113 | venv_creative/lib/python3.13/site-packages/torch/ao/pruning/_experimental/activation_sparsifier/activation_sparsifier.py | 175 | 21 | invalid syntax | `self.state[name]["mask"] = [0 for _ in range(0, len(features))]` |
| 2114 | venv_creative/lib/python3.13/site-packages/torch/_refs/__init__.py | 4463 | 44 | too many nested parentheses | `return torch.roll(torch.flatten(a), shifts, 0).view(a.shape)` |
| 2115 | venv_creative/lib/python3.13/site-packages/torch/_refs/nn/functional/__init__.py | 1097 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 1089 | `) -> TensorLikeType:` |
| 2116 | venv_creative/lib/python3.13/site-packages/torch/profiler/_memory_profiler.py | 17 | 1 | invalid syntax | `from torch._utils import _element_size` |
| 2117 | venv_creative/lib/python3.13/site-packages/torch/export/unflatten.py | 1218 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 1212 | `}` |
| 2118 | venv_creative/lib/python3.13/site-packages/torch/export/_draft_export.py | 20 | 1 | invalid syntax | `from ._trace import _export` |
| 2119 | venv_creative/lib/python3.13/site-packages/torch/export/pt2_archive/_package_weights.py | 24 | 12 | unexpected indent | `self.shape = tensor.shape` |
| 2120 | venv_creative/lib/python3.13/site-packages/torch/nested/_internal/nested_tensor.py | 16 | 8 | unexpected indent | `from torch._subclasses.functional_tensor import mb_unwrap_functional_tensor` |
| 2121 | venv_creative/lib/python3.13/site-packages/torch/nested/_internal/ops.py | 967 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 962 | `).reshape(` |
| 2122 | venv_creative/lib/python3.13/site-packages/torch/nested/_internal/sdpa.py | 14 | 1 | invalid syntax | `from torch.nn.attention import SDPBackend` |
| 2123 | venv_creative/lib/python3.13/site-packages/torch/_strobelight/cli_function_profiler.py | 20 | 5 | invalid syntax. Perhaps you forgot a comma? | `"%(name)s, line %(lineno)d, %(asctime)s, %(levelname)s: %(message)s"` |
| 2124 | venv_creative/lib/python3.13/site-packages/torch/distributions/transforms.py | 18 | 1 | invalid syntax | `from torch.nn.functional import pad, softplus` |
| 2125 | venv_creative/lib/python3.13/site-packages/torch/distributions/multivariate_normal.py | 55 | 9 | invalid syntax. Perhaps you forgot a comma? | `list(range(outer_batch_dims))` |
| 2126 | venv_creative/lib/python3.13/site-packages/torch/distributions/lowrank_multivariate_normal.py | 42 | 1 | invalid syntax | `def _batch_lowrank_mahalanobis(W, D, x, capacitance_tril):` |
| 2127 | venv_creative/lib/python3.13/site-packages/torch/distributions/lkj_cholesky.py | 76 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"Expected dim to be an integer greater than or equal to 2. Found dim={dim}."` |
| 2128 | venv_creative/lib/python3.13/site-packages/torch/distributions/distribution.py | 46 | 16 | unexpected indent | `Distribution._validate_args = value` |
| 2129 | venv_creative/lib/python3.13/site-packages/torch/distributions/kl.py | 31 | 1 | invalid syntax | `from .multivariate_normal import MultivariateNormal, _batch_mahalanobis` |
| 2130 | venv_creative/lib/python3.13/site-packages/torch/distributions/constraints.py | 79 | 1 | invalid syntax | `class Constraint:` |
| 2131 | venv_creative/lib/python3.13/site-packages/torch/package/glob_group.py | 70 | 5 | invalid syntax | `def _glob_list(elems: GlobPattern, separator: str = "."):` |
| 2132 | venv_creative/lib/python3.13/site-packages/websockets/auth.py | 9 | 8 | unexpected indent | `from .legacy.auth import __all__  # noqa: F401` |
| 2133 | venv_creative/lib/python3.13/site-packages/websockets/protocol.py | 13 | 1 | invalid syntax | `from .extensions import Extension` |
| 2134 | venv_creative/lib/python3.13/site-packages/websockets/client.py | 15 | 1 | invalid syntax | `from .extensions import ClientExtensionFactory, Extension` |
| 2135 | venv_creative/lib/python3.13/site-packages/websockets/__init__.py | 85 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 2136 | venv_creative/lib/python3.13/site-packages/websockets/asyncio/compatibility.py | 9 | 8 | unexpected indent | `aiter = aiter` |
| 2137 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/axes_grid1/axes_divider.py | 54 | 12 | unexpected indent | `self.set_anchor(anchor)` |
| 2138 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/mplot3d/axes3d.py | 44 | 1 | invalid syntax | `class Axes3D(Axes):` |
| 2139 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/mplot3d/axis3d.py | 53 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_AXINFO = {` |
| 2140 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/mplot3d/art3d.py | 23 | 1 | invalid syntax | `from matplotlib.colors import Normalize` |
| 2141 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/mplot3d/tests/test_axes3d.py | 2751 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 2743 | `),` |
| 2142 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/axisartist/axislines.py | 142 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self._loc = loc` |
| 2143 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/axisartist/grid_finder.py | 91 | 9 | invalid syntax | `return self._add_pad(xt.min(), xt.max(), yt.min(), yt.max())` |
| 2144 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/axisartist/axis_artist.py | 147 | 12 | unexpected indent | `self.stale = True` |
| 2145 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/axisartist/axisline_style.py | 43 | 9 | invalid syntax | `def set_line_mutation_scale(self, scale):` |
| 2146 | venv_creative/lib/python3.13/site-packages/mpl_toolkits/axisartist/floating_axes.py | 42 | 35 | invalid syntax | `if nth_coord_ticks is None:` |
| 2147 | venv_creative/lib/python3.13/site-packages/filelock/asyncio.py | 40 | 8 | unexpected indent | `run_in_executor: bool = True` |
| 2148 | venv_creative/lib/python3.13/site-packages/engineio/server.py | 229 | 25 | invalid syntax. Perhaps you forgot a comma? | `r = self._bad_request('Not an accepted origin.')` |
| 2149 | venv_creative/lib/python3.13/site-packages/engineio/packet.py | 47 | 13 | invalid syntax | `else:` |
| 2150 | venv_creative/lib/python3.13/site-packages/engineio/async_server.py | 221 | 17 | invalid syntax | `for client in self.sockets.values()` |
| 2151 | venv_creative/lib/python3.13/site-packages/sqlalchemy/exc.py | 62 | 5 | invalid syntax | `def __str__(self) -> str:` |
| 2152 | venv_creative/lib/python3.13/site-packages/sqlalchemy/connectors/asyncio.py | 20 | 1 | invalid syntax | `from ..engine import AdaptedConnection` |
| 2153 | venv_creative/lib/python3.13/site-packages/sqlalchemy/connectors/aioodbc.py | 19 | 1 | invalid syntax | `from .pyodbc import PyODBCConnector` |
| 2154 | venv_creative/lib/python3.13/site-packages/sqlalchemy/util/preloaded.py | 24 | 8 | unexpected indent | `from sqlalchemy.engine import default as _engine_default` |
| 2155 | venv_creative/lib/python3.13/site-packages/sqlalchemy/util/deprecations.py | 20 | 1 | invalid syntax | `from .. import exc` |
| 2156 | venv_creative/lib/python3.13/site-packages/sqlalchemy/util/langhelpers.py | 34 | 1 | invalid syntax | `from .. import exc` |
| 2157 | venv_creative/lib/python3.13/site-packages/sqlalchemy/util/typing.py | 758 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 751 | `}` |
| 2158 | venv_creative/lib/python3.13/site-packages/sqlalchemy/ext/associationproxy.py | 27 | 1 | invalid syntax | `from .. import ColumnElement, exc, inspect, orm, util` |
| 2159 | venv_creative/lib/python3.13/site-packages/sqlalchemy/ext/mypy/plugin.py | 24 | 1 | invalid syntax | `from mypy.plugin import (AttributeContext, ClassDefContext, DynamicClassDefContext,` |
| 2160 | venv_creative/lib/python3.13/site-packages/sqlalchemy/ext/asyncio/result.py | 15 | 1 | invalid syntax | `from ... import util` |
| 2161 | venv_creative/lib/python3.13/site-packages/sqlalchemy/ext/asyncio/engine.py | 16 | 1 | invalid syntax | `from ... import exc, inspection, util` |
| 2162 | venv_creative/lib/python3.13/site-packages/sqlalchemy/testing/exclusions.py | 95 | 5 | invalid syntax | `def _extend(self, other):` |
| 2163 | venv_creative/lib/python3.13/site-packages/sqlalchemy/testing/util.py | 30 | 1 | invalid syntax | `from ..sql import schema` |
| 2164 | venv_creative/lib/python3.13/site-packages/sqlalchemy/testing/assertions.py | 76 | 8 | unexpected indent | `def decorate(fn, *args, **kw):` |
| 2165 | venv_creative/lib/python3.13/site-packages/sqlalchemy/testing/profiling.py | 71 | 13 | invalid syntax. Perhaps you forgot a comma? | `config.options is not None and config.options.force_write_profiles` |
| 2166 | venv_creative/lib/python3.13/site-packages/sqlalchemy/testing/plugin/pytestplugin.py | 81 | 17 | invalid syntax | `def __call__(` |
| 2167 | venv_creative/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_results.py | 43 | 5 | invalid syntax | `@classmethod` |
| 2168 | venv_creative/lib/python3.13/site-packages/sqlalchemy/testing/suite/test_dialect.py | 18 | 1 | invalid syntax | `from ..assertions import expect_raises, expect_raises_message` |
| 2169 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/asyncpg.py | 208 | 1 | invalid syntax | `from .types import BIT, BYTEA, CITEXT` |
| 2170 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/psycopg.py | 121 | 1 | invalid syntax | `from .base import INTERVAL, REGCONFIG, PGCompiler, PGIdentifierPreparer` |
| 2171 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/psycopg2.py | 526 | 1 | invalid syntax | `from .base import PGIdentifierPreparer` |
| 2172 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/postgresql/named_types.py | 106 | 64 | invalid syntax | `) and not self._check_for_name_in_memos(checkfirst, kw):` |
| 2173 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/oracledb.py | 646 | 1 | invalid syntax | `from ...engine import default` |
| 2174 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/oracle/base.py | 3690 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 3684 | `}` |
| 2175 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/aiosqlite.py | 89 | 1 | invalid syntax | `from ... import pool, util` |
| 2176 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/sqlite/pysqlite.py | 465 | 28 | invalid syntax. Perhaps you forgot a comma? | `description_encoding = None` |
| 2177 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/asyncmy.py | 41 | 1 | invalid syntax | `from ...util.concurrency import await_fallback, await_only` |
| 2178 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/aiomysql.py | 43 | 1 | invalid syntax | `from ...util.concurrency import await_fallback, await_only` |
| 2179 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/reflection.py | 15 | 1 | invalid syntax | `from ... import types as sqltypes` |
| 2180 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/mariadbconnector.py | 47 | 5 | invalid syntax | `from ...engine.url import URL` |
| 2181 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/types.py | 47 | 1 | invalid syntax | `class _FloatType(_NumericType, sqltypes.Float[Union[decimal.Decimal, float]]):` |
| 2182 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/mysqldb.py | 102 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 2183 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/pymysql.py | 66 | 5 | invalid syntax | `from ...engine.url import URL` |
| 2184 | venv_creative/lib/python3.13/site-packages/sqlalchemy/dialects/mysql/base.py | 2285 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 2276 | `):` |
| 2185 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/loading.py | 649 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 644 | `}` |
| 2186 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/query.py | 196 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 190 | `):` |
| 2187 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/attributes.py | 27 | 1 | invalid syntax | `from .. import event, exc, inspection, util` |
| 2188 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/strategies.py | 1782 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 1776 | `},` |
| 2189 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/mapper.py | 216 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 194 | `):` |
| 2190 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/context.py | 141 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 133 | `):` |
| 2191 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/collections.py | 128 | 1 | invalid syntax | `from .. import exc as sa_exc` |
| 2192 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/_orm_constructors.py | 127 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 98 | `) -> MappedColumn[Any]:` |
| 2193 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/descriptor_props.py | 220 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 207 | `):` |
| 2194 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/decl_api.py | 630 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 624 | `) -> None:` |
| 2195 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/bulk_persistence.py | 1566 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 1561 | `}` |
| 2196 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/state_changes.py | 73 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 67 | `) -> Callable[[_F], _F]:` |
| 2197 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/unitofwork.py | 29 | 8 | unexpected indent | `from .interfaces import MapperProperty` |
| 2198 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/base.py | 20 | 1 | invalid syntax | `from .. import exc as sa_exc` |
| 2199 | venv_creative/lib/python3.13/site-packages/sqlalchemy/orm/relationships.py | 398 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 380 | `):` |
| 2200 | venv_creative/lib/python3.13/site-packages/sqlalchemy/engine/interfaces.py | 19 | 1 | invalid syntax | `from .. import util` |
| 2201 | venv_creative/lib/python3.13/site-packages/sqlalchemy/engine/util.py | 39 | 8 | unexpected indent | `def decorated(fn, self, connection):  # type: ignore` |
| 2202 | venv_creative/lib/python3.13/site-packages/sqlalchemy/engine/reflection.py | 1821 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 1810 | `}` |
| 2203 | venv_creative/lib/python3.13/site-packages/sqlalchemy/engine/result.py | 2606 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 2598 | `):` |
| 2204 | venv_creative/lib/python3.13/site-packages/sqlalchemy/engine/default.py | 1008 | 25 | closing parenthesis '}' does not match opening parenthesis '(' on line 999 | `}` |
| 2205 | venv_creative/lib/python3.13/site-packages/sqlalchemy/engine/processors.py | 33 | 8 | unexpected indent | `from sqlalchemy.cyextension.processors import \` |
| 2206 | venv_creative/lib/python3.13/site-packages/sqlalchemy/engine/base.py | 18 | 1 | invalid syntax | `from .. import exc, inspection, log, util` |
| 2207 | venv_creative/lib/python3.13/site-packages/sqlalchemy/engine/cursor.py | 229 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 216 | `}` |
| 2208 | venv_creative/lib/python3.13/site-packages/sqlalchemy/pool/impl.py | 27 | 1 | invalid syntax | `if typing.TYPE_CHECKING:` |
| 2209 | venv_creative/lib/python3.13/site-packages/sqlalchemy/pool/base.py | 1017 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 1009 | `) -> None:` |
| 2210 | venv_creative/lib/python3.13/site-packages/sqlalchemy/event/registry.py | 28 | 1 | invalid syntax | `from .. import exc, util` |
| 2211 | venv_creative/lib/python3.13/site-packages/sqlalchemy/sql/compiler.py | 1899 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 1879 | `}` |
| 2212 | venv_creative/lib/python3.13/site-packages/sqlalchemy/sql/visitors.py | 23 | 1 | invalid syntax | `from .. import exc, util` |
| 2213 | venv_creative/lib/python3.13/site-packages/sqlalchemy/sql/events.py | 19 | 8 | unexpected indent | `from .schema import Column, Constraint, SchemaItem, Table` |
| 2214 | venv_creative/lib/python3.13/site-packages/sqlalchemy/sql/elements.py | 1037 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 1032 | `) -> BinaryExpression[bool]: ...` |
| 2215 | venv_creative/lib/python3.13/site-packages/sqlalchemy/sql/sqltypes.py | 22 | 1 | invalid syntax | `from uuid import UUID as _python_UUID` |
| 2216 | venv_creative/lib/python3.13/site-packages/sqlalchemy/sql/selectable.py | 1518 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1513 | `) -> ColumnElement[bool]:` |
| 2217 | venv_creative/lib/python3.13/site-packages/sqlalchemy/sql/coercions.py | 229 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 220 | `) -> ColumnElement[_T]: ...` |
| 2218 | venv_creative/lib/python3.13/site-packages/sqlalchemy/sql/base.py | 230 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 225 | `) -> Iterator[FromClause]:` |
| 2219 | venv_creative/lib/python3.13/site-packages/sqlalchemy/sql/type_api.py | 19 | 1 | invalid syntax | `from .. import exc, util` |
| 2220 | venv_creative/lib/python3.13/site-packages/shellingham/posix/__init__.py | 39 | 1 | invalid syntax | `def _iter_process_parents(pid, max_depth = 10):` |
| 2221 | venv_creative/lib/python3.13/site-packages/regex/test_regex.py | 952 | 43 | too many nested parentheses | `self.assertEqual(bool(regex.search(r"(?iV1)f\uFB03",` |
| 2222 | venv_creative/lib/python3.13/site-packages/outcome/_impl.py | 9 | 1 | invalid syntax | `import attr` |
| 2223 | venv_creative/lib/python3.13/site-packages/numpy/__init__.py | 176 | 5 | invalid syntax | `for ta in ["float96", "float128", "complex192", "complex256"]:` |
| 2224 | venv_creative/lib/python3.13/site-packages/numpy/ctypeslib.py | 57 | 1 | invalid syntax | `import os` |
| 2225 | venv_creative/lib/python3.13/site-packages/numpy/core/_multiarray_umath.py | 8 | 32 | unindent does not match any outer indentation level | `if isinstance(attr, ufunc):` |
| 2226 | venv_creative/lib/python3.13/site-packages/numpy/linalg/tests/test_linalg.py | 18 | 1 | invalid syntax | `from numpy._core import swapaxes` |
| 2227 | venv_creative/lib/python3.13/site-packages/numpy/ma/core.py | 80 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `MaskType = np.bool` |
| 2228 | venv_creative/lib/python3.13/site-packages/numpy/ma/timer_comparison.py | 32 | 12 | unexpected indent | `self.nomask = module.nomask` |
| 2229 | venv_creative/lib/python3.13/site-packages/numpy/ma/tests/test_core.py | 992 | 48 | closing parenthesis ')' does not match opening parenthesis '[' on line 988 | `0.0),` |
| 2230 | venv_creative/lib/python3.13/site-packages/numpy/ma/tests/test_subclassing.py | 15 | 1 | invalid syntax | `from numpy.ma.testutils import assert_equal` |
| 2231 | venv_creative/lib/python3.13/site-packages/numpy/ma/tests/test_mrecords.py | 550 | 41 | invalid decimal literal | `assert_equal(mrectxt.C, [1, 2, 3.e + 5, -1e-10])` |
| 2232 | venv_creative/lib/python3.13/site-packages/numpy/_core/records.py | 22 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `ndarray = sb.ndarray` |
| 2233 | venv_creative/lib/python3.13/site-packages/numpy/_core/memmap.py | 255 | 9 | invalid syntax | `with f_ctx as fid:` |
| 2234 | venv_creative/lib/python3.13/site-packages/numpy/_core/numeric.py | 2423 | 28 | invalid decimal literal | `def allclose(a, b, rtol = 1.e - 5, atol = 1.e - 8, equal_nan = False):` |
| 2235 | venv_creative/lib/python3.13/site-packages/numpy/_core/einsumfunc.py | 201 | 58 | invalid syntax. Perhaps you forgot a comma? | `idx_contract, idx_removed, len(con), idx_dict` |
| 2236 | venv_creative/lib/python3.13/site-packages/numpy/_core/numerictypes.py | 90 | 9 | invalid syntax | `__all__ = [` |
| 2237 | venv_creative/lib/python3.13/site-packages/numpy/_core/arrayprint.py | 11 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `__docformat__ = 'restructuredtext'` |
| 2238 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_scalar_methods.py | 107 | 41 | closing parenthesis ')' does not match opening parenthesis '[' on line 103 | `[0, 1, 0, -8, 12]),` |
| 2239 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_scalarmath.py | 22 | 7 | invalid syntax | `types = [np.bool, np.byte, np.ubyte, np.short, np.ushort, np.intc, np.uintc,` |
| 2240 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_array_coercion.py | 181 | 5 | invalid syntax | `def test_basic_stringlength(self, obj):` |
| 2241 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_arrayprint.py | 14 | 1 | invalid syntax | `from numpy.testing._private.utils import run_threaded` |
| 2242 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_half.py | 17 | 5 | invalid syntax | `else:` |
| 2243 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_shape_base.py | 7 | 1 | invalid syntax | `from numpy._core.shape_base import (_block_concatenate, _block_dispatcher, _block_setup,` |
| 2244 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_deprecations.py | 19 | 1 | invalid syntax | `try:` |
| 2245 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_simd.py | 141 | 16 | unexpected indent | `return ' '.join(target)` |
| 2246 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_scalarinherit.py | 90 | 30 | unindent does not match any outer indentation level | `np_u = np.str_('abc')` |
| 2247 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_indexing.py | 18 | 1 | invalid syntax | `class TestIndexing:` |
| 2248 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_umath.py | 724 | 24 | invalid decimal literal | `x = np.array([1.e + 110, 1.e - 110], dtype = np.complex128)` |
| 2249 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_numeric.py | 4831 | 38 | too many nested parentheses | `np.broadcast(np.broadcast(*arrs[:0]), np.broadcast(*arrs[0:])),` |
| 2250 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_datetime.py | 2074 | 26 | too many nested parentheses | `np.array(['+1980 - 02 - 29T01:02:03'], np.dtype('M8[s]')),` |
| 2251 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_custom_dtypes.py | 197 | 5 | invalid syntax | `def test_addition_cast_safety(self):` |
| 2252 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_scalarprint.py | 17 | 1 | invalid syntax | `class TestRealScalars:` |
| 2253 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_casting_unittests.py | 236 | 9 | invalid syntax | `else:` |
| 2254 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_ufunc.py | 21 | 1 | invalid syntax | `from numpy.testing._private.utils import requires_memory` |
| 2255 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_getlimits.py | 74 | 1 | invalid syntax | `def assert_iinfo_equal(i1, i2):` |
| 2256 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_einsum.py | 12 | 7 | invalid syntax | `chars = 'abcdefghij'` |
| 2257 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_longdouble.py | 12 | 9 | invalid syntax | `LD_INFO = np.finfo(np.longdouble)` |
| 2258 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_multiarray.py | 5445 | 40 | too many nested parentheses | `@pytest.mark.parametrize('method', ['max', 'min'])` |
| 2259 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_nditer.py | 2286 | 42 | too many nested parentheses | `assert_raises(ValueError, lambda i: i[0], i)` |
| 2260 | venv_creative/lib/python3.13/site-packages/numpy/_core/tests/test_regression.py | 3087 | 67 | invalid decimal literal | `buf = np.array([-5.171866611150749e-07 + 2.5618634555957426e - 07j,` |
| 2261 | venv_creative/lib/python3.13/site-packages/numpy/tests/test_warnings.py | 51 | 54 | invalid syntax | `len(p.ls) == 1 or p.ls[-2] == 'warnings'):` |
| 2262 | venv_creative/lib/python3.13/site-packages/numpy/f2py/cfuncs.py | 95 | 1 | cannot assign to subscript here. Maybe you meant '==' instead of '='? | `typedefs['complex_float'] = 'typedef struct {float r,i;} complex_float;'` |
| 2263 | venv_creative/lib/python3.13/site-packages/numpy/f2py/crackfortran.py | 270 | 5 | cannot assign to subscript here. Maybe you meant '==' instead of '='? | `badnames[n] = n + '_bn'` |
| 2264 | venv_creative/lib/python3.13/site-packages/numpy/f2py/symbolic.py | 200 | 13 | invalid syntax | `assert isinstance(data[1], (int, str)), data` |
| 2265 | venv_creative/lib/python3.13/site-packages/numpy/f2py/auxfuncs.py | 45 | 32 | invalid syntax. Perhaps you forgot a comma? | `'process_f2cmap_dict', 'containscommon'` |
| 2266 | venv_creative/lib/python3.13/site-packages/numpy/f2py/tests/test_parameter.py | 9 | 15 | '[' was never closed | `sources = [` |
| 2267 | venv_creative/lib/python3.13/site-packages/numpy/f2py/tests/test_regression.py | 21 | 54 | unindent does not match any outer indentation level | `pytest.raises(ValueError, self.module.foo, x)` |
| 2268 | venv_creative/lib/python3.13/site-packages/numpy/testing/tests/test_utils.py | 23 | 1 | invalid syntax | `class _GenericTest:` |
| 2269 | venv_creative/lib/python3.13/site-packages/numpy/testing/_private/utils.py | 52 | 1 | invalid syntax | `class KnownFailureException(Exception):` |
| 2270 | venv_creative/lib/python3.13/site-packages/numpy/lib/_user_array_impl.py | 17 | 1 | invalid syntax | `from numpy._core.overrides import set_module` |
| 2271 | venv_creative/lib/python3.13/site-packages/numpy/lib/_histograms_impl.py | 24 | 1 | invalid syntax | `def _ptp(x):` |
| 2272 | venv_creative/lib/python3.13/site-packages/numpy/lib/_arraypad_impl.py | 113 | 5 | invalid syntax | `order = 'F' if array.flags.fnc else 'C'  # Fortran and not also C - order` |
| 2273 | venv_creative/lib/python3.13/site-packages/numpy/lib/_npyio_impl.py | 31 | 9 | invalid syntax | `__all__ = [` |
| 2274 | venv_creative/lib/python3.13/site-packages/numpy/lib/_function_base_impl.py | 22 | 1 | invalid syntax | `from numpy._core.numerictypes import typecodes` |
| 2275 | venv_creative/lib/python3.13/site-packages/numpy/lib/_datasource.py | 482 | 12 | unexpected indent | `from urllib.request import urlopen` |
| 2276 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_type_check.py | 528 | 31 | invalid decimal literal | `b = real_if_close(a + 1e - 15j)` |
| 2277 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_shape_base.py | 11 | 1 | invalid syntax | `from numpy.exceptions import AxisError` |
| 2278 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_arrayterator.py | 31 | 8 | unexpected indent | `start = [randint(dim) for dim in shape]` |
| 2279 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_io.py | 2930 | 29 | too many nested parentheses | `control = np.array([(0, 1), (2, 3)],` |
| 2280 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_function_base.py | 3124 | 15 | too many nested parentheses | `i0(B),` |
| 2281 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_arraypad.py | 10 | 5 | invalid syntax. Perhaps you forgot a comma? | `np._core.sctypes["uint"]` |
| 2282 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_stride_tricks.py | 9 | 1 | invalid syntax | `from numpy.testing import (assert_, assert_array_equal, assert_equal, assert_raises,` |
| 2283 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_loadtxt.py | 806 | 73 | invalid decimal literal | `("float32", 9.2557e-41), ("complex64", 9.2557e-41 + 2.8622554e - 29j),` |
| 2284 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_format.py | 677 | 31 | closing parenthesis ')' does not match opening parenthesis '[' on line 671 | `(3,)),` |
| 2285 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_histograms.py | 12 | 1 | invalid syntax | `class TestHistogram:` |
| 2286 | venv_creative/lib/python3.13/site-packages/numpy/lib/tests/test_regression.py | 10 | 1 | invalid syntax | `class TestRegression:` |
| 2287 | venv_creative/lib/python3.13/site-packages/numpy/fft/tests/test_helper.py | 39 | 9 | invalid syntax. Perhaps you forgot a comma? | `assert_array_almost_equal(fft.ifftshift(shifted, axes=(0, 1)), freqs)` |
| 2288 | venv_creative/lib/python3.13/site-packages/numpy/random/_pickle.py | 33 | 12 | unexpected indent | `elif bit_generator in BitGenerators:` |
| 2289 | venv_creative/lib/python3.13/site-packages/numpy/random/tests/test_generator_mt19937.py | 1848 | 28 | too many nested parentheses | `desired = np.array([0.233278563284287, 9.424140804347195])` |
| 2290 | venv_creative/lib/python3.13/site-packages/numpy/random/tests/test_randomstate.py | 16 | 11 | invalid syntax | `INT_FUNCS = {'binomial': (100.0, 0.6),` |
| 2291 | venv_creative/lib/python3.13/site-packages/numpy/random/tests/test_direct.py | 11 | 1 | invalid syntax | `from numpy.random._common import interface` |
| 2292 | venv_creative/lib/python3.13/site-packages/more_itertools/more.py | 13 | 1 | invalid syntax | `from math import ceil, comb, e, exp, factorial, floor, fsum, log, log1p, perm, tau` |
| 2293 | venv_creative/lib/python3.13/site-packages/more_itertools/recipes.py | 21 | 1 | invalid syntax | `from math import comb, gcd, isqrt, prod` |
| 2294 | venv_creative/lib/python3.13/site-packages/antlr4/ListTokenSource.py | 49 | 12 | unexpected indent | `self._factory = CommonTokenFactory.DEFAULT` |
| 2295 | venv_creative/lib/python3.13/site-packages/antlr4/ParserRuleContext.py | 30 | 30 | '(' was never closed | `from antlr4.tree.Tree import (INVALID_INTERVAL, ErrorNodeImpl, ParseTree,` |
| 2296 | venv_creative/lib/python3.13/site-packages/antlr4/LL1Analyzer.py | 13 | 1 | invalid syntax | `from antlr4.IntervalSet import IntervalSet` |
| 2297 | venv_creative/lib/python3.13/site-packages/antlr4/PredictionContext.py | 27 | 24 | unindent does not match any outer indentation level | `globalNodeCount = 1` |
| 2298 | venv_creative/lib/python3.13/site-packages/antlr4/Lexer.py | 25 | 1 | invalid syntax | `from antlr4.InputStream import InputStream` |
| 2299 | venv_creative/lib/python3.13/site-packages/antlr4/xpath/XPath.py | 56 | 1 | invalid syntax | `from antlr4.atn.ATNDeserializer import ATNDeserializer` |
| 2300 | venv_creative/lib/python3.13/site-packages/antlr4/atn/ATNConfigSet.py | 25 | 17 | '(' was never closed | `__slots__ = (` |
| 2301 | venv_creative/lib/python3.13/site-packages/antlr4/atn/ATN.py | 13 | 17 | '(' was never closed | `__slots__ = (` |
| 2302 | venv_creative/lib/python3.13/site-packages/antlr4/atn/ATNSimulator.py | 9 | 38 | '(' was never closed | `from antlr4.PredictionContext import (PredictionContext, PredictionContextCache,` |
| 2303 | venv_creative/lib/python3.13/site-packages/antlr4/atn/LexerAction.py | 247 | 8 | unexpected indent | `def __init__(self, ruleIndex:int, actionIndex:int):` |
| 2304 | venv_creative/lib/python3.13/site-packages/antlr4/atn/ATNDeserializer.py | 86 | 1 | expected ':' | `#             and atn.grammarType == ATNType.PARSER:` |
| 2305 | venv_creative/lib/python3.13/site-packages/antlr4/atn/LexerATNSimulator.py | 37 | 1 | invalid syntax | `from antlr4.Token import Token` |
| 2306 | venv_creative/lib/python3.13/site-packages/antlr4/atn/ParserATNSimulator.py | 245 | 1 | invalid syntax | `from antlr4.atn.PredictionMode import PredictionMode` |
| 2307 | venv_creative/lib/python3.13/site-packages/antlr4/atn/ATNConfig.py | 34 | 5 | invalid syntax | `def __init__(self, state:ATNState = None, alt:int = None, context:PredictionContext = None, semantic:SemanticContext = None, config:ATNConfig = None):` |
| 2308 | venv_creative/lib/python3.13/site-packages/antlr4/error/ErrorStrategy.py | 14 | 1 | invalid syntax | `from antlr4.IntervalSet import IntervalSet` |
| 2309 | venv_creative/lib/python3.13/site-packages/PIL/ImageFile.py | 94 | 5 | invalid syntax | `raise _get_oserror(error, encoder = False)` |
| 2310 | venv_creative/lib/python3.13/site-packages/PIL/GifImagePlugin.py | 40 | 1 | invalid syntax | `from ._binary import i16le as i16` |
| 2311 | venv_creative/lib/python3.13/site-packages/PIL/ImageDraw2.py | 100 | 16 | unexpected indent | `width = pen.width` |
| 2312 | venv_creative/lib/python3.13/site-packages/PIL/ImageDraw.py | 268 | 51 | invalid syntax | `for i in range(1, len(points) - 1):` |
| 2313 | venv_creative/lib/python3.13/site-packages/PIL/TgaImagePlugin.py | 118 | 33 | invalid syntax. Perhaps you forgot a comma? | `"BGRA;15Z", bytes(2 * start) + self.fp.read(2 * size)` |
| 2314 | venv_creative/lib/python3.13/site-packages/PIL/ImageShow.py | 126 | 16 | unexpected indent | `os.system(self.get_command(path, **options))  # nosec` |
| 2315 | venv_creative/lib/python3.13/site-packages/PIL/WebPImagePlugin.py | 34 | 9 | invalid syntax | `return True` |
| 2316 | venv_creative/lib/python3.13/site-packages/PIL/TiffImagePlugin.py | 289 | 1 | invalid syntax | `if not getattr(Image.core, "libtiff_support_custom_tags", True):` |
| 2317 | venv_creative/lib/python3.13/site-packages/PIL/Image.py | 53 | 1 | invalid syntax | `from ._binary import i32le, o32be, o32le` |
| 2318 | venv_creative/lib/python3.13/site-packages/requests/models.py | 19 | 1 | invalid syntax | `from urllib3.fields import RequestField` |
| 2319 | venv_creative/lib/python3.13/site-packages/requests/utils.py | 33 | 1 | invalid syntax | `from .compat import parse_http_list as _parse_list_header` |
| 2320 | venv_creative/lib/python3.13/site-packages/anyio/_backends/_trio.py | 14 | 1 | invalid syntax | `from concurrent.futures import Future` |
| 2321 | venv_creative/lib/python3.13/site-packages/anyio/_backends/_asyncio.py | 2417 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 2412 | `) -> None:` |
| 2322 | venv_creative/lib/python3.13/site-packages/anyio/_core/_asyncio_selector_thread.py | 56 | 12 | unexpected indent | `self._closed = True` |
| 2323 | venv_creative/lib/python3.13/site-packages/anyio/streams/memory.py | 53 | 41 | invalid syntax. Perhaps you forgot a comma? | `init = False, default_factory = OrderedDict` |
| 2324 | venv_creative/lib/python3.13/site-packages/anyio/streams/file.py | 9 | 16 | '(' was never closed | `from .. import (BrokenResourceError, ClosedResourceError, EndOfStream,` |
| 2325 | venv_creative/lib/python3.13/site-packages/gradio/utils.py | 38 | 1 | invalid syntax | `from contextlib import contextmanager` |
| 2326 | venv_creative/lib/python3.13/site-packages/gradio/blocks.py | 95 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 83 | `}` |
| 2327 | venv_creative/lib/python3.13/site-packages/gradio/oauth.py | 58 | 1 | invalid syntax | `def _add_oauth_routes(app: fastapi.FastAPI) -> None:` |
| 2328 | venv_creative/lib/python3.13/site-packages/gradio/components/highlighted_text.py | 96 | 12 | unexpected indent | `self.rtl = rtl` |
| 2329 | venv_creative/lib/python3.13/site-packages/gradio/components/bar_plot.py | 83 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 49 | `):` |
| 2330 | venv_creative/lib/python3.13/site-packages/gradio/components/native_plot.py | 117 | 12 | unexpected indent | `self.title = title` |
| 2331 | venv_creative/lib/python3.13/site-packages/gradio/components/scatter_plot.py | 112 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 78 | `):` |
| 2332 | venv_creative/lib/python3.13/site-packages/gradio/components/label.py | 89 | 12 | unexpected indent | `self.show_heading = show_heading` |
| 2333 | venv_creative/lib/python3.13/site-packages/gradio/components/dialogue.py | 38 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `data_model = DialogueModel` |
| 2334 | venv_creative/lib/python3.13/site-packages/gradio/components/line_plot.py | 100 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 66 | `):` |
| 2335 | venv_creative/lib/python3.13/site-packages/gradio/_frontend_code/lite/examples/transformers_basic/run.py | 4 | 8 | 'await' outside function | `pipe = await pipeline('sentiment - analysis')` |
| 2336 | venv_creative/lib/python3.13/site-packages/gradio/themes/base.py | 2052 | 52 | too many nested parentheses | `self.loader_color = loader_color or getattr(` |
| 2337 | venv_creative/lib/python3.13/site-packages/pip/_internal/utils/subprocess.py | 55 | 1 | invalid syntax | `def reveal_command_args(args: list[str] ¦ CommandArgs) -> list[str]:` |
| 2338 | venv_creative/lib/python3.13/site-packages/pip/_internal/utils/wheel.py | 41 | 8 | unexpected indent | `subdirs = {p.split("/", 1)[0] for p in source.namelist()}` |
| 2339 | venv_creative/lib/python3.13/site-packages/pip/_internal/utils/unpacking.py | 20 | 1 | invalid syntax | `from pip._internal.utils.misc import ensure_dir` |
| 2340 | venv_creative/lib/python3.13/site-packages/pip/_internal/cli/parser.py | 218 | 21 | invalid syntax | `continue` |
| 2341 | venv_creative/lib/python3.13/site-packages/pip/_internal/cli/autocompletion.py | 38 | 8 | unexpected indent | `subcommand_name: str ¦ None = None` |
| 2342 | venv_creative/lib/python3.13/site-packages/pip/_internal/operations/install/wheel.py | 30 | 1 | invalid syntax | `from pip._internal.models.direct_url import DIRECT_URL_METADATA_NAME, DirectUrl` |
| 2343 | venv_creative/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/reporter.py | 54 | 16 | unexpected indent | `msg += "\n    "` |
| 2344 | venv_creative/lib/python3.13/site-packages/pip/_internal/resolution/resolvelib/resolver.py | 22 | 1 | invalid syntax | `from pip._internal.utils.packaging import get_requirement` |
| 2345 | venv_creative/lib/python3.13/site-packages/pip/_internal/index/sources.py | 20 | 8 | invalid syntax | `logger = logging.getLogger(__name__)` |
| 2346 | venv_creative/lib/python3.13/site-packages/pip/_internal/index/package_finder.py | 18 | 1 | invalid syntax | `from pip._internal.index.collector import LinkCollector, parse_links` |
| 2347 | venv_creative/lib/python3.13/site-packages/pip/_internal/commands/configuration.py | 15 | 1 | invalid syntax | `from pip._internal.exceptions import PipError` |
| 2348 | venv_creative/lib/python3.13/site-packages/pip/_internal/commands/list.py | 102 | 9 | invalid syntax. Perhaps you forgot a comma? | `self.cmd_opts.add_option(cmdoptions.list_path())` |
| 2349 | venv_creative/lib/python3.13/site-packages/pip/_internal/commands/cache.py | 56 | 5 | positional argument follows keyword argument | `def handler_map(self) -> dict[str, Callable[[Values, list[str]], None]]:` |
| 2350 | venv_creative/lib/python3.13/site-packages/pip/_internal/commands/help.py | 17 | 44 | '(' was never closed | `from pip._internal.commands import (commands_dict, create_command,` |
| 2351 | venv_creative/lib/python3.13/site-packages/pip/_vendor/packaging/_manylinux.py | 48 | 1 | invalid syntax | `def _is_linux_i686(executable: str) -> bool:` |
| 2352 | venv_creative/lib/python3.13/site-packages/pip/_vendor/packaging/specifiers.py | 249 | 5 | invalid syntax | `def __init__(self, spec: str = "", prereleases: bool ¦ None = None) -> None:` |
| 2353 | venv_creative/lib/python3.13/site-packages/pip/_vendor/truststore/_windows.py | 10 | 1 | invalid syntax | `from ctypes.wintypes import (BOOL, DWORD, HANDLE, LONG, LPCSTR, LPCVOID, LPCWSTR,` |
| 2354 | venv_creative/lib/python3.13/site-packages/pip/_vendor/msgpack/fallback.py | 97 | 12 | unexpected indent | `if unpacker._got_extradata():` |
| 2355 | venv_creative/lib/python3.13/site-packages/pip/_vendor/pygments/style.py | 137 | 16 | unexpected indent | `color = _ansimap[color]` |
| 2356 | venv_creative/lib/python3.13/site-packages/pip/_vendor/pygments/filters/__init__.py | 20 | 1 | invalid syntax | `from pip._vendor.pygments.util import (ClassNotFound, OptionError, get_bool_opt,` |
| 2357 | venv_creative/lib/python3.13/site-packages/pip/_vendor/distlib/compat.py | 22 | 8 | unexpected indent | `text_type = unicode` |
| 2358 | venv_creative/lib/python3.13/site-packages/pip/_vendor/distlib/util.py | 43 | 8 | invalid syntax | `logger = logging.getLogger(__name__)` |
| 2359 | venv_creative/lib/python3.13/site-packages/pip/_vendor/distlib/scripts.py | 23 | 8 | invalid syntax | `logger = logging.getLogger(__name__)` |
| 2360 | venv_creative/lib/python3.13/site-packages/pip/_vendor/distro/distro.py | 45 | 1 | invalid syntax | `try:` |
| 2361 | venv_creative/lib/python3.13/site-packages/pip/_vendor/requests/models.py | 19 | 1 | invalid syntax | `from pip._vendor.urllib3.fields import RequestField` |
| 2362 | venv_creative/lib/python3.13/site-packages/pip/_vendor/requests/utils.py | 33 | 1 | invalid syntax | `from .compat import parse_http_list as _parse_list_header` |
| 2363 | venv_creative/lib/python3.13/site-packages/pip/_vendor/pyproject_hooks/_impl.py | 123 | 8 | unexpected indent | `norm_source = os.path.normcase(abs_source)` |
| 2364 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/logging.py | 65 | 22 | invalid syntax | `HIGHLIGHTER_CLASS: ClassVar[Type[Highlighter]] = ReprHighlighter` |
| 2365 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/console.py | 687 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 655 | `):` |
| 2366 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/color.py | 303 | 1 | invalid syntax | `@rich_repr` |
| 2367 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/style.py | 86 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_style_map = {` |
| 2368 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/traceback.py | 599 | 25 | closing parenthesis '}' does not match opening parenthesis '(' on line 590 | `}` |
| 2369 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/palette.py | 25 | 12 | unexpected indent | `from pip._vendor.rich.style import Style` |
| 2370 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/pretty.py | 1079 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 1069 | `),` |
| 2371 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/columns.py | 49 | 12 | unexpected indent | `self.equal = equal` |
| 2372 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/syntax.py | 14 | 1 | invalid syntax | `from pip._vendor.pygments.lexer import Lexer` |
| 2373 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/table.py | 7 | 1 | invalid syntax | `from . import box, errors` |
| 2374 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/segment.py | 11 | 1 | invalid syntax | `from .cells import (_is_single_cell_widths, cached_cell_len, cell_len,` |
| 2375 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/progress.py | 23 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 2376 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/_win32_console.py | 71 | 1 | invalid syntax | `class CONSOLE_CURSOR_INFO(ctypes.Structure):` |
| 2377 | venv_creative/lib/python3.13/site-packages/pip/_vendor/rich/panel.py | 67 | 12 | unexpected indent | `self.style = style` |
| 2378 | venv_creative/lib/python3.13/site-packages/pip/_vendor/tomli_w/_writer.py | 10 | 8 | unexpected indent | `from decimal import Decimal` |
| 2379 | venv_creative/lib/python3.13/site-packages/pip/_vendor/urllib3/response.py | 22 | 1 | invalid syntax | `from .packages import six` |
| 2380 | venv_creative/lib/python3.13/site-packages/pip/_vendor/urllib3/connectionpool.py | 18 | 1 | invalid syntax | `from .exceptions import (ClosedPoolError, EmptyPoolError, HeaderParsingError,` |
| 2381 | venv_creative/lib/python3.13/site-packages/pip/_vendor/urllib3/util/wait.py | 65 | 22 | unindent does not match any outer indentation level | `else:` |
| 2382 | venv_creative/lib/python3.13/site-packages/pip/_vendor/urllib3/util/retry.py | 15 | 1 | invalid syntax | `from ..packages import six` |
| 2383 | venv_creative/lib/python3.13/site-packages/pip/_vendor/urllib3/packages/six.py | 254 | 12 | unexpected indent | `return None` |
| 2384 | venv_creative/lib/python3.13/site-packages/pip/_vendor/pkg_resources/__init__.py | 66 | 1 | invalid syntax | `import _imp` |
| 2385 | venv_creative/lib/python3.13/site-packages/pip/_vendor/resolvelib/structs.py | 10 | 4 | invalid syntax | `KT = TypeVar("KT")  # Identifier.` |
| 2386 | venv_creative/lib/python3.13/site-packages/pip/_vendor/platformdirs/api.py | 12 | 8 | unexpected indent | `from typing import Literal` |
| 2387 | venv_creative/lib/python3.13/site-packages/pip/_vendor/platformdirs/windows.py | 239 | 12 | unexpected indent | `import winreg  # noqa: PLC0415` |
| 2388 | venv_creative/lib/python3.13/site-packages/imageio/v2.py | 44 | 13 | invalid syntax. Perhaps you forgot a comma? | `"Memory size could not be parsed "` |
| 2389 | venv_creative/lib/python3.13/site-packages/imageio/core/request.py | 262 | 21 | invalid syntax. Perhaps you forgot a comma? | `"`extension` should be a file extension starting with a `.`,"` |
| 2390 | venv_creative/lib/python3.13/site-packages/imageio/core/imopen.py | 12 | 1 | invalid syntax | `def imopen(` |
| 2391 | venv_creative/lib/python3.13/site-packages/imageio/plugins/_tifffile.py | 417 | 1 | invalid syntax | `def imread(files, **kwargs):` |
| 2392 | venv_creative/lib/python3.13/site-packages/imageio/plugins/_freeimage.py | 333 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 325 | `}` |
| 2393 | venv_creative/lib/python3.13/site-packages/imageio/plugins/ffmpeg.py | 172 | 1 | invalid syntax | `def get_exe():  # pragma: no cover` |
| 2394 | venv_creative/lib/python3.13/site-packages/imageio/plugins/_swf.py | 319 | 12 | unexpected indent | `bb += int2uint32(len(self.bytes))` |
| 2395 | venv_creative/lib/python3.13/site-packages/imageio/plugins/pillowmulti.py | 47 | 21 | invalid syntax. Perhaps you forgot a comma? | `f"Pillow v{pillow_version} is not supported by ImageIO's legacy "` |
| 2396 | venv_creative/lib/python3.13/site-packages/imageio/plugins/_bsdf.py | 62 | 8 | unexpected indent | `text_type = unicode  # noqa` |
| 2397 | venv_creative/lib/python3.13/site-packages/imageio/plugins/_dicom.py | 273 | 65 | invalid syntax. Perhaps you forgot a comma? | `self._unpackPrefix + "HH", SequenceDelimiterTag[0], SequenceDelimiterTag[1]` |
| 2398 | venv_creative/lib/python3.13/site-packages/imageio/plugins/dicom.py | 184 | 33 | invalid syntax. Perhaps you forgot a comma? | `"DICOM file contained compressed data. "` |
| 2399 | venv_creative/lib/python3.13/site-packages/socketio/server.py | 175 | 5 | invalid syntax | `def send(self, data, to = None, room = None, skip_sid = None, namespace = None,` |
| 2400 | venv_creative/lib/python3.13/site-packages/socketio/base_client.py | 36 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `reason = engineio.Client.reason` |
| 2401 | venv_creative/lib/python3.13/site-packages/socketio/async_redis_manager.py | 11 | 12 | unexpected indent | `except ImportError:` |
| 2402 | venv_creative/lib/python3.13/site-packages/socketio/async_server.py | 124 | 5 | invalid syntax | `def is_asyncio_based(self):` |
| 2403 | venv_creative/lib/python3.13/site-packages/sklearn/multiclass.py | 1272 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 1263 | `}` |
| 2404 | venv_creative/lib/python3.13/site-packages/sklearn/multioutput.py | 706 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 696 | `}` |
| 2405 | venv_creative/lib/python3.13/site-packages/sklearn/naive_bayes.py | 1418 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 1410 | `}` |
| 2406 | venv_creative/lib/python3.13/site-packages/sklearn/pipeline.py | 560 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 555 | `}` |
| 2407 | venv_creative/lib/python3.13/site-packages/sklearn/exceptions.py | 23 | 1 | invalid syntax | `class UnsetMetadataPassedError(ValueError):` |
| 2408 | venv_creative/lib/python3.13/site-packages/sklearn/calibration.py | 258 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 247 | `}` |
| 2409 | venv_creative/lib/python3.13/site-packages/sklearn/tree/_export.py | 46 | 12 | unexpected indent | `rgb = [` |
| 2410 | venv_creative/lib/python3.13/site-packages/sklearn/tree/_reingold_tilford.py | 14 | 25 | '[' was never closed | `self.children = [` |
| 2411 | venv_creative/lib/python3.13/site-packages/sklearn/tree/tests/test_tree.py | 30 | 1 | invalid syntax | `from sklearn.tree._classes import (CRITERIA_CLF, CRITERIA_REG, DENSE_SPLITTERS,` |
| 2412 | venv_creative/lib/python3.13/site-packages/sklearn/tree/tests/test_export.py | 21 | 3 | invalid syntax | `X = [[-2, -1], [-1, -1], [-1, -2], [1, 1], [1, 2], [2, 1]]` |
| 2413 | venv_creative/lib/python3.13/site-packages/sklearn/metrics/_regression.py | 1081 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 1074 | `},` |
| 2414 | venv_creative/lib/python3.13/site-packages/sklearn/metrics/_ranking.py | 28 | 1 | invalid syntax | `from ..utils._encode import _encode, _unique` |
| 2415 | venv_creative/lib/python3.13/site-packages/sklearn/metrics/cluster/tests/test_supervised.py | 16 | 1 | invalid syntax | `from sklearn.metrics.cluster._supervised import _generalized_average, check_clusterings` |
| 2416 | venv_creative/lib/python3.13/site-packages/sklearn/metrics/cluster/tests/test_unsupervised.py | 13 | 1 | invalid syntax | `from sklearn.metrics.cluster._unsupervised import _silhouette_reduce` |
| 2417 | venv_creative/lib/python3.13/site-packages/sklearn/metrics/_plot/tests/test_common_curve_display.py | 14 | 1 | invalid syntax | `from sklearn.pipeline import make_pipeline` |
| 2418 | venv_creative/lib/python3.13/site-packages/sklearn/metrics/tests/test_common.py | 1479 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1473 | `),` |
| 2419 | venv_creative/lib/python3.13/site-packages/sklearn/metrics/tests/test_score_objects.py | 18 | 1 | invalid syntax | `from sklearn.linear_model import LogisticRegression, Perceptron, Ridge` |
| 2420 | venv_creative/lib/python3.13/site-packages/sklearn/metrics/tests/test_ranking.py | 2457 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 2447 | `),` |
| 2421 | venv_creative/lib/python3.13/site-packages/sklearn/metrics/tests/test_regression.py | 19 | 1 | invalid syntax | `from sklearn.metrics._regression import _check_reg_targets` |
| 2422 | venv_creative/lib/python3.13/site-packages/sklearn/ensemble/_base.py | 37 | 19 | invalid syntax | `) from exc` |
| 2423 | venv_creative/lib/python3.13/site-packages/sklearn/ensemble/_stacking.py | 653 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 648 | `}` |
| 2424 | venv_creative/lib/python3.13/site-packages/sklearn/ensemble/tests/test_common.py | 36 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 28 | `),` |
| 2425 | venv_creative/lib/python3.13/site-packages/sklearn/ensemble/tests/test_bagging.py | 121 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 102 | `),` |
| 2426 | venv_creative/lib/python3.13/site-packages/sklearn/ensemble/tests/test_stacking.py | 352 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 345 | `},` |
| 2427 | venv_creative/lib/python3.13/site-packages/sklearn/ensemble/tests/test_weight_boosting.py | 324 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 314 | `),` |
| 2428 | venv_creative/lib/python3.13/site-packages/sklearn/ensemble/tests/test_gradient_boosting.py | 32 | 1 | invalid syntax | `from sklearn.utils.fixes import COO_CONTAINERS, CSC_CONTAINERS, CSR_CONTAINERS` |
| 2429 | venv_creative/lib/python3.13/site-packages/sklearn/ensemble/_hist_gradient_boosting/gradient_boosting.py | 171 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 156 | `}` |
| 2430 | venv_creative/lib/python3.13/site-packages/sklearn/ensemble/_hist_gradient_boosting/tests/test_gradient_boosting.py | 18 | 1 | invalid syntax | `from sklearn.base import BaseEstimator, TransformerMixin, clone, is_regressor` |
| 2431 | venv_creative/lib/python3.13/site-packages/sklearn/cluster/_optics.py | 272 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 261 | `}` |
| 2432 | venv_creative/lib/python3.13/site-packages/sklearn/cluster/_dbscan.py | 351 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 340 | `}` |
| 2433 | venv_creative/lib/python3.13/site-packages/sklearn/cluster/_kmeans.py | 891 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 881 | `}` |
| 2434 | venv_creative/lib/python3.13/site-packages/sklearn/cluster/_birch.py | 16 | 1 | invalid syntax | `from ..exceptions import ConvergenceWarning` |
| 2435 | venv_creative/lib/python3.13/site-packages/sklearn/cluster/tests/test_dbscan.py | 32 | 59 | invalid syntax. Perhaps you forgot a comma? | `D, metric="precomputed", eps = eps, min_samples = min_samples` |
| 2436 | venv_creative/lib/python3.13/site-packages/sklearn/cluster/tests/test_birch.py | 28 | 5 | invalid syntax | `assert n_samples_leaves == X.shape[0]` |
| 2437 | venv_creative/lib/python3.13/site-packages/sklearn/cluster/tests/test_hierarchical.py | 23 | 1 | invalid syntax | `from sklearn.cluster._hierarchical_fast import (average_merge, max_merge,` |
| 2438 | venv_creative/lib/python3.13/site-packages/sklearn/cluster/tests/test_spectral.py | 39 | 1 | invalid syntax | `@pytest.mark.parametrize("csr_container", CSR_CONTAINERS)` |
| 2439 | venv_creative/lib/python3.13/site-packages/sklearn/feature_extraction/_dict_vectorizer.py | 113 | 12 | unexpected indent | `self.sparse = sparse` |
| 2440 | venv_creative/lib/python3.13/site-packages/sklearn/feature_extraction/text.py | 1234 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 1224 | `}` |
| 2441 | venv_creative/lib/python3.13/site-packages/sklearn/feature_extraction/tests/test_text.py | 22 | 1 | invalid syntax | `from sklearn.model_selection import GridSearchCV, cross_val_score, train_test_split` |
| 2442 | venv_creative/lib/python3.13/site-packages/sklearn/semi_supervised/_label_propagation.py | 141 | 12 | unexpected indent | `self.alpha = alpha` |
| 2443 | venv_creative/lib/python3.13/site-packages/sklearn/semi_supervised/_self_training.py | 172 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 161 | `}` |
| 2444 | venv_creative/lib/python3.13/site-packages/sklearn/semi_supervised/tests/test_self_training.py | 23 | 44 | invalid syntax. Perhaps you forgot a comma? | `iris.data, iris.target, random_state = 0` |
| 2445 | venv_creative/lib/python3.13/site-packages/sklearn/gaussian_process/tests/test_gpr.py | 25 | 1 | invalid syntax | `def f(x):` |
| 2446 | venv_creative/lib/python3.13/site-packages/sklearn/compose/_target.py | 17 | 1 | invalid syntax | `from ..utils._param_validation import HasMethods` |
| 2447 | venv_creative/lib/python3.13/site-packages/sklearn/compose/tests/test_target.py | 28 | 5 | invalid syntax | `with pytest.raises(` |
| 2448 | venv_creative/lib/python3.13/site-packages/sklearn/compose/tests/test_column_transformer.py | 166 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 160 | `).T` |
| 2449 | venv_creative/lib/python3.13/site-packages/sklearn/datasets/_samples_generator.py | 1858 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 1851 | `},` |
| 2450 | venv_creative/lib/python3.13/site-packages/sklearn/datasets/tests/test_svmlight_format.py | 18 | 1 | invalid syntax | `from sklearn.utils.fixes import CSR_CONTAINERS` |
| 2451 | venv_creative/lib/python3.13/site-packages/sklearn/datasets/tests/test_openml.py | 925 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 907 | `}` |
| 2452 | venv_creative/lib/python3.13/site-packages/sklearn/externals/_arff.py | 147 | 21 | invalid syntax. Perhaps you forgot a comma? | `__author_email__ = ('renato.ppontes@gmail.com, '` |
| 2453 | venv_creative/lib/python3.13/site-packages/sklearn/externals/array_api_compat/common/_helpers.py | 22 | 1 | invalid syntax | `from ._typing import Array, Device, HasShape, Namespace, SupportsArrayNamespace` |
| 2454 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_metaestimators.py | 80 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 70 | `),` |
| 2455 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_multioutput.py | 384 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 375 | `),` |
| 2456 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_multiclass.py | 16 | 1 | invalid syntax | `from sklearn.metrics import precision_score, recall_score` |
| 2457 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_metadata_routing.py | 29 | 1 | invalid syntax | `from sklearn.utils import metadata_routing` |
| 2458 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_calibration.py | 13 | 1 | invalid syntax | `from sklearn.datasets import load_iris, make_blobs, make_classification` |
| 2459 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_metaestimators_metadata_routing.py | 322 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 308 | `},` |
| 2460 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_naive_bayes.py | 819 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 810 | `),` |
| 2461 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_base.py | 19 | 1 | invalid syntax | `from sklearn.cluster import KMeans` |
| 2462 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_pipeline.py | 1701 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 1694 | `),` |
| 2463 | venv_creative/lib/python3.13/site-packages/sklearn/tests/metadata_routing_common.py | 11 | 1 | invalid syntax | `from sklearn.metrics._scorer import _Scorer, mean_squared_error` |
| 2464 | venv_creative/lib/python3.13/site-packages/sklearn/tests/test_kernel_approximation.py | 11 | 1 | invalid syntax | `from sklearn.metrics.pairwise import (chi2_kernel, kernel_metrics, polynomial_kernel,` |
| 2465 | venv_creative/lib/python3.13/site-packages/sklearn/linear_model/_least_angle.py | 28 | 1 | invalid syntax | `from ..utils._param_validation import Hidden, Interval, StrOptions, validate_params` |
| 2466 | venv_creative/lib/python3.13/site-packages/sklearn/linear_model/_stochastic_gradient.py | 1304 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 1297 | `}` |
| 2467 | venv_creative/lib/python3.13/site-packages/sklearn/linear_model/_ransac.py | 283 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 273 | `}` |
| 2468 | venv_creative/lib/python3.13/site-packages/sklearn/linear_model/_glm/glm.py | 149 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 139 | `}` |
| 2469 | venv_creative/lib/python3.13/site-packages/sklearn/linear_model/tests/test_ridge.py | 13 | 1 | invalid syntax | `from sklearn.exceptions import ConvergenceWarning` |
| 2470 | venv_creative/lib/python3.13/site-packages/sklearn/linear_model/tests/test_ransac.py | 10 | 1 | invalid syntax | `from sklearn.linear_model._ransac import _dynamic_max_trials` |
| 2471 | venv_creative/lib/python3.13/site-packages/sklearn/impute/_base.py | 333 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 325 | `}` |
| 2472 | venv_creative/lib/python3.13/site-packages/sklearn/impute/_iterative.py | 315 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 305 | `}` |
| 2473 | venv_creative/lib/python3.13/site-packages/sklearn/utils/_available_if.py | 26 | 12 | unexpected indent | `update_wrapper(self, fn)` |
| 2474 | venv_creative/lib/python3.13/site-packages/sklearn/utils/estimator_checks.py | 5589 | 57 | too many nested parentheses | `feature_names_in = [f"col{i}" for i in range(X.shape[1])]` |
| 2475 | venv_creative/lib/python3.13/site-packages/sklearn/utils/_pprint.py | 205 | 5 | invalid syntax | `def _pprint_estimator(self, object, stream, indent, allowance, context, level):` |
| 2476 | venv_creative/lib/python3.13/site-packages/sklearn/utils/_tags.py | 307 | 1 | invalid syntax | `def get_tags(estimator) -> Tags:` |
| 2477 | venv_creative/lib/python3.13/site-packages/sklearn/utils/validation.py | 76 | 13 | invalid syntax | `args_msg = ", ".join(args_msg)` |
| 2478 | venv_creative/lib/python3.13/site-packages/sklearn/utils/tests/test_pprint.py | 76 | 12 | unexpected indent | `self.n_features_to_select = n_features_to_select` |
| 2479 | venv_creative/lib/python3.13/site-packages/sklearn/utils/tests/test_validation.py | 1307 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 1299 | `),` |
| 2480 | venv_creative/lib/python3.13/site-packages/sklearn/utils/tests/test_indexing.py | 15 | 1 | invalid syntax | `from sklearn.utils._indexing import (_determine_key_type, _get_column_indices,` |
| 2481 | venv_creative/lib/python3.13/site-packages/sklearn/utils/tests/test_estimator_checks.py | 25 | 1 | invalid syntax | `from sklearn.linear_model import (LinearRegression, LogisticRegression,` |
| 2482 | venv_creative/lib/python3.13/site-packages/sklearn/utils/tests/test_multiclass.py | 186 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 166 | `}` |
| 2483 | venv_creative/lib/python3.13/site-packages/sklearn/utils/tests/test_encode.py | 28 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `ids=["int64", "float32 - nan", "object", "object - None", "str"],` |
| 2484 | venv_creative/lib/python3.13/site-packages/sklearn/utils/tests/test_testing.py | 579 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 567 | `):` |
| 2485 | venv_creative/lib/python3.13/site-packages/sklearn/utils/_repr_html/estimator.py | 171 | 9 | invalid syntax. Perhaps you forgot a comma? | `f'<div class="{outer_class}"><div'` |
| 2486 | venv_creative/lib/python3.13/site-packages/sklearn/utils/_repr_html/tests/test_estimator.py | 208 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 202 | `),` |
| 2487 | venv_creative/lib/python3.13/site-packages/sklearn/covariance/_empirical_covariance.py | 35 | 1 | invalid syntax | `def log_likelihood(emp_cov, precision):` |
| 2488 | venv_creative/lib/python3.13/site-packages/sklearn/covariance/_shrunk_covariance.py | 36 | 60 | invalid syntax. Perhaps you forgot a comma? | `X, assume_centered = assume_centered, block_size = block_size` |
| 2489 | venv_creative/lib/python3.13/site-packages/sklearn/covariance/_robust_covariance.py | 116 | 1 | invalid syntax | `def _c_step(` |
| 2490 | venv_creative/lib/python3.13/site-packages/sklearn/neural_network/tests/test_mlp.py | 20 | 1 | invalid syntax | `from sklearn.exceptions import ConvergenceWarning` |
| 2491 | venv_creative/lib/python3.13/site-packages/sklearn/feature_selection/_rfe.py | 215 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 207 | `}` |
| 2492 | venv_creative/lib/python3.13/site-packages/sklearn/feature_selection/_from_model.py | 257 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 248 | `}` |
| 2493 | venv_creative/lib/python3.13/site-packages/sklearn/feature_selection/_univariate_selection.py | 128 | 1 | invalid syntax | `def f_classif(X, y):` |
| 2494 | venv_creative/lib/python3.13/site-packages/sklearn/feature_selection/_sequential.py | 177 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 165 | `}` |
| 2495 | venv_creative/lib/python3.13/site-packages/sklearn/feature_selection/tests/test_rfe.py | 149 | 40 | unindent does not match any outer indentation level | `X, y = load_iris(return_X_y = True)` |
| 2496 | venv_creative/lib/python3.13/site-packages/sklearn/feature_selection/tests/test_from_model.py | 20 | 1 | invalid syntax | `from sklearn.pipeline import make_pipeline` |
| 2497 | venv_creative/lib/python3.13/site-packages/sklearn/feature_selection/tests/test_base.py | 61 | 8 | unexpected indent | `with pytest.raises(ValueError):` |
| 2498 | venv_creative/lib/python3.13/site-packages/sklearn/svm/_base.py | 98 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 80 | `}` |
| 2499 | venv_creative/lib/python3.13/site-packages/sklearn/svm/tests/test_svm.py | 13 | 1 | invalid syntax | `from sklearn import base, datasets, linear_model, metrics, svm` |
| 2500 | venv_creative/lib/python3.13/site-packages/sklearn/manifold/_locally_linear.py | 17 | 1 | invalid syntax | `from ..neighbors import NearestNeighbors` |
| 2501 | venv_creative/lib/python3.13/site-packages/sklearn/manifold/_t_sne.py | 830 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 819 | `}` |
| 2502 | venv_creative/lib/python3.13/site-packages/sklearn/manifold/_spectral_embedding.py | 652 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 633 | `}` |
| 2503 | venv_creative/lib/python3.13/site-packages/sklearn/mixture/_bayesian_mixture.py | 381 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 374 | `}` |
| 2504 | venv_creative/lib/python3.13/site-packages/sklearn/mixture/tests/test_bayesian_mixture.py | 25 | 9 | invalid syntax. Perhaps you forgot a comma? | `gammaln(weight_concentration)` |
| 2505 | venv_creative/lib/python3.13/site-packages/sklearn/preprocessing/tests/test_label.py | 12 | 1 | invalid syntax | `from sklearn.utils._array_api import (_convert_to_numpy,` |
| 2506 | venv_creative/lib/python3.13/site-packages/sklearn/preprocessing/tests/test_encoders.py | 2651 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 2644 | `).T` |
| 2507 | venv_creative/lib/python3.13/site-packages/sklearn/preprocessing/tests/test_function_transformer.py | 11 | 1 | invalid syntax | `from sklearn.utils.fixes import CSC_CONTAINERS, CSR_CONTAINERS` |
| 2508 | venv_creative/lib/python3.13/site-packages/sklearn/preprocessing/tests/test_data.py | 118 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 109 | `),` |
| 2509 | venv_creative/lib/python3.13/site-packages/sklearn/frozen/_frozen.py | 146 | 16 | unexpected indent | `if kwargs:` |
| 2510 | venv_creative/lib/python3.13/site-packages/sklearn/model_selection/_search.py | 489 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 472 | `}` |
| 2511 | venv_creative/lib/python3.13/site-packages/sklearn/model_selection/_classification_threshold.py | 75 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 68 | `}` |
| 2512 | venv_creative/lib/python3.13/site-packages/sklearn/model_selection/_validation.py | 126 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 107 | `},` |
| 2513 | venv_creative/lib/python3.13/site-packages/sklearn/model_selection/_search_successive_halving.py | 101 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 92 | `}` |
| 2514 | venv_creative/lib/python3.13/site-packages/sklearn/model_selection/tests/test_split.py | 177 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 161 | `):` |
| 2515 | venv_creative/lib/python3.13/site-packages/sklearn/model_selection/tests/test_validation.py | 23 | 1 | invalid syntax | `from sklearn.ensemble import RandomForestClassifier` |
| 2516 | venv_creative/lib/python3.13/site-packages/sklearn/model_selection/tests/test_search.py | 1029 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 1022 | `),` |
| 2517 | venv_creative/lib/python3.13/site-packages/sklearn/model_selection/tests/test_successive_halving.py | 15 | 1 | invalid syntax | `from sklearn.model_selection._search_successive_halving import (_SubsampleMetaSplitter,` |
| 2518 | venv_creative/lib/python3.13/site-packages/sklearn/model_selection/tests/test_classification_threshold.py | 9 | 1 | invalid syntax | `from sklearn.dummy import DummyClassifier` |
| 2519 | venv_creative/lib/python3.13/site-packages/sklearn/decomposition/_nmf.py | 1198 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 1185 | `}` |
| 2520 | venv_creative/lib/python3.13/site-packages/sklearn/decomposition/_lda.py | 25 | 1 | invalid syntax | `from ..utils import check_random_state, gen_batches, gen_even_slices` |
| 2521 | venv_creative/lib/python3.13/site-packages/sklearn/decomposition/tests/test_dict_learning.py | 14 | 1 | invalid syntax | `from sklearn.decomposition._dict_learning import _update_dict` |
| 2522 | venv_creative/lib/python3.13/site-packages/sklearn/decomposition/tests/test_kernel_pca.py | 18 | 1 | invalid syntax | `from sklearn.utils.fixes import CSR_CONTAINERS` |
| 2523 | venv_creative/lib/python3.13/site-packages/sklearn/cross_decomposition/tests/test_pls.py | 13 | 1 | invalid syntax | `from sklearn.datasets import load_linnerud, make_regression` |
| 2524 | venv_creative/lib/python3.13/site-packages/sklearn/neighbors/tests/test_neighbors_pipeline.py | 19 | 1 | invalid syntax | `from sklearn.pipeline import make_pipeline` |
| 2525 | venv_creative/lib/python3.13/site-packages/sklearn/neighbors/tests/test_lof.py | 18 | 1 | invalid syntax | `from sklearn.utils.fixes import CSR_CONTAINERS` |
| 2526 | venv_creative/lib/python3.13/site-packages/sklearn/neighbors/tests/test_nca.py | 46 | 59 | invalid syntax. Perhaps you forgot a comma? | `n_components = 2, init="identity", random_state = 42` |
| 2527 | venv_creative/lib/python3.13/site-packages/contourpy/util/renderer.py | 11 | 38 | '(' was never closed | `from contourpy._contourpy import (CoordinateArray, FillReturn, FillType, LineReturn,` |
| 2528 | venv_creative/lib/python3.13/site-packages/face_alignment/utils.py | 45 | 5 | invalid syntax | `if normalize:` |
| 2529 | venv_creative/lib/python3.13/site-packages/face_alignment/detection/sfd/sfd_detector.py | 23 | 12 | unexpected indent | `if path_to_detector is None:` |
| 2530 | venv_creative/lib/python3.13/site-packages/face_alignment/detection/dlib/dlib_detector.py | 19 | 12 | unexpected indent | `if 'cuda' in device:` |
| 2531 | venv_creative/lib/python3.13/site-packages/face_alignment/detection/blazeface/blazeface_detector.py | 24 | 12 | unexpected indent | `self.back_model = back_model` |
| 2532 | venv_creative/lib/python3.13/site-packages/httpx/_status_codes.py | 132 | 8 | unexpected indent | `BAD_REQUEST = 400, "Bad Request"` |
| 2533 | venv_creative/lib/python3.13/site-packages/joblib/_dask.py | 14 | 1 | invalid syntax | `from .parallel import AutoBatchingMixin, ParallelBackendBase, parallel_config` |
| 2534 | venv_creative/lib/python3.13/site-packages/joblib/compressor.py | 30 | 5 | invalid syntax. Perhaps you forgot a comma? | `"LZ4 is not installed. Install it with pip: https://python - lz4.readthedocs.io/"` |
| 2535 | venv_creative/lib/python3.13/site-packages/joblib/parallel.py | 1333 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 1323 | `},` |
| 2536 | venv_creative/lib/python3.13/site-packages/joblib/_parallel_backends.py | 18 | 1 | invalid syntax | `if mp is not None:` |
| 2537 | venv_creative/lib/python3.13/site-packages/joblib/executor.py | 45 | 13 | invalid syntax. Perhaps you forgot a comma? | `dict(timeout = timeout, initializer = initializer, initargs = initargs)` |
| 2538 | venv_creative/lib/python3.13/site-packages/joblib/test/test_numpy_pickle.py | 32 | 1 | invalid syntax | `from joblib.numpy_pickle_utils import (_IO_BUFFER_SIZE, _detect_compressor,` |
| 2539 | venv_creative/lib/python3.13/site-packages/joblib/test/test_parallel.py | 687 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 671 | `),` |
| 2540 | venv_creative/lib/python3.13/site-packages/joblib/test/test_memory.py | 32 | 1 | invalid syntax | `from joblib.parallel import Parallel, delayed` |
| 2541 | venv_creative/lib/python3.13/site-packages/joblib/externals/loky/process_executor.py | 208 | 51 | invalid syntax | `for _, (shutdown_lock, thread_wakeup) in items:` |
| 2542 | venv_creative/lib/python3.13/site-packages/attr/setters.py | 49 | 8 | unexpected indent | `if not v:` |
| 2543 | venv_creative/lib/python3.13/site-packages/attr/_make.py | 26 | 1 | invalid syntax | `from .exceptions import (DefaultAlreadySetError, FrozenInstanceError,` |
| 2544 | venv_creative/lib/python3.13/site-packages/attr/_funcs.py | 84 | 13 | invalid syntax | `elif isinstance(v, (tuple, list, set, frozenset)):` |
| 2545 | venv_creative/lib/python3.13/site-packages/tiktoken/registry.py | 52 | 29 | invalid syntax. Perhaps you forgot a comma? | `f"Duplicate encoding name {enc_name} in tiktoken plugin {mod_name}"` |
| 2546 | venv_creative/lib/python3.13/site-packages/tiktoken/_educational.py | 94 | 1 | invalid syntax | `def bpe_encode(` |
| 2547 | venv_creative/lib/python3.13/site-packages/transformers/tokenization_utils.py | 906 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 878 | `) -> BatchEncoding:` |
| 2548 | venv_creative/lib/python3.13/site-packages/transformers/modeling_rope_utils.py | 52 | 52 | invalid syntax. Perhaps you forgot a comma? | `self.config, device, seq_len = original_max_position_embeddings + 1` |
| 2549 | venv_creative/lib/python3.13/site-packages/transformers/video_utils.py | 33 | 1 | invalid syntax | `from .utils import (is_av_available, is_cv2_available, is_decord_available,` |
| 2550 | venv_creative/lib/python3.13/site-packages/transformers/trainer_seq2seq.py | 39 | 8 | unexpected indent | `from .feature_extraction_utils import FeatureExtractionMixin` |
| 2551 | venv_creative/lib/python3.13/site-packages/transformers/modeling_flax_pytorch_utils.py | 69 | 17 | invalid syntax | `raise` |
| 2552 | venv_creative/lib/python3.13/site-packages/transformers/feature_extraction_utils.py | 35 | 1 | invalid syntax | `from .utils.hub import cached_files` |
| 2553 | venv_creative/lib/python3.13/site-packages/transformers/tokenization_utils_base.py | 3061 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 3039 | `) -> BatchEncoding:` |
| 2554 | venv_creative/lib/python3.13/site-packages/transformers/testing_utils.py | 2501 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 2488 | `}` |
| 2555 | venv_creative/lib/python3.13/site-packages/transformers/trainer_utils.py | 39 | 1 | invalid syntax | `if is_torch_available():` |
| 2556 | venv_creative/lib/python3.13/site-packages/transformers/__init__.py | 308 | 1 | closing parenthesis '}' does not match opening parenthesis '[' on line 284 | `}` |
| 2557 | venv_creative/lib/python3.13/site-packages/transformers/convert_slow_tokenizer.py | 29 | 1 | invalid syntax | `from tokenizers.models import BPE, Unigram, WordPiece` |
| 2558 | venv_creative/lib/python3.13/site-packages/transformers/training_args.py | 845 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 839 | `},` |
| 2559 | venv_creative/lib/python3.13/site-packages/transformers/cache_utils.py | 13 | 1 | invalid syntax | `if is_hqq_available():` |
| 2560 | venv_creative/lib/python3.13/site-packages/transformers/tokenization_utils_fast.py | 577 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 555 | `) -> BatchEncoding:` |
| 2561 | venv_creative/lib/python3.13/site-packages/transformers/modeling_utils.py | 5702 | 45 | too many nested parentheses | `kernelize(model, device = Device(type = model.device.type))` |
| 2562 | venv_creative/lib/python3.13/site-packages/transformers/trainer.py | 396 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 384 | `):` |
| 2563 | venv_creative/lib/python3.13/site-packages/transformers/masking_utils.py | 30 | 1 | invalid syntax | `if is_torch_flex_attn_available():` |
| 2564 | venv_creative/lib/python3.13/site-packages/transformers/tokenization_mistral_common.py | 764 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 743 | `) -> BatchEncoding:` |
| 2565 | venv_creative/lib/python3.13/site-packages/transformers/trainer_pt_utils.py | 48 | 1 | invalid syntax | `if is_training_run_on_sagemaker():` |
| 2566 | venv_creative/lib/python3.13/site-packages/transformers/modeling_tf_utils.py | 2603 | 21 | closing parenthesis '}' does not match opening parenthesis '(' on line 2597 | `}` |
| 2567 | venv_creative/lib/python3.13/site-packages/transformers/onnx/__main__.py | 46 | 5 | invalid syntax | `else:` |
| 2568 | venv_creative/lib/python3.13/site-packages/transformers/loss/loss_grounding_dino.py | 24 | 1 | invalid syntax | `if is_scipy_available():` |
| 2569 | venv_creative/lib/python3.13/site-packages/transformers/loss/loss_for_object_detection.py | 25 | 1 | invalid syntax | `if is_accelerate_available():` |
| 2570 | venv_creative/lib/python3.13/site-packages/transformers/loss/loss_d_fine.py | 59 | 1 | invalid syntax | `def weighting_function(max_num_bins: int, up: torch.Tensor, reg_scale: int) -> torch.Tensor:` |
| 2571 | venv_creative/lib/python3.13/site-packages/transformers/quantizers/quantizer_torchao.py | 66 | 8 | unexpected indent | `from torchao.quantization.linear_activation_quantized_tensor import \` |
| 2572 | venv_creative/lib/python3.13/site-packages/transformers/quantizers/quantizer_gptq.py | 28 | 1 | invalid syntax | `from ..utils.quantization_config import GPTQConfig, QuantizationConfigMixin` |
| 2573 | venv_creative/lib/python3.13/site-packages/transformers/quantizers/base.py | 62 | 12 | unexpected indent | `self.modules_to_not_convert = kwargs.pop("modules_to_not_convert", [])` |
| 2574 | venv_creative/lib/python3.13/site-packages/transformers/pipelines/pt_utils.py | 308 | 28 | unexpected indent | `else:` |
| 2575 | venv_creative/lib/python3.13/site-packages/transformers/pipelines/text_to_audio.py | 99 | 5 | invalid syntax | `def __init__(self, *args, vocoder = None, sampling_rate = None, no_processor = True, **kwargs):` |
| 2576 | venv_creative/lib/python3.13/site-packages/transformers/pipelines/__init__.py | 32 | 1 | invalid syntax | `from ..models.auto.image_processing_auto import (IMAGE_PROCESSOR_MAPPING,` |
| 2577 | venv_creative/lib/python3.13/site-packages/transformers/pipelines/audio_utils.py | 35 | 5 | invalid syntax | `try:` |
| 2578 | venv_creative/lib/python3.13/site-packages/transformers/pipelines/automatic_speech_recognition.py | 26 | 1 | invalid syntax | `from .audio_utils import ffmpeg_read` |
| 2579 | venv_creative/lib/python3.13/site-packages/transformers/pipelines/base.py | 48 | 1 | invalid syntax | `from ..utils.deprecation import deprecate_kwarg` |
| 2580 | venv_creative/lib/python3.13/site-packages/transformers/utils/metrics.py | 170 | 12 | unexpected indent | `return decorator(func)` |
| 2581 | venv_creative/lib/python3.13/site-packages/transformers/utils/quantization_config.py | 35 | 1 | invalid syntax | `from .import_utils import is_auto_gptq_available` |
| 2582 | venv_creative/lib/python3.13/site-packages/transformers/models/__init__.py | 21 | 8 | unexpected indent | `from .albert import *` |
| 2583 | venv_creative/lib/python3.13/site-packages/transformers/models/dots1/configuration_dots1.py | 192 | 12 | unexpected indent | `self.sliding_window = sliding_window` |
| 2584 | venv_creative/lib/python3.13/site-packages/transformers/models/dots1/__init__.py | 21 | 8 | unexpected indent | `from .modeling_dots1 import *` |
| 2585 | venv_creative/lib/python3.13/site-packages/transformers/models/dots1/modeling_dots1.py | 198 | 84 | invalid syntax. Perhaps you forgot a comma? | `config.hidden_size, config.num_attention_heads * self.head_dim, bias = config.attention_bias` |
| 2586 | venv_creative/lib/python3.13/site-packages/transformers/models/metaclip_2/configuration_metaclip_2.py | 113 | 12 | unexpected indent | `self.attention_dropout = attention_dropout` |
| 2587 | venv_creative/lib/python3.13/site-packages/transformers/models/metaclip_2/modeling_metaclip_2.py | 19 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 2588 | venv_creative/lib/python3.13/site-packages/transformers/models/metaclip_2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_metaclip_2 import *` |
| 2589 | venv_creative/lib/python3.13/site-packages/transformers/models/metaclip_2/modular_metaclip_2.py | 10 | 1 | invalid syntax | `from ...modeling_outputs import BaseModelOutput, BaseModelOutputWithPooling` |
| 2590 | venv_creative/lib/python3.13/site-packages/transformers/models/nllb_moe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_nllb_moe import *` |
| 2591 | venv_creative/lib/python3.13/site-packages/transformers/models/sew_d/modeling_sew_d.py | 35 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2592 | venv_creative/lib/python3.13/site-packages/transformers/models/sew_d/__init__.py | 21 | 8 | unexpected indent | `from .modeling_sew_d import *` |
| 2593 | venv_creative/lib/python3.13/site-packages/transformers/models/sew_d/configuration_sew_d.py | 232 | 12 | unexpected indent | `self.max_position_embeddings = max_position_embeddings` |
| 2594 | venv_creative/lib/python3.13/site-packages/transformers/models/table_transformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_table_transformer import *` |
| 2595 | venv_creative/lib/python3.13/site-packages/transformers/models/bark/__init__.py | 21 | 8 | unexpected indent | `from .modeling_bark import *` |
| 2596 | venv_creative/lib/python3.13/site-packages/transformers/models/convnextv2/modeling_tf_convnextv2.py | 29 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFModelInputType, TFPreTrainedModel,` |
| 2597 | venv_creative/lib/python3.13/site-packages/transformers/models/convnextv2/modeling_convnextv2.py | 29 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2598 | venv_creative/lib/python3.13/site-packages/transformers/models/convnextv2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_convnextv2 import *` |
| 2599 | venv_creative/lib/python3.13/site-packages/transformers/models/llama4/image_processing_llama4_fast.py | 28 | 1 | invalid syntax | `from ...image_utils import ImageInput, PILImageResampling, SizeDict` |
| 2600 | venv_creative/lib/python3.13/site-packages/transformers/models/llama4/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_llama4_fast import *` |
| 2601 | venv_creative/lib/python3.13/site-packages/transformers/models/vitpose/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_vitpose import *` |
| 2602 | venv_creative/lib/python3.13/site-packages/transformers/models/vitpose/configuration_vitpose.py | 97 | 29 | invalid syntax | `if use_timm_backbone:` |
| 2603 | venv_creative/lib/python3.13/site-packages/transformers/models/vitpose/image_processing_vitpose.py | 31 | 1 | invalid syntax | `from ...utils import (TensorType, is_scipy_available, is_torch_available,` |
| 2604 | venv_creative/lib/python3.13/site-packages/transformers/models/mlcd/modeling_mlcd.py | 77 | 13 | invalid syntax. Perhaps you forgot a comma? | `torch.arange(num_patches_height, device = self.inv_freq.device).unsqueeze(1).expand(-1, num_patches_width)` |
| 2605 | venv_creative/lib/python3.13/site-packages/transformers/models/mlcd/modular_mlcd.py | 31 | 1 | invalid syntax | `from ..llama.modeling_llama import eager_attention_forward` |
| 2606 | venv_creative/lib/python3.13/site-packages/transformers/models/mlcd/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mlcd import *` |
| 2607 | venv_creative/lib/python3.13/site-packages/transformers/models/mlcd/configuration_mlcd.py | 113 | 12 | unexpected indent | `self.attention_dropout = attention_dropout` |
| 2608 | venv_creative/lib/python3.13/site-packages/transformers/models/pixtral/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_pixtral import *` |
| 2609 | venv_creative/lib/python3.13/site-packages/transformers/models/pixtral/image_processing_pixtral.py | 31 | 1 | invalid syntax | `from ...utils import TensorType, is_vision_available, logging` |
| 2610 | venv_creative/lib/python3.13/site-packages/transformers/models/glpn/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_glpn import *` |
| 2611 | venv_creative/lib/python3.13/site-packages/transformers/models/glpn/image_processing_glpn.py | 35 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, logging,` |
| 2612 | venv_creative/lib/python3.13/site-packages/transformers/models/glpn/modeling_glpn.py | 53 | 8 | unexpected indent | `return output` |
| 2613 | venv_creative/lib/python3.13/site-packages/transformers/models/bigbird_pegasus/__init__.py | 21 | 8 | unexpected indent | `from .modeling_bigbird_pegasus import *` |
| 2614 | venv_creative/lib/python3.13/site-packages/transformers/models/bigbird_pegasus/modeling_bigbird_pegasus.py | 33 | 1 | invalid syntax | `from ...modeling_flash_attention_utils import FlashAttentionKwargs` |
| 2615 | venv_creative/lib/python3.13/site-packages/transformers/models/biogpt/__init__.py | 21 | 8 | unexpected indent | `from .modeling_biogpt import *` |
| 2616 | venv_creative/lib/python3.13/site-packages/transformers/models/visual_bert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_visual_bert import *` |
| 2617 | venv_creative/lib/python3.13/site-packages/transformers/models/visual_bert/modeling_visual_bert.py | 32 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2618 | venv_creative/lib/python3.13/site-packages/transformers/models/video_llava/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_video_llava import *` |
| 2619 | venv_creative/lib/python3.13/site-packages/transformers/models/video_llava/image_processing_video_llava.py | 26 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 2620 | venv_creative/lib/python3.13/site-packages/transformers/models/cohere/__init__.py | 21 | 8 | unexpected indent | `from .modeling_cohere import *` |
| 2621 | venv_creative/lib/python3.13/site-packages/transformers/models/udop/configuration_udop.py | 129 | 12 | unexpected indent | `self.feed_forward_proj = feed_forward_proj` |
| 2622 | venv_creative/lib/python3.13/site-packages/transformers/models/udop/tokenization_udop_fast.py | 252 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 246 | `) -> BatchEncoding:` |
| 2623 | venv_creative/lib/python3.13/site-packages/transformers/models/udop/__init__.py | 21 | 8 | unexpected indent | `from .modeling_udop import *` |
| 2624 | venv_creative/lib/python3.13/site-packages/transformers/models/udop/processing_udop.py | 115 | 17 | invalid syntax. Perhaps you forgot a comma? | `boxes = output_kwargs["text_kwargs"].pop("boxes", None)` |
| 2625 | venv_creative/lib/python3.13/site-packages/transformers/models/udop/modeling_udop.py | 44 | 1 | invalid syntax | `from ...utils.deprecation import deprecate_kwarg` |
| 2626 | venv_creative/lib/python3.13/site-packages/transformers/models/udop/tokenization_udop.py | 560 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 554 | `) -> BatchEncoding:` |
| 2627 | venv_creative/lib/python3.13/site-packages/transformers/models/blip_2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_blip_2 import *` |
| 2628 | venv_creative/lib/python3.13/site-packages/transformers/models/blip_2/processing_blip_2.py | 28 | 1 | invalid syntax | `from ...utils import logging` |
| 2629 | venv_creative/lib/python3.13/site-packages/transformers/models/flava/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_flava import *` |
| 2630 | venv_creative/lib/python3.13/site-packages/transformers/models/flava/image_processing_flava.py | 34 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2631 | venv_creative/lib/python3.13/site-packages/transformers/models/flava/processing_flava.py | 29 | 1 | invalid syntax | `from ...utils import TensorType` |
| 2632 | venv_creative/lib/python3.13/site-packages/transformers/models/albert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_albert import *` |
| 2633 | venv_creative/lib/python3.13/site-packages/transformers/models/albert/modeling_tf_albert.py | 33 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 2634 | venv_creative/lib/python3.13/site-packages/transformers/models/cohere2_vision/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_cohere2_vision_fast import *` |
| 2635 | venv_creative/lib/python3.13/site-packages/transformers/models/cohere2_vision/modular_cohere2_vision.py | 28 | 1 | invalid syntax | `from transformers.models.got_ocr2.image_processing_got_ocr2_fast import \` |
| 2636 | venv_creative/lib/python3.13/site-packages/transformers/models/cohere2_vision/configuration_cohere2_vision.py | 57 | 12 | unexpected indent | `self.image_token_id = image_token_id` |
| 2637 | venv_creative/lib/python3.13/site-packages/transformers/models/cohere2_vision/modeling_cohere2_vision.py | 46 | 12 | unexpected indent | `self.intermediate_size = config.alignment_intermediate_size` |
| 2638 | venv_creative/lib/python3.13/site-packages/transformers/models/videomae/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_videomae import *` |
| 2639 | venv_creative/lib/python3.13/site-packages/transformers/models/videomae/image_processing_videomae.py | 26 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 2640 | venv_creative/lib/python3.13/site-packages/transformers/models/videomae/modeling_videomae.py | 51 | 1 | invalid syntax | `class VideoMAEDecoderOutput(ModelOutput):` |
| 2641 | venv_creative/lib/python3.13/site-packages/transformers/models/starcoder2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_starcoder2 import *` |
| 2642 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt_oss/__init__.py | 21 | 8 | unexpected indent | `from .modeling_gpt_oss import *` |
| 2643 | venv_creative/lib/python3.13/site-packages/transformers/models/vits/__init__.py | 21 | 8 | unexpected indent | `from .modeling_vits import *` |
| 2644 | venv_creative/lib/python3.13/site-packages/transformers/models/vits/modeling_vits.py | 48 | 1 | invalid syntax | `class VitsModelOutput(ModelOutput):` |
| 2645 | venv_creative/lib/python3.13/site-packages/transformers/models/olmoe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_olmoe import *` |
| 2646 | venv_creative/lib/python3.13/site-packages/transformers/models/speech_to_text/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_speech_to_text import *` |
| 2647 | venv_creative/lib/python3.13/site-packages/transformers/models/speech_to_text/processing_speech_to_text.py | 48 | 12 | unexpected indent | `self._in_target_context_manager = False` |
| 2648 | venv_creative/lib/python3.13/site-packages/transformers/models/gemma/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_gemma import *` |
| 2649 | venv_creative/lib/python3.13/site-packages/transformers/models/aimv2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_aimv2 import *` |
| 2650 | venv_creative/lib/python3.13/site-packages/transformers/models/time_series_transformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_time_series_transformer import *` |
| 2651 | venv_creative/lib/python3.13/site-packages/transformers/models/time_series_transformer/modeling_time_series_transformer.py | 32 | 1 | invalid syntax | `from ...modeling_flash_attention_utils import FlashAttentionKwargs` |
| 2652 | venv_creative/lib/python3.13/site-packages/transformers/models/mllama/image_processing_mllama.py | 31 | 1 | invalid syntax | `from ...utils import TensorType, logging` |
| 2653 | venv_creative/lib/python3.13/site-packages/transformers/models/mllama/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_mllama import *` |
| 2654 | venv_creative/lib/python3.13/site-packages/transformers/models/mllama/modeling_mllama.py | 867 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 860 | `}` |
| 2655 | venv_creative/lib/python3.13/site-packages/transformers/models/omdet_turbo/__init__.py | 21 | 8 | unexpected indent | `from .modeling_omdet_turbo import *` |
| 2656 | venv_creative/lib/python3.13/site-packages/transformers/models/clvp/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_clvp import *` |
| 2657 | venv_creative/lib/python3.13/site-packages/transformers/models/clvp/modeling_clvp.py | 35 | 1 | invalid syntax | `from ...modeling_outputs import (BaseModelOutput,` |
| 2658 | venv_creative/lib/python3.13/site-packages/transformers/models/clvp/configuration_clvp.py | 121 | 12 | unexpected indent | `self.attention_dropout = attention_dropout` |
| 2659 | venv_creative/lib/python3.13/site-packages/transformers/models/m2m_100/__init__.py | 21 | 8 | unexpected indent | `from .modeling_m2m_100 import *` |
| 2660 | venv_creative/lib/python3.13/site-packages/transformers/models/olmo2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_olmo2 import *` |
| 2661 | venv_creative/lib/python3.13/site-packages/transformers/models/superglue/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_superglue import *` |
| 2662 | venv_creative/lib/python3.13/site-packages/transformers/models/superglue/image_processing_superglue.py | 29 | 1 | invalid syntax | `from ...utils import TensorType, logging, requires_backends` |
| 2663 | venv_creative/lib/python3.13/site-packages/transformers/models/emu3/image_processing_emu3.py | 32 | 1 | invalid syntax | `from ...utils import TensorType, is_vision_available, logging` |
| 2664 | venv_creative/lib/python3.13/site-packages/transformers/models/emu3/configuration_emu3.py | 105 | 12 | unexpected indent | `self.base_channels = base_channels` |
| 2665 | venv_creative/lib/python3.13/site-packages/transformers/models/emu3/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_emu3 import *` |
| 2666 | venv_creative/lib/python3.13/site-packages/transformers/models/emu3/modular_emu3.py | 37 | 1 | invalid syntax | `from ..llama.modeling_llama import (LlamaAttention, LlamaDecoderLayer, LlamaForCausalLM,` |
| 2667 | venv_creative/lib/python3.13/site-packages/transformers/models/emu3/modeling_emu3.py | 136 | 84 | invalid syntax. Perhaps you forgot a comma? | `config.hidden_size, config.num_attention_heads * self.head_dim, bias = config.attention_bias` |
| 2668 | venv_creative/lib/python3.13/site-packages/transformers/models/got_ocr2/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_got_ocr2 import *` |
| 2669 | venv_creative/lib/python3.13/site-packages/transformers/models/got_ocr2/image_processing_got_ocr2.py | 31 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2670 | venv_creative/lib/python3.13/site-packages/transformers/models/diffllama/__init__.py | 21 | 8 | unexpected indent | `from .modeling_diffllama import *` |
| 2671 | venv_creative/lib/python3.13/site-packages/transformers/models/squeezebert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_squeezebert import *` |
| 2672 | venv_creative/lib/python3.13/site-packages/transformers/models/squeezebert/modeling_squeezebert.py | 31 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2673 | venv_creative/lib/python3.13/site-packages/transformers/models/swin/modeling_swin.py | 35 | 1 | invalid syntax | `from ...utils import ModelOutput, auto_docstring, logging, torch_int` |
| 2674 | venv_creative/lib/python3.13/site-packages/transformers/models/swin/__init__.py | 21 | 8 | unexpected indent | `from .modeling_swin import *` |
| 2675 | venv_creative/lib/python3.13/site-packages/transformers/models/swin/modeling_tf_swin.py | 35 | 1 | invalid syntax | `from ...tf_utils import shape_list` |
| 2676 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilenet_v1/image_processing_mobilenet_v1.py | 26 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 2677 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilenet_v1/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_mobilenet_v1 import *` |
| 2678 | venv_creative/lib/python3.13/site-packages/transformers/models/convnext/modeling_tf_convnext.py | 27 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFModelInputType, TFPreTrainedModel,` |
| 2679 | venv_creative/lib/python3.13/site-packages/transformers/models/convnext/image_processing_convnext.py | 26 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 2680 | venv_creative/lib/python3.13/site-packages/transformers/models/convnext/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_convnext import *` |
| 2681 | venv_creative/lib/python3.13/site-packages/transformers/models/convnext/modeling_convnext.py | 29 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2682 | venv_creative/lib/python3.13/site-packages/transformers/models/arcee/__init__.py | 21 | 8 | unexpected indent | `from .modeling_arcee import *` |
| 2683 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt_neox/__init__.py | 21 | 8 | unexpected indent | `from .modeling_gpt_neox import *` |
| 2684 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt_neox/modeling_gpt_neox.py | 25 | 1 | invalid syntax | `from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS, dynamic_rope_update` |
| 2685 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt_neox/modular_gpt_neox.py | 19 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 2686 | venv_creative/lib/python3.13/site-packages/transformers/models/poolformer/modeling_poolformer.py | 30 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2687 | venv_creative/lib/python3.13/site-packages/transformers/models/poolformer/image_processing_poolformer.py | 26 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 2688 | venv_creative/lib/python3.13/site-packages/transformers/models/poolformer/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_poolformer import *` |
| 2689 | venv_creative/lib/python3.13/site-packages/transformers/models/mimi/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mimi import *` |
| 2690 | venv_creative/lib/python3.13/site-packages/transformers/models/wavlm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_wavlm import *` |
| 2691 | venv_creative/lib/python3.13/site-packages/transformers/models/marian/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_marian import *` |
| 2692 | venv_creative/lib/python3.13/site-packages/transformers/models/marian/modeling_tf_marian.py | 31 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss, TFPreTrainedModel,` |
| 2693 | venv_creative/lib/python3.13/site-packages/transformers/models/vilt/image_processing_vilt.py | 31 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2694 | venv_creative/lib/python3.13/site-packages/transformers/models/vilt/processing_vilt.py | 28 | 1 | invalid syntax | `from ...utils import TensorType` |
| 2695 | venv_creative/lib/python3.13/site-packages/transformers/models/vilt/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_vilt import *` |
| 2696 | venv_creative/lib/python3.13/site-packages/transformers/models/vilt/image_processing_vilt_fast.py | 26 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 2697 | venv_creative/lib/python3.13/site-packages/transformers/models/vilt/modeling_vilt.py | 34 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2698 | venv_creative/lib/python3.13/site-packages/transformers/models/electra/__init__.py | 21 | 8 | unexpected indent | `from .modeling_electra import *` |
| 2699 | venv_creative/lib/python3.13/site-packages/transformers/models/electra/modeling_tf_electra.py | 33 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 2700 | venv_creative/lib/python3.13/site-packages/transformers/models/exaone4/__init__.py | 21 | 8 | unexpected indent | `from .modeling_exaone4 import *` |
| 2701 | venv_creative/lib/python3.13/site-packages/transformers/models/evolla/__init__.py | 21 | 8 | unexpected indent | `from .modeling_evolla import *` |
| 2702 | venv_creative/lib/python3.13/site-packages/transformers/models/evolla/modeling_evolla.py | 646 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 641 | `}` |
| 2703 | venv_creative/lib/python3.13/site-packages/transformers/models/perception_lm/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_perception_lm_fast import *` |
| 2704 | venv_creative/lib/python3.13/site-packages/transformers/models/bit/image_processing_bit.py | 26 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 2705 | venv_creative/lib/python3.13/site-packages/transformers/models/bit/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_bit import *` |
| 2706 | venv_creative/lib/python3.13/site-packages/transformers/models/bit/modeling_bit.py | 33 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2707 | venv_creative/lib/python3.13/site-packages/transformers/models/luke/__init__.py | 21 | 8 | unexpected indent | `from .modeling_luke import *` |
| 2708 | venv_creative/lib/python3.13/site-packages/transformers/models/luke/tokenization_luke.py | 873 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 850 | `) -> BatchEncoding:` |
| 2709 | venv_creative/lib/python3.13/site-packages/transformers/models/deberta/__init__.py | 21 | 8 | unexpected indent | `from .modeling_deberta import *` |
| 2710 | venv_creative/lib/python3.13/site-packages/transformers/models/deberta/modeling_tf_deberta.py | 31 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 2711 | venv_creative/lib/python3.13/site-packages/transformers/models/granite/__init__.py | 21 | 8 | unexpected indent | `from .modeling_granite import *` |
| 2712 | venv_creative/lib/python3.13/site-packages/transformers/models/gemma2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_gemma2 import *` |
| 2713 | venv_creative/lib/python3.13/site-packages/transformers/models/mixtral/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mixtral import *` |
| 2714 | venv_creative/lib/python3.13/site-packages/transformers/models/pix2struct/configuration_pix2struct.py | 130 | 12 | unexpected indent | `self.use_cache = use_cache` |
| 2715 | venv_creative/lib/python3.13/site-packages/transformers/models/pix2struct/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_pix2struct import *` |
| 2716 | venv_creative/lib/python3.13/site-packages/transformers/models/conditional_detr/modeling_conditional_detr.py | 31 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2717 | venv_creative/lib/python3.13/site-packages/transformers/models/conditional_detr/image_processing_conditional_detr.py | 32 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 2718 | venv_creative/lib/python3.13/site-packages/transformers/models/conditional_detr/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_conditional_detr import *` |
| 2719 | venv_creative/lib/python3.13/site-packages/transformers/models/vision_text_dual_encoder/processing_vision_text_dual_encoder.py | 62 | 33 | invalid syntax. Perhaps you forgot a comma? | `feature_extractor = kwargs.pop("feature_extractor")` |
| 2720 | venv_creative/lib/python3.13/site-packages/transformers/models/vision_text_dual_encoder/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_vision_text_dual_encoder import *` |
| 2721 | venv_creative/lib/python3.13/site-packages/transformers/models/vision_text_dual_encoder/modeling_flax_vision_text_dual_encoder.py | 30 | 1 | invalid syntax | `from ...utils import add_start_docstrings, logging` |
| 2722 | venv_creative/lib/python3.13/site-packages/transformers/models/mvp/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mvp import *` |
| 2723 | venv_creative/lib/python3.13/site-packages/transformers/models/timesfm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_timesfm import *` |
| 2724 | venv_creative/lib/python3.13/site-packages/transformers/models/pvt_v2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_pvt_v2 import *` |
| 2725 | venv_creative/lib/python3.13/site-packages/transformers/models/pvt_v2/modeling_pvt_v2.py | 58 | 8 | unexpected indent | `return output` |
| 2726 | venv_creative/lib/python3.13/site-packages/transformers/models/donut/modeling_donut_swin.py | 36 | 1 | invalid syntax | `from ...utils import ModelOutput, auto_docstring, logging, torch_int` |
| 2727 | venv_creative/lib/python3.13/site-packages/transformers/models/donut/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_donut import *` |
| 2728 | venv_creative/lib/python3.13/site-packages/transformers/models/donut/processing_donut.py | 67 | 33 | invalid syntax. Perhaps you forgot a comma? | `feature_extractor = kwargs.pop("feature_extractor")` |
| 2729 | venv_creative/lib/python3.13/site-packages/transformers/models/donut/image_processing_donut.py | 26 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 2730 | venv_creative/lib/python3.13/site-packages/transformers/models/sam/image_processing_sam_fast.py | 31 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 2731 | venv_creative/lib/python3.13/site-packages/transformers/models/sam/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_sam import *` |
| 2732 | venv_creative/lib/python3.13/site-packages/transformers/models/sam/image_processing_sam.py | 33 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_tf_available,` |
| 2733 | venv_creative/lib/python3.13/site-packages/transformers/models/mpt/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mpt import *` |
| 2734 | venv_creative/lib/python3.13/site-packages/transformers/models/shieldgemma2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_shieldgemma2 import *` |
| 2735 | venv_creative/lib/python3.13/site-packages/transformers/models/maskformer/modeling_maskformer_swin.py | 36 | 1 | invalid syntax | `from ...utils import auto_docstring, torch_int` |
| 2736 | venv_creative/lib/python3.13/site-packages/transformers/models/maskformer/__init__.py | 21 | 8 | unexpected indent | `from .configuration_maskformer_swin import *` |
| 2737 | venv_creative/lib/python3.13/site-packages/transformers/models/maskformer/image_processing_maskformer.py | 28 | 1 | invalid syntax | `from ...image_transforms import (PaddingMode, get_resize_output_image_size, pad,` |
| 2738 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_vl_hybrid/image_processing_deepseek_vl_hybrid.py | 35 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2739 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_vl_hybrid/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_deepseek_vl_fast_hybrid import *` |
| 2740 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_vl_hybrid/image_processing_deepseek_vl_hybrid_fast.py | 31 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 2741 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_vl_hybrid/modular_deepseek_vl_hybrid.py | 27 | 1 | invalid syntax | `from ...image_transforms import convert_to_rgb, to_channel_dimension_format` |
| 2742 | venv_creative/lib/python3.13/site-packages/transformers/models/markuplm/tokenization_markuplm.py | 714 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 688 | `) -> BatchEncoding:` |
| 2743 | venv_creative/lib/python3.13/site-packages/transformers/models/markuplm/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_markuplm import *` |
| 2744 | venv_creative/lib/python3.13/site-packages/transformers/models/markuplm/feature_extraction_markuplm.py | 55 | 46 | invalid syntax. Perhaps you forgot a comma? | `0 if 1 == len(siblings) else next(i for i, s in enumerate(siblings, 1) if s is child)` |
| 2745 | venv_creative/lib/python3.13/site-packages/transformers/models/markuplm/tokenization_markuplm_fast.py | 468 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 442 | `) -> BatchEncoding:` |
| 2746 | venv_creative/lib/python3.13/site-packages/transformers/models/cpmant/__init__.py | 21 | 8 | unexpected indent | `from .modeling_cpmant import *` |
| 2747 | venv_creative/lib/python3.13/site-packages/transformers/models/led/__init__.py | 21 | 8 | unexpected indent | `from .modeling_led import *` |
| 2748 | venv_creative/lib/python3.13/site-packages/transformers/models/led/modeling_led.py | 93 | 9 | invalid syntax | `return super().forward(positions)` |
| 2749 | venv_creative/lib/python3.13/site-packages/transformers/models/vjepa2/__init__.py | 22 | 8 | unexpected indent | `from .modeling_vjepa2 import *` |
| 2750 | venv_creative/lib/python3.13/site-packages/transformers/models/vjepa2/modeling_vjepa2.py | 40 | 1 | invalid syntax | `class VJEPA2WithMaskedInputPredictorOutput(ModelOutput):` |
| 2751 | venv_creative/lib/python3.13/site-packages/transformers/models/olmo/__init__.py | 21 | 8 | unexpected indent | `from .modeling_olmo import *` |
| 2752 | venv_creative/lib/python3.13/site-packages/transformers/models/chameleon/modeling_chameleon.py | 79 | 12 | unexpected indent | `self.dim = dim` |
| 2753 | venv_creative/lib/python3.13/site-packages/transformers/models/chameleon/image_processing_chameleon.py | 26 | 1 | invalid syntax | `from ...image_utils import (ChannelDimension, ImageInput, PILImageResampling,` |
| 2754 | venv_creative/lib/python3.13/site-packages/transformers/models/chameleon/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_chameleon import *` |
| 2755 | venv_creative/lib/python3.13/site-packages/transformers/models/longt5/configuration_longt5.py | 128 | 12 | unexpected indent | `self.feed_forward_proj = feed_forward_proj` |
| 2756 | venv_creative/lib/python3.13/site-packages/transformers/models/longt5/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_longt5 import *` |
| 2757 | venv_creative/lib/python3.13/site-packages/transformers/models/longt5/modeling_longt5.py | 36 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2758 | venv_creative/lib/python3.13/site-packages/transformers/models/phi3/__init__.py | 21 | 8 | unexpected indent | `from .modeling_phi3 import *` |
| 2759 | venv_creative/lib/python3.13/site-packages/transformers/models/phi3/configuration_phi3.py | 175 | 12 | unexpected indent | `self._rope_scaling_adjustment()` |
| 2760 | venv_creative/lib/python3.13/site-packages/transformers/models/gemma3/image_processing_gemma3.py | 32 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2761 | venv_creative/lib/python3.13/site-packages/transformers/models/gemma3/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_gemma3 import *` |
| 2762 | venv_creative/lib/python3.13/site-packages/transformers/models/colqwen2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_colqwen2 import *` |
| 2763 | venv_creative/lib/python3.13/site-packages/transformers/models/eomt/modeling_eomt.py | 63 | 1 | invalid syntax | `class EomtForUniversalSegmentationOutput(ModelOutput):` |
| 2764 | venv_creative/lib/python3.13/site-packages/transformers/models/eomt/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_eomt import *` |
| 2765 | venv_creative/lib/python3.13/site-packages/transformers/models/eomt/image_processing_eomt.py | 30 | 1 | invalid syntax | `from ...utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD, TensorType,` |
| 2766 | venv_creative/lib/python3.13/site-packages/transformers/models/esm/modeling_tf_esm.py | 28 | 1 | invalid syntax | `from ...modeling_tf_outputs import (TFBaseModelOutputWithPastAndCrossAttentions,` |
| 2767 | venv_creative/lib/python3.13/site-packages/transformers/models/esm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_esm import *` |
| 2768 | venv_creative/lib/python3.13/site-packages/transformers/models/esm/modeling_esm.py | 676 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 671 | `}` |
| 2769 | venv_creative/lib/python3.13/site-packages/transformers/models/esm/modeling_esmfold.py | 2314 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 2302 | `}` |
| 2770 | venv_creative/lib/python3.13/site-packages/transformers/models/univnet/feature_extraction_univnet.py | 24 | 1 | invalid syntax | `from ...feature_extraction_sequence_utils import SequenceFeatureExtractor` |
| 2771 | venv_creative/lib/python3.13/site-packages/transformers/models/univnet/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_univnet import *` |
| 2772 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4/configuration_glm4.py | 136 | 12 | unexpected indent | `self.head_dim = head_dim` |
| 2773 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4/__init__.py | 21 | 8 | unexpected indent | `from .modeling_glm4 import *` |
| 2774 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4/modeling_glm4.py | 38 | 1 | invalid syntax | `from ...modeling_outputs import BaseModelOutputWithPast, CausalLMOutputWithPast` |
| 2775 | venv_creative/lib/python3.13/site-packages/transformers/models/big_bird/__init__.py | 21 | 8 | unexpected indent | `from .modeling_big_bird import *` |
| 2776 | venv_creative/lib/python3.13/site-packages/transformers/models/big_bird/modeling_flax_big_bird.py | 38 | 1 | invalid syntax | `from ...modeling_flax_utils import (ACT2FN, FlaxPreTrainedModel,` |
| 2777 | venv_creative/lib/python3.13/site-packages/transformers/models/big_bird/modeling_big_bird.py | 39 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2778 | venv_creative/lib/python3.13/site-packages/transformers/models/hunyuan_v1_moe/__init__.py | 8 | 8 | unexpected indent | `from .modeling_hunyuan import *` |
| 2779 | venv_creative/lib/python3.13/site-packages/transformers/models/auto/__init__.py | 21 | 8 | unexpected indent | `from .configuration_auto import *` |
| 2780 | venv_creative/lib/python3.13/site-packages/transformers/models/bert_generation/__init__.py | 21 | 8 | unexpected indent | `from .modeling_bert_generation import *` |
| 2781 | venv_creative/lib/python3.13/site-packages/transformers/models/wav2vec2_with_lm/processing_wav2vec2_with_lm.py | 99 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"`feature_extractor` has to be of type `Wav2Vec2FeatureExtractor` or `SeamlessM4TFeatureExtractor`, but is {type(feature_extractor)}"` |
| 2782 | venv_creative/lib/python3.13/site-packages/transformers/models/vit_msn/__init__.py | 21 | 8 | unexpected indent | `from .modeling_vit_msn import *` |
| 2783 | venv_creative/lib/python3.13/site-packages/transformers/models/vit_msn/modeling_vit_msn.py | 98 | 9 | invalid syntax | `return torch.cat((class_pos_embed, patch_pos_embed), dim = 1)` |
| 2784 | venv_creative/lib/python3.13/site-packages/transformers/models/rt_detr/image_processing_rt_detr.py | 30 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 2785 | venv_creative/lib/python3.13/site-packages/transformers/models/rt_detr/__init__.py | 22 | 8 | unexpected indent | `from .configuration_rt_detr_resnet import *` |
| 2786 | venv_creative/lib/python3.13/site-packages/transformers/models/dab_detr/__init__.py | 22 | 8 | unexpected indent | `from .modeling_dab_detr import *` |
| 2787 | venv_creative/lib/python3.13/site-packages/transformers/models/kosmos2_5/configuration_kosmos2_5.py | 102 | 25 | '(' was never closed | `super().__init__(` |
| 2788 | venv_creative/lib/python3.13/site-packages/transformers/models/kosmos2_5/__init__.py | 22 | 8 | unexpected indent | `from .image_processing_kosmos2_5 import *` |
| 2789 | venv_creative/lib/python3.13/site-packages/transformers/models/kosmos2_5/image_processing_kosmos2_5_fast.py | 26 | 1 | invalid syntax | `from ...image_utils import ChannelDimension, ImageInput, get_image_size` |
| 2790 | venv_creative/lib/python3.13/site-packages/transformers/models/kosmos2_5/modeling_kosmos2_5.py | 36 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 2791 | venv_creative/lib/python3.13/site-packages/transformers/models/zamba2/configuration_zamba2.py | 182 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.vocab_size = vocab_size` |
| 2792 | venv_creative/lib/python3.13/site-packages/transformers/models/zamba2/modeling_zamba2.py | 40 | 1 | invalid syntax | `from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS, dynamic_rope_update` |
| 2793 | venv_creative/lib/python3.13/site-packages/transformers/models/zamba2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_zamba2 import *` |
| 2794 | venv_creative/lib/python3.13/site-packages/transformers/models/zamba2/modular_zamba2.py | 38 | 1 | invalid syntax | `from ..zamba.modeling_zamba import (ZambaAttention, ZambaAttentionDecoderLayer,` |
| 2795 | venv_creative/lib/python3.13/site-packages/transformers/models/jetmoe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_jetmoe import *` |
| 2796 | venv_creative/lib/python3.13/site-packages/transformers/models/lxmert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_lxmert import *` |
| 2797 | venv_creative/lib/python3.13/site-packages/transformers/models/clip/configuration_clip.py | 131 | 12 | unexpected indent | `self.attention_dropout = attention_dropout` |
| 2798 | venv_creative/lib/python3.13/site-packages/transformers/models/clip/modeling_tf_clip.py | 33 | 1 | invalid syntax | `from ...tf_utils import check_embeddings_within_bounds, shape_list, stable_softmax` |
| 2799 | venv_creative/lib/python3.13/site-packages/transformers/models/clip/modeling_flax_clip.py | 34 | 1 | invalid syntax | `from ...utils import ModelOutput, add_start_docstrings, logging` |
| 2800 | venv_creative/lib/python3.13/site-packages/transformers/models/clip/image_processing_clip.py | 26 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 2801 | venv_creative/lib/python3.13/site-packages/transformers/models/clip/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_clip import *` |
| 2802 | venv_creative/lib/python3.13/site-packages/transformers/models/clip/processing_clip.py | 54 | 33 | invalid syntax. Perhaps you forgot a comma? | `feature_extractor = kwargs.pop("feature_extractor")` |
| 2803 | venv_creative/lib/python3.13/site-packages/transformers/models/clip/modeling_clip.py | 29 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 2804 | venv_creative/lib/python3.13/site-packages/transformers/models/qwen2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_qwen2 import *` |
| 2805 | venv_creative/lib/python3.13/site-packages/transformers/models/ctrl/__init__.py | 21 | 8 | unexpected indent | `from .modeling_ctrl import *` |
| 2806 | venv_creative/lib/python3.13/site-packages/transformers/models/ctrl/modeling_tf_ctrl.py | 27 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss, TFModelInputType,` |
| 2807 | venv_creative/lib/python3.13/site-packages/transformers/models/hubert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_hubert import *` |
| 2808 | venv_creative/lib/python3.13/site-packages/transformers/models/sam_hq/modeling_sam_hq.py | 36 | 1 | invalid syntax | `from ...activations import ACT2FN` |
| 2809 | venv_creative/lib/python3.13/site-packages/transformers/models/sam_hq/modular_sam_hq.py | 30 | 1 | invalid syntax | `from ..sam.modeling_sam import (SamFeedForward, SamImageSegmentationOutput,` |
| 2810 | venv_creative/lib/python3.13/site-packages/transformers/models/sam_hq/__init__.py | 21 | 8 | unexpected indent | `from .modeling_sam_hq import *` |
| 2811 | venv_creative/lib/python3.13/site-packages/transformers/models/groupvit/configuration_groupvit.py | 122 | 12 | unexpected indent | `self.attention_dropout = attention_dropout` |
| 2812 | venv_creative/lib/python3.13/site-packages/transformers/models/groupvit/modeling_groupvit.py | 31 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 2813 | venv_creative/lib/python3.13/site-packages/transformers/models/groupvit/__init__.py | 21 | 8 | unexpected indent | `from .modeling_groupvit import *` |
| 2814 | venv_creative/lib/python3.13/site-packages/transformers/models/groupvit/modeling_tf_groupvit.py | 33 | 1 | invalid syntax | `from ...tf_utils import check_embeddings_within_bounds, shape_list, stable_softmax` |
| 2815 | venv_creative/lib/python3.13/site-packages/transformers/models/granitemoe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_granitemoe import *` |
| 2816 | venv_creative/lib/python3.13/site-packages/transformers/models/pvt/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_pvt import *` |
| 2817 | venv_creative/lib/python3.13/site-packages/transformers/models/pvt/image_processing_pvt.py | 30 | 1 | invalid syntax | `from ...utils import TensorType, filter_out_non_signature_kwargs, logging` |
| 2818 | venv_creative/lib/python3.13/site-packages/transformers/models/pvt/modeling_pvt.py | 59 | 8 | unexpected indent | `return output` |
| 2819 | venv_creative/lib/python3.13/site-packages/transformers/models/helium/__init__.py | 21 | 8 | unexpected indent | `from .modeling_helium import *` |
| 2820 | venv_creative/lib/python3.13/site-packages/transformers/models/mluke/tokenization_mluke.py | 693 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 670 | `) -> BatchEncoding:` |
| 2821 | venv_creative/lib/python3.13/site-packages/transformers/models/superpoint/image_processing_superpoint.py | 28 | 1 | invalid syntax | `from ...utils import TensorType, logging, requires_backends` |
| 2822 | venv_creative/lib/python3.13/site-packages/transformers/models/superpoint/modeling_superpoint.py | 80 | 1 | invalid syntax | `class SuperPointKeypointDescriptionOutput(ModelOutput):` |
| 2823 | venv_creative/lib/python3.13/site-packages/transformers/models/superpoint/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_superpoint import *` |
| 2824 | venv_creative/lib/python3.13/site-packages/transformers/models/reformer/modeling_reformer.py | 38 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2825 | venv_creative/lib/python3.13/site-packages/transformers/models/reformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_reformer import *` |
| 2826 | venv_creative/lib/python3.13/site-packages/transformers/models/t5gemma/__init__.py | 21 | 8 | unexpected indent | `from .modeling_encdecgemma2 import *` |
| 2827 | venv_creative/lib/python3.13/site-packages/transformers/models/sew/configuration_sew.py | 211 | 12 | unexpected indent | `self.hidden_act = hidden_act` |
| 2828 | venv_creative/lib/python3.13/site-packages/transformers/models/sew/modular_sew.py | 41 | 1 | invalid syntax | `from .configuration_sew import SEWConfig` |
| 2829 | venv_creative/lib/python3.13/site-packages/transformers/models/sew/__init__.py | 21 | 8 | unexpected indent | `from .modeling_sew import *` |
| 2830 | venv_creative/lib/python3.13/site-packages/transformers/models/sew/modeling_sew.py | 40 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 2831 | venv_creative/lib/python3.13/site-packages/transformers/models/oneformer/image_processing_oneformer.py | 30 | 1 | invalid syntax | `from ...image_transforms import (PaddingMode, get_resize_output_image_size, pad,` |
| 2832 | venv_creative/lib/python3.13/site-packages/transformers/models/oneformer/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_oneformer import *` |
| 2833 | venv_creative/lib/python3.13/site-packages/transformers/models/llava_next_video/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_llava_next_video import *` |
| 2834 | venv_creative/lib/python3.13/site-packages/transformers/models/llava_next_video/image_processing_llava_next_video.py | 26 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 2835 | venv_creative/lib/python3.13/site-packages/transformers/models/falcon_mamba/configuration_falcon_mamba.py | 144 | 34 | '(' was never closed | `self.intermediate_size = (` |
| 2836 | venv_creative/lib/python3.13/site-packages/transformers/models/falcon_mamba/__init__.py | 21 | 8 | unexpected indent | `from .modeling_falcon_mamba import *` |
| 2837 | venv_creative/lib/python3.13/site-packages/transformers/models/focalnet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_focalnet import *` |
| 2838 | venv_creative/lib/python3.13/site-packages/transformers/models/focalnet/configuration_focalnet.py | 24 | 8 | invalid syntax | `logger = logging.get_logger(__name__)` |
| 2839 | venv_creative/lib/python3.13/site-packages/transformers/models/focalnet/modeling_focalnet.py | 47 | 1 | invalid syntax | `class FocalNetEncoderOutput(ModelOutput):` |
| 2840 | venv_creative/lib/python3.13/site-packages/transformers/models/resnet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_resnet import *` |
| 2841 | venv_creative/lib/python3.13/site-packages/transformers/models/mask2former/image_processing_mask2former.py | 27 | 1 | invalid syntax | `from ...image_transforms import (PaddingMode, get_resize_output_image_size, pad,` |
| 2842 | venv_creative/lib/python3.13/site-packages/transformers/models/mask2former/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_mask2former import *` |
| 2843 | venv_creative/lib/python3.13/site-packages/transformers/models/grounding_dino/image_processing_grounding_dino_fast.py | 17 | 1 | invalid syntax | `from ...image_transforms import center_to_corners_format, corners_to_center_format` |
| 2844 | venv_creative/lib/python3.13/site-packages/transformers/models/grounding_dino/modular_grounding_dino.py | 42 | 8 | unexpected indent | `return boxes` |
| 2845 | venv_creative/lib/python3.13/site-packages/transformers/models/grounding_dino/modeling_grounding_dino.py | 69 | 17 | invalid syntax. Perhaps you forgot a comma? | `value_list[level_id]` |
| 2846 | venv_creative/lib/python3.13/site-packages/transformers/models/grounding_dino/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_grounding_dino import *` |
| 2847 | venv_creative/lib/python3.13/site-packages/transformers/models/grounding_dino/image_processing_grounding_dino.py | 32 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 2848 | venv_creative/lib/python3.13/site-packages/transformers/models/grounding_dino/processing_grounding_dino.py | 52 | 8 | unexpected indent | `posmaps = posmaps.clone()` |
| 2849 | venv_creative/lib/python3.13/site-packages/transformers/models/lfm2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_lfm2 import *` |
| 2850 | venv_creative/lib/python3.13/site-packages/transformers/models/lfm2/modular_lfm2.py | 35 | 1 | invalid syntax | `from .configuration_lfm2 import Lfm2Config` |
| 2851 | venv_creative/lib/python3.13/site-packages/transformers/models/lfm2/modeling_lfm2.py | 124 | 21 | invalid syntax. Perhaps you forgot a comma? | `(intermediate_size + config.block_multiple_of - 1) // config.block_multiple_of` |
| 2852 | venv_creative/lib/python3.13/site-packages/transformers/models/tapas/modeling_tapas.py | 126 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 115 | `):` |
| 2853 | venv_creative/lib/python3.13/site-packages/transformers/models/tapas/modeling_tf_tapas.py | 32 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 2854 | venv_creative/lib/python3.13/site-packages/transformers/models/tapas/__init__.py | 21 | 8 | unexpected indent | `from .modeling_tapas import *` |
| 2855 | venv_creative/lib/python3.13/site-packages/transformers/models/tapas/tokenization_tapas.py | 577 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 547 | `) -> BatchEncoding:` |
| 2856 | venv_creative/lib/python3.13/site-packages/transformers/models/qwen3/__init__.py | 21 | 8 | unexpected indent | `from .modeling_qwen3 import *` |
| 2857 | venv_creative/lib/python3.13/site-packages/transformers/models/data2vec/modeling_data2vec_vision.py | 34 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2858 | venv_creative/lib/python3.13/site-packages/transformers/models/data2vec/modeling_tf_data2vec_vision.py | 32 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFModelInputType, TFPreTrainedModel,` |
| 2859 | venv_creative/lib/python3.13/site-packages/transformers/models/data2vec/__init__.py | 21 | 8 | unexpected indent | `from .configuration_data2vec_text import *` |
| 2860 | venv_creative/lib/python3.13/site-packages/transformers/models/dinat/modeling_dinat.py | 34 | 1 | invalid syntax | `from ...utils.backbone_utils import BackboneMixin` |
| 2861 | venv_creative/lib/python3.13/site-packages/transformers/models/dinat/__init__.py | 21 | 8 | unexpected indent | `from .modeling_dinat import *` |
| 2862 | venv_creative/lib/python3.13/site-packages/transformers/models/zamba/__init__.py | 21 | 8 | unexpected indent | `from .modeling_zamba import *` |
| 2863 | venv_creative/lib/python3.13/site-packages/transformers/models/zamba/configuration_zamba.py | 198 | 12 | unexpected indent | `self.mamba_dt_rank = math.ceil(self.hidden_size / 16) if mamba_dt_rank == "auto" else mamba_dt_rank` |
| 2864 | venv_creative/lib/python3.13/site-packages/transformers/models/zamba/modeling_zamba.py | 39 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 2865 | venv_creative/lib/python3.13/site-packages/transformers/models/mamba/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mamba import *` |
| 2866 | venv_creative/lib/python3.13/site-packages/transformers/models/mamba/configuration_mamba.py | 136 | 12 | unexpected indent | `self.intermediate_size = int(expand * self.hidden_size)` |
| 2867 | venv_creative/lib/python3.13/site-packages/transformers/models/stablelm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_stablelm import *` |
| 2868 | venv_creative/lib/python3.13/site-packages/transformers/models/speech_encoder_decoder/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_speech_encoder_decoder import *` |
| 2869 | venv_creative/lib/python3.13/site-packages/transformers/models/zoedepth/image_processing_zoedepth.py | 35 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_torch_available,` |
| 2870 | venv_creative/lib/python3.13/site-packages/transformers/models/zoedepth/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_zoedepth import *` |
| 2871 | venv_creative/lib/python3.13/site-packages/transformers/models/zoedepth/modeling_zoedepth.py | 1104 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 1094 | `}` |
| 2872 | venv_creative/lib/python3.13/site-packages/transformers/models/seamless_m4t/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_seamless_m4t import *` |
| 2873 | venv_creative/lib/python3.13/site-packages/transformers/models/herbert/__init__.py | 21 | 8 | unexpected indent | `from .tokenization_herbert_fast import *` |
| 2874 | venv_creative/lib/python3.13/site-packages/transformers/models/umt5/configuration_umt5.py | 122 | 12 | unexpected indent | `self.feed_forward_proj = feed_forward_proj` |
| 2875 | venv_creative/lib/python3.13/site-packages/transformers/models/umt5/__init__.py | 21 | 8 | unexpected indent | `from .modeling_umt5 import *` |
| 2876 | venv_creative/lib/python3.13/site-packages/transformers/models/cohere2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_cohere2 import *` |
| 2877 | venv_creative/lib/python3.13/site-packages/transformers/models/apertus/__init__.py | 26 | 8 | unexpected indent | `from .modeling_apertus import *` |
| 2878 | venv_creative/lib/python3.13/site-packages/transformers/models/pegasus_x/__init__.py | 21 | 8 | unexpected indent | `from .modeling_pegasus_x import *` |
| 2879 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlmv2/tokenization_layoutlmv2.py | 600 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 574 | `) -> BatchEncoding:` |
| 2880 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlmv2/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_layoutlmv2 import *` |
| 2881 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlmv2/processing_layoutlmv2.py | 28 | 1 | invalid syntax | `from ...utils import TensorType` |
| 2882 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlmv2/tokenization_layoutlmv2_fast.py | 352 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 326 | `) -> BatchEncoding:` |
| 2883 | venv_creative/lib/python3.13/site-packages/transformers/models/dinov3_vit/modeling_dinov3_vit.py | 59 | 5 | invalid syntax | `def forward(self, pixel_values: torch.Tensor, bool_masked_pos: Optional[torch.Tensor] = None) -> torch.Tensor:` |
| 2884 | venv_creative/lib/python3.13/site-packages/transformers/models/dinov3_vit/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_dinov3_vit_fast import *` |
| 2885 | venv_creative/lib/python3.13/site-packages/transformers/models/granitemoehybrid/configuration_granitemoehybrid.py | 237 | 12 | unexpected indent | `self.layer_types = layer_types` |
| 2886 | venv_creative/lib/python3.13/site-packages/transformers/models/granitemoehybrid/__init__.py | 23 | 8 | unexpected indent | `from .modeling_granitemoehybrid import *` |
| 2887 | venv_creative/lib/python3.13/site-packages/transformers/models/granitemoehybrid/modeling_granitemoehybrid.py | 37 | 1 | invalid syntax | `from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS, dynamic_rope_update` |
| 2888 | venv_creative/lib/python3.13/site-packages/transformers/models/unispeech_sat/__init__.py | 21 | 8 | unexpected indent | `from .modeling_unispeech_sat import *` |
| 2889 | venv_creative/lib/python3.13/site-packages/transformers/models/t5/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_t5 import *` |
| 2890 | venv_creative/lib/python3.13/site-packages/transformers/models/t5/configuration_t5.py | 120 | 12 | unexpected indent | `self.feed_forward_proj = feed_forward_proj` |
| 2891 | venv_creative/lib/python3.13/site-packages/transformers/models/t5/modeling_tf_t5.py | 35 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss, TFModelInputType,` |
| 2892 | venv_creative/lib/python3.13/site-packages/transformers/models/granite_speech/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_granite_speech import *` |
| 2893 | venv_creative/lib/python3.13/site-packages/transformers/models/granite_speech/configuration_granite_speech.py | 105 | 12 | unexpected indent | `self.max_pos_emb = max_pos_emb` |
| 2894 | venv_creative/lib/python3.13/site-packages/transformers/models/dpr/modeling_dpr.py | 45 | 1 | invalid syntax | `class DPRContextEncoderOutput(ModelOutput):` |
| 2895 | venv_creative/lib/python3.13/site-packages/transformers/models/dpr/__init__.py | 21 | 8 | unexpected indent | `from .modeling_dpr import *` |
| 2896 | venv_creative/lib/python3.13/site-packages/transformers/models/recurrent_gemma/__init__.py | 21 | 8 | unexpected indent | `from .modeling_recurrent_gemma import *` |
| 2897 | venv_creative/lib/python3.13/site-packages/transformers/models/recurrent_gemma/configuration_recurrent_gemma.py | 138 | 12 | unexpected indent | `self.block_types = list(block_types)` |
| 2898 | venv_creative/lib/python3.13/site-packages/transformers/models/recurrent_gemma/modeling_recurrent_gemma.py | 178 | 5 | invalid syntax | `def forward(` |
| 2899 | venv_creative/lib/python3.13/site-packages/transformers/models/minimax/modular_minimax.py | 45 | 8 | invalid syntax | `logger = logging.get_logger(__name__)` |
| 2900 | venv_creative/lib/python3.13/site-packages/transformers/models/minimax/configuration_minimax.py | 192 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.vocab_size = vocab_size` |
| 2901 | venv_creative/lib/python3.13/site-packages/transformers/models/minimax/__init__.py | 23 | 8 | unexpected indent | `from .modeling_minimax import *` |
| 2902 | venv_creative/lib/python3.13/site-packages/transformers/models/minimax/modeling_minimax.py | 42 | 1 | invalid syntax | `from ...modeling_outputs import MoeCausalLMOutputWithPast, MoeModelOutputWithPast` |
| 2903 | venv_creative/lib/python3.13/site-packages/transformers/models/rwkv/__init__.py | 21 | 8 | unexpected indent | `from .modeling_rwkv import *` |
| 2904 | venv_creative/lib/python3.13/site-packages/transformers/models/jamba/configuration_jamba.py | 204 | 12 | unexpected indent | `self.mamba_dt_rank = math.ceil(self.hidden_size / 16) if mamba_dt_rank == "auto" else mamba_dt_rank` |
| 2905 | venv_creative/lib/python3.13/site-packages/transformers/models/jamba/__init__.py | 21 | 8 | unexpected indent | `from .modeling_jamba import *` |
| 2906 | venv_creative/lib/python3.13/site-packages/transformers/models/jamba/modeling_jamba.py | 37 | 1 | invalid syntax | `from ...modeling_layers import (GenericForSequenceClassification,` |
| 2907 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlmv3/tokenization_layoutlmv3.py | 765 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 739 | `) -> BatchEncoding:` |
| 2908 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlmv3/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_layoutlmv3 import *` |
| 2909 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlmv3/tokenization_layoutlmv3_fast.py | 395 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 369 | `) -> BatchEncoding:` |
| 2910 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlmv3/image_processing_layoutlmv3.py | 31 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs,` |
| 2911 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlmv3/processing_layoutlmv3.py | 28 | 1 | invalid syntax | `from ...utils import TensorType` |
| 2912 | venv_creative/lib/python3.13/site-packages/transformers/models/bloom/modeling_flax_bloom.py | 35 | 1 | invalid syntax | `from ...modeling_flax_utils import FlaxPreTrainedModel, append_call_sample_docstring` |
| 2913 | venv_creative/lib/python3.13/site-packages/transformers/models/bloom/__init__.py | 21 | 8 | unexpected indent | `from .modeling_bloom import *` |
| 2914 | venv_creative/lib/python3.13/site-packages/transformers/models/bloom/modeling_bloom.py | 38 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2915 | venv_creative/lib/python3.13/site-packages/transformers/models/phimoe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_phimoe import *` |
| 2916 | venv_creative/lib/python3.13/site-packages/transformers/models/nllb/__init__.py | 21 | 8 | unexpected indent | `from .tokenization_nllb_fast import *` |
| 2917 | venv_creative/lib/python3.13/site-packages/transformers/models/xlm_roberta/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_xlm_roberta import *` |
| 2918 | venv_creative/lib/python3.13/site-packages/transformers/models/xlm_roberta/modeling_tf_xlm_roberta.py | 35 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss,` |
| 2919 | venv_creative/lib/python3.13/site-packages/transformers/models/clipseg/configuration_clipseg.py | 116 | 12 | unexpected indent | `self.attention_dropout = attention_dropout` |
| 2920 | venv_creative/lib/python3.13/site-packages/transformers/models/clipseg/__init__.py | 21 | 8 | unexpected indent | `from .modeling_clipseg import *` |
| 2921 | venv_creative/lib/python3.13/site-packages/transformers/models/clipseg/processing_clipseg.py | 54 | 33 | invalid syntax. Perhaps you forgot a comma? | `feature_extractor = kwargs.pop("feature_extractor")` |
| 2922 | venv_creative/lib/python3.13/site-packages/transformers/models/clipseg/modeling_clipseg.py | 31 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 2923 | venv_creative/lib/python3.13/site-packages/transformers/models/code_llama/__init__.py | 21 | 8 | unexpected indent | `from .tokenization_code_llama_fast import *` |
| 2924 | venv_creative/lib/python3.13/site-packages/transformers/models/efficientnet/configuration_efficientnet.py | 136 | 12 | unexpected indent | `self.kernel_sizes = kernel_sizes` |
| 2925 | venv_creative/lib/python3.13/site-packages/transformers/models/efficientnet/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_efficientnet import *` |
| 2926 | venv_creative/lib/python3.13/site-packages/transformers/models/efficientnet/image_processing_efficientnet.py | 30 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2927 | venv_creative/lib/python3.13/site-packages/transformers/models/efficientnet/modeling_efficientnet.py | 31 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2928 | venv_creative/lib/python3.13/site-packages/transformers/models/mgp_str/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mgp_str import *` |
| 2929 | venv_creative/lib/python3.13/site-packages/transformers/models/mgp_str/processing_mgp_str.py | 64 | 26 | '(' was never closed | `warnings.warn(` |
| 2930 | venv_creative/lib/python3.13/site-packages/transformers/models/mgp_str/modeling_mgp_str.py | 53 | 8 | unexpected indent | `return output` |
| 2931 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilebert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mobilebert import *` |
| 2932 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilebert/modeling_tf_mobilebert.py | 34 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 2933 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilebert/modeling_mobilebert.py | 41 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2934 | venv_creative/lib/python3.13/site-packages/transformers/models/informer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_informer import *` |
| 2935 | venv_creative/lib/python3.13/site-packages/transformers/models/informer/configuration_informer.py | 193 | 21 | invalid syntax. Perhaps you forgot a comma? | `"The cardinality should be a list of the same length as `num_static_categorical_features`"` |
| 2936 | venv_creative/lib/python3.13/site-packages/transformers/models/informer/modeling_informer.py | 36 | 1 | invalid syntax | `from ...modeling_flash_attention_utils import FlashAttentionKwargs` |
| 2937 | venv_creative/lib/python3.13/site-packages/transformers/models/informer/modular_informer.py | 30 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 2938 | venv_creative/lib/python3.13/site-packages/transformers/models/kosmos2/modeling_kosmos2.py | 36 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 2939 | venv_creative/lib/python3.13/site-packages/transformers/models/kosmos2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_kosmos2 import *` |
| 2940 | venv_creative/lib/python3.13/site-packages/transformers/models/kosmos2/configuration_kosmos2.py | 108 | 25 | '(' was never closed | `super().__init__(` |
| 2941 | venv_creative/lib/python3.13/site-packages/transformers/models/blip/image_processing_blip.py | 30 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2942 | venv_creative/lib/python3.13/site-packages/transformers/models/blip/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_blip import *` |
| 2943 | venv_creative/lib/python3.13/site-packages/transformers/models/rag/__init__.py | 21 | 8 | unexpected indent | `from .modeling_rag import *` |
| 2944 | venv_creative/lib/python3.13/site-packages/transformers/models/rag/modeling_tf_rag.py | 32 | 1 | invalid syntax | `from ...utils import (ModelOutput, add_start_docstrings_to_model_forward, logging,` |
| 2945 | venv_creative/lib/python3.13/site-packages/transformers/models/rag/retrieval_rag.py | 31 | 1 | invalid syntax | `from .configuration_rag import RagConfig` |
| 2946 | venv_creative/lib/python3.13/site-packages/transformers/models/rag/tokenization_rag.py | 34 | 12 | unexpected indent | `self.current_tokenizer = self.question_encoder` |
| 2947 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilevitv2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mobilevitv2 import *` |
| 2948 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilevitv2/modeling_mobilevitv2.py | 34 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2949 | venv_creative/lib/python3.13/site-packages/transformers/models/modernbert/configuration_modernbert.py | 185 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.vocab_size = vocab_size` |
| 2950 | venv_creative/lib/python3.13/site-packages/transformers/models/modernbert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_modernbert import *` |
| 2951 | venv_creative/lib/python3.13/site-packages/transformers/models/modernbert/modeling_modernbert.py | 41 | 1 | invalid syntax | `from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS, dynamic_rope_update` |
| 2952 | venv_creative/lib/python3.13/site-packages/transformers/models/modernbert/modular_modernbert.py | 37 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 2953 | venv_creative/lib/python3.13/site-packages/transformers/models/codegen/__init__.py | 21 | 8 | unexpected indent | `from .modeling_codegen import *` |
| 2954 | venv_creative/lib/python3.13/site-packages/transformers/models/deit/modeling_deit.py | 31 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 2955 | venv_creative/lib/python3.13/site-packages/transformers/models/deit/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_deit import *` |
| 2956 | venv_creative/lib/python3.13/site-packages/transformers/models/deit/image_processing_deit.py | 30 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2957 | venv_creative/lib/python3.13/site-packages/transformers/models/deit/modeling_tf_deit.py | 31 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFPreTrainedModel, TFSequenceClassificationLoss,` |
| 2958 | venv_creative/lib/python3.13/site-packages/transformers/models/dpt/modular_dpt.py | 26 | 1 | invalid syntax | `from ...image_transforms import group_images_by_shape, reorder_images` |
| 2959 | venv_creative/lib/python3.13/site-packages/transformers/models/dpt/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_dpt import *` |
| 2960 | venv_creative/lib/python3.13/site-packages/transformers/models/dpt/image_processing_dpt.py | 38 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2961 | venv_creative/lib/python3.13/site-packages/transformers/models/dpt/modeling_dpt.py | 37 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 2962 | venv_creative/lib/python3.13/site-packages/transformers/models/dpt/image_processing_dpt_fast.py | 32 | 1 | invalid syntax | `from ...image_transforms import group_images_by_shape, reorder_images` |
| 2963 | venv_creative/lib/python3.13/site-packages/transformers/models/wav2vec2/processing_wav2vec2.py | 55 | 12 | unexpected indent | `self._in_target_context_manager = False` |
| 2964 | venv_creative/lib/python3.13/site-packages/transformers/models/wav2vec2/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_wav2vec2 import *` |
| 2965 | venv_creative/lib/python3.13/site-packages/transformers/models/voxtral/__init__.py | 22 | 8 | unexpected indent | `from .modeling_voxtral import *` |
| 2966 | venv_creative/lib/python3.13/site-packages/transformers/models/fastspeech2_conformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_fastspeech2_conformer import *` |
| 2967 | venv_creative/lib/python3.13/site-packages/transformers/models/fastspeech2_conformer/modeling_fastspeech2_conformer.py | 33 | 8 | invalid syntax | `logger = logging.get_logger(__name__)` |
| 2968 | venv_creative/lib/python3.13/site-packages/transformers/models/fastspeech2_conformer/configuration_fastspeech2_conformer.py | 235 | 40 | invalid syntax | `if encoder_kernel_size % 2 == 0:` |
| 2969 | venv_creative/lib/python3.13/site-packages/transformers/models/siglip/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_siglip import *` |
| 2970 | venv_creative/lib/python3.13/site-packages/transformers/models/siglip/image_processing_siglip.py | 28 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2971 | venv_creative/lib/python3.13/site-packages/transformers/models/moonshine/__init__.py | 21 | 8 | unexpected indent | `from .modeling_moonshine import *` |
| 2972 | venv_creative/lib/python3.13/site-packages/transformers/models/moonshine/modeling_moonshine.py | 36 | 1 | invalid syntax | `from ...modeling_flash_attention_utils import FlashAttentionKwargs` |
| 2973 | venv_creative/lib/python3.13/site-packages/transformers/models/moonshine/configuration_moonshine.py | 221 | 12 | unexpected indent | `self.is_encoder_decoder = is_encoder_decoder` |
| 2974 | venv_creative/lib/python3.13/site-packages/transformers/models/moonshine/modular_moonshine.py | 30 | 1 | invalid syntax | `from ...modeling_flash_attention_utils import FlashAttentionKwargs` |
| 2975 | venv_creative/lib/python3.13/site-packages/transformers/models/colpali/__init__.py | 21 | 8 | unexpected indent | `from .modeling_colpali import *` |
| 2976 | venv_creative/lib/python3.13/site-packages/transformers/models/pegasus/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_pegasus import *` |
| 2977 | venv_creative/lib/python3.13/site-packages/transformers/models/pegasus/modeling_tf_pegasus.py | 31 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss, TFModelInputType,` |
| 2978 | venv_creative/lib/python3.13/site-packages/transformers/models/qwen2_5_vl/__init__.py | 21 | 8 | unexpected indent | `from .modeling_qwen2_5_vl import *` |
| 2979 | venv_creative/lib/python3.13/site-packages/transformers/models/bart/__init__.py | 21 | 8 | unexpected indent | `from .modeling_bart import *` |
| 2980 | venv_creative/lib/python3.13/site-packages/transformers/models/doge/__init__.py | 22 | 8 | unexpected indent | `from .modeling_doge import *` |
| 2981 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_vl/image_processing_deepseek_vl_fast.py | 31 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, PILImageResampling,` |
| 2982 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_vl/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_deepseek_vl import *` |
| 2983 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_vl/image_processing_deepseek_vl.py | 34 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2984 | venv_creative/lib/python3.13/site-packages/transformers/models/yoso/__init__.py | 21 | 8 | unexpected indent | `from .modeling_yoso import *` |
| 2985 | venv_creative/lib/python3.13/site-packages/transformers/models/timm_wrapper/modeling_timm_wrapper.py | 42 | 1 | invalid syntax | `class TimmWrapperModelOutput(ModelOutput):` |
| 2986 | venv_creative/lib/python3.13/site-packages/transformers/models/timm_wrapper/__init__.py | 21 | 8 | unexpected indent | `from .modeling_timm_wrapper import *` |
| 2987 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_v2/modeling_deepseek_v2.py | 38 | 1 | invalid syntax | `from ...modeling_outputs import BaseModelOutputWithPast, CausalLMOutputWithPast` |
| 2988 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_v2/__init__.py | 22 | 8 | unexpected indent | `from .modeling_deepseek_v2 import *` |
| 2989 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_v2/modular_deepseek_v2.py | 36 | 8 | invalid syntax | `logger = logging.get_logger(__name__)` |
| 2990 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_v2/configuration_deepseek_v2.py | 186 | 25 | '(' was never closed | `super().__init__(` |
| 2991 | venv_creative/lib/python3.13/site-packages/transformers/models/janus/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_janus import *` |
| 2992 | venv_creative/lib/python3.13/site-packages/transformers/models/janus/modular_janus.py | 32 | 1 | invalid syntax | `from ...generation.utils import GenerateDecoderOnlyOutput` |
| 2993 | venv_creative/lib/python3.13/site-packages/transformers/models/janus/image_processing_janus.py | 36 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 2994 | venv_creative/lib/python3.13/site-packages/transformers/models/janus/image_processing_janus_fast.py | 24 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ImageInput,` |
| 2995 | venv_creative/lib/python3.13/site-packages/transformers/models/mamba2/configuration_mamba2.py | 143 | 17 | invalid syntax. Perhaps you forgot a comma? | `"Inconsistent configuration: hidden_size * expand "` |
| 2996 | venv_creative/lib/python3.13/site-packages/transformers/models/mamba2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mamba2 import *` |
| 2997 | venv_creative/lib/python3.13/site-packages/transformers/models/switch_transformers/configuration_switch_transformers.py | 170 | 12 | unexpected indent | `self.use_cache = use_cache` |
| 2998 | venv_creative/lib/python3.13/site-packages/transformers/models/switch_transformers/__init__.py | 21 | 8 | unexpected indent | `from .modeling_switch_transformers import *` |
| 2999 | venv_creative/lib/python3.13/site-packages/transformers/models/autoformer/modeling_autoformer.py | 34 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 3000 | venv_creative/lib/python3.13/site-packages/transformers/models/autoformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_autoformer import *` |
| 3001 | venv_creative/lib/python3.13/site-packages/transformers/models/camembert/modeling_tf_camembert.py | 35 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss,` |
| 3002 | venv_creative/lib/python3.13/site-packages/transformers/models/camembert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_camembert import *` |
| 3003 | venv_creative/lib/python3.13/site-packages/transformers/models/gemma3n/modular_gemma3n.py | 43 | 1 | invalid syntax | `from ..gemma3.modeling_gemma3 import (Gemma3Attention, Gemma3DecoderLayer,` |
| 3004 | venv_creative/lib/python3.13/site-packages/transformers/models/gemma3n/feature_extraction_gemma3n.py | 188 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.min_frequency = min_frequency` |
| 3005 | venv_creative/lib/python3.13/site-packages/transformers/models/gemma3n/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_gemma3n import *` |
| 3006 | venv_creative/lib/python3.13/site-packages/transformers/models/gemma3n/configuration_gemma3n.py | 244 | 9 | invalid syntax | `if isinstance(intermediate_size, Sequence) and (intsize_len := len(intermediate_size)) != num_hidden_layers:` |
| 3007 | venv_creative/lib/python3.13/site-packages/transformers/models/roformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_roformer import *` |
| 3008 | venv_creative/lib/python3.13/site-packages/transformers/models/roformer/modeling_tf_roformer.py | 32 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss,` |
| 3009 | venv_creative/lib/python3.13/site-packages/transformers/models/timesformer/modeling_timesformer.py | 114 | 73 | invalid syntax. Perhaps you forgot a comma? | `other_pos_embed, size=(patch_height, patch_width), mode="nearest"` |
| 3010 | venv_creative/lib/python3.13/site-packages/transformers/models/timesformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_timesformer import *` |
| 3011 | venv_creative/lib/python3.13/site-packages/transformers/models/deformable_detr/image_processing_deformable_detr.py | 32 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 3012 | venv_creative/lib/python3.13/site-packages/transformers/models/deformable_detr/__init__.py | 22 | 8 | unexpected indent | `from .feature_extraction_deformable_detr import *` |
| 3013 | venv_creative/lib/python3.13/site-packages/transformers/models/depth_pro/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_depth_pro import *` |
| 3014 | venv_creative/lib/python3.13/site-packages/transformers/models/depth_pro/image_processing_depth_pro.py | 35 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs,` |
| 3015 | venv_creative/lib/python3.13/site-packages/transformers/models/align/modeling_align.py | 32 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3016 | venv_creative/lib/python3.13/site-packages/transformers/models/align/__init__.py | 21 | 8 | unexpected indent | `from .modeling_align import *` |
| 3017 | venv_creative/lib/python3.13/site-packages/transformers/models/align/configuration_align.py | 240 | 12 | unexpected indent | `self.kernel_sizes = kernel_sizes` |
| 3018 | venv_creative/lib/python3.13/site-packages/transformers/models/align/processing_align.py | 118 | 43 | '(' was never closed | `output_kwargs = self._merge_kwargs(` |
| 3019 | venv_creative/lib/python3.13/site-packages/transformers/models/modernbert_decoder/configuration_modernbert_decoder.py | 159 | 25 | '(' was never closed | `super().__init__(` |
| 3020 | venv_creative/lib/python3.13/site-packages/transformers/models/modernbert_decoder/__init__.py | 21 | 8 | unexpected indent | `from .modeling_modernbert_decoder import *` |
| 3021 | venv_creative/lib/python3.13/site-packages/transformers/models/modernbert_decoder/modeling_modernbert_decoder.py | 39 | 1 | invalid syntax | `from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS, dynamic_rope_update` |
| 3022 | venv_creative/lib/python3.13/site-packages/transformers/models/modernbert_decoder/modular_modernbert_decoder.py | 33 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS` |
| 3023 | venv_creative/lib/python3.13/site-packages/transformers/models/d_fine/__init__.py | 22 | 8 | unexpected indent | `from .modeling_d_fine import *` |
| 3024 | venv_creative/lib/python3.13/site-packages/transformers/models/vit/image_processing_vit.py | 30 | 1 | invalid syntax | `from ...utils import TensorType, filter_out_non_signature_kwargs, logging` |
| 3025 | venv_creative/lib/python3.13/site-packages/transformers/models/vit/modeling_vit.py | 31 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3026 | venv_creative/lib/python3.13/site-packages/transformers/models/vit/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_vit import *` |
| 3027 | venv_creative/lib/python3.13/site-packages/transformers/models/vit/modeling_tf_vit.py | 30 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFModelInputType, TFPreTrainedModel,` |
| 3028 | venv_creative/lib/python3.13/site-packages/transformers/models/segformer/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_segformer import *` |
| 3029 | venv_creative/lib/python3.13/site-packages/transformers/models/segformer/modeling_segformer.py | 30 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3030 | venv_creative/lib/python3.13/site-packages/transformers/models/segformer/modeling_tf_segformer.py | 29 | 1 | invalid syntax | `from ...modeling_tf_outputs import (TFBaseModelOutput, TFSemanticSegmenterOutput,` |
| 3031 | venv_creative/lib/python3.13/site-packages/transformers/models/segformer/image_processing_segformer.py | 25 | 1 | invalid syntax | `from ...image_transforms import resize, to_channel_dimension_format` |
| 3032 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt_neo/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_gpt_neo import *` |
| 3033 | venv_creative/lib/python3.13/site-packages/transformers/models/vitmatte/image_processing_vitmatte.py | 30 | 1 | invalid syntax | `from ...utils import TensorType, filter_out_non_signature_kwargs, logging` |
| 3034 | venv_creative/lib/python3.13/site-packages/transformers/models/vitmatte/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_vitmatte import *` |
| 3035 | venv_creative/lib/python3.13/site-packages/transformers/models/paligemma/__init__.py | 21 | 8 | unexpected indent | `from .modeling_paligemma import *` |
| 3036 | venv_creative/lib/python3.13/site-packages/transformers/models/dbrx/__init__.py | 21 | 8 | unexpected indent | `from .modeling_dbrx import *` |
| 3037 | venv_creative/lib/python3.13/site-packages/transformers/models/encoder_decoder/__init__.py | 21 | 8 | unexpected indent | `from .modeling_encoder_decoder import *` |
| 3038 | venv_creative/lib/python3.13/site-packages/transformers/models/barthez/__init__.py | 21 | 8 | unexpected indent | `from .tokenization_barthez_fast import *` |
| 3039 | venv_creative/lib/python3.13/site-packages/transformers/models/xlm/modeling_tf_xlm.py | 34 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFModelInputType, TFMultipleChoiceLoss,` |
| 3040 | venv_creative/lib/python3.13/site-packages/transformers/models/xlm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_tf_xlm import *` |
| 3041 | venv_creative/lib/python3.13/site-packages/transformers/models/bert/modeling_tf_bert.py | 37 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss,` |
| 3042 | venv_creative/lib/python3.13/site-packages/transformers/models/bert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_bert import *` |
| 3043 | venv_creative/lib/python3.13/site-packages/transformers/models/xlstm/configuration_xlstm.py | 30 | 20 | invalid syntax | `external_xlstm = True` |
| 3044 | venv_creative/lib/python3.13/site-packages/transformers/models/xlstm/__init__.py | 21 | 8 | unexpected indent | `from modeling_xlstm import *` |
| 3045 | venv_creative/lib/python3.13/site-packages/transformers/models/mistral3/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mistral3 import *` |
| 3046 | venv_creative/lib/python3.13/site-packages/transformers/models/musicgen/configuration_musicgen.py | 116 | 12 | unexpected indent | `self.layerdrop = layerdrop` |
| 3047 | venv_creative/lib/python3.13/site-packages/transformers/models/musicgen/modeling_musicgen.py | 35 | 1 | invalid syntax | `from ...modeling_attn_mask_utils import (_prepare_4d_attention_mask,` |
| 3048 | venv_creative/lib/python3.13/site-packages/transformers/models/musicgen/__init__.py | 21 | 8 | unexpected indent | `from .modeling_musicgen import *` |
| 3049 | venv_creative/lib/python3.13/site-packages/transformers/models/musicgen/processing_musicgen.py | 49 | 12 | unexpected indent | `self._in_target_context_manager = False` |
| 3050 | venv_creative/lib/python3.13/site-packages/transformers/models/plbart/__init__.py | 21 | 8 | unexpected indent | `from .modeling_plbart import *` |
| 3051 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_v3/modeling_deepseek_v3.py | 24 | 1 | invalid syntax | `from ...modeling_outputs import BaseModelOutputWithPast, CausalLMOutputWithPast` |
| 3052 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_v3/modular_deepseek_v3.py | 23 | 1 | invalid syntax | `from .configuration_deepseek_v3 import DeepseekV3Config` |
| 3053 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_v3/__init__.py | 21 | 8 | unexpected indent | `from .modeling_deepseek_v3 import *` |
| 3054 | venv_creative/lib/python3.13/site-packages/transformers/models/deepseek_v3/configuration_deepseek_v3.py | 209 | 12 | unexpected indent | `self.kv_lora_rank = kv_lora_rank` |
| 3055 | venv_creative/lib/python3.13/site-packages/transformers/models/ovis2/__init__.py | 23 | 8 | unexpected indent | `from .image_processing_ovis2 import *` |
| 3056 | venv_creative/lib/python3.13/site-packages/transformers/models/ovis2/image_processing_ovis2.py | 30 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 3057 | venv_creative/lib/python3.13/site-packages/transformers/models/wav2vec2_conformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_wav2vec2_conformer import *` |
| 3058 | venv_creative/lib/python3.13/site-packages/transformers/models/aria/modular_aria.py | 27 | 1 | invalid syntax | `from ...image_transforms import (PaddingMode, convert_to_rgb, pad, resize,` |
| 3059 | venv_creative/lib/python3.13/site-packages/transformers/models/aria/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_aria import *` |
| 3060 | venv_creative/lib/python3.13/site-packages/transformers/models/aria/image_processing_aria.py | 30 | 1 | invalid syntax | `from ...image_transforms import (PaddingMode, convert_to_rgb, pad, resize,` |
| 3061 | venv_creative/lib/python3.13/site-packages/transformers/models/owlvit/processing_owlvit.py | 37 | 1 | invalid syntax | `class OwlViTImagesKwargs(ImagesKwargs, total = False):` |
| 3062 | venv_creative/lib/python3.13/site-packages/transformers/models/owlvit/modeling_owlvit.py | 30 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 3063 | venv_creative/lib/python3.13/site-packages/transformers/models/owlvit/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_owlvit import *` |
| 3064 | venv_creative/lib/python3.13/site-packages/transformers/models/owlvit/image_processing_owlvit.py | 27 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 3065 | venv_creative/lib/python3.13/site-packages/transformers/models/vipllava/__init__.py | 21 | 8 | unexpected indent | `from .modeling_vipllava import *` |
| 3066 | venv_creative/lib/python3.13/site-packages/transformers/models/ernie4_5_moe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_ernie4_5_moe import *` |
| 3067 | venv_creative/lib/python3.13/site-packages/transformers/models/ijepa/modeling_ijepa.py | 19 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3068 | venv_creative/lib/python3.13/site-packages/transformers/models/ijepa/__init__.py | 21 | 8 | unexpected indent | `from .modeling_ijepa import *` |
| 3069 | venv_creative/lib/python3.13/site-packages/transformers/models/idefics3/image_processing_idefics3.py | 27 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 3070 | venv_creative/lib/python3.13/site-packages/transformers/models/idefics3/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_idefics3 import *` |
| 3071 | venv_creative/lib/python3.13/site-packages/transformers/models/idefics3/modeling_idefics3.py | 49 | 1 | invalid syntax | `class Idefics3BaseModelOutputWithPast(ModelOutput):` |
| 3072 | venv_creative/lib/python3.13/site-packages/transformers/models/patchtst/modeling_patchtst.py | 93 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"embed_dim must be divisible by num_heads (got `embed_dim`: {self.embed_dim}"` |
| 3073 | venv_creative/lib/python3.13/site-packages/transformers/models/patchtst/__init__.py | 21 | 8 | unexpected indent | `from .modeling_patchtst import *` |
| 3074 | venv_creative/lib/python3.13/site-packages/transformers/models/blenderbot/__init__.py | 21 | 8 | unexpected indent | `from .modeling_blenderbot import *` |
| 3075 | venv_creative/lib/python3.13/site-packages/transformers/models/musicgen_melody/configuration_musicgen_melody.py | 118 | 12 | unexpected indent | `self.layerdrop = layerdrop` |
| 3076 | venv_creative/lib/python3.13/site-packages/transformers/models/musicgen_melody/__init__.py | 21 | 8 | unexpected indent | `from .modeling_musicgen_melody import *` |
| 3077 | venv_creative/lib/python3.13/site-packages/transformers/models/musicgen_melody/modeling_musicgen_melody.py | 35 | 1 | invalid syntax | `from ...modeling_attn_mask_utils import (_prepare_4d_causal_attention_mask,` |
| 3078 | venv_creative/lib/python3.13/site-packages/transformers/models/clap/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_clap import *` |
| 3079 | venv_creative/lib/python3.13/site-packages/transformers/models/clap/modeling_clap.py | 32 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3080 | venv_creative/lib/python3.13/site-packages/transformers/models/clap/configuration_clap.py | 133 | 12 | unexpected indent | `self.layer_norm_eps = layer_norm_eps` |
| 3081 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilevit/modeling_mobilevit.py | 35 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3082 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilevit/image_processing_mobilevit.py | 26 | 1 | invalid syntax | `from ...image_utils import (ChannelDimension, ImageInput, PILImageResampling,` |
| 3083 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilevit/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_mobilevit import *` |
| 3084 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilevit/modeling_tf_mobilevit.py | 29 | 1 | invalid syntax | `from ...modeling_tf_outputs import (TFBaseModelOutput, TFBaseModelOutputWithPooling,` |
| 3085 | venv_creative/lib/python3.13/site-packages/transformers/models/idefics/processing_idefics.py | 264 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 251 | `) -> BatchFeature:` |
| 3086 | venv_creative/lib/python3.13/site-packages/transformers/models/idefics/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_idefics import *` |
| 3087 | venv_creative/lib/python3.13/site-packages/transformers/models/idefics/image_processing_idefics.py | 27 | 1 | invalid syntax | `from ...utils import TensorType, is_torch_available` |
| 3088 | venv_creative/lib/python3.13/site-packages/transformers/models/idefics/configuration_idefics.py | 101 | 12 | unexpected indent | `self.hidden_act = hidden_act` |
| 3089 | venv_creative/lib/python3.13/site-packages/transformers/models/convbert/modeling_tf_convbert.py | 29 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 3090 | venv_creative/lib/python3.13/site-packages/transformers/models/convbert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_convbert import *` |
| 3091 | venv_creative/lib/python3.13/site-packages/transformers/models/moshi/__init__.py | 21 | 8 | unexpected indent | `from .modeling_moshi import *` |
| 3092 | venv_creative/lib/python3.13/site-packages/transformers/models/moshi/modeling_moshi.py | 34 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 3093 | venv_creative/lib/python3.13/site-packages/transformers/models/hiera/__init__.py | 21 | 8 | unexpected indent | `from .modeling_hiera import *` |
| 3094 | venv_creative/lib/python3.13/site-packages/transformers/models/hiera/modeling_hiera.py | 33 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3095 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilenet_v2/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_mobilenet_v2 import *` |
| 3096 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilenet_v2/image_processing_mobilenet_v2.py | 26 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 3097 | venv_creative/lib/python3.13/site-packages/transformers/models/mobilenet_v2/modeling_mobilenet_v2.py | 29 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3098 | venv_creative/lib/python3.13/site-packages/transformers/models/vision_encoder_decoder/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_vision_encoder_decoder import *` |
| 3099 | venv_creative/lib/python3.13/site-packages/transformers/models/chinese_clip/processing_chinese_clip.py | 61 | 33 | invalid syntax. Perhaps you forgot a comma? | `feature_extractor = kwargs.pop("feature_extractor")` |
| 3100 | venv_creative/lib/python3.13/site-packages/transformers/models/chinese_clip/modeling_chinese_clip.py | 30 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3101 | venv_creative/lib/python3.13/site-packages/transformers/models/chinese_clip/image_processing_chinese_clip.py | 26 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 3102 | venv_creative/lib/python3.13/site-packages/transformers/models/chinese_clip/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_chinese_clip import *` |
| 3103 | venv_creative/lib/python3.13/site-packages/transformers/models/chinese_clip/configuration_chinese_clip.py | 141 | 12 | unexpected indent | `self.layer_norm_eps = layer_norm_eps` |
| 3104 | venv_creative/lib/python3.13/site-packages/transformers/models/vivit/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_vivit import *` |
| 3105 | venv_creative/lib/python3.13/site-packages/transformers/models/vivit/image_processing_vivit.py | 28 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 3106 | venv_creative/lib/python3.13/site-packages/transformers/models/vivit/modeling_vivit.py | 29 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3107 | venv_creative/lib/python3.13/site-packages/transformers/models/csm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_csm import *` |
| 3108 | venv_creative/lib/python3.13/site-packages/transformers/models/csm/generation_csm.py | 27 | 1 | invalid syntax | `from ...generation.logits_process import LogitsProcessorList` |
| 3109 | venv_creative/lib/python3.13/site-packages/transformers/models/csm/processing_csm.py | 182 | 42 | unindent does not match any outer indentation level | `audio = make_list_of_audio(audio)` |
| 3110 | venv_creative/lib/python3.13/site-packages/transformers/models/upernet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_upernet import *` |
| 3111 | venv_creative/lib/python3.13/site-packages/transformers/models/trocr/processing_trocr.py | 63 | 33 | invalid syntax. Perhaps you forgot a comma? | `feature_extractor = kwargs.pop("feature_extractor")` |
| 3112 | venv_creative/lib/python3.13/site-packages/transformers/models/trocr/__init__.py | 21 | 8 | unexpected indent | `from .modeling_trocr import *` |
| 3113 | venv_creative/lib/python3.13/site-packages/transformers/models/hunyuan_v1_dense/__init__.py | 8 | 8 | unexpected indent | `from .modeling_hunyuan_v1_dense import *` |
| 3114 | venv_creative/lib/python3.13/site-packages/transformers/models/efficientloftr/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_efficientloftr import *` |
| 3115 | venv_creative/lib/python3.13/site-packages/transformers/models/efficientloftr/image_processing_efficientloftr.py | 29 | 1 | invalid syntax | `from ...utils import TensorType, logging, requires_backends` |
| 3116 | venv_creative/lib/python3.13/site-packages/transformers/models/efficientloftr/configuration_efficientloftr.py | 154 | 9 | invalid syntax | `self.stage_block_out_channels = [` |
| 3117 | venv_creative/lib/python3.13/site-packages/transformers/models/xcodec/__init__.py | 21 | 8 | unexpected indent | `from .modeling_xcodec import *` |
| 3118 | venv_creative/lib/python3.13/site-packages/transformers/models/smolvlm/modeling_smolvlm.py | 129 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.num_patches_per_side = self.image_size // self.patch_size` |
| 3119 | venv_creative/lib/python3.13/site-packages/transformers/models/smolvlm/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_smolvlm import *` |
| 3120 | venv_creative/lib/python3.13/site-packages/transformers/models/smolvlm/image_processing_smolvlm.py | 33 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 3121 | venv_creative/lib/python3.13/site-packages/transformers/models/unispeech/__init__.py | 21 | 8 | unexpected indent | `from .modeling_unispeech import *` |
| 3122 | venv_creative/lib/python3.13/site-packages/transformers/models/idefics2/image_processing_idefics2.py | 30 | 1 | invalid syntax | `from ...utils import TensorType, is_vision_available, logging` |
| 3123 | venv_creative/lib/python3.13/site-packages/transformers/models/idefics2/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_idefics2 import *` |
| 3124 | venv_creative/lib/python3.13/site-packages/transformers/models/xlm_roberta_xl/__init__.py | 21 | 8 | unexpected indent | `from .modeling_xlm_roberta_xl import *` |
| 3125 | venv_creative/lib/python3.13/site-packages/transformers/models/xlm_roberta_xl/modeling_xlm_roberta_xl.py | 32 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 3126 | venv_creative/lib/python3.13/site-packages/transformers/models/llava_next/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_llava_next import *` |
| 3127 | venv_creative/lib/python3.13/site-packages/transformers/models/llava_next/image_processing_llava_next.py | 27 | 1 | invalid syntax | `from ...image_transforms import (PaddingMode, convert_to_rgb,` |
| 3128 | venv_creative/lib/python3.13/site-packages/transformers/models/seed_oss/__init__.py | 21 | 8 | unexpected indent | `from .modeling_seed_oss import *` |
| 3129 | venv_creative/lib/python3.13/site-packages/transformers/models/altclip/__init__.py | 21 | 8 | unexpected indent | `from .modeling_altclip import *` |
| 3130 | venv_creative/lib/python3.13/site-packages/transformers/models/altclip/configuration_altclip.py | 137 | 12 | unexpected indent | `self.layer_norm_eps = layer_norm_eps` |
| 3131 | venv_creative/lib/python3.13/site-packages/transformers/models/altclip/modeling_altclip.py | 32 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3132 | venv_creative/lib/python3.13/site-packages/transformers/models/imagegpt/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_imagegpt import *` |
| 3133 | venv_creative/lib/python3.13/site-packages/transformers/models/imagegpt/modeling_imagegpt.py | 35 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3134 | venv_creative/lib/python3.13/site-packages/transformers/models/dia/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_dia import *` |
| 3135 | venv_creative/lib/python3.13/site-packages/transformers/models/dia/processing_dia.py | 107 | 24 | invalid syntax | `if text is None:` |
| 3136 | venv_creative/lib/python3.13/site-packages/transformers/models/splinter/__init__.py | 21 | 8 | unexpected indent | `from .modeling_splinter import *` |
| 3137 | venv_creative/lib/python3.13/site-packages/transformers/models/longformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_longformer import *` |
| 3138 | venv_creative/lib/python3.13/site-packages/transformers/models/longformer/modeling_longformer.py | 33 | 1 | invalid syntax | `from ...utils import ModelOutput, auto_docstring, logging` |
| 3139 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutxlm/processing_layoutxlm.py | 28 | 1 | invalid syntax | `from ...utils import TensorType` |
| 3140 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutxlm/tokenization_layoutxlm_fast.py | 475 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 449 | `) -> BatchEncoding:` |
| 3141 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutxlm/tokenization_layoutxlm.py | 649 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 623 | `) -> BatchEncoding:` |
| 3142 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutxlm/__init__.py | 21 | 8 | unexpected indent | `from .tokenization_layoutxlm import *` |
| 3143 | venv_creative/lib/python3.13/site-packages/transformers/models/yolos/modeling_yolos.py | 47 | 1 | invalid syntax | `class YolosObjectDetectionOutput(ModelOutput):` |
| 3144 | venv_creative/lib/python3.13/site-packages/transformers/models/yolos/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_yolos import *` |
| 3145 | venv_creative/lib/python3.13/site-packages/transformers/models/yolos/image_processing_yolos.py | 30 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 3146 | venv_creative/lib/python3.13/site-packages/transformers/models/opt/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_opt import *` |
| 3147 | venv_creative/lib/python3.13/site-packages/transformers/models/nystromformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_nystromformer import *` |
| 3148 | venv_creative/lib/python3.13/site-packages/transformers/models/dinov3_convnext/__init__.py | 21 | 8 | unexpected indent | `from .modeling_dinov3_convnext import *` |
| 3149 | venv_creative/lib/python3.13/site-packages/transformers/models/dinov3_convnext/modeling_dinov3_convnext.py | 53 | 8 | unexpected indent | `return output` |
| 3150 | venv_creative/lib/python3.13/site-packages/transformers/models/decision_transformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_decision_transformer import *` |
| 3151 | venv_creative/lib/python3.13/site-packages/transformers/models/decision_transformer/modeling_decision_transformer.py | 35 | 1 | invalid syntax | `from ...utils import ModelOutput, auto_docstring, logging` |
| 3152 | venv_creative/lib/python3.13/site-packages/transformers/models/beit/modeling_beit.py | 35 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3153 | venv_creative/lib/python3.13/site-packages/transformers/models/beit/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_beit import *` |
| 3154 | venv_creative/lib/python3.13/site-packages/transformers/models/beit/image_processing_beit.py | 25 | 1 | invalid syntax | `from ...image_transforms import resize, to_channel_dimension_format` |
| 3155 | venv_creative/lib/python3.13/site-packages/transformers/models/beit/modeling_flax_beit.py | 32 | 1 | invalid syntax | `from ...modeling_flax_utils import (ACT2FN, FlaxPreTrainedModel,` |
| 3156 | venv_creative/lib/python3.13/site-packages/transformers/models/bamba/__init__.py | 21 | 8 | unexpected indent | `from .modeling_bamba import *` |
| 3157 | venv_creative/lib/python3.13/site-packages/transformers/models/bamba/modular_bamba.py | 32 | 1 | invalid syntax | `from transformers.models.llama.modeling_llama import (LlamaAttention, LlamaForCausalLM,` |
| 3158 | venv_creative/lib/python3.13/site-packages/transformers/models/bamba/configuration_bamba.py | 191 | 12 | unexpected indent | `self.mamba_chunk_size = mamba_chunk_size` |
| 3159 | venv_creative/lib/python3.13/site-packages/transformers/models/bamba/modeling_bamba.py | 53 | 1 | invalid syntax | `else:` |
| 3160 | venv_creative/lib/python3.13/site-packages/transformers/models/timm_backbone/__init__.py | 21 | 8 | unexpected indent | `from .modeling_timm_backbone import *` |
| 3161 | venv_creative/lib/python3.13/site-packages/transformers/models/x_clip/modeling_x_clip.py | 30 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 3162 | venv_creative/lib/python3.13/site-packages/transformers/models/x_clip/configuration_x_clip.py | 110 | 12 | unexpected indent | `self.attention_dropout = attention_dropout` |
| 3163 | venv_creative/lib/python3.13/site-packages/transformers/models/x_clip/processing_x_clip.py | 54 | 33 | invalid syntax. Perhaps you forgot a comma? | `feature_extractor = kwargs.pop("feature_extractor")` |
| 3164 | venv_creative/lib/python3.13/site-packages/transformers/models/x_clip/__init__.py | 21 | 8 | unexpected indent | `from .modeling_x_clip import *` |
| 3165 | venv_creative/lib/python3.13/site-packages/transformers/models/cvt/modeling_tf_cvt.py | 30 | 1 | invalid syntax | `from ...tf_utils import shape_list, stable_softmax` |
| 3166 | venv_creative/lib/python3.13/site-packages/transformers/models/cvt/__init__.py | 21 | 8 | unexpected indent | `from .modeling_cvt import *` |
| 3167 | venv_creative/lib/python3.13/site-packages/transformers/models/cvt/modeling_cvt.py | 44 | 1 | invalid syntax | `class BaseModelOutputWithCLSToken(ModelOutput):` |
| 3168 | venv_creative/lib/python3.13/site-packages/transformers/models/cpm/__init__.py | 21 | 8 | unexpected indent | `from .tokenization_cpm_fast import *` |
| 3169 | venv_creative/lib/python3.13/site-packages/transformers/models/depth_anything/modeling_depth_anything.py | 42 | 12 | unexpected indent | `if factor > 1:` |
| 3170 | venv_creative/lib/python3.13/site-packages/transformers/models/depth_anything/__init__.py | 21 | 8 | unexpected indent | `from .modeling_depth_anything import *` |
| 3171 | venv_creative/lib/python3.13/site-packages/transformers/models/siglip2/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_siglip2 import *` |
| 3172 | venv_creative/lib/python3.13/site-packages/transformers/models/siglip2/image_processing_siglip2.py | 31 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 3173 | venv_creative/lib/python3.13/site-packages/transformers/models/roberta/modeling_tf_roberta.py | 35 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss,` |
| 3174 | venv_creative/lib/python3.13/site-packages/transformers/models/roberta/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_roberta import *` |
| 3175 | venv_creative/lib/python3.13/site-packages/transformers/models/vitdet/modeling_vitdet.py | 102 | 13 | invalid syntax | `return new_abs_pos_embeddings.permute(0, 2, 3, 1)` |
| 3176 | venv_creative/lib/python3.13/site-packages/transformers/models/vitdet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_vitdet import *` |
| 3177 | venv_creative/lib/python3.13/site-packages/transformers/models/prompt_depth_anything/modular_prompt_depth_anything.py | 25 | 1 | invalid syntax | `from transformers.utils.generic import torch_int` |
| 3178 | venv_creative/lib/python3.13/site-packages/transformers/models/prompt_depth_anything/modeling_prompt_depth_anything.py | 47 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.activation1 = nn.ReLU()` |
| 3179 | venv_creative/lib/python3.13/site-packages/transformers/models/prompt_depth_anything/__init__.py | 23 | 12 | unexpected indent | `from .modeling_prompt_depth_anything import (PromptDepthAnythingForDepthEstimation,` |
| 3180 | venv_creative/lib/python3.13/site-packages/transformers/models/prompt_depth_anything/image_processing_prompt_depth_anything.py | 33 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, logging,` |
| 3181 | venv_creative/lib/python3.13/site-packages/transformers/models/tvp/image_processing_tvp.py | 27 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 3182 | venv_creative/lib/python3.13/site-packages/transformers/models/tvp/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_tvp import *` |
| 3183 | venv_creative/lib/python3.13/site-packages/transformers/models/aya_vision/modular_aya_vision.py | 30 | 1 | invalid syntax | `from ...activations import ACT2FN` |
| 3184 | venv_creative/lib/python3.13/site-packages/transformers/models/aya_vision/__init__.py | 21 | 8 | unexpected indent | `from .modeling_aya_vision import *` |
| 3185 | venv_creative/lib/python3.13/site-packages/transformers/models/aya_vision/configuration_aya_vision.py | 73 | 12 | unexpected indent | `self.adapter_layer_norm_eps = adapter_layer_norm_eps` |
| 3186 | venv_creative/lib/python3.13/site-packages/transformers/models/aya_vision/modeling_aya_vision.py | 48 | 12 | unexpected indent | `self.alignment_intermediate_size = getattr(` |
| 3187 | venv_creative/lib/python3.13/site-packages/transformers/models/aya_vision/processing_aya_vision.py | 26 | 1 | invalid syntax | `from ...tokenization_utils_base import PreTokenizedInput, TextInput` |
| 3188 | venv_creative/lib/python3.13/site-packages/transformers/models/audio_spectrogram_transformer/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_audio_spectrogram_transformer import *` |
| 3189 | venv_creative/lib/python3.13/site-packages/transformers/models/audio_spectrogram_transformer/modeling_audio_spectrogram_transformer.py | 29 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3190 | venv_creative/lib/python3.13/site-packages/transformers/models/fuyu/processing_fuyu.py | 95 | 5 | invalid syntax | `for bi in range(batch_size):` |
| 3191 | venv_creative/lib/python3.13/site-packages/transformers/models/fuyu/image_processing_fuyu.py | 30 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_torch_available,` |
| 3192 | venv_creative/lib/python3.13/site-packages/transformers/models/fuyu/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_fuyu import *` |
| 3193 | venv_creative/lib/python3.13/site-packages/transformers/models/fuyu/configuration_fuyu.py | 182 | 12 | unexpected indent | `self.image_token_id = image_token_id` |
| 3194 | venv_creative/lib/python3.13/site-packages/transformers/models/gptj/modeling_gptj.py | 34 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 3195 | venv_creative/lib/python3.13/site-packages/transformers/models/gptj/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_gptj import *` |
| 3196 | venv_creative/lib/python3.13/site-packages/transformers/models/gptj/modeling_tf_gptj.py | 27 | 1 | invalid syntax | `from ...modeling_tf_outputs import (TFBaseModelOutputWithPast, TFCausalLMOutputWithPast,` |
| 3197 | venv_creative/lib/python3.13/site-packages/transformers/models/distilbert/modeling_tf_distilbert.py | 33 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 3198 | venv_creative/lib/python3.13/site-packages/transformers/models/distilbert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_distilbert import *` |
| 3199 | venv_creative/lib/python3.13/site-packages/transformers/models/dac/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_dac import *` |
| 3200 | venv_creative/lib/python3.13/site-packages/transformers/models/dac/modeling_dac.py | 217 | 12 | unexpected indent | `return output_tensor` |
| 3201 | venv_creative/lib/python3.13/site-packages/transformers/models/encodec/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_encodec import *` |
| 3202 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4v_moe/configuration_glm4v_moe.py | 309 | 12 | unexpected indent | `self.first_k_dense_replace = first_k_dense_replace` |
| 3203 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4v_moe/modular_glm4v_moe.py | 34 | 1 | invalid syntax | `from ..glm4v.configuration_glm4v import Glm4vConfig, Glm4vVisionConfig` |
| 3204 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4v_moe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_glm4v_moe import *` |
| 3205 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4v_moe/modeling_glm4v_moe.py | 45 | 1 | invalid syntax | `from ...utils.deprecation import deprecate_kwarg` |
| 3206 | venv_creative/lib/python3.13/site-packages/transformers/models/lightglue/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_lightglue import *` |
| 3207 | venv_creative/lib/python3.13/site-packages/transformers/models/lightglue/image_processing_lightglue.py | 35 | 1 | invalid syntax | `from ...utils import TensorType, is_matplotlib_available, logging, requires_backends` |
| 3208 | venv_creative/lib/python3.13/site-packages/transformers/models/bridgetower/configuration_bridgetower.py | 90 | 12 | unexpected indent | `self.layer_norm_eps = layer_norm_eps` |
| 3209 | venv_creative/lib/python3.13/site-packages/transformers/models/bridgetower/image_processing_bridgetower_fast.py | 27 | 1 | invalid syntax | `from ...image_utils import OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, PILImageResampling` |
| 3210 | venv_creative/lib/python3.13/site-packages/transformers/models/bridgetower/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_bridgetower import *` |
| 3211 | venv_creative/lib/python3.13/site-packages/transformers/models/bridgetower/modeling_bridgetower.py | 35 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3212 | venv_creative/lib/python3.13/site-packages/transformers/models/bridgetower/image_processing_bridgetower.py | 27 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 3213 | venv_creative/lib/python3.13/site-packages/transformers/models/mt5/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_mt5 import *` |
| 3214 | venv_creative/lib/python3.13/site-packages/transformers/models/mt5/configuration_mt5.py | 122 | 12 | unexpected indent | `self.feed_forward_proj = feed_forward_proj` |
| 3215 | venv_creative/lib/python3.13/site-packages/transformers/models/deberta_v2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_deberta_v2 import *` |
| 3216 | venv_creative/lib/python3.13/site-packages/transformers/models/deberta_v2/modeling_tf_deberta_v2.py | 29 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 3217 | venv_creative/lib/python3.13/site-packages/transformers/models/speecht5/feature_extraction_speecht5.py | 26 | 1 | invalid syntax | `from ...feature_extraction_sequence_utils import SequenceFeatureExtractor` |
| 3218 | venv_creative/lib/python3.13/site-packages/transformers/models/speecht5/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_speecht5 import *` |
| 3219 | venv_creative/lib/python3.13/site-packages/transformers/models/speecht5/modeling_speecht5.py | 35 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 3220 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4_moe/modular_glm4_moe.py | 34 | 1 | invalid syntax | `from ..gpt_neox.modeling_gpt_neox import apply_rotary_pos_emb  # noqa` |
| 3221 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4_moe/modeling_glm4_moe.py | 121 | 8 | unexpected indent | `q_embed = (q_rot * cos) + (rotate_half(q_rot) * sin)` |
| 3222 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4_moe/configuration_glm4_moe.py | 236 | 12 | unexpected indent | `self.first_k_dense_replace = first_k_dense_replace` |
| 3223 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4_moe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_glm4_moe import *` |
| 3224 | venv_creative/lib/python3.13/site-packages/transformers/models/qwen2_vl/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_qwen2_vl import *` |
| 3225 | venv_creative/lib/python3.13/site-packages/transformers/models/qwen2_vl/image_processing_qwen2_vl.py | 36 | 1 | invalid syntax | `from ...utils import TensorType, logging` |
| 3226 | venv_creative/lib/python3.13/site-packages/transformers/models/mm_grounding_dino/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mm_grounding_dino import *` |
| 3227 | venv_creative/lib/python3.13/site-packages/transformers/models/mm_grounding_dino/modeling_mm_grounding_dino.py | 97 | 17 | invalid syntax. Perhaps you forgot a comma? | `value_list[level_id]` |
| 3228 | venv_creative/lib/python3.13/site-packages/transformers/models/swiftformer/modeling_tf_swiftformer.py | 27 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFPreTrainedModel, keras, keras_serializable,` |
| 3229 | venv_creative/lib/python3.13/site-packages/transformers/models/swiftformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_swiftformer import *` |
| 3230 | venv_creative/lib/python3.13/site-packages/transformers/models/swiftformer/modeling_swiftformer.py | 30 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3231 | venv_creative/lib/python3.13/site-packages/transformers/models/nougat/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_nougat_fast import *` |
| 3232 | venv_creative/lib/python3.13/site-packages/transformers/models/nougat/image_processing_nougat.py | 26 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 3233 | venv_creative/lib/python3.13/site-packages/transformers/models/swinv2/modeling_swinv2.py | 35 | 1 | invalid syntax | `from ...utils import ModelOutput, auto_docstring, logging, torch_int` |
| 3234 | venv_creative/lib/python3.13/site-packages/transformers/models/swinv2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_swinv2 import *` |
| 3235 | venv_creative/lib/python3.13/site-packages/transformers/models/regnet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_regnet import *` |
| 3236 | venv_creative/lib/python3.13/site-packages/transformers/models/pop2piano/__init__.py | 21 | 8 | unexpected indent | `from .modeling_pop2piano import *` |
| 3237 | venv_creative/lib/python3.13/site-packages/transformers/models/pop2piano/tokenization_pop2piano.py | 536 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 521 | `) -> BatchEncoding:` |
| 3238 | venv_creative/lib/python3.13/site-packages/transformers/models/pop2piano/configuration_pop2piano.py | 111 | 12 | unexpected indent | `self.feed_forward_proj = feed_forward_proj` |
| 3239 | venv_creative/lib/python3.13/site-packages/transformers/models/qwen2_5_omni/__init__.py | 21 | 8 | unexpected indent | `from .modeling_qwen2_5_omni import *` |
| 3240 | venv_creative/lib/python3.13/site-packages/transformers/models/mbart50/__init__.py | 21 | 8 | unexpected indent | `from .tokenization_mbart50_fast import *` |
| 3241 | venv_creative/lib/python3.13/site-packages/transformers/models/roberta_prelayernorm/modeling_tf_roberta_prelayernorm.py | 35 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss,` |
| 3242 | venv_creative/lib/python3.13/site-packages/transformers/models/roberta_prelayernorm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_roberta_prelayernorm import *` |
| 3243 | venv_creative/lib/python3.13/site-packages/transformers/models/roberta_prelayernorm/modeling_roberta_prelayernorm.py | 38 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3244 | venv_creative/lib/python3.13/site-packages/transformers/models/roberta_prelayernorm/modeling_flax_roberta_prelayernorm.py | 40 | 1 | invalid syntax | `from ...modeling_flax_utils import (ACT2FN, FlaxPreTrainedModel,` |
| 3245 | venv_creative/lib/python3.13/site-packages/transformers/models/wav2vec2_bert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_wav2vec2_bert import *` |
| 3246 | venv_creative/lib/python3.13/site-packages/transformers/models/levit/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_levit import *` |
| 3247 | venv_creative/lib/python3.13/site-packages/transformers/models/levit/image_processing_levit.py | 27 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 3248 | venv_creative/lib/python3.13/site-packages/transformers/models/patchtsmixer/modeling_patchtsmixer.py | 120 | 9 | invalid syntax | `return position_enc` |
| 3249 | venv_creative/lib/python3.13/site-packages/transformers/models/patchtsmixer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_patchtsmixer import *` |
| 3250 | venv_creative/lib/python3.13/site-packages/transformers/models/patchtsmixer/configuration_patchtsmixer.py | 203 | 12 | unexpected indent | `self.num_layers = num_layers` |
| 3251 | venv_creative/lib/python3.13/site-packages/transformers/models/seamless_m4t_v2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_seamless_m4t_v2 import *` |
| 3252 | venv_creative/lib/python3.13/site-packages/transformers/models/dinov2_with_registers/modeling_dinov2_with_registers.py | 35 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3253 | venv_creative/lib/python3.13/site-packages/transformers/models/dinov2_with_registers/__init__.py | 21 | 8 | unexpected indent | `from .modeling_dinov2_with_registers import *` |
| 3254 | venv_creative/lib/python3.13/site-packages/transformers/models/xlnet/modeling_xlnet.py | 76 | 39 | invalid syntax | `for i, b in enumerate(model.layer):` |
| 3255 | venv_creative/lib/python3.13/site-packages/transformers/models/xlnet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_tf_xlnet import *` |
| 3256 | venv_creative/lib/python3.13/site-packages/transformers/models/xlnet/modeling_tf_xlnet.py | 37 | 1 | invalid syntax | `from ...tf_utils import check_embeddings_within_bounds, shape_list, stable_softmax` |
| 3257 | venv_creative/lib/python3.13/site-packages/transformers/models/mpnet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mpnet import *` |
| 3258 | venv_creative/lib/python3.13/site-packages/transformers/models/mpnet/modeling_tf_mpnet.py | 33 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 3259 | venv_creative/lib/python3.13/site-packages/transformers/models/ernie/__init__.py | 21 | 8 | unexpected indent | `from .modeling_ernie import *` |
| 3260 | venv_creative/lib/python3.13/site-packages/transformers/models/falcon_h1/modular_falcon_h1.py | 119 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 109 | `}` |
| 3261 | venv_creative/lib/python3.13/site-packages/transformers/models/falcon_h1/configuration_falcon_h1.py | 226 | 12 | unexpected indent | `self.mamba_chunk_size = mamba_chunk_size` |
| 3262 | venv_creative/lib/python3.13/site-packages/transformers/models/falcon_h1/__init__.py | 21 | 8 | unexpected indent | `from .modeling_falcon_h1 import *` |
| 3263 | venv_creative/lib/python3.13/site-packages/transformers/models/falcon_h1/modeling_falcon_h1.py | 115 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 105 | `}` |
| 3264 | venv_creative/lib/python3.13/site-packages/transformers/models/instructblip/__init__.py | 21 | 8 | unexpected indent | `from .modeling_instructblip import *` |
| 3265 | venv_creative/lib/python3.13/site-packages/transformers/models/bros/__init__.py | 21 | 8 | unexpected indent | `from .modeling_bros import *` |
| 3266 | venv_creative/lib/python3.13/site-packages/transformers/models/detr/__init__.py | 22 | 8 | unexpected indent | `from .feature_extraction_detr import *` |
| 3267 | venv_creative/lib/python3.13/site-packages/transformers/models/detr/image_processing_detr.py | 31 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 3268 | venv_creative/lib/python3.13/site-packages/transformers/models/hgnet_v2/__init__.py | 22 | 8 | unexpected indent | `from .modeling_hgnet_v2 import *` |
| 3269 | venv_creative/lib/python3.13/site-packages/transformers/models/florence2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_florence2 import *` |
| 3270 | venv_creative/lib/python3.13/site-packages/transformers/models/florence2/modeling_florence2.py | 36 | 1 | invalid syntax | `from ..auto import AutoModel` |
| 3271 | venv_creative/lib/python3.13/site-packages/transformers/models/sam2_video/__init__.py | 21 | 8 | unexpected indent | `from .modeling_sam2_video import *` |
| 3272 | venv_creative/lib/python3.13/site-packages/transformers/models/mra/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mra import *` |
| 3273 | venv_creative/lib/python3.13/site-packages/transformers/models/internvl/modeling_internvl.py | 39 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3274 | venv_creative/lib/python3.13/site-packages/transformers/models/internvl/modular_internvl.py | 40 | 1 | invalid syntax | `from .configuration_internvl import InternVLConfig, InternVLVisionConfig` |
| 3275 | venv_creative/lib/python3.13/site-packages/transformers/models/internvl/__init__.py | 21 | 8 | unexpected indent | `from .modeling_internvl import *` |
| 3276 | venv_creative/lib/python3.13/site-packages/transformers/models/llava/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_llava_fast import *` |
| 3277 | venv_creative/lib/python3.13/site-packages/transformers/models/llava/image_processing_llava.py | 26 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 3278 | venv_creative/lib/python3.13/site-packages/transformers/models/perceiver/modeling_perceiver.py | 39 | 1 | invalid syntax | `from ...utils import ModelOutput, auto_docstring, logging, torch_int` |
| 3279 | venv_creative/lib/python3.13/site-packages/transformers/models/perceiver/image_processing_perceiver.py | 30 | 1 | invalid syntax | `from ...utils import (TensorType, filter_out_non_signature_kwargs, is_vision_available,` |
| 3280 | venv_creative/lib/python3.13/site-packages/transformers/models/perceiver/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_perceiver import *` |
| 3281 | venv_creative/lib/python3.13/site-packages/transformers/models/perceiver/configuration_perceiver.py | 163 | 12 | unexpected indent | `self.cross_attention_widening_factor = cross_attention_widening_factor` |
| 3282 | venv_creative/lib/python3.13/site-packages/transformers/models/instructblipvideo/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_instructblipvideo import *` |
| 3283 | venv_creative/lib/python3.13/site-packages/transformers/models/instructblipvideo/image_processing_instructblipvideo.py | 32 | 1 | invalid syntax | `from ...utils import TensorType, filter_out_non_signature_kwargs, logging` |
| 3284 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt2/modeling_gpt2.py | 42 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3285 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_gpt2 import *` |
| 3286 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt2/modeling_tf_gpt2.py | 31 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss, TFConv1D,` |
| 3287 | venv_creative/lib/python3.13/site-packages/transformers/models/ibert/modeling_ibert.py | 36 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3288 | venv_creative/lib/python3.13/site-packages/transformers/models/ibert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_ibert import *` |
| 3289 | venv_creative/lib/python3.13/site-packages/transformers/models/ibert/quant_modules.py | 95 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `w = self.weight` |
| 3290 | venv_creative/lib/python3.13/site-packages/transformers/models/glm/modular_glm.py | 28 | 1 | invalid syntax | `from ..phi3.modeling_phi3 import Phi3MLP` |
| 3291 | venv_creative/lib/python3.13/site-packages/transformers/models/glm/configuration_glm.py | 136 | 12 | unexpected indent | `self.head_dim = head_dim` |
| 3292 | venv_creative/lib/python3.13/site-packages/transformers/models/glm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_glm import *` |
| 3293 | venv_creative/lib/python3.13/site-packages/transformers/models/glm/modeling_glm.py | 37 | 1 | invalid syntax | `from ...modeling_outputs import BaseModelOutputWithPast, CausalLMOutputWithPast` |
| 3294 | venv_creative/lib/python3.13/site-packages/transformers/models/granitemoeshared/modeling_granitemoeshared.py | 37 | 1 | invalid syntax | `from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS, dynamic_rope_update` |
| 3295 | venv_creative/lib/python3.13/site-packages/transformers/models/granitemoeshared/__init__.py | 21 | 8 | unexpected indent | `from .modeling_granitemoeshared import *` |
| 3296 | venv_creative/lib/python3.13/site-packages/transformers/models/granitemoeshared/modular_granitemoeshared.py | 31 | 1 | invalid syntax | `from .configuration_granitemoeshared import GraniteMoeSharedConfig` |
| 3297 | venv_creative/lib/python3.13/site-packages/transformers/models/flaubert/modeling_tf_flaubert.py | 35 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFModelInputType, TFMultipleChoiceLoss,` |
| 3298 | venv_creative/lib/python3.13/site-packages/transformers/models/flaubert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flaubert import *` |
| 3299 | venv_creative/lib/python3.13/site-packages/transformers/models/vit_mae/__init__.py | 21 | 8 | unexpected indent | `from .modeling_tf_vit_mae import *` |
| 3300 | venv_creative/lib/python3.13/site-packages/transformers/models/vit_mae/modeling_tf_vit_mae.py | 33 | 1 | invalid syntax | `from ...modeling_tf_outputs import TFBaseModelOutput` |
| 3301 | venv_creative/lib/python3.13/site-packages/transformers/models/vit_mae/modeling_vit_mae.py | 49 | 1 | invalid syntax | `class ViTMAEModelOutput(ModelOutput):` |
| 3302 | venv_creative/lib/python3.13/site-packages/transformers/models/roc_bert/modeling_roc_bert.py | 38 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3303 | venv_creative/lib/python3.13/site-packages/transformers/models/roc_bert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_roc_bert import *` |
| 3304 | venv_creative/lib/python3.13/site-packages/transformers/models/prophetnet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_prophetnet import *` |
| 3305 | venv_creative/lib/python3.13/site-packages/transformers/models/prophetnet/modeling_prophetnet.py | 53 | 9 | invalid syntax. Perhaps you forgot a comma? | `torch.ones((ngram, sequence_length, sequence_length), device = device, dtype = dtype) * torch.finfo(dtype).min` |
| 3306 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4v/image_processing_glm4v.py | 31 | 1 | invalid syntax | `from ...utils import TensorType, logging` |
| 3307 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4v/modular_glm4v.py | 41 | 1 | invalid syntax | `from ...utils.generic import check_model_inputs` |
| 3308 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4v/__init__.py | 21 | 8 | unexpected indent | `from .modeling_glm4v import *` |
| 3309 | venv_creative/lib/python3.13/site-packages/transformers/models/glm4v/modeling_glm4v.py | 45 | 1 | invalid syntax | `from ...utils.generic import check_model_inputs` |
| 3310 | venv_creative/lib/python3.13/site-packages/transformers/models/textnet/image_processing_textnet.py | 26 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 3311 | venv_creative/lib/python3.13/site-packages/transformers/models/textnet/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_textnet import *` |
| 3312 | venv_creative/lib/python3.13/site-packages/transformers/models/falcon/__init__.py | 21 | 8 | unexpected indent | `from .modeling_falcon import *` |
| 3313 | venv_creative/lib/python3.13/site-packages/transformers/models/falcon/modeling_falcon.py | 34 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 3314 | venv_creative/lib/python3.13/site-packages/transformers/models/blenderbot_small/__init__.py | 21 | 8 | unexpected indent | `from .modeling_blenderbot_small import *` |
| 3315 | venv_creative/lib/python3.13/site-packages/transformers/models/phi4_multimodal/modeling_phi4_multimodal.py | 43 | 1 | invalid syntax | `from ...modeling_rope_utils import ROPE_INIT_FUNCTIONS, dynamic_rope_update` |
| 3316 | venv_creative/lib/python3.13/site-packages/transformers/models/phi4_multimodal/feature_extraction_phi4_multimodal.py | 78 | 5 | invalid syntax | `def __call__(` |
| 3317 | venv_creative/lib/python3.13/site-packages/transformers/models/phi4_multimodal/__init__.py | 22 | 8 | unexpected indent | `from .feature_extraction_phi4_multimodal import *` |
| 3318 | venv_creative/lib/python3.13/site-packages/transformers/models/phi4_multimodal/configuration_phi4_multimodal.py | 396 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.vocab_size = vocab_size` |
| 3319 | venv_creative/lib/python3.13/site-packages/transformers/models/phi4_multimodal/modular_phi4_multimodal.py | 32 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3320 | venv_creative/lib/python3.13/site-packages/transformers/models/megatron_bert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_megatron_bert import *` |
| 3321 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt_bigcode/__init__.py | 21 | 8 | unexpected indent | `from .modeling_gpt_bigcode import *` |
| 3322 | venv_creative/lib/python3.13/site-packages/transformers/models/funnel/modeling_tf_funnel.py | 32 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 3323 | venv_creative/lib/python3.13/site-packages/transformers/models/funnel/__init__.py | 21 | 8 | unexpected indent | `from .convert_funnel_original_tf_checkpoint_to_pytorch import *` |
| 3324 | venv_creative/lib/python3.13/site-packages/transformers/models/funnel/modeling_funnel.py | 33 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3325 | venv_creative/lib/python3.13/site-packages/transformers/models/smollm3/__init__.py | 21 | 8 | unexpected indent | `from .modeling_smollm3 import *` |
| 3326 | venv_creative/lib/python3.13/site-packages/transformers/models/phi/__init__.py | 21 | 8 | unexpected indent | `from .modeling_phi import *` |
| 3327 | venv_creative/lib/python3.13/site-packages/transformers/models/phi/configuration_phi.py | 206 | 12 | unexpected indent | `self.qk_layernorm = qk_layernorm` |
| 3328 | venv_creative/lib/python3.13/site-packages/transformers/models/fsmt/__init__.py | 21 | 8 | unexpected indent | `from .modeling_fsmt import *` |
| 3329 | venv_creative/lib/python3.13/site-packages/transformers/models/xmod/modeling_xmod.py | 37 | 1 | invalid syntax | `from ...modeling_utils import PreTrainedModel` |
| 3330 | venv_creative/lib/python3.13/site-packages/transformers/models/xmod/__init__.py | 21 | 8 | unexpected indent | `from .modeling_xmod import *` |
| 3331 | venv_creative/lib/python3.13/site-packages/transformers/models/xmod/configuration_xmod.py | 163 | 12 | unexpected indent | `self.adapter_layer_norm = adapter_layer_norm` |
| 3332 | venv_creative/lib/python3.13/site-packages/transformers/models/sam2/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_sam2_fast import *` |
| 3333 | venv_creative/lib/python3.13/site-packages/transformers/models/sam2/image_processing_sam2_fast.py | 35 | 1 | invalid syntax | `from ...image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 3334 | venv_creative/lib/python3.13/site-packages/transformers/models/vitpose_backbone/__init__.py | 11 | 8 | unexpected indent | `from .modeling_vitpose_backbone import *` |
| 3335 | venv_creative/lib/python3.13/site-packages/transformers/models/persimmon/__init__.py | 21 | 8 | unexpected indent | `from .modeling_persimmon import *` |
| 3336 | venv_creative/lib/python3.13/site-packages/transformers/models/rt_detr_v2/__init__.py | 22 | 8 | unexpected indent | `from .modeling_rt_detr_v2 import *` |
| 3337 | venv_creative/lib/python3.13/site-packages/transformers/models/gpt_neox_japanese/__init__.py | 21 | 8 | unexpected indent | `from .modeling_gpt_neox_japanese import *` |
| 3338 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlm/modeling_tf_layoutlm.py | 32 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFMaskedLanguageModelingLoss, TFModelInputType,` |
| 3339 | venv_creative/lib/python3.13/site-packages/transformers/models/layoutlm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_layoutlm import *` |
| 3340 | venv_creative/lib/python3.13/site-packages/transformers/models/owlv2/image_processing_owlv2.py | 27 | 1 | invalid syntax | `from ...image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 3341 | venv_creative/lib/python3.13/site-packages/transformers/models/owlv2/image_processing_owlv2_fast.py | 29 | 1 | invalid syntax | `from ...image_transforms import (center_to_corners_format, group_images_by_shape,` |
| 3342 | venv_creative/lib/python3.13/site-packages/transformers/models/owlv2/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_owlv2 import *` |
| 3343 | venv_creative/lib/python3.13/site-packages/transformers/models/owlv2/modular_owlv2.py | 24 | 1 | invalid syntax | `from ...image_transforms import group_images_by_shape, reorder_images` |
| 3344 | venv_creative/lib/python3.13/site-packages/transformers/models/owlv2/modeling_owlv2.py | 30 | 1 | invalid syntax | `from ...modeling_layers import GradientCheckpointingLayer` |
| 3345 | venv_creative/lib/python3.13/site-packages/transformers/models/ernie4_5/__init__.py | 21 | 8 | unexpected indent | `from .modeling_ernie4_5 import *` |
| 3346 | venv_creative/lib/python3.13/site-packages/transformers/models/kyutai_speech_to_text/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_kyutai_speech_to_text import *` |
| 3347 | venv_creative/lib/python3.13/site-packages/transformers/models/git/__init__.py | 21 | 8 | unexpected indent | `from .modeling_git import *` |
| 3348 | venv_creative/lib/python3.13/site-packages/transformers/models/mistral/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_mistral import *` |
| 3349 | venv_creative/lib/python3.13/site-packages/transformers/models/qwen2_moe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_qwen2_moe import *` |
| 3350 | venv_creative/lib/python3.13/site-packages/transformers/models/nemotron/configuration_nemotron.py | 143 | 12 | unexpected indent | `rope_config_validation(self)` |
| 3351 | venv_creative/lib/python3.13/site-packages/transformers/models/nemotron/__init__.py | 21 | 8 | unexpected indent | `from .modeling_nemotron import *` |
| 3352 | venv_creative/lib/python3.13/site-packages/transformers/models/nemotron/modeling_nemotron.py | 34 | 1 | invalid syntax | `from ...modeling_layers import (GenericForQuestionAnswering,` |
| 3353 | venv_creative/lib/python3.13/site-packages/transformers/models/fnet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_fnet import *` |
| 3354 | venv_creative/lib/python3.13/site-packages/transformers/models/bitnet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_bitnet import *` |
| 3355 | venv_creative/lib/python3.13/site-packages/transformers/models/canine/__init__.py | 21 | 8 | unexpected indent | `from .modeling_canine import *` |
| 3356 | venv_creative/lib/python3.13/site-packages/transformers/models/openai/modeling_tf_openai.py | 30 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss, TFConv1D,` |
| 3357 | venv_creative/lib/python3.13/site-packages/transformers/models/openai/__init__.py | 21 | 8 | unexpected indent | `from .modeling_openai import *` |
| 3358 | venv_creative/lib/python3.13/site-packages/transformers/models/dinov2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_dinov2 import *` |
| 3359 | venv_creative/lib/python3.13/site-packages/transformers/models/dinov2/modeling_dinov2.py | 30 | 1 | invalid syntax | `from ...modeling_utils import ALL_ATTENTION_FUNCTIONS, PreTrainedModel` |
| 3360 | venv_creative/lib/python3.13/site-packages/transformers/models/dinov2/modeling_flax_dinov2.py | 33 | 1 | invalid syntax | `from ...modeling_flax_utils import (ACT2FN, FlaxPreTrainedModel,` |
| 3361 | venv_creative/lib/python3.13/site-packages/transformers/models/lilt/__init__.py | 21 | 8 | unexpected indent | `from .modeling_lilt import *` |
| 3362 | venv_creative/lib/python3.13/site-packages/transformers/models/llama/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_llama import *` |
| 3363 | venv_creative/lib/python3.13/site-packages/transformers/models/whisper/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_whisper import *` |
| 3364 | venv_creative/lib/python3.13/site-packages/transformers/models/whisper/processing_whisper.py | 44 | 12 | unexpected indent | `self._in_target_context_manager = False` |
| 3365 | venv_creative/lib/python3.13/site-packages/transformers/models/whisper/english_normalizer.py | 128 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 122 | `}` |
| 3366 | venv_creative/lib/python3.13/site-packages/transformers/models/llava_onevision/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_llava_onevision import *` |
| 3367 | venv_creative/lib/python3.13/site-packages/transformers/models/llava_onevision/image_processing_llava_onevision.py | 27 | 1 | invalid syntax | `from ...image_transforms import (PaddingMode, convert_to_rgb, pad, resize,` |
| 3368 | venv_creative/lib/python3.13/site-packages/transformers/models/qwen2_audio/__init__.py | 21 | 8 | unexpected indent | `from .modeling_qwen2_audio import *` |
| 3369 | venv_creative/lib/python3.13/site-packages/transformers/models/rembert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_rembert import *` |
| 3370 | venv_creative/lib/python3.13/site-packages/transformers/models/rembert/modeling_tf_rembert.py | 33 | 1 | invalid syntax | `from ...modeling_tf_utils import (TFCausalLanguageModelingLoss,` |
| 3371 | venv_creative/lib/python3.13/site-packages/transformers/models/qwen3_moe/__init__.py | 21 | 8 | unexpected indent | `from .modeling_qwen3_moe import *` |
| 3372 | venv_creative/lib/python3.13/site-packages/transformers/models/seggpt/image_processing_seggpt.py | 29 | 1 | invalid syntax | `from ...utils import TensorType, is_torch_available, logging, requires_backends` |
| 3373 | venv_creative/lib/python3.13/site-packages/transformers/models/seggpt/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_seggpt import *` |
| 3374 | venv_creative/lib/python3.13/site-packages/transformers/models/seggpt/modeling_seggpt.py | 44 | 1 | invalid syntax | `class SegGptEncoderOutput(ModelOutput):` |
| 3375 | venv_creative/lib/python3.13/site-packages/transformers/models/swin2sr/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_swin2sr import *` |
| 3376 | venv_creative/lib/python3.13/site-packages/transformers/models/swin2sr/modeling_swin2sr.py | 34 | 1 | invalid syntax | `from ...utils import ModelOutput, auto_docstring, logging` |
| 3377 | venv_creative/lib/python3.13/site-packages/transformers/models/swin2sr/image_processing_swin2sr.py | 29 | 1 | invalid syntax | `from ...utils import TensorType, filter_out_non_signature_kwargs, logging` |
| 3378 | venv_creative/lib/python3.13/site-packages/transformers/models/mbart/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_mbart import *` |
| 3379 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/__init__.py | 21 | 8 | unexpected indent | `from .deta import *` |
| 3380 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/graphormer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_graphormer import *` |
| 3381 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/trajectory_transformer/modeling_trajectory_transformer.py | 35 | 1 | invalid syntax | `from .configuration_trajectory_transformer import TrajectoryTransformerConfig` |
| 3382 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/trajectory_transformer/__init__.py | 21 | 8 | unexpected indent | `from .modeling_trajectory_transformer import *` |
| 3383 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/xlm_prophetnet/__init__.py | 21 | 8 | unexpected indent | `from .modeling_xlm_prophetnet import *` |
| 3384 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/xlm_prophetnet/modeling_xlm_prophetnet.py | 37 | 1 | invalid syntax | `from ....utils.deprecation import deprecate_kwarg` |
| 3385 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/qdqbert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_qdqbert import *` |
| 3386 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/nat/__init__.py | 21 | 8 | unexpected indent | `from .modeling_nat import *` |
| 3387 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/nat/modeling_nat.py | 36 | 1 | invalid syntax | `from ....utils.backbone_utils import BackboneMixin` |
| 3388 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/open_llama/modeling_open_llama.py | 37 | 1 | invalid syntax | `from ....modeling_utils import PreTrainedModel` |
| 3389 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/open_llama/__init__.py | 21 | 8 | unexpected indent | `from .modeling_open_llama import *` |
| 3390 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/transfo_xl/modeling_transfo_xl.py | 34 | 1 | invalid syntax | `from .configuration_transfo_xl import TransfoXLConfig` |
| 3391 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/transfo_xl/modeling_tf_transfo_xl.py | 32 | 1 | invalid syntax | `from ....tf_utils import shape_list, stable_softmax` |
| 3392 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/transfo_xl/__init__.py | 21 | 8 | unexpected indent | `from .modeling_tf_transfo_xl import *` |
| 3393 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/transfo_xl/tokenization_transfo_xl.py | 36 | 1 | invalid syntax | `if is_sacremoses_available():` |
| 3394 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/ernie_m/__init__.py | 21 | 8 | unexpected indent | `from .modeling_ernie_m import *` |
| 3395 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/van/modeling_van.py | 32 | 1 | invalid syntax | `from ....modeling_utils import PreTrainedModel` |
| 3396 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/van/__init__.py | 21 | 8 | unexpected indent | `from .modeling_van import *` |
| 3397 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/tvlt/processing_tvlt.py | 45 | 12 | unexpected indent | `self.feature_extractor = feature_extractor` |
| 3398 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/tvlt/image_processing_tvlt.py | 26 | 1 | invalid syntax | `from ....image_utils import (IMAGENET_STANDARD_MEAN, IMAGENET_STANDARD_STD,` |
| 3399 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/tvlt/__init__.py | 11 | 8 | unexpected indent | `from .feature_extraction_tvlt import *` |
| 3400 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/mctct/processing_mctct.py | 46 | 12 | unexpected indent | `self._in_target_context_manager = False` |
| 3401 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/mctct/feature_extraction_mctct.py | 27 | 1 | invalid syntax | `from ....feature_extraction_sequence_utils import SequenceFeatureExtractor` |
| 3402 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/mctct/__init__.py | 21 | 8 | unexpected indent | `from .feature_extraction_mctct import *` |
| 3403 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/nezha/__init__.py | 21 | 8 | unexpected indent | `from .modeling_nezha import *` |
| 3404 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/mmbt/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mmbt import *` |
| 3405 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/mega/__init__.py | 21 | 8 | unexpected indent | `from .modeling_mega import *` |
| 3406 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/mega/modeling_mega.py | 34 | 1 | invalid syntax | `from ....modeling_utils import PreTrainedModel` |
| 3407 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/jukebox/tokenization_jukebox.py | 33 | 1 | invalid syntax | `from ....utils.generic import _is_jax, _is_numpy` |
| 3408 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/jukebox/__init__.py | 21 | 8 | unexpected indent | `from .modeling_jukebox import *` |
| 3409 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/jukebox/modeling_jukebox.py | 36 | 8 | invalid syntax | `logger = logging.get_logger(__name__)` |
| 3410 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/tapex/tokenization_tapex.py | 29 | 1 | invalid syntax | `from ....tokenization_utils import AddedToken, PreTrainedTokenizer` |
| 3411 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/vit_hybrid/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_vit_hybrid import *` |
| 3412 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/vit_hybrid/image_processing_vit_hybrid.py | 26 | 1 | invalid syntax | `from ....image_utils import (OPENAI_CLIP_MEAN, OPENAI_CLIP_STD, ChannelDimension,` |
| 3413 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/vit_hybrid/modeling_vit_hybrid.py | 32 | 1 | invalid syntax | `from ....modeling_utils import PreTrainedModel` |
| 3414 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/deta/modeling_deta.py | 38 | 1 | invalid syntax | `from ....modeling_attn_mask_utils import _prepare_4d_attention_mask` |
| 3415 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/deta/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_deta import *` |
| 3416 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/deta/image_processing_deta.py | 30 | 1 | invalid syntax | `from ....image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 3417 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/retribert/__init__.py | 21 | 8 | unexpected indent | `from .modeling_retribert import *` |
| 3418 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/speech_to_text_2/__init__.py | 21 | 8 | unexpected indent | `from .modeling_speech_to_text_2 import *` |
| 3419 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/speech_to_text_2/processing_speech_to_text_2.py | 47 | 12 | unexpected indent | `self._in_target_context_manager = False` |
| 3420 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/efficientformer/__init__.py | 21 | 8 | unexpected indent | `from .image_processing_efficientformer import *` |
| 3421 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/efficientformer/modeling_efficientformer.py | 31 | 1 | invalid syntax | `from ....modeling_utils import PreTrainedModel` |
| 3422 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/efficientformer/image_processing_efficientformer.py | 26 | 1 | invalid syntax | `from ....image_utils import (IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD,` |
| 3423 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/efficientformer/modeling_tf_efficientformer.py | 28 | 1 | invalid syntax | `from ....modeling_tf_utils import (TFPreTrainedModel, TFSequenceClassificationLoss,` |
| 3424 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/realm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_realm import *` |
| 3425 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/gptsan_japanese/modeling_gptsan_japanese.py | 27 | 1 | invalid syntax | `from ....modeling_utils import PreTrainedModel` |
| 3426 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/gptsan_japanese/__init__.py | 21 | 8 | unexpected indent | `from .modeling_gptsan_japanese import *` |
| 3427 | venv_creative/lib/python3.13/site-packages/transformers/models/deprecated/gptsan_japanese/configuration_gptsan_japanese.py | 91 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `attribute_map = {` |
| 3428 | venv_creative/lib/python3.13/site-packages/transformers/models/xglm/__init__.py | 21 | 8 | unexpected indent | `from .modeling_flax_xglm import *` |
| 3429 | venv_creative/lib/python3.13/site-packages/transformers/integrations/peft.py | 29 | 1 | invalid syntax | `if is_torch_available():` |
| 3430 | venv_creative/lib/python3.13/site-packages/transformers/integrations/tensor_parallel.py | 217 | 12 | unexpected indent | `else:` |
| 3431 | venv_creative/lib/python3.13/site-packages/transformers/integrations/executorch.py | 22 | 1 | invalid syntax | `from ..generation.configuration_utils import GenerationConfig` |
| 3432 | venv_creative/lib/python3.13/site-packages/transformers/commands/add_new_model_like.py | 39 | 8 | unexpected indent | `from libcst import matchers as m` |
| 3433 | venv_creative/lib/python3.13/site-packages/transformers/commands/serving.py | 40 | 1 | invalid syntax | `from transformers.utils.import_utils import (is_fastapi_available, is_librosa_available,` |
| 3434 | venv_creative/lib/python3.13/site-packages/transformers/commands/chat.py | 51 | 19 | invalid syntax | `ALLOWED_KEY_CHARS = set(string.ascii_letters + string.whitespace)` |
| 3435 | venv_creative/lib/python3.13/site-packages/transformers/commands/train.py | 62 | 61 | invalid syntax. Perhaps you forgot a comma? | `"--column_label", type = int, default = 0, help="Column of the dataset csv file with example labels."` |
| 3436 | venv_creative/lib/python3.13/site-packages/transformers/data/data_collator.py | 287 | 9 | invalid syntax | `if "label" in batch:` |
| 3437 | venv_creative/lib/python3.13/site-packages/transformers/generation/flax_utils.py | 34 | 1 | invalid syntax | `from ..utils import ModelOutput, logging` |
| 3438 | venv_creative/lib/python3.13/site-packages/transformers/generation/stopping_criteria.py | 90 | 9 | invalid syntax | `return torch.full((input_ids.shape[0],), is_done, device = input_ids.device, dtype = torch.bool)` |
| 3439 | venv_creative/lib/python3.13/site-packages/transformers/generation/candidate_generator.py | 36 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 3440 | venv_creative/lib/python3.13/site-packages/transformers/generation/watermarking.py | 38 | 8 | invalid syntax | `logger = logging.get_logger(__name__)` |
| 3441 | venv_creative/lib/python3.13/site-packages/transformers/generation/utils.py | 4150 | 43 | too many nested parentheses | `next_token_scores, max(2, 1 + n_eos_tokens) * group_size, dim = 1, largest = True, sorted = True` |
| 3442 | venv_creative/lib/python3.13/site-packages/transformers/generation/tf_utils.py | 34 | 1 | invalid syntax | `from ..tf_utils import shape_list, stable_softmax` |
| 3443 | venv_creative/lib/python3.13/site-packages/transformers/generation/continuous_batching/cache.py | 68 | 21 | invalid syntax. Perhaps you forgot a comma? | `f"Number of key value heads {self.num_key_value_heads} must be divisible by tensor parallel size {tp_size}."` |
| 3444 | venv_creative/lib/python3.13/site-packages/transformers/generation/continuous_batching/continuous_api.py | 37 | 1 | invalid syntax | `from .scheduler import SCHEDULER_MAPPING, FIFOScheduler, Scheduler` |
| 3445 | venv_creative/lib/python3.13/site-packages/facexlib/matting/mobilenetv2.py | 16 | 12 | unexpected indent | `new_v = max(min_value, int(v + divisor / 2) // divisor * divisor)` |
| 3446 | venv_creative/lib/python3.13/site-packages/facexlib/utils/face_restoration_helper.py | 79 | 9 | cannot assign to attribute here. Maybe you meant '==' instead of '='? | `self.face_template = self.face_template * (face_size / 512.0)` |
| 3447 | venv_creative/lib/python3.13/site-packages/facexlib/parsing/parsenet.py | 173 | 12 | unexpected indent | `self.encoder = []` |
| 3448 | venv_creative/lib/python3.13/site-packages/facexlib/detection/matlab_cp2tform.py | 67 | 8 | unexpected indent | `y = xy[:, 1].reshape((-1, 1))  # use reshape to keep a column vector` |
| 3449 | venv_creative/lib/python3.13/site-packages/facexlib/detection/retinaface_utils.py | 52 | 5 | invalid syntax | `return list(keep)` |
| 3450 | venv_creative/lib/python3.13/site-packages/multipart/__init__.py | 24 | 8 | unexpected indent | `from python_multipart import (__all__, __author__, __copyright__, __license__,` |
| 3451 | venv_creative/lib/python3.13/site-packages/pooch/core.py | 25 | 1 | invalid syntax | `def retrieve(` |
| 3452 | venv_creative/lib/python3.13/site-packages/pooch/tests/test_processors.py | 36 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `ids=["auto", "lzma", "xz", "bz2", "gz", "name"],` |
| 3453 | venv_creative/lib/python3.13/site-packages/pooch/tests/test_downloaders.py | 462 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 450 | `}` |
| 3454 | venv_creative/lib/python3.13/site-packages/tqdm/_monitor.py | 35 | 12 | unexpected indent | `self.tqdm_cls = tqdm_cls` |
| 3455 | venv_creative/lib/python3.13/site-packages/tqdm/std.py | 26 | 12 | invalid syntax | `__author__ = "https://github.com / tqdm / tqdm#contributions"` |
| 3456 | venv_creative/lib/python3.13/site-packages/tqdm/rich.py | 16 | 1 | invalid syntax | `from .std import TqdmExperimentalWarning` |
| 3457 | venv_creative/lib/python3.13/site-packages/tqdm/contrib/concurrent.py | 70 | 8 | unexpected indent | `return _executor_map(ThreadPoolExecutor, fn, *iterables, **tqdm_kwargs)` |
| 3458 | venv_creative/lib/python3.13/site-packages/tqdm/contrib/telegram.py | 51 | 9 | invalid syntax | `except Exception as e:` |
| 3459 | venv_creative/lib/python3.13/site-packages/tqdm/contrib/discord.py | 54 | 9 | invalid syntax | `except Exception as e:` |
| 3460 | venv_creative/lib/python3.13/site-packages/fastapi/routing.py | 103 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 94 | `}` |
| 3461 | venv_creative/lib/python3.13/site-packages/fastapi/_compat.py | 215 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 209 | `) -> Dict[str, Any]:` |
| 3462 | venv_creative/lib/python3.13/site-packages/_yaml/__init__.py | 14 | 8 | unexpected indent | `raise exc("No module named '_yaml'")` |
| 3463 | venv_creative/lib/python3.13/site-packages/simple_websocket/ws.py | 12 | 1 | invalid syntax | `from wsproto.extensions import PerMessageDeflate` |
| 3464 | venv_creative/lib/python3.13/site-packages/torchaudio/models/rnnt.py | 211 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.time_reduction = _TimeReduction(time_reduction_stride)` |
| 3465 | venv_creative/lib/python3.13/site-packages/torchaudio/models/squim/subjective.py | 89 | 12 | unexpected indent | `self.predictor = predictor` |
| 3466 | venv_creative/lib/python3.13/site-packages/torchaudio/models/decoder/_ctc_decoder.py | 44 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_PretrainedFiles = namedtuple("PretrainedFiles", ["lexicon", "tokens", "lm"])` |
| 3467 | venv_creative/lib/python3.13/site-packages/torchaudio/models/wav2vec2/model.py | 42 | 12 | unexpected indent | `self.encoder = encoder` |
| 3468 | venv_creative/lib/python3.13/site-packages/torchaudio/prototype/models/_conformer_wav2vec2.py | 51 | 11 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `B, T, D = input.shape` |
| 3469 | venv_creative/lib/python3.13/site-packages/torchaudio/compliance/kaldi.py | 24 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `EPSILON = torch.tensor(torch.finfo(torch.float).eps)` |
| 3470 | venv_creative/lib/python3.13/site-packages/torchaudio/functional/filtering.py | 333 | 5 | invalid syntax | `return output_waveform` |
| 3471 | venv_creative/lib/python3.13/site-packages/torchaudio/functional/functional.py | 59 | 1 | invalid syntax | `def spectrogram(` |
| 3472 | venv_creative/lib/python3.13/site-packages/rich/logging.py | 65 | 22 | invalid syntax | `HIGHLIGHTER_CLASS: ClassVar[Type[Highlighter]] = ReprHighlighter` |
| 3473 | venv_creative/lib/python3.13/site-packages/rich/console.py | 687 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 655 | `):` |
| 3474 | venv_creative/lib/python3.13/site-packages/rich/color.py | 303 | 1 | invalid syntax | `@rich_repr` |
| 3475 | venv_creative/lib/python3.13/site-packages/rich/style.py | 86 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_style_map = {` |
| 3476 | venv_creative/lib/python3.13/site-packages/rich/traceback.py | 599 | 25 | closing parenthesis '}' does not match opening parenthesis '(' on line 590 | `}` |
| 3477 | venv_creative/lib/python3.13/site-packages/rich/palette.py | 25 | 12 | unexpected indent | `from rich.style import Style` |
| 3478 | venv_creative/lib/python3.13/site-packages/rich/pretty.py | 1079 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 1069 | `),` |
| 3479 | venv_creative/lib/python3.13/site-packages/rich/columns.py | 49 | 12 | unexpected indent | `self.equal = equal` |
| 3480 | venv_creative/lib/python3.13/site-packages/rich/syntax.py | 14 | 1 | invalid syntax | `from pygments.lexer import Lexer` |
| 3481 | venv_creative/lib/python3.13/site-packages/rich/table.py | 7 | 1 | invalid syntax | `from . import box, errors` |
| 3482 | venv_creative/lib/python3.13/site-packages/rich/segment.py | 11 | 1 | invalid syntax | `from .cells import (_is_single_cell_widths, cached_cell_len, cell_len,` |
| 3483 | venv_creative/lib/python3.13/site-packages/rich/progress.py | 23 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 3484 | venv_creative/lib/python3.13/site-packages/rich/_win32_console.py | 71 | 1 | invalid syntax | `class CONSOLE_CURSOR_INFO(ctypes.Structure):` |
| 3485 | venv_creative/lib/python3.13/site-packages/rich/panel.py | 67 | 12 | unexpected indent | `self.style = style` |
| 3486 | venv_creative/lib/python3.13/site-packages/matplotlib/legend_handler.py | 147 | 9 | invalid syntax | `for a in artists:` |
| 3487 | venv_creative/lib/python3.13/site-packages/matplotlib/axis.py | 38 | 1 | invalid syntax | `class Tick(martist.Artist):` |
| 3488 | venv_creative/lib/python3.13/site-packages/matplotlib/quiver.py | 342 | 12 | unexpected indent | `self.label = label` |
| 3489 | venv_creative/lib/python3.13/site-packages/matplotlib/backend_bases.py | 720 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 716 | `}` |
| 3490 | venv_creative/lib/python3.13/site-packages/matplotlib/colorbar.py | 209 | 1 | invalid syntax | `class Colorbar:` |
| 3491 | venv_creative/lib/python3.13/site-packages/matplotlib/cbook.py | 83 | 55 | invalid syntax | `if QtWidgets and QtWidgets.QApplication.instance():` |
| 3492 | venv_creative/lib/python3.13/site-packages/matplotlib/bezier.py | 466 | 56 | invalid decimal literal | `def check_if_parallel(dx1, dy1, dx2, dy2, tolerance = 1.e - 5):` |
| 3493 | venv_creative/lib/python3.13/site-packages/matplotlib/figure.py | 53 | 1 | invalid syntax | `from matplotlib.gridspec import GridSpec, SubplotParams` |
| 3494 | venv_creative/lib/python3.13/site-packages/matplotlib/_mathtext.py | 611 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 605 | `}` |
| 3495 | venv_creative/lib/python3.13/site-packages/matplotlib/offsetbox.py | 54 | 5 | invalid syntax | `@functools.wraps(meth)` |
| 3496 | venv_creative/lib/python3.13/site-packages/matplotlib/lines.py | 24 | 1 | invalid syntax | `from .path import Path` |
| 3497 | venv_creative/lib/python3.13/site-packages/matplotlib/widgets.py | 158 | 17 | expected 'else' after 'if' expression | `return ((event.xdata, event.ydata) if event.inaxes is self.ax` |
| 3498 | venv_creative/lib/python3.13/site-packages/matplotlib/animation.py | 23 | 1 | invalid syntax | `from PIL import Image` |
| 3499 | venv_creative/lib/python3.13/site-packages/matplotlib/_mathtext_data.py | 1398 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 1302 | `},` |
| 3500 | venv_creative/lib/python3.13/site-packages/matplotlib/backend_tools.py | 129 | 5 | invalid syntax | `def set_figure(self, figure):` |
| 3501 | venv_creative/lib/python3.13/site-packages/matplotlib/patches.py | 27 | 1 | invalid syntax | `from .path import Path` |
| 3502 | venv_creative/lib/python3.13/site-packages/matplotlib/collections.py | 44 | 1 | invalid syntax | `class Collection(mcolorizer.ColorizingArtist):` |
| 3503 | venv_creative/lib/python3.13/site-packages/matplotlib/text.py | 24 | 6 | invalid syntax | `_log = logging.getLogger(__name__)` |
| 3504 | venv_creative/lib/python3.13/site-packages/matplotlib/mlab.py | 130 | 1 | invalid syntax | `def detrend_mean(x, axis = None):` |
| 3505 | venv_creative/lib/python3.13/site-packages/matplotlib/layout_engine.py | 87 | 16 | unexpected indent | `return self._colorbar_gridspec` |
| 3506 | venv_creative/lib/python3.13/site-packages/matplotlib/dates.py | 1399 | 33 | closing parenthesis '}' does not match opening parenthesis '[' on line 1394 | `}` |
| 3507 | venv_creative/lib/python3.13/site-packages/matplotlib/_type1font.py | 251 | 40 | invalid syntax | `if match.group() == '(':` |
| 3508 | venv_creative/lib/python3.13/site-packages/matplotlib/ticker.py | 161 | 1 | invalid syntax | `class _DummyAxis:` |
| 3509 | venv_creative/lib/python3.13/site-packages/matplotlib/contour.py | 59 | 1 | positional argument follows keyword argument | `class ContourLabeler:` |
| 3510 | venv_creative/lib/python3.13/site-packages/matplotlib/patheffects.py | 44 | 5 | invalid syntax | `def _update_gc(self, gc, new_gc_dict):` |
| 3511 | venv_creative/lib/python3.13/site-packages/matplotlib/streamplot.py | 114 | 5 | invalid syntax | `if integration_direction == 'both':` |
| 3512 | venv_creative/lib/python3.13/site-packages/matplotlib/colors.py | 1259 | 61 | closing parenthesis '}' does not match opening parenthesis '(' on line 1254 | `for key, data in self._segmentdata.items()}` |
| 3513 | venv_creative/lib/python3.13/site-packages/matplotlib/tri/_triinterpolate.py | 1326 | 16 | invalid decimal literal | `tol = 1.e - 10` |
| 3514 | venv_creative/lib/python3.13/site-packages/matplotlib/tri/_tricontour.py | 40 | 16 | unexpected indent | `if self.levels is None:` |
| 3515 | venv_creative/lib/python3.13/site-packages/matplotlib/axes/_axes.py | 5619 | 20 | invalid decimal literal | `padding = 1.e - 9 * (xmax - xmin)` |
| 3516 | venv_creative/lib/python3.13/site-packages/matplotlib/axes/_base.py | 988 | 41 | closing parenthesis '}' does not match opening parenthesis '(' on line 984 | `for name in self._axis_names}` |
| 3517 | venv_creative/lib/python3.13/site-packages/matplotlib/sphinxext/mathmpl.py | 108 | 5 | invalid syntax | `return [node], []` |
| 3518 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/backend_gtk3cairo.py | 19 | 47 | unindent does not match any outer indentation level | `allocation = self.get_allocation()` |
| 3519 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/backend_pdf.py | 1110 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 1106 | `}` |
| 3520 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/backend_gtk4.py | 12 | 1 | invalid syntax | `try:` |
| 3521 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/backend_gtk3.py | 13 | 1 | invalid syntax | `try:` |
| 3522 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/backend_gtk4cairo.py | 25 | 44 | unindent does not match any outer indentation level | `self._renderer.set_context(ctx)` |
| 3523 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/_backend_tk.py | 25 | 1 | invalid syntax | `from PIL import Image, ImageTk` |
| 3524 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/backend_svg.py | 1202 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 1196 | `}` |
| 3525 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/backend_ps.py | 32 | 1 | invalid syntax | `from matplotlib.backends.backend_mixed import MixedModeRenderer` |
| 3526 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/backend_agg.py | 34 | 1 | invalid syntax | `from matplotlib.backends._backend_agg import RendererAgg as _RendererAgg` |
| 3527 | venv_creative/lib/python3.13/site-packages/matplotlib/backends/qt_editor/_formlayout.py | 79 | 9 | invalid syntax | `if color.isValid():` |
| 3528 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_lines.py | 135 | 9 | invalid syntax. Perhaps you forgot a comma? | `ax.plot(range(10), linestyle = ls)` |
| 3529 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_backend_bases.py | 12 | 1 | invalid syntax | `from matplotlib.backend_tools import RubberbandBase` |
| 3530 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_tightlayout.py | 19 | 1 | invalid syntax | `def example_plot(ax, fontsize = 12):` |
| 3531 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_dates.py | 47 | 1 | invalid syntax | `@pytest.mark.parametrize('dtype', ['datetime64[s]',` |
| 3532 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_texmanager.py | 43 | 1 | invalid syntax | `def test_font_selection(rc, preamble, family):` |
| 3533 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_backends_interactive.py | 42 | 5 | invalid syntax | `def wait_for(self, terminator):` |
| 3534 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_subplots.py | 80 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 73 | `}` |
| 3535 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_ticker.py | 475 | 33 | invalid decimal literal | `test_value = np.array([1.e - 01, 2.e - 01, 5.e - 01, 1.e + 00, 2.e + 00, 5.e + 00,` |
| 3536 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_image.py | 1886 | 93 | closing parenthesis ')' does not match opening parenthesis '[' on line 1882 | `['data', 'rgba', 'data', 'rgba', 'auto']):` |
| 3537 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_colorbar.py | 68 | 5 | positional argument follows keyword argument | `return fig` |
| 3538 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_colors.py | 32 | 1 | invalid syntax | `def test_create_lookup_table(N, result):` |
| 3539 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_mlab.py | 1003 | 52 | invalid decimal literal | `assert_allclose(np.mean(cohsq), 0.837, atol = 1.e - 3)` |
| 3540 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_agg.py | 39 | 5 | invalid syntax. Perhaps you forgot a comma? | `buf.seek(0)` |
| 3541 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_units.py | 74 | 9 | invalid syntax | `else:` |
| 3542 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_widgets.py | 17 | 1 | invalid syntax | `from numpy.testing import assert_allclose` |
| 3543 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_contour.py | 64 | 1 | invalid syntax | `def test_contour_shape_error(args, message):` |
| 3544 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_triangulation.py | 602 | 20 | invalid decimal literal | `epsilon = 1.e - 10  # Distance for loc boundary` |
| 3545 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_bbox_tight.py | 17 | 1 | invalid syntax | `def test_bbox_inches_tight():` |
| 3546 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_cbook.py | 103 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 94 | `}` |
| 3547 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_path.py | 75 | 30 | closing parenthesis ')' does not match opening parenthesis '[' on line 71 | `closed = True), False, False),` |
| 3548 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_collections.py | 21 | 1 | invalid syntax | `from matplotlib.testing.decorators import check_figures_equal, image_comparison` |
| 3549 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_axes.py | 459 | 57 | closing parenthesis ')' does not match opening parenthesis '[' on line 453 | `[Path.MOVETO, Path.LINETO] * 4),` |
| 3550 | venv_creative/lib/python3.13/site-packages/matplotlib/tests/test_legend.py | 46 | 1 | invalid syntax | `def test_legend_generator():` |
| 3551 | venv_creative/lib/python3.13/site-packages/matplotlib/_api/deprecation.py | 35 | 13 | cannot assign to expression here. Maybe you meant '==' instead of '='? | `("The %(name)s %(obj_type)s" if obj_type else "%(name)s") +` |
| 3552 | venv_creative/lib/python3.13/site-packages/yaml/scanner.py | 279 | 5 | invalid syntax | `def next_possible_simple_key(self):` |
| 3553 | venv_creative/lib/python3.13/site-packages/yaml/error.py | 74 | 76 | unmatched ')' | `or self.context_mark.column != self.problem_mark.column):` |
| 3554 | venv_creative/lib/python3.13/site-packages/yaml/composer.py | 56 | 9 | invalid syntax | `return document` |
| 3555 | venv_creative/lib/python3.13/site-packages/yaml/events.py | 18 | 9 | invalid syntax | `arguments = ', '.join(['%s=%r' % (key, getattr(self, key))` |
| 3556 | venv_creative/lib/python3.13/site-packages/yaml/__init__.py | 12 | 8 | unexpected indent | `__with_libyaml__ = True` |
| 3557 | venv_creative/lib/python3.13/site-packages/yaml/representer.py | 7 | 1 | invalid syntax | `import base64` |
| 3558 | venv_creative/lib/python3.13/site-packages/yaml/reader.py | 45 | 9 | invalid syntax | `else:` |
| 3559 | venv_creative/lib/python3.13/site-packages/yaml/resolver.py | 80 | 1 | expected ':' | `#                 and not isinstance(node_check, str) \` |
| 3560 | venv_creative/lib/python3.13/site-packages/yaml/emitter.py | 86 | 12 | unexpected indent | `self.open_ended = False` |
| 3561 | venv_creative/lib/python3.13/site-packages/loguru/_better_exceptions.py | 37 | 9 | invalid syntax. Perhaps you forgot a comma? | `{` |
| 3562 | venv_creative/lib/python3.13/site-packages/loguru/_handler.py | 63 | 12 | unexpected indent | `self._exception_formatter = exception_formatter` |
| 3563 | venv_creative/lib/python3.13/site-packages/loguru/_logger.py | 116 | 1 | invalid syntax | `from ._simple_sinks import AsyncSink, CallableSink, StandardSink, StreamSink` |
| 3564 | venv_creative/lib/python3.13/site-packages/loguru/_simple_sinks.py | 46 | 48 | '(' was never closed | `record = logging.getLogger().makeRecord(` |
| 3565 | venv_creative/lib/python3.13/site-packages/uvicorn/logging.py | 71 | 12 | unexpected indent | `return super().formatMessage(recordcopy)` |
| 3566 | venv_creative/lib/python3.13/site-packages/uvicorn/middleware/wsgi.py | 19 | 1 | invalid syntax | `def build_environ(scope: HTTPScope, message: ASGIReceiveEvent, body: io.BytesIO) -> Environ:` |
| 3567 | venv_creative/lib/python3.13/site-packages/gradio_client/documentation.py | 37 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"Found another attribute before docstring for {attr} in {cls.__name__}: "` |
| 3568 | venv_creative/lib/python3.13/site-packages/gradio_client/client.py | 220 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 214 | `}` |
| 3569 | venv_creative/lib/python3.13/site-packages/filterpy/examples/bearing_only.py | 40 | 30 | invalid decimal literal | `sf = SUKF(2, 1, dt, alpha = 1.e - 4, beta = 2., kappa = 1.)` |
| 3570 | venv_creative/lib/python3.13/site-packages/filterpy/kalman/CubatureKalmanFilter.py | 326 | 12 | unexpected indent | `self.x_prior = self.x.copy()` |
| 3571 | venv_creative/lib/python3.13/site-packages/filterpy/kalman/UKF.py | 392 | 12 | unexpected indent | `self.x, self.P = UT(self.sigmas_f, self.Wm, self.Wc, self.Q,` |
| 3572 | venv_creative/lib/python3.13/site-packages/filterpy/kalman/EKF.py | 231 | 12 | unexpected indent | `self.x_prior = np.copy(self.x)` |
| 3573 | venv_creative/lib/python3.13/site-packages/filterpy/kalman/ensemble_kalman_filter.py | 269 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.S = P_zz` |
| 3574 | venv_creative/lib/python3.13/site-packages/filterpy/kalman/square_root.py | 169 | 12 | unexpected indent | `self.x_prior = np.copy(self.x)` |
| 3575 | venv_creative/lib/python3.13/site-packages/filterpy/kalman/fading_memory.py | 156 | 9 | invalid syntax | `assert alpha >= 1` |
| 3576 | venv_creative/lib/python3.13/site-packages/filterpy/kalman/kalman_filter.py | 491 | 12 | unexpected indent | `self.x_prior = self.x.copy()` |
| 3577 | venv_creative/lib/python3.13/site-packages/numba/misc/appdirs.py | 147 | 19 | invalid syntax | `if appname:` |
| 3578 | venv_creative/lib/python3.13/site-packages/numba/misc/numba_sysinfo.py | 186 | 9 | ':' expected after dictionary key | `p = psutil.Process()` |
| 3579 | venv_creative/lib/python3.13/site-packages/numba/misc/gdb_hook.py | 19 | 1 | invalid syntax | `def _confirm_gdb(need_ptrace_attach = True):` |
| 3580 | venv_creative/lib/python3.13/site-packages/numba/experimental/structref.py | 15 | 1 | invalid syntax | `from numba.core.typing.templates import AttributeTemplate` |
| 3581 | venv_creative/lib/python3.13/site-packages/numba/core/dispatcher.py | 18 | 1 | invalid syntax | `from numba.core.bytecode import get_code_object` |
| 3582 | venv_creative/lib/python3.13/site-packages/numba/core/serialize.py | 93 | 12 | unexpected indent | `self.states = states` |
| 3583 | venv_creative/lib/python3.13/site-packages/numba/core/funcdesc.py | 41 | 5 | invalid syntax | `def __init__(self, native, modname, qualname, unique_name, doc,` |
| 3584 | venv_creative/lib/python3.13/site-packages/numba/core/postproc.py | 66 | 5 | invalid syntax | `@cached_property` |
| 3585 | venv_creative/lib/python3.13/site-packages/numba/core/transforms.py | 14 | 1 | invalid syntax | `from numba.core.utils import PYVERSION` |
| 3586 | venv_creative/lib/python3.13/site-packages/numba/core/tracing.py | 177 | 12 | unexpected indent | `if inspect.ismodule(arg0):` |
| 3587 | venv_creative/lib/python3.13/site-packages/numba/core/config.py | 38 | 30 | invalid syntax. Perhaps you forgot a comma? | `raise ValueError("Compute capability must be specified as a "` |
| 3588 | venv_creative/lib/python3.13/site-packages/numba/core/analysis.py | 143 | 34 | invalid syntax. Perhaps you forgot a comma? | `outgoing_live_map = dict((out_blk, live_map[out_blk])` |
| 3589 | venv_creative/lib/python3.13/site-packages/numba/core/inline_closurecall.py | 303 | 26 | unterminated string literal (detected at line 304) | `raise ValueError("Reduce function cannot be found for njit \` |
| 3590 | venv_creative/lib/python3.13/site-packages/numba/core/ir_utils.py | 19 | 1 | invalid syntax | `from numba.core.errors import (CompilerError, NumbaPendingDeprecationWarning,` |
| 3591 | venv_creative/lib/python3.13/site-packages/numba/core/old_boxing.py | 72 | 1 | invalid syntax | `@box(types.Float)` |
| 3592 | venv_creative/lib/python3.13/site-packages/numba/core/callconv.py | 39 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `int32_t = ir.IntType(32)` |
| 3593 | venv_creative/lib/python3.13/site-packages/numba/core/new_boxing.py | 88 | 1 | invalid syntax | `@box(types.PythonInteger)` |
| 3594 | venv_creative/lib/python3.13/site-packages/numba/core/ir.py | 19 | 1 | invalid syntax | `from numba.core.utils import (BINOPS_TO_OPERATORS, INPLACE_BINOPS_TO_OPERATORS,` |
| 3595 | venv_creative/lib/python3.13/site-packages/numba/core/utils.py | 299 | 5 | invalid syntax | `def copy(self):` |
| 3596 | venv_creative/lib/python3.13/site-packages/numba/core/debuginfo.py | 134 | 13 | invalid syntax. Perhaps you forgot a comma? | `m = self.module` |
| 3597 | venv_creative/lib/python3.13/site-packages/numba/core/typeinfer.py | 29 | 1 | invalid syntax | `from numba.core.funcdesc import qualifying_prefix` |
| 3598 | venv_creative/lib/python3.13/site-packages/numba/core/errors.py | 56 | 9 | invalid syntax | `else:` |
| 3599 | venv_creative/lib/python3.13/site-packages/numba/core/typed_passes.py | 13 | 1 | invalid syntax | `from numba.core.annotations import type_annotations` |
| 3600 | venv_creative/lib/python3.13/site-packages/numba/core/bytecode.py | 32 | 1 | invalid syntax | `def get_function_object(obj):` |
| 3601 | venv_creative/lib/python3.13/site-packages/numba/core/untyped_passes.py | 10 | 1 | invalid syntax | `from numba.core.analysis import (compute_cfg_from_blocks, compute_use_defs,` |
| 3602 | venv_creative/lib/python3.13/site-packages/numba/core/controlflow.py | 18 | 1 | invalid syntax | `class CFBlock(object):` |
| 3603 | venv_creative/lib/python3.13/site-packages/numba/core/base.py | 16 | 1 | invalid syntax | `from numba.core.compiler_lock import global_compiler_lock` |
| 3604 | venv_creative/lib/python3.13/site-packages/numba/core/cgutils.py | 104 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self._builder = builder` |
| 3605 | venv_creative/lib/python3.13/site-packages/numba/core/pythonapi.py | 172 | 9 | invalid syntax | `return builder.load(ret)` |
| 3606 | venv_creative/lib/python3.13/site-packages/numba/core/typeconv/rules.py | 58 | 12 | unexpected indent | `tcr.unsafe_unsafe(types.uintp, types.voidptr)` |
| 3607 | venv_creative/lib/python3.13/site-packages/numba/core/types/functions.py | 26 | 21 | invalid syntax. Perhaps you forgot a comma? | `_header_template = (_header_lead + " {the_function} found for signature:\n \n "` |
| 3608 | venv_creative/lib/python3.13/site-packages/numba/core/types/function_type.py | 7 | 1 | invalid syntax | `from abc import ABC, abstractmethod` |
| 3609 | venv_creative/lib/python3.13/site-packages/numba/core/types/common.py | 66 | 13 | invalid syntax | `raise NumbaTypeError(msg.format(dtype))` |
| 3610 | venv_creative/lib/python3.13/site-packages/numba/core/runtime/nrtopt.py | 30 | 1 | invalid syntax | `def _remove_redundant_nrt_refct(llvmir):` |
| 3611 | venv_creative/lib/python3.13/site-packages/numba/core/typing/npydecl.py | 11 | 1 | invalid syntax | `from numba.core.typing.templates import (AbstractTemplate, AttributeTemplate,` |
| 3612 | venv_creative/lib/python3.13/site-packages/numba/core/typing/templates.py | 26 | 1 | invalid syntax | `class Signature(object):` |
| 3613 | venv_creative/lib/python3.13/site-packages/numba/core/typing/context.py | 218 | 23 | unindent does not match any outer indentation level | `res = None` |
| 3614 | venv_creative/lib/python3.13/site-packages/numba/cuda/dispatcher.py | 37 | 1 | invalid syntax | `class _Kernel(serialize.ReduceMixin):` |
| 3615 | venv_creative/lib/python3.13/site-packages/numba/cuda/deviceufunc.py | 145 | 17 | invalid syntax | `if all_matches:` |
| 3616 | venv_creative/lib/python3.13/site-packages/numba/cuda/vector_types.py | 121 | 12 | unexpected indent | `cases = [signature(vector_type, *arglist) for arglist in overloads]` |
| 3617 | venv_creative/lib/python3.13/site-packages/numba/cuda/__init__.py | 8 | 8 | unexpected indent | `from .device_init import _auto_device` |
| 3618 | venv_creative/lib/python3.13/site-packages/numba/cuda/random.py | 30 | 31 | '(' was never closed | `xoroshiro128p_dtype = np.dtype([('s0', np.uint64), ('s1', np.uint64)],` |
| 3619 | venv_creative/lib/python3.13/site-packages/numba/cuda/cudadecl.py | 12 | 1 | invalid syntax | `from numba.core.typing.templates import (AbstractTemplate, AttributeTemplate,` |
| 3620 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/nocuda/test_dummyarray.py | 31 | 5 | invalid syntax | `def test_slice0_1d(self):` |
| 3621 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudapy/test_localmem.py | 128 | 54 | unindent does not match any outer indentation level | `with self.assertRaisesRegex(TypingError, re):` |
| 3622 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudapy/test_multiprocessing.py | 15 | 8 | unexpected indent | `try:` |
| 3623 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudapy/test_gufunc_scalar.py | 83 | 9 | invalid syntax | `def saxpy(a, x, y, out):` |
| 3624 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudapy/test_exception.py | 164 | 16 | unexpected indent | `else:` |
| 3625 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudapy/test_userexc.py | 9 | 17 | '(' was never closed | `regex_pattern = (` |
| 3626 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudapy/test_sm_creation.py | 24 | 12 | invalid syntax. Perhaps you forgot a comma? | `i, j = cuda.grid(2)` |
| 3627 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudapy/test_warp_ops.py | 151 | 12 | unexpected indent | `compiled[1, nelem](ary, xor)` |
| 3628 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudapy/test_complex.py | 22 | 1 | invalid syntax | `def compile_scalar_func(pyfunc, argtypes, restype):` |
| 3629 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudadrv/test_detect.py | 11 | 1 | invalid syntax | `from numba.tests.support import captured_stdout` |
| 3630 | venv_creative/lib/python3.13/site-packages/numba/cuda/tests/cudadrv/test_deallocations.py | 10 | 1 | invalid syntax | `from numba.tests.support import captured_stderr` |
| 3631 | venv_creative/lib/python3.13/site-packages/numba/cuda/simulator/__init__.py | 7 | 34 | '(' was never closed | `from .cudadrv.devicearray import (auto_device, device_array, device_array_like,` |
| 3632 | venv_creative/lib/python3.13/site-packages/numba/cuda/cudadrv/dummyarray.py | 27 | 1 | invalid syntax | `class Dim(object):` |
| 3633 | venv_creative/lib/python3.13/site-packages/numba/cuda/cudadrv/driver.py | 32 | 1 | invalid syntax | `from itertools import product` |
| 3634 | venv_creative/lib/python3.13/site-packages/numba/stencils/stencilparfor.py | 21 | 1 | invalid syntax | `from numba.core.typing import signature` |
| 3635 | venv_creative/lib/python3.13/site-packages/numba/tests/test_builtins.py | 409 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `cfunc = jit((types.complex64,), **flags)(pyfunc)` |
| 3636 | venv_creative/lib/python3.13/site-packages/numba/tests/test_array_manipulation.py | 173 | 8 | unexpected indent | `y = arr.y` |
| 3637 | venv_creative/lib/python3.13/site-packages/numba/tests/test_dictobject.py | 22 | 1 | invalid syntax | `from numba.typed import Dict, List, dictobject` |
| 3638 | venv_creative/lib/python3.13/site-packages/numba/tests/test_linalg.py | 2616 | 36 | invalid decimal literal | `b[0] = 1e-14 + 1e - 14j` |
| 3639 | venv_creative/lib/python3.13/site-packages/numba/tests/enum_usecases.py | 39 | 8 | unexpected indent | `square = 500` |
| 3640 | venv_creative/lib/python3.13/site-packages/numba/tests/test_debuginfo.py | 210 | 5 | invalid syntax | `def test_DILocation(self):` |
| 3641 | venv_creative/lib/python3.13/site-packages/numba/tests/test_typeinfer.py | 41 | 1 | invalid syntax | `class TestArgRetCasting(unittest.TestCase):` |
| 3642 | venv_creative/lib/python3.13/site-packages/numba/tests/test_typeguard.py | 30 | 12 | unexpected indent | `self._exception_type = getattr(typeguard, 'TypeCheckError', TypeError)` |
| 3643 | venv_creative/lib/python3.13/site-packages/numba/tests/test_mangling.py | 17 | 12 | unexpected indent | `name = default_mangler(fname, argtypes)` |
| 3644 | venv_creative/lib/python3.13/site-packages/numba/tests/test_npdatetime.py | 147 | 12 | unexpected indent | `for unit in all_units + ('',):` |
| 3645 | venv_creative/lib/python3.13/site-packages/numba/tests/test_np_functions.py | 653 | 46 | invalid decimal literal | `5e-21 + 0j, -5e-21 + 0j, 5e - 21j, +(0 - 5e - 21j)                 # noqa` |
| 3646 | venv_creative/lib/python3.13/site-packages/numba/tests/test_ir_inlining.py | 20 | 1 | invalid syntax | `from numba.core.typed_passes import InlineOverloads` |
| 3647 | venv_creative/lib/python3.13/site-packages/numba/tests/test_array_exprs.py | 16 | 1 | invalid syntax | `from numba.tests.support import (MemoryLeakMixin, TestCase, create_temp_module,` |
| 3648 | venv_creative/lib/python3.13/site-packages/numba/tests/test_jitclasses.py | 2132 | 32 | closing parenthesis ')' does not match opening parenthesis '[' on line 2126 | `test_values):` |
| 3649 | venv_creative/lib/python3.13/site-packages/numba/tests/test_obj_lifetime.py | 300 | 5 | invalid syntax | `def test_simple1(self):` |
| 3650 | venv_creative/lib/python3.13/site-packages/numba/tests/test_extending.py | 348 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 341 | `):` |
| 3651 | venv_creative/lib/python3.13/site-packages/numba/tests/test_remove_dead.py | 19 | 1 | invalid syntax | `from numba.core.registry import cpu_target` |
| 3652 | venv_creative/lib/python3.13/site-packages/numba/tests/test_literal_dispatch.py | 12 | 1 | invalid syntax | `from numba.core.typing import signature` |
| 3653 | venv_creative/lib/python3.13/site-packages/numba/tests/test_ir.py | 35 | 9 | invalid syntax. Perhaps you forgot a comma? | `self.assertIs(top.get('orange'), orange)` |
| 3654 | venv_creative/lib/python3.13/site-packages/numba/tests/test_generators.py | 226 | 5 | invalid syntax | `def test_gen5_objmode(self):` |
| 3655 | venv_creative/lib/python3.13/site-packages/numba/tests/test_dictimpl.py | 63 | 16 | unexpected indent | `else:` |
| 3656 | venv_creative/lib/python3.13/site-packages/numba/tests/test_exceptions.py | 13 | 19 | invalid syntax | `force_pyobj_flags = {'nopython': False, 'forceobj': True}` |
| 3657 | venv_creative/lib/python3.13/site-packages/numba/tests/test_comprehension.py | 169 | 21 | invalid syntax. Perhaps you forgot a comma? | `return [(a, b, c)` |
| 3658 | venv_creative/lib/python3.13/site-packages/numba/tests/test_mathlib.py | 198 | 5 | invalid syntax | `def run_binary(self, pyfunc, x_types, x_values, y_values, prec='exact'):` |
| 3659 | venv_creative/lib/python3.13/site-packages/numba/tests/test_ctypes.py | 34 | 5 | invalid syntax | `def test_from_ctypes(self):` |
| 3660 | venv_creative/lib/python3.13/site-packages/numba/tests/test_np_randomgen.py | 16 | 1 | invalid syntax | `from numpy.random import MT19937, Generator` |
| 3661 | venv_creative/lib/python3.13/site-packages/numba/tests/test_usecases.py | 20 | 12 | unexpected indent | `cfunc = njit((types.int32, types.int32))(pyfunc)` |
| 3662 | venv_creative/lib/python3.13/site-packages/numba/tests/test_try_except.py | 12 | 1 | invalid syntax | `from numba.tests.support import (MemoryLeakMixin, TestCase, captured_stdout,` |
| 3663 | venv_creative/lib/python3.13/site-packages/numba/tests/test_sort.py | 485 | 44 | unindent does not match any outer indentation level | `orig_keys = sum(chunks, [])` |
| 3664 | venv_creative/lib/python3.13/site-packages/numba/tests/test_alignment.py | 37 | 12 | unexpected indent | `@njit((rec[:],))` |
| 3665 | venv_creative/lib/python3.13/site-packages/numba/tests/test_array_methods.py | 17 | 13 | invalid syntax | `TIMEDELTA_M = 'timedelta64[M]'` |
| 3666 | venv_creative/lib/python3.13/site-packages/numba/tests/test_stencils.py | 50 | 1 | invalid syntax | `@stencil` |
| 3667 | venv_creative/lib/python3.13/site-packages/numba/tests/test_dataflow.py | 158 | 12 | unexpected indent | `cfunc = jit((types.int32,), **flags)(pyfunc)` |
| 3668 | venv_creative/lib/python3.13/site-packages/numba/tests/test_buffer_protocol.py | 86 | 13 | invalid syntax | `yield array.array(letter, [i + offset for i in range(n)])` |
| 3669 | venv_creative/lib/python3.13/site-packages/numba/tests/test_array_analysis.py | 17 | 1 | invalid syntax | `from numba.core.untyped_passes import (DeadBranchPrune, ExtractByteCode, FixupArgs,` |
| 3670 | venv_creative/lib/python3.13/site-packages/numba/tests/test_runtests.py | 75 | 5 | invalid syntax | `def _get_numba_tests_from_listing(self, listing):` |
| 3671 | venv_creative/lib/python3.13/site-packages/numba/tests/test_compile_cache.py | 35 | 13 | invalid syntax | `assert function.is_declaration` |
| 3672 | venv_creative/lib/python3.13/site-packages/numba/tests/test_refop_pruning.py | 95 | 5 | invalid syntax | `@TestCase.run_test_in_subprocess` |
| 3673 | venv_creative/lib/python3.13/site-packages/numba/tests/test_ufuncs.py | 132 | 5 | invalid syntax | `@functools.lru_cache(maxsize = None)` |
| 3674 | venv_creative/lib/python3.13/site-packages/numba/tests/test_unicode_array.py | 280 | 21 | invalid syntax. Perhaps you forgot a comma? | `(np.array([b'123']), 0)` |
| 3675 | venv_creative/lib/python3.13/site-packages/numba/tests/test_compiler_flags.py | 116 | 12 | unexpected indent | `flags = Flags()` |
| 3676 | venv_creative/lib/python3.13/site-packages/numba/tests/test_withlifting.py | 26 | 1 | invalid syntax | `def get_func_ir(func):` |
| 3677 | venv_creative/lib/python3.13/site-packages/numba/tests/test_parfors.py | 31 | 1 | invalid syntax | `from numba.core import (compiler, config, cpu, errors, inline_closurecall, ir, rewrites,` |
| 3678 | venv_creative/lib/python3.13/site-packages/numba/tests/test_sets.py | 15 | 7 | invalid syntax | `Point = namedtuple('Point', ('a', 'b'))` |
| 3679 | venv_creative/lib/python3.13/site-packages/numba/tests/test_dyn_array.py | 315 | 9 | invalid syntax. Perhaps you forgot a comma? | `self.assert_array_nrt_refct(cfunc(arr_a, arr_b), 1)` |
| 3680 | venv_creative/lib/python3.13/site-packages/numba/tests/test_types.py | 20 | 1 | invalid syntax | `from numba.core.types.abstract import _typecache` |
| 3681 | venv_creative/lib/python3.13/site-packages/numba/tests/test_codegen.py | 172 | 12 | unexpected indent | `with warnings.catch_warnings(record = True) as w:` |
| 3682 | venv_creative/lib/python3.13/site-packages/numba/tests/test_random.py | 200 | 1 | invalid syntax | `class BaseTest(TestCase):` |
| 3683 | venv_creative/lib/python3.13/site-packages/numba/tests/doc_examples/test_interval_example.py | 92 | 27 | '[' was never closed | `members = [('lo', types.float64),` |
| 3684 | venv_creative/lib/python3.13/site-packages/numba/tests/doc_examples/test_structref_usage.py | 140 | 12 | unexpected indent | `from numba.core.extending import overload_method` |
| 3685 | venv_creative/lib/python3.13/site-packages/numba/tests/npyufunc/test_ufuncbuilding.py | 88 | 9 | invalid syntax. Perhaps you forgot a comma? | `builder.add("(int64, int64)")` |
| 3686 | venv_creative/lib/python3.13/site-packages/numba/tests/npyufunc/test_errors.py | 53 | 12 | unexpected indent | `self.assertEqual(list(out), [1, 2, 0, 3, 0, 4])` |
| 3687 | venv_creative/lib/python3.13/site-packages/numba/tests/npyufunc/test_dufunc.py | 13 | 1 | invalid syntax | `from numba.np.numpy_support import from_dtype` |
| 3688 | venv_creative/lib/python3.13/site-packages/numba/tests/npyufunc/test_gufunc.py | 46 | 9 | invalid syntax. Perhaps you forgot a comma? | `gufunc.add((float32[:, :], float32[:, :], float32[:, :]))` |
| 3689 | venv_creative/lib/python3.13/site-packages/numba/testing/main.py | 113 | 9 | invalid syntax | `raise ValueError(msg)` |
| 3690 | venv_creative/lib/python3.13/site-packages/numba/cpython/setobj.py | 20 | 1 | invalid syntax | `from numba.cpython import slicing` |
| 3691 | venv_creative/lib/python3.13/site-packages/numba/cpython/new_hashing.py | 25 | 13 | invalid syntax | `_hash_width = sys.hash_info.width` |
| 3692 | venv_creative/lib/python3.13/site-packages/numba/cpython/old_hashing.py | 25 | 13 | invalid syntax | `_hash_width = sys.hash_info.width` |
| 3693 | venv_creative/lib/python3.13/site-packages/numba/cpython/listobj.py | 18 | 1 | invalid syntax | `from numba.cpython import slicing` |
| 3694 | venv_creative/lib/python3.13/site-packages/numba/cpython/new_tupleobj.py | 15 | 1 | invalid syntax | `@lower_builtin(types.NamedTupleClass, types.VarArg(types.Any))` |
| 3695 | venv_creative/lib/python3.13/site-packages/numba/cpython/new_numbers.py | 15 | 1 | invalid syntax | `from numba.cpython.unsafe.numbers import viewer` |
| 3696 | venv_creative/lib/python3.13/site-packages/numba/cpython/old_builtins.py | 15 | 1 | invalid syntax | `from numba.core.extending import intrinsic, overload` |
| 3697 | venv_creative/lib/python3.13/site-packages/numba/cpython/old_numbers.py | 15 | 1 | invalid syntax | `from numba.cpython.unsafe.numbers import viewer` |
| 3698 | venv_creative/lib/python3.13/site-packages/numba/cpython/iterators.py | 12 | 1 | invalid syntax | `@lower_builtin('getiter', types.IteratorType)` |
| 3699 | venv_creative/lib/python3.13/site-packages/numba/cpython/new_builtins.py | 15 | 1 | invalid syntax | `from numba.core.extending import intrinsic, overload` |
| 3700 | venv_creative/lib/python3.13/site-packages/numba/cpython/old_tupleobj.py | 15 | 1 | invalid syntax | `@lower_builtin(types.NamedTupleClass, types.VarArg(types.Any))` |
| 3701 | venv_creative/lib/python3.13/site-packages/numba/parfors/parfor.py | 5065 | 29 | too many nested parentheses | `if (all([x.name in indices or` |
| 3702 | venv_creative/lib/python3.13/site-packages/numba/typed/typedlist.py | 22 | 1 | invalid syntax | `from numba.core.imputils import numba_typeref_ctor` |
| 3703 | venv_creative/lib/python3.13/site-packages/numba/typed/listobject.py | 15 | 1 | invalid syntax | `from numba.core.imputils import RefType, impl_ret_borrowed, iternext_impl` |
| 3704 | venv_creative/lib/python3.13/site-packages/numba/typed/dictobject.py | 17 | 1 | invalid syntax | `from numba.core.imputils import (RefType, impl_ret_borrowed, impl_ret_untracked,` |
| 3705 | venv_creative/lib/python3.13/site-packages/numba/np/new_arraymath.py | 16 | 1 | invalid syntax | `from numba.core.extending import intrinsic, overload, overload_method, register_jitable` |
| 3706 | venv_creative/lib/python3.13/site-packages/numba/np/linalg.py | 2111 | 27 | invalid decimal literal | `def pinv_impl(a, rcond = 1.e - 15):` |
| 3707 | venv_creative/lib/python3.13/site-packages/numba/np/npdatetime_helpers.py | 104 | 12 | unexpected indent | `else:` |
| 3708 | venv_creative/lib/python3.13/site-packages/numba/np/old_arraymath.py | 16 | 1 | invalid syntax | `from numba.core.extending import intrinsic, overload, overload_method, register_jitable` |
| 3709 | venv_creative/lib/python3.13/site-packages/numba/np/arrayobj.py | 4497 | 45 | too many nested parentheses | `ptr = builder.gep(arr.data, [index])` |
| 3710 | venv_creative/lib/python3.13/site-packages/numba/np/npdatetime.py | 18 | 1 | invalid syntax | `from numba.extending import overload_method` |
| 3711 | venv_creative/lib/python3.13/site-packages/numba/np/ufunc/array_exprs.py | 88 | 51 | unindent does not match any outer indentation level | `array_assigns[target_name] = instr` |
| 3712 | venv_creative/lib/python3.13/site-packages/numba/np/math/numbers.py | 93 | 5 | invalid syntax | `with builder.if_then(builder.not_(is_overflow), likely = True):` |
| 3713 | venv_creative/lib/python3.13/site-packages/numba/np/random/new_distributions.py | 16 | 1 | invalid syntax | `from numba.np.random.generator_core import (next_double, next_float, next_uint32,` |
| 3714 | venv_creative/lib/python3.13/site-packages/numba/np/random/old_distributions.py | 18 | 1 | invalid syntax | `from numba.np.random.generator_core import (next_double, next_float, next_uint32,` |
| 3715 | venv_creative/lib/python3.13/site-packages/numba/np/polynomial/polynomial_functions.py | 137 | 9 | invalid syntax | `else:` |
| 3716 | venv_creative/lib/python3.13/site-packages/torchgen/gen.py | 1599 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 1594 | `) -> dict[str, list[str]]:` |
| 3717 | venv_creative/lib/python3.13/site-packages/torchgen/gen_aoti_c_shim.py | 19 | 1 | invalid syntax | `from torchgen.utils import FileManager, mapMaybe` |
| 3718 | venv_creative/lib/python3.13/site-packages/torchgen/utils.py | 95 | 41 | unindent does not match any outer indentation level | `msg = textwrap.indent(msg, "  ")` |
| 3719 | venv_creative/lib/python3.13/site-packages/torchgen/gen_lazy_tensor.py | 354 | 1 | closing parenthesis ')' does not match opening parenthesis '[' on line 327 | `) -> None:` |
| 3720 | venv_creative/lib/python3.13/site-packages/torchgen/selective_build/selector.py | 15 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 3721 | venv_creative/lib/python3.13/site-packages/torchgen/packaged/autograd/gen_autograd_functions.py | 611 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 605 | `},` |
| 3722 | venv_creative/lib/python3.13/site-packages/torchgen/packaged/autograd/gen_variable_type.py | 970 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 964 | `),` |
| 3723 | venv_creative/lib/python3.13/site-packages/torchgen/dest/ufunc.py | 13 | 1 | invalid syntax | `from torchgen.context import with_native_function` |
| 3724 | venv_creative/lib/python3.13/site-packages/torchgen/dest/register_dispatch_key.py | 18 | 1 | invalid syntax | `from torchgen.context import method_with_native_function, native_function_manager` |
| 3725 | venv_creative/lib/python3.13/site-packages/torchgen/api/python.py | 14 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 3726 | venv_creative/lib/python3.13/site-packages/torchgen/api/lazy.py | 11 | 1 | invalid syntax | `from torchgen.model import (Argument, BaseTy, BaseType, FunctionSchema, ListType,` |
| 3727 | venv_creative/lib/python3.13/site-packages/urllib3/response.py | 38 | 1 | invalid syntax | `from .util.response import is_fp_closed, is_response_to_head` |
| 3728 | venv_creative/lib/python3.13/site-packages/urllib3/util/ssl_.py | 79 | 24 | invalid syntax | `if typing.TYPE_CHECKING:` |
| 3729 | venv_creative/lib/python3.13/site-packages/urllib3/util/retry.py | 225 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 219 | `) -> None:` |
| 3730 | venv_creative/lib/python3.13/site-packages/urllib3/contrib/emscripten/fetch.py | 51 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 3731 | venv_creative/lib/python3.13/site-packages/feedparser/mixin.py | 487 | 5 | invalid syntax | `def push(self, element, expecting_text):` |
| 3732 | venv_creative/lib/python3.13/site-packages/feedparser/encodings.py | 54 | 15 | invalid syntax | `EBCDIC_MARKER = b'\x4C\x6F\xA7\x94'` |
| 3733 | venv_creative/lib/python3.13/site-packages/feedparser/api.py | 112 | 1 | expected ':' | `#         and urllib.parse.urlparse(url_file_stream_or_string)[0] in ('http', 'https', 'ftp', 'file', 'feed'):` |
| 3734 | venv_creative/lib/python3.13/site-packages/feedparser/namespaces/_base.py | 151 | 12 | unexpected indent | `context = self._get_context()` |
| 3735 | venv_creative/lib/python3.13/site-packages/setuptools/depends.py | 54 | 16 | '(' was never closed | `return (` |
| 3736 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/packaging/_manylinux.py | 48 | 1 | invalid syntax | `def _is_linux_i686(executable: str) -> bool:` |
| 3737 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/packaging/specifiers.py | 249 | 5 | invalid syntax | `def __init__(self, spec: str = "", prereleases: bool ¦ None = None) -> None:` |
| 3738 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/inflect/__init__.py | 69 | 1 | invalid syntax | `from more_itertools import windowed_complete` |
| 3739 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/wheel/_bdist_wheel.py | 113 | 9 | invalid syntax | `return fallback` |
| 3740 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/_manylinux.py | 46 | 1 | invalid syntax | `def _is_linux_i686(executable: str) -> bool:` |
| 3741 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/wheel/vendored/packaging/specifiers.py | 247 | 5 | invalid syntax | `def __init__(self, spec: str = "", prereleases: Optional[bool] = None) -> None:` |
| 3742 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/more_itertools/more.py | 11 | 1 | invalid syntax | `from math import comb, e, exp, factorial, floor, fsum, log, perm, tau` |
| 3743 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/backports/tarfile/__init__.py | 79 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `NUL = b"\0"                     # the null character` |
| 3744 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/autocommand/automain.py | 63 | 12 | unexpected indent | `else:` |
| 3745 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/api.py | 42 | 12 | unexpected indent | `"""` |
| 3746 | venv_creative/lib/python3.13/site-packages/setuptools/_vendor/platformdirs/windows.py | 239 | 12 | unexpected indent | `import winreg  # noqa: PLC0415` |
| 3747 | venv_creative/lib/python3.13/site-packages/setuptools/tests/test_build_py.py | 35 | 5 | invalid syntax. Perhaps you forgot a comma? | `os.makedirs('path / subpath')` |
| 3748 | venv_creative/lib/python3.13/site-packages/setuptools/tests/test_sdist.py | 291 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 283 | `}` |
| 3749 | venv_creative/lib/python3.13/site-packages/setuptools/command/bdist_wheel.py | 93 | 9 | invalid syntax | `return fallback` |
| 3750 | venv_creative/lib/python3.13/site-packages/setuptools/_distutils/dist.py | 28 | 1 | invalid syntax | `from .fancy_getopt import FancyGetopt, translate_longopt` |
| 3751 | venv_creative/lib/python3.13/site-packages/setuptools/_distutils/tests/test_extension.py | 26 | 18 | '[' was never closed | `wanted = [` |
| 3752 | venv_creative/lib/python3.13/site-packages/setuptools/_distutils/tests/test_install_data.py | 39 | 12 | unexpected indent | `cmd.ensure_finalized()` |
| 3753 | venv_creative/lib/python3.13/site-packages/setuptools/_distutils/tests/test_util.py | 21 | 1 | invalid syntax | `import pytest` |
| 3754 | venv_creative/lib/python3.13/site-packages/setuptools/_distutils/tests/test_install_headers.py | 31 | 12 | unexpected indent | `cmd.install_dir = os.path.join(pkg_dir, 'inst')` |
| 3755 | venv_creative/lib/python3.13/site-packages/setuptools/_distutils/tests/test_sdist.py | 64 | 5 | invalid syntax | `with path.Path(self.tmp_dir):` |
| 3756 | venv_creative/lib/python3.13/site-packages/setuptools/_distutils/command/build_ext.py | 25 | 1 | invalid syntax | `from ..extension import Extension` |
| 3757 | venv_creative/lib/python3.13/site-packages/setuptools/_distutils/command/install.py | 235 | 20 | invalid syntax | `boolean_options: ClassVar[list[str]] = ['compile', 'force', 'skip - build']` |
| 3758 | venv_creative/lib/python3.13/site-packages/pkg_resources/__init__.py | 59 | 1 | invalid syntax | `import _imp` |
| 3759 | venv_creative/lib/python3.13/site-packages/aifc/__init__.py | 162 | 1 | invalid syntax | `class Error(Exception):` |
| 3760 | venv_creative/lib/python3.13/site-packages/pydantic/functional_validators.py | 14 | 1 | invalid syntax | `from pydantic_core import PydanticUndefined` |
| 3761 | venv_creative/lib/python3.13/site-packages/pydantic/__init__.py | 18 | 5 | invalid syntax | `from . import dataclasses` |
| 3762 | venv_creative/lib/python3.13/site-packages/pydantic/mypy.py | 20 | 1 | invalid syntax | `from mypy.options import Options` |
| 3763 | venv_creative/lib/python3.13/site-packages/pydantic/json_schema.py | 723 | 21 | closing parenthesis '}' does not match opening parenthesis '(' on line 707 | `}` |
| 3764 | venv_creative/lib/python3.13/site-packages/pydantic/networks.py | 14 | 1 | invalid syntax | `from typing import TYPE_CHECKING, Annotated, Any, ClassVar` |
| 3765 | venv_creative/lib/python3.13/site-packages/pydantic/type_adapter.py | 20 | 1 | invalid syntax | `from .config import ConfigDict` |
| 3766 | venv_creative/lib/python3.13/site-packages/pydantic/dataclasses.py | 12 | 1 | invalid syntax | `from warnings import warn` |
| 3767 | venv_creative/lib/python3.13/site-packages/pydantic/v1/fields.py | 821 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 809 | `}` |
| 3768 | venv_creative/lib/python3.13/site-packages/pydantic/v1/validators.py | 658 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 649 | `),` |
| 3769 | venv_creative/lib/python3.13/site-packages/pydantic/v1/types.py | 14 | 1 | invalid syntax | `from uuid import UUID` |
| 3770 | venv_creative/lib/python3.13/site-packages/pydantic/v1/networks.py | 6 | 1 | invalid syntax | `from typing import (TYPE_CHECKING, Any, Collection, Dict, Generator, List, Match,` |
| 3771 | venv_creative/lib/python3.13/site-packages/pydantic/v1/dataclasses.py | 53 | 1 | invalid syntax | `from pydantic.v1.class_validators import gather_all_validators` |
| 3772 | venv_creative/lib/python3.13/site-packages/pydantic/v1/main.py | 823 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 808 | `}` |
| 3773 | venv_creative/lib/python3.13/site-packages/pydantic/_internal/_generate_schema.py | 596 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 588 | `),` |
| 3774 | venv_creative/lib/python3.13/site-packages/pydantic/_internal/_discriminated_union.py | 14 | 8 | unexpected indent | `from ._core_metadata import CoreMetadata` |
| 3775 | venv_creative/lib/python3.13/site-packages/pydantic/deprecated/class_validators.py | 72 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `V1RootValidator = Union[` |
| 3776 | venv_creative/lib/python3.13/site-packages/einops/_backends.py | 534 | 12 | unexpected indent | `return HashableTuple(tuple(shape))` |
| 3777 | venv_creative/lib/python3.13/site-packages/einops/tests/test_parsing.py | 30 | 17 | '[' was never closed | `for name in [` |
| 3778 | venv_creative/lib/python3.13/site-packages/einops/tests/test_examples.py | 135 | 9 | did you forget parentheses around the comprehension target? | `test1,` |
| 3779 | venv_creative/lib/python3.13/site-packages/reportlab/platypus/paraparser.py | 2696 | 21 | invalid syntax | `self.nlines += 1` |
| 3780 | venv_creative/lib/python3.13/site-packages/reportlab/platypus/flowables.py | 43 | 9 | invalid syntax | `__all__ = '''AnchorFlowable BalancedColumns BulletDrawer CallerMacro CondPageBreak DDIndenter DocAssert` |
| 3781 | venv_creative/lib/python3.13/site-packages/reportlab/platypus/para.py | 2455 | 38 | closing parenthesis ')' does not match opening parenthesis '[' on line 2443 | `) + [` |
| 3782 | venv_creative/lib/python3.13/site-packages/reportlab/platypus/frames.py | 16 | 1 | invalid syntax | `import logging` |
| 3783 | venv_creative/lib/python3.13/site-packages/reportlab/platypus/figures.py | 45 | 12 | unexpected indent | `self.captionBackColor = captionBackColor` |
| 3784 | venv_creative/lib/python3.13/site-packages/reportlab/platypus/paragraph.py | 12 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `__version__='3.5.20'` |
| 3785 | venv_creative/lib/python3.13/site-packages/reportlab/platypus/tables.py | 12 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `__version__='3.5.21'` |
| 3786 | venv_creative/lib/python3.13/site-packages/reportlab/pdfbase/pdfmetrics.py | 31 | 1 | invalid syntax | `from reportlab.pdfbase import _fontdata, rl_codecs` |
| 3787 | venv_creative/lib/python3.13/site-packages/reportlab/pdfbase/pdfdoc.py | 29 | 1 | invalid syntax | `from reportlab.lib.utils import (TimeStamp, _digester, annotateException, bytestr,` |
| 3788 | venv_creative/lib/python3.13/site-packages/reportlab/pdfbase/acroform.py | 12 | 1 | invalid syntax | `from reportlab.pdfbase.pdfmetrics import stringWidth` |
| 3789 | venv_creative/lib/python3.13/site-packages/reportlab/pdfbase/pdfutils.py | 168 | 12 | '(' was never closed | `return (text` |
| 3790 | venv_creative/lib/python3.13/site-packages/reportlab/pdfgen/textobject.py | 84 | 17 | invalid syntax. Perhaps you forgot a comma? | `_bidiKS.add(klassName,NS[klassName])` |
| 3791 | venv_creative/lib/python3.13/site-packages/reportlab/pdfgen/canvas.py | 2131 | 60 | unterminated triple-quoted string literal (detected at line 2222) | `got drawn, without necessarily saving pages to disk"""` |
| 3792 | venv_creative/lib/python3.13/site-packages/reportlab/lib/testutils.py | 121 | 1 | invalid syntax | `def mockUrlRead(name):` |
| 3793 | venv_creative/lib/python3.13/site-packages/reportlab/lib/attrmap.py | 191 | 13 | '{' was never closed | `{'__attrproxy__':[],` |
| 3794 | venv_creative/lib/python3.13/site-packages/reportlab/lib/corp.py | 49 | 5 | invalid syntax | `def __init__(self):` |
| 3795 | venv_creative/lib/python3.13/site-packages/reportlab/lib/normalDate.py | 159 | 5 | invalid syntax | `def __add__(self, days):` |
| 3796 | venv_creative/lib/python3.13/site-packages/reportlab/lib/colors.py | 248 | 5 | invalid syntax | `def fader(self, n, reverse = False):` |
| 3797 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/shapes.py | 347 | 5 | invalid syntax | `def __init__(self, *elements, **keywords):` |
| 3798 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/svgpath.py | 13 | 1 | invalid syntax | `def split_floats(op, min_num, value):` |
| 3799 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/renderSVG.py | 224 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self.doc = implementation.createDocument(None,"svg",doctype)` |
| 3800 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/renderPS.py | 19 | 1 | invalid syntax | `from reportlab.pdfgen.canvas import FILL_EVEN_ODD` |
| 3801 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/widgetbase.py | 179 | 5 | invalid syntax | `def __init__(self,x = 0,y = 0,scale = 1.0,contents = None):` |
| 3802 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/renderPM.py | 140 | 20 | unexpected indent | `if len(da)!=2 or not isinstance(da[1],(list,tuple)):` |
| 3803 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/testshapes.py | 41 | 13 | did you forget parentheses around the comprehension target? | `('Adventurer Light SF','Advlit.ttf'),('ArialMS','ARIAL.TTF'),` |
| 3804 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/renderPDF.py | 25 | 1 | invalid syntax | `from reportlab.graphics.shapes import *` |
| 3805 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/slidebox.py | 48 | 5 | invalid syntax | `def __init__(self):` |
| 3806 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/doughnut.py | 22 | 1 | invalid syntax | `from reportlab.graphics.shapes import Drawing, Group, Wedge` |
| 3807 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/piecharts.py | 27 | 1 | invalid syntax | `from reportlab.graphics.widgetbase import PropHolder, TypedPropertyCollection` |
| 3808 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/areas.py | 32 | 5 | invalid syntax | `def __init__(self):` |
| 3809 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/legends.py | 14 | 1 | invalid syntax | `from reportlab.graphics.widgetbase import PropHolder, TypedPropertyCollection, Widget` |
| 3810 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/lineplots.py | 351 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 347 | `):` |
| 3811 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/barcharts.py | 22 | 1 | invalid syntax | `from reportlab.graphics.charts.legends import _objStr` |
| 3812 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/linecharts.py | 357 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 353 | `):` |
| 3813 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/markers.py | 23 | 8 | unexpected indent | `rect.fillColor = None` |
| 3814 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/utils3d.py | 33 | 24 | invalid syntax | `if xdepth or ydepth:` |
| 3815 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/textlabels.py | 10 | 1 | invalid syntax | `from reportlab.graphics.widgetbase import PropHolder, Widget` |
| 3816 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/axes.py | 41 | 1 | invalid syntax | `from reportlab.graphics.charts.utils import nextRoundNumber` |
| 3817 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/charts/spider.py | 23 | 1 | invalid syntax | `from reportlab.graphics.widgetbase import PropHolder, TypedPropertyCollection` |
| 3818 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/barcode/eanbc.py | 7 | 1 | invalid syntax | `from reportlab.graphics.charts.areas import PlotArea` |
| 3819 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/barcode/usps4s.py | 52 | 5 | invalid syntax | `else:` |
| 3820 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/barcode/qrencoder.py | 48 | 16 | unexpected indent | `self.data = data` |
| 3821 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/barcode/lto.py | 51 | 1 | expected ':' | `#             or (subtype not in ascii_uppercase + string_digits) :` |
| 3822 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/barcode/code39.py | 260 | 20 | unexpected indent | `self.encoded = _encode39(self.encoded, self.checksum,self.stop)` |
| 3823 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/barcode/qr.py | 77 | 1 | invalid syntax | `class QrCodeWidget(Widget):` |
| 3824 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/barcode/code128.py | 277 | 1 | expected ':' | `#                     and l[i + 1] in digits:` |
| 3825 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/barcode/code93.py | 241 | 20 | unexpected indent | `self.encoded = _encode93(self.encoded)` |
| 3826 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/barcode/dmtx.py | 19 | 1 | invalid syntax | `from reportlab.platypus.paraparser import _num as paraparser_num` |
| 3827 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/widgets/grids.py | 10 | 1 | invalid syntax | `from reportlab.graphics.widgetbase import Widget` |
| 3828 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/widgets/markers.py | 49 | 5 | invalid syntax | `def __init__(self,*args,**kw):` |
| 3829 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/widgets/table.py | 19 | 23 | '(' was never closed | `_attrMap = AttrMap(` |
| 3830 | venv_creative/lib/python3.13/site-packages/reportlab/graphics/widgets/signsandsymbols.py | 59 | 5 | invalid syntax | `def __init__(self):` |
| 3831 | venv_creative/lib/python3.13/site-packages/psutil/__init__.py | 53 | 1 | invalid syntax | `from ._common import wrap_numbers as _wrap_numbers` |
| 3832 | venv_creative/lib/python3.13/site-packages/psutil/_psbsd.py | 23 | 16 | invalid syntax | `__extra__all__ = []` |
| 3833 | venv_creative/lib/python3.13/site-packages/psutil/_pslinux.py | 35 | 16 | invalid syntax | `__extra__all__ = [` |
| 3834 | venv_creative/lib/python3.13/site-packages/psutil/tests/test_posix.py | 26 | 1 | invalid syntax | `if POSIX:` |
| 3835 | venv_creative/lib/python3.13/site-packages/psutil/tests/test_linux.py | 34 | 1 | invalid syntax | `if LINUX:` |
| 3836 | venv_creative/lib/python3.13/site-packages/psutil/tests/test_process.py | 1650 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 1644 | `}` |
| 3837 | venv_creative/lib/python3.13/site-packages/omegaconf/dictconfig.py | 8 | 1 | invalid syntax | `from ._utils import (_DEFAULT_MARKER_, ValueKind, _get_value, _is_interpolation,` |
| 3838 | venv_creative/lib/python3.13/site-packages/omegaconf/grammar_visitor.py | 46 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 37 | `):` |
| 3839 | venv_creative/lib/python3.13/site-packages/omegaconf/_utils.py | 183 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 175 | `}` |
| 3840 | venv_creative/lib/python3.13/site-packages/future/moves/pickle.py | 11 | 12 | unexpected indent | `except ImportError:` |
| 3841 | venv_creative/lib/python3.13/site-packages/future/moves/test/support.py | 10 | 8 | unexpected indent | `if sys.version_info[:2] >= (3, 10):` |
| 3842 | venv_creative/lib/python3.13/site-packages/future/moves/urllib/request.py | 13 | 5 | invalid syntax | `from urllib.request import *` |
| 3843 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/scrolledtext.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3844 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/colorchooser.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3845 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/commondialog.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3846 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/messagebox.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3847 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/dialog.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3848 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/constants.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3849 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/dnd.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3850 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/__init__.py | 9 | 8 | unexpected indent | `from Tkinter import (_cnfmerge, _default_root, _flatten, _setit,` |
| 3851 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/ttk.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3852 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/filedialog.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3853 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/font.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3854 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/tix.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3855 | venv_creative/lib/python3.13/site-packages/future/moves/tkinter/simpledialog.py | 10 | 12 | unexpected indent | `except ImportError:` |
| 3856 | venv_creative/lib/python3.13/site-packages/future/moves/http/cookies.py | 10 | 8 | unexpected indent | `from Cookie import Morsel  # left out of __all__ on Py2.7!` |
| 3857 | venv_creative/lib/python3.13/site-packages/future/moves/http/server.py | 10 | 8 | unexpected indent | `from CGIHTTPServer import *` |
| 3858 | venv_creative/lib/python3.13/site-packages/future/moves/http/client.py | 7 | 8 | unexpected indent | `from httplib import HTTPMessage` |
| 3859 | venv_creative/lib/python3.13/site-packages/future/moves/dbm/__init__.py | 10 | 8 | unexpected indent | `from whichdb import *` |
| 3860 | venv_creative/lib/python3.13/site-packages/future/types/newint.py | 72 | 9 | invalid syntax | `if base != 10:` |
| 3861 | venv_creative/lib/python3.13/site-packages/future/utils/__init__.py | 177 | 8 | unexpected indent | `integer_types = int,` |
| 3862 | venv_creative/lib/python3.13/site-packages/future/utils/surrogateescape.py | 101 | 16 | unexpected indent | `return str().join(decoded)` |
| 3863 | venv_creative/lib/python3.13/site-packages/future/backports/misc.py | 137 | 29 | invalid syntax. Perhaps you forgot a comma? | `raise TypeError("descriptor '__init__' of 'OrderedDict' object "` |
| 3864 | venv_creative/lib/python3.13/site-packages/future/backports/test/support.py | 106 | 1 | invalid syntax | `class Error(Exception):` |
| 3865 | venv_creative/lib/python3.13/site-packages/future/backports/urllib/error.py | 35 | 12 | unexpected indent | `self.reason = reason` |
| 3866 | venv_creative/lib/python3.13/site-packages/future/backports/urllib/request.py | 119 | 1 | invalid syntax | `from .response import addclosehook, addinfourl` |
| 3867 | venv_creative/lib/python3.13/site-packages/future/backports/http/server.py | 305 | 24 | unexpected indent | `version_number = int(version_number[0]), int(version_number[1])` |
| 3868 | venv_creative/lib/python3.13/site-packages/future/backports/http/client.py | 100 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `HTTP_PORT = 80` |
| 3869 | venv_creative/lib/python3.13/site-packages/future/backports/http/cookiejar.py | 41 | 1 | invalid syntax | `import copy` |
| 3870 | venv_creative/lib/python3.13/site-packages/future/backports/xmlrpc/server.py | 176 | 9 | invalid syntax | `else:` |
| 3871 | venv_creative/lib/python3.13/site-packages/future/backports/xmlrpc/client.py | 248 | 1 | invalid syntax | `class ResponseError(Error):` |
| 3872 | venv_creative/lib/python3.13/site-packages/future/backports/email/_header_value_parser.py | 218 | 5 | invalid syntax | `@property` |
| 3873 | venv_creative/lib/python3.13/site-packages/future/backports/email/message.py | 161 | 12 | unexpected indent | `fp = StringIO()` |
| 3874 | venv_creative/lib/python3.13/site-packages/future/backports/email/charset.py | 18 | 1 | invalid syntax | `from functools import partial` |
| 3875 | venv_creative/lib/python3.13/site-packages/future/backports/email/feedparser.py | 209 | 1 | expected ':' | `#             and not root.is_multipart():` |
| 3876 | venv_creative/lib/python3.13/site-packages/future/backports/email/headerregistry.py | 43 | 33 | invalid syntax. Perhaps you forgot a comma? | `raise TypeError("addrspec specified when username and / or "` |
| 3877 | venv_creative/lib/python3.13/site-packages/future/standard_library/__init__.py | 242 | 1 | invalid syntax | `class RenameImport(object):` |
| 3878 | venv_creative/lib/python3.13/site-packages/lxml/_elementpath.py | 75 | 1 | invalid syntax | `def xpath_tokenizer(pattern, namespaces = None, with_prefixes = True):` |
| 3879 | venv_creative/lib/python3.13/site-packages/lxml/isoschematron/__init__.py | 32 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `XML_SCHEMA_NS = "http://www.w3.org / 2001 / XMLSchema"` |
| 3880 | venv_creative/lib/python3.13/site-packages/lxml/html/__init__.py | 42 | 1 | invalid syntax | `import copy` |
| 3881 | venv_creative/lib/python3.13/site-packages/lxml/html/formfill.py | 9 | 1 | invalid syntax | `try:` |
| 3882 | venv_creative/lib/python3.13/site-packages/lxml/html/_difflib.py | 57 | 1 | invalid syntax | `from collections import namedtuple as _namedtuple` |
| 3883 | venv_creative/lib/python3.13/site-packages/lxml/html/diff.py | 34 | 5 | invalid syntax | `from cython.cimports.lxml.html._difflib import SequenceMatcher` |
| 3884 | venv_creative/lib/python3.13/site-packages/scipy/odr/_odrpack.py | 51 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `odr = __odrpack.odr` |
| 3885 | venv_creative/lib/python3.13/site-packages/scipy/odr/tests/test_odr.py | 13 | 1 | invalid syntax | `from pytest import raises as assert_raises` |
| 3886 | venv_creative/lib/python3.13/site-packages/scipy/cluster/hierarchy.py | 141 | 1 | invalid syntax | `from scipy._lib._disjoint_set import DisjointSet` |
| 3887 | venv_creative/lib/python3.13/site-packages/scipy/ndimage/_interpolation.py | 47 | 1 | invalid syntax | `@docfiller` |
| 3888 | venv_creative/lib/python3.13/site-packages/scipy/ndimage/tests/test_interpolation.py | 1587 | 25 | too many nested parentheses | `x = xp.asarray([[1, 2, 3],` |
| 3889 | venv_creative/lib/python3.13/site-packages/scipy/ndimage/tests/test_ni_support.py | 8 | 9 | '[' was never closed | `[` |
| 3890 | venv_creative/lib/python3.13/site-packages/scipy/ndimage/tests/test_filters.py | 1911 | 45 | too many nested parentheses | `assert_array_almost_equal(xp.asarray([[4, 6, 10], [10, 12, 16]]), output.real)` |
| 3891 | venv_creative/lib/python3.13/site-packages/scipy/ndimage/tests/test_fourier.py | 11 | 18 | invalid syntax | `skip_xp_backends = pytest.mark.skip_xp_backends` |
| 3892 | venv_creative/lib/python3.13/site-packages/scipy/linalg/interpolative.py | 389 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_DTYPE_ERROR = ValueError("invalid input dtype (input must be float64 or complex128)")` |
| 3893 | venv_creative/lib/python3.13/site-packages/scipy/linalg/tests/test_basic.py | 1999 | 63 | invalid decimal literal | `assert_allclose(np.linalg.norm(adiff1), 5e-4, atol = 5.e - 4)` |
| 3894 | venv_creative/lib/python3.13/site-packages/scipy/linalg/tests/test_decomp.py | 12 | 1 | invalid syntax | `from numpy.testing import (assert_, assert_allclose, assert_almost_equal,` |
| 3895 | venv_creative/lib/python3.13/site-packages/scipy/linalg/tests/test_lapack.py | 256 | 64 | closing parenthesis ')' does not match opening parenthesis '[' on line 252 | `dtype = dtype),` |
| 3896 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_linprog_ip.py | 119 | 20 | unexpected indent | `else:` |
| 3897 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_shgo.py | 487 | 30 | invalid syntax. Perhaps you forgot a comma? | `shc.fail_routine(mes="Failed to find a feasible minimizer point. "` |
| 3898 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_optimize.py | 27 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `__docformat__ = "restructuredtext en"` |
| 3899 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_linprog_simplex.py | 239 | 13 | invalid syntax. Perhaps you forgot a comma? | `f"The pivot operation produces a pivot value of:{pivval: .1e}, "` |
| 3900 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_minimize.py | 24 | 1 | invalid syntax | `from ._differentiable_functions import FD_METHODS` |
| 3901 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_lbfgsb_py.py | 51 | 9 | invalid syntax | `__all__ = ['fmin_l_bfgs_b', 'LbfgsInvHessProduct']` |
| 3902 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_basinhopping.py | 17 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_new_accept_test_signature = inspect.Signature(parameters = _params)` |
| 3903 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_hessian_update_strategy.py | 59 | 5 | invalid syntax | `def update(self, delta_x, delta_grad):` |
| 3904 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_linesearch.py | 27 | 1 | invalid syntax | `class LineSearchWarning(RuntimeWarning):` |
| 3905 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_chandrupatla.py | 133 | 65 | invalid syntax. Perhaps you forgot a comma? | `func, args, xatol, xrtol, fatol, frtol, maxiter, callback = res` |
| 3906 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_dual_annealing.py | 49 | 24 | invalid decimal literal | `MIN_VISIT_BOUND = 1.e - 10` |
| 3907 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_trustregion_exact.py | 15 | 1 | invalid syntax | `def _minimize_trustregion_exact(fun, x0, args=(), jac = None, hess = None,` |
| 3908 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_differentialevolution.py | 13 | 1 | invalid syntax | `from scipy.optimize import OptimizeResult, minimize` |
| 3909 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_bracket.py | 31 | 8 | unexpected indent | `xl0, xr0, xmin, xmax, factor = xp_promote(` |
| 3910 | venv_creative/lib/python3.13/site-packages/scipy/optimize/tests/test_optimize.py | 3022 | 19 | too many nested parentheses | `(np.array([1., 0, 0, 0]), -.3),` |
| 3911 | venv_creative/lib/python3.13/site-packages/scipy/optimize/tests/test__basinhopping.py | 18 | 1 | invalid syntax | `def func1d(x):` |
| 3912 | venv_creative/lib/python3.13/site-packages/scipy/optimize/tests/test_linprog.py | 2832 | 34 | too many nested parentheses | `@pytest.mark.xfail(condition=(sys.maxsize < 2 ** 32 and` |
| 3913 | venv_creative/lib/python3.13/site-packages/scipy/optimize/tests/test__differential_evolution.py | 14 | 1 | invalid syntax | `from pytest import raises as assert_raises` |
| 3914 | venv_creative/lib/python3.13/site-packages/scipy/optimize/tests/test_minimize_constrained.py | 982 | 57 | invalid decimal literal | `assert np.allclose(result.x, x_opt, atol = 1.e - 3)` |
| 3915 | venv_creative/lib/python3.13/site-packages/scipy/optimize/tests/test_quadratic_assignment.py | 46 | 8 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `A, B = np.array(A), np.array(B)` |
| 3916 | venv_creative/lib/python3.13/site-packages/scipy/optimize/tests/test__numdiff.py | 15 | 1 | invalid syntax | `from scipy.sparse import csc_array, csr_array, lil_array` |
| 3917 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_shgo_lib/_complex.py | 183 | 13 | invalid syntax | `elif self.g_cons is not None:` |
| 3918 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_highspy/_highs_wrapper.py | 153 | 13 | invalid syntax | `continue` |
| 3919 | venv_creative/lib/python3.13/site-packages/scipy/optimize/_trustregion_constr/qp_subproblem.py | 24 | 1 | invalid syntax | `def eqp_kktfact(H, c, A, b):` |
| 3920 | venv_creative/lib/python3.13/site-packages/scipy/integrate/_quadpack_py.py | 454 | 20 | invalid syntax. Perhaps you forgot a comma? | `integral = re_retval[0] + 1j * im_retval[0]` |
| 3921 | venv_creative/lib/python3.13/site-packages/scipy/integrate/_ode.py | 379 | 16 | unexpected indent | `self._y = asarray(y, self._integrator.scalar)` |
| 3922 | venv_creative/lib/python3.13/site-packages/scipy/integrate/_quad_vec.py | 44 | 12 | unexpected indent | `self._tmin = sys.float_info.min**0.5` |
| 3923 | venv_creative/lib/python3.13/site-packages/scipy/integrate/_cubature.py | 14 | 1 | invalid syntax | `from scipy.integrate._rules._base import _split_subregion` |
| 3924 | venv_creative/lib/python3.13/site-packages/scipy/integrate/_lebedev.py | 4863 | 29 | unindent does not match any outer indentation level | `leb.x[start] = a` |
| 3925 | venv_creative/lib/python3.13/site-packages/scipy/integrate/_tanhsinh.py | 344 | 5 | invalid syntax | `with np.errstate(over='ignore', invalid='ignore', divide='ignore'):` |
| 3926 | venv_creative/lib/python3.13/site-packages/scipy/integrate/tests/test_tanhsinh.py | 66 | 1 | invalid syntax | `class TestTanhSinh:` |
| 3927 | venv_creative/lib/python3.13/site-packages/scipy/integrate/tests/test_integrate.py | 12 | 1 | invalid syntax | `from pytest import raises as assert_raises` |
| 3928 | venv_creative/lib/python3.13/site-packages/scipy/integrate/_ivp/bdf.py | 13 | 11 | invalid syntax | `MAX_ORDER = 5` |
| 3929 | venv_creative/lib/python3.13/site-packages/scipy/io/_mmio.py | 261 | 5 | invalid syntax | `@property` |
| 3930 | venv_creative/lib/python3.13/site-packages/scipy/io/_netcdf.py | 321 | 17 | expression cannot contain assignment, perhaps you meant "=="? | `self._mm = None` |
| 3931 | venv_creative/lib/python3.13/site-packages/scipy/io/tests/test_idl.py | 94 | 74 | invalid decimal literal | `np.complex128(1.1987253647623157e+112 - 5.1987258887729157e + 307j)` |
| 3932 | venv_creative/lib/python3.13/site-packages/scipy/io/_harwell_boeing/_fortran_format_parser.py | 151 | 12 | unexpected indent | `self.repeat = repeat` |
| 3933 | venv_creative/lib/python3.13/site-packages/scipy/io/matlab/_mio5.py | 93 | 1 | invalid syntax | `from ._mio5_utils import VarReader5` |
| 3934 | venv_creative/lib/python3.13/site-packages/scipy/io/matlab/tests/test_miobase.py | 16 | 8 | unexpected indent | `assert_equal(matdims(np.array([[2,3]])), (1, 2))  # 2 - D array, row vector` |
| 3935 | venv_creative/lib/python3.13/site-packages/scipy/io/matlab/tests/test_mio.py | 23 | 1 | invalid syntax | `from pytest import raises as assert_raises` |
| 3936 | venv_creative/lib/python3.13/site-packages/scipy/_lib/_util.py | 19 | 1 | invalid syntax | `from scipy._lib._docscrape import FunctionDoc, Parameter` |
| 3937 | venv_creative/lib/python3.13/site-packages/scipy/_lib/_docscrape.py | 201 | 12 | unexpected indent | `if len(l2) >= 3 and (set(l2) in ({"-"}, {"="})) and len(l2) != len(l1):` |
| 3938 | venv_creative/lib/python3.13/site-packages/scipy/_lib/array_api_compat/common/_helpers.py | 22 | 1 | invalid syntax | `from ._typing import Array, Device, HasShape, Namespace, SupportsArrayNamespace` |
| 3939 | venv_creative/lib/python3.13/site-packages/scipy/_lib/tests/test_warnings.py | 61 | 17 | invalid syntax | `case _:` |
| 3940 | venv_creative/lib/python3.13/site-packages/scipy/_lib/tests/test__util.py | 21 | 1 | invalid syntax | `from scipy._lib.array_api_extra.testing import lazy_xp_function` |
| 3941 | venv_creative/lib/python3.13/site-packages/scipy/_lib/tests/test_doccer.py | 87 | 12 | unexpected indent | `def func():` |
| 3942 | venv_creative/lib/python3.13/site-packages/scipy/_lib/tests/test_ccallback.py | 112 | 12 | unexpected indent | `assert_raises(ValueError, caller, func, ERROR_VALUE)` |
| 3943 | venv_creative/lib/python3.13/site-packages/scipy/_lib/pyprima/cobyla/cobyla.py | 38 | 1 | invalid syntax | `from ..common.evaluate import evaluate, moderatec, moderatef, moderatex` |
| 3944 | venv_creative/lib/python3.13/site-packages/scipy/_lib/cobyqa/models.py | 689 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 680 | `).T,` |
| 3945 | venv_creative/lib/python3.13/site-packages/scipy/_lib/cobyqa/problem.py | 132 | 13 | invalid syntax. Perhaps you forgot a comma? | `np.all(self.xl <= self.xu)` |
| 3946 | venv_creative/lib/python3.13/site-packages/scipy/_lib/cobyqa/main.py | 1127 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 1121 | `),` |
| 3947 | venv_creative/lib/python3.13/site-packages/scipy/_lib/cobyqa/subsolvers/optim.py | 1247 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 1239 | `).T,` |
| 3948 | venv_creative/lib/python3.13/site-packages/scipy/special/_precompute/wright_bessel_data.py | 116 | 20 | invalid decimal literal | `[1.5, 1.e - 10, 500],` |
| 3949 | venv_creative/lib/python3.13/site-packages/scipy/special/tests/test_basic.py | 3301 | 40 | too many nested parentheses | `@pytest.mark.parametrize("extend", ["zero", "complex"])` |
| 3950 | venv_creative/lib/python3.13/site-packages/scipy/special/tests/test_logsumexp.py | 278 | 48 | invalid decimal literal | `x = xp.asarray([0, 0.+2.2204460492503132e - 17j])` |
| 3951 | venv_creative/lib/python3.13/site-packages/scipy/special/tests/test_zeta.py | 210 | 16 | invalid decimal literal | `((-2 + 1e - 15j), (3.288175809370978e-32 - 3.0448457058393275e - 17j), 1e-07),` |
| 3952 | venv_creative/lib/python3.13/site-packages/scipy/special/tests/test_support_alternative_backends.py | 14 | 1 | invalid syntax | `from scipy._lib._array_api_no_0d import xp_assert_close` |
| 3953 | venv_creative/lib/python3.13/site-packages/scipy/special/tests/test_legendre.py | 1163 | 37 | invalid decimal literal | `for h in [1e-3, 1e - 3j]:` |
| 3954 | venv_creative/lib/python3.13/site-packages/scipy/special/tests/test_exponential_integrals.py | 20 | 30 | invalid decimal literal | `sc.exp1(-1 + 1e - 20j),` |
| 3955 | venv_creative/lib/python3.13/site-packages/scipy/special/tests/test_hyp2f1.py | 42 | 31 | invalid decimal literal | `z_mpmath = z.real + 1.0e - 15j` |
| 3956 | venv_creative/lib/python3.13/site-packages/scipy/special/tests/test_lambertw.py | 105 | 41 | invalid decimal literal | `@pytest.mark.parametrize('z', [1e-316, -2e - 320j, -5e-318 + 1e - 320j])` |
| 3957 | venv_creative/lib/python3.13/site-packages/scipy/special/tests/test_specfun.py | 30 | 50 | invalid decimal literal | `res = special.hyp2f1(5 + 5e-16, 2, 2, -1.0 + 5e - 16j)` |
| 3958 | venv_creative/lib/python3.13/site-packages/scipy/differentiate/_differentiate.py | 35 | 5 | invalid syntax | `if (not np.issubdtype(tols.dtype, np.number) or np.any(tols < 0)` |
| 3959 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/_rgi.py | 30 | 21 | invalid syntax. Perhaps you forgot a comma? | `f"The points in dimension {i} must be strictly ascending or "` |
| 3960 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/_polyint.py | 8 | 1 | invalid syntax | `from scipy.special import factorial` |
| 3961 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/_bsplines.py | 11 | 1 | invalid syntax | `from scipy.optimize import minimize_scalar` |
| 3962 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/_bary_rational.py | 49 | 22 | invalid syntax. Perhaps you forgot a comma? | `axis=-1` |
| 3963 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/_interpolate.py | 172 | 1 | invalid syntax | `def _do_extrapolate(fill_value):` |
| 3964 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/_fitpack2.py | 23 | 1 | invalid syntax | `import warnings` |
| 3965 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/_fitpack_py.py | 6 | 1 | invalid syntax | `import numpy as np` |
| 3966 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/tests/test_bsplines.py | 22 | 1 | invalid syntax | `from scipy.interpolate import _bsplines as _b` |
| 3967 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/tests/test_interpnd.py | 25 | 1 | invalid syntax | `class TestLinearNDInterpolation:` |
| 3968 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/tests/test_bary_rational.py | 432 | 68 | invalid decimal literal | `mask = (p.real >= -1) & (p.real <= 1) & (np.abs(p.imag) < 1.e - 12)` |
| 3969 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/tests/test_polyint.py | 11 | 1 | invalid syntax | `from scipy._lib._testutils import _run_concurrent_barrier` |
| 3970 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/tests/test_rgi.py | 134 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 129 | `),` |
| 3971 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/tests/test_fitpack2.py | 14 | 1 | invalid syntax | `from scipy._lib._testutils import _run_concurrent_barrier` |
| 3972 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/tests/test_rbfinterp.py | 14 | 1 | invalid syntax | `from scipy.spatial import cKDTree  # type: ignore[attr - defined]` |
| 3973 | venv_creative/lib/python3.13/site-packages/scipy/interpolate/tests/test_interpolate.py | 2909 | 24 | too many nested parentheses | `p = NdPPoly(c, (x, y, z))` |
| 3974 | venv_creative/lib/python3.13/site-packages/scipy/fft/tests/test_basic.py | 27 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dtype = xp.complex128` |
| 3975 | venv_creative/lib/python3.13/site-packages/scipy/fft/_pocketfft/tests/test_real_transforms.py | 14 | 18 | invalid syntax | `fftpack_test_dir = join(dirname(__file__), '..', '..', '..', 'fftpack', 'tests')` |
| 3976 | venv_creative/lib/python3.13/site-packages/scipy/sparse/_base.py | 17 | 9 | invalid syntax | `__all__ = ['isspmatrix', 'issparse', 'sparray',` |
| 3977 | venv_creative/lib/python3.13/site-packages/scipy/sparse/_data.py | 69 | 9 | invalid syntax | `return self._with_data(-self.data)` |
| 3978 | venv_creative/lib/python3.13/site-packages/scipy/sparse/_compressed.py | 22 | 1 | invalid syntax | `from ._sputils import (broadcast_shapes, check_shape, downcast_intp_index,` |
| 3979 | venv_creative/lib/python3.13/site-packages/scipy/sparse/_bsr.py | 21 | 1 | invalid syntax | `from ._sputils import check_shape, getdata, getdtype, isshape, to_native, upcast` |
| 3980 | venv_creative/lib/python3.13/site-packages/scipy/sparse/_coo.py | 21 | 1 | invalid syntax | `from ._sputils import (check_reshape_kwargs, check_shape, downcast_intp_index,` |
| 3981 | venv_creative/lib/python3.13/site-packages/scipy/sparse/_construct.py | 1214 | 69 | closing parenthesis ')' does not match opening parenthesis '[' | `where values are generated uniformly randomly in the range [0, 1).` |
| 3982 | venv_creative/lib/python3.13/site-packages/scipy/sparse/_dok.py | 20 | 1 | invalid syntax | `class _dok_base(_spbase, IndexMixin, dict):` |
| 3983 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/_interface.py | 168 | 13 | invalid syntax | `return obj` |
| 3984 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/_expm_multiply.py | 216 | 5 | invalid syntax | `return X` |
| 3985 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/_svdp.py | 211 | 13 | invalid syntax. Perhaps you forgot a comma? | `"kmax must be greater than or equal to k, "` |
| 3986 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/_eigen/arpack/tests/test_arpack.py | 154 | 13 | invalid syntax | `elif OPpart == 'i':` |
| 3987 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/_eigen/tests/test_svds.py | 146 | 5 | invalid syntax | `@pytest.mark.parametrize("args", _A_validation_inputs)` |
| 3988 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/_eigen/lobpcg/tests/test_lobpcg.py | 51 | 10 | invalid decimal literal | `S = 1.e - 4` |
| 3989 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/tests/test_special_sparse_arrays.py | 41 | 9 | invalid syntax | `elif bc == 'dirichlet':` |
| 3990 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/tests/test_propack.py | 34 | 1 | invalid syntax | `def generate_matrix(constructor, n, m, f,` |
| 3991 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/tests/test_interface.py | 49 | 21 | closing parenthesis '}' does not match opening parenthesis '(' on line 45 | `},` |
| 3992 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/_isolve/tfqmr.py | 103 | 8 | unexpected indent | `if np.linalg.norm(b) == 0.:` |
| 3993 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/_isolve/iterative.py | 21 | 9 | invalid syntax | `raise ValueError(msg)` |
| 3994 | venv_creative/lib/python3.13/site-packages/scipy/sparse/linalg/_isolve/_gcrotmk.py | 171 | 35 | invalid syntax | `if res < atol or breakdown:` |
| 3995 | venv_creative/lib/python3.13/site-packages/scipy/sparse/tests/test_base.py | 5795 | 27 | too many nested parentheses | `Asp = dia_matrix(([[0., 1., 2.], [3., 4., 5.]], [1, -2]), (5, 5))` |
| 3996 | venv_creative/lib/python3.13/site-packages/scipy/sparse/csgraph/tests/test_shortest_path.py | 16 | 12 | invalid syntax | `directed_G = np.array([[0, 3, 3, 0, 0],` |
| 3997 | venv_creative/lib/python3.13/site-packages/scipy/spatial/distance.py | 109 | 1 | invalid syntax | `import dataclasses` |
| 3998 | venv_creative/lib/python3.13/site-packages/scipy/spatial/tests/test_kdtree.py | 14 | 1 | invalid syntax | `from pytest import raises as assert_raises` |
| 3999 | venv_creative/lib/python3.13/site-packages/scipy/spatial/transform/tests/test_rotation_spline.py | 14 | 12 | invalid syntax | `pytestmark = pytest.mark.skip_xp_backends(np_only = True)` |
| 4000 | venv_creative/lib/python3.13/site-packages/scipy/spatial/transform/tests/test_rotation.py | 2202 | 50 | too many nested parentheses | `r = Rotation.from_quat(xp.asarray(rnd.uniform(size=(5, 4))))` |
| 4001 | venv_creative/lib/python3.13/site-packages/scipy/spatial/transform/tests/test_rigid_transform.py | 8 | 1 | invalid syntax | `from scipy.spatial.transform import RigidTransform, Rotation` |
| 4002 | venv_creative/lib/python3.13/site-packages/scipy/signal/_ltisys.py | 30 | 1 | invalid syntax | `from scipy import linalg` |
| 4003 | venv_creative/lib/python3.13/site-packages/scipy/signal/_spectral_py.py | 21 | 1 | invalid syntax | `def lombscargle(` |
| 4004 | venv_creative/lib/python3.13/site-packages/scipy/signal/_signaltools.py | 115 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 111 | `):` |
| 4005 | venv_creative/lib/python3.13/site-packages/scipy/signal/_filter_design.py | 13 | 1 | invalid syntax | `from numpy.polynomial.polynomial import polyval as npp_polyval` |
| 4006 | venv_creative/lib/python3.13/site-packages/scipy/signal/_short_time_fft.py | 55 | 5 | invalid syntax | `if issubclass(win.dtype.type, np.integer):` |
| 4007 | venv_creative/lib/python3.13/site-packages/scipy/signal/tests/test_cont2discrete.py | 7 | 1 | invalid syntax | `from scipy.signal import cont2discrete as c2d` |
| 4008 | venv_creative/lib/python3.13/site-packages/scipy/signal/tests/test_ltisys.py | 106 | 18 | invalid decimal literal | `P = [0 - 1e - 6j,0 + 1e - 6j,-10,10]` |
| 4009 | venv_creative/lib/python3.13/site-packages/scipy/signal/tests/test_short_time_fft.py | 34 | 1 | invalid syntax | `from scipy.signal.windows import blackman, gaussian, hamming, nuttall, triang` |
| 4010 | venv_creative/lib/python3.13/site-packages/scipy/signal/tests/test_dltisys.py | 11 | 1 | invalid syntax | `from scipy.signal import (BadCoefficients, StateSpace, TransferFunction, ZerosPolesGain,` |
| 4011 | venv_creative/lib/python3.13/site-packages/scipy/signal/tests/test_filter_design.py | 2086 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 2080 | `), check_dtype = False` |
| 4012 | venv_creative/lib/python3.13/site-packages/scipy/signal/tests/test_peak_finding.py | 12 | 1 | invalid syntax | `from scipy.signal._peak_finding_utils import PeakPropertyWarning, _local_maxima_1d` |
| 4013 | venv_creative/lib/python3.13/site-packages/scipy/signal/tests/test_windows.py | 105 | 59 | closing parenthesis ')' does not match opening parenthesis '[' on line 100 | `dtype = xp.float64),` |
| 4014 | venv_creative/lib/python3.13/site-packages/scipy/stats/_mgc.py | 87 | 5 | invalid syntax | `with MapWrapper(workers) as mapwrapper:` |
| 4015 | venv_creative/lib/python3.13/site-packages/scipy/stats/_wilcoxon.py | 60 | 5 | invalid syntax | `def sf(self, k):` |
| 4016 | venv_creative/lib/python3.13/site-packages/scipy/stats/_stats_py.py | 51 | 1 | invalid syntax | `from scipy._lib._bunch import _make_tuple_bunch` |
| 4017 | venv_creative/lib/python3.13/site-packages/scipy/stats/_qmvnt.py | 140 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `q = q * (bt[s - 1] + gm[s - 1] * reordered)` |
| 4018 | venv_creative/lib/python3.13/site-packages/scipy/stats/_odds_ratio.py | 44 | 12 | unexpected indent | `while func(nc) > 0:` |
| 4019 | venv_creative/lib/python3.13/site-packages/scipy/stats/_qmc.py | 30 | 1 | invalid syntax | `from ._sobol import (_MAXDIM, _categorize, _cscramble, _draw, _fast_forward,` |
| 4020 | venv_creative/lib/python3.13/site-packages/scipy/stats/_discrete_distns.py | 22 | 1 | invalid syntax | `from ._distn_infrastructure import (_isintegral, _ShapeInfo, _vectorize_rvs_over_shapes,` |
| 4021 | venv_creative/lib/python3.13/site-packages/scipy/stats/_kde.py | 26 | 1 | invalid syntax | `from scipy import linalg, special` |
| 4022 | venv_creative/lib/python3.13/site-packages/scipy/stats/_hypotests.py | 28 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `Epps_Singleton_2sampResult = namedtuple('Epps_Singleton_2sampResult',` |
| 4023 | venv_creative/lib/python3.13/site-packages/scipy/stats/_sampling.py | 101 | 5 | invalid syntax | `else:` |
| 4024 | venv_creative/lib/python3.13/site-packages/scipy/stats/_continuous_distns.py | 11154 | 42 | too many nested parentheses | `cdf[i_small_cdf] = super()._cdf(x[i_small_cdf], a[i_small_cdf])` |
| 4025 | venv_creative/lib/python3.13/site-packages/scipy/stats/_correlation.py | 20 | 31 | unindent does not match any outer indentation level | `j = np.argsort(x, axis=-1)` |
| 4026 | venv_creative/lib/python3.13/site-packages/scipy/stats/_axis_nan_policy.py | 17 | 5 | invalid syntax. Perhaps you forgot a comma? | `"One or more sample arguments is too small; all "` |
| 4027 | venv_creative/lib/python3.13/site-packages/scipy/stats/_distribution_infrastructure.py | 44 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_SKIP_ALL = "skip_all"` |
| 4028 | venv_creative/lib/python3.13/site-packages/scipy/stats/_mannwhitneyu.py | 463 | 11 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `x, y, xy = _broadcast_concatenate(x, y, axis)` |
| 4029 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_morestats.py | 3412 | 89 | closing parenthesis '}' does not match opening parenthesis '[' on line 3408 | `1: np.array([0.16769015, 358.66510252])}),` |
| 4030 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_continuous.py | 23 | 1 | invalid syntax | `from scipy.stats._fit import _kolmogorov_smirnov` |
| 4031 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_stats.py | 4010 | 35 | too many nested parentheses | `assert_equal(stats.iqr(x, axis = 1, nan_policy='propagate'),` |
| 4032 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_fast_gen_inversion.py | 42 | 8 | unexpected indent | `urng = np.random.default_rng(20375857)` |
| 4033 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_mstats_extras.py | 58 | 1 | invalid syntax | `def test_trimmed_mean_ci():` |
| 4034 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_survival.py | 165 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `d4 = [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1]` |
| 4035 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_multivariate.py | 3112 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 3097 | `), (` |
| 4036 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_axis_nan_policy.py | 27 | 13 | invalid syntax | `SCIPY_XSLOW = int(os.environ.get('SCIPY_XSLOW', '0'))` |
| 4037 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/common_tests.py | 39 | 14 | invalid syntax. Perhaps you forgot a comma? | `_a, _b = distfn.support(*args)` |
| 4038 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_distributions.py | 3449 | 25 | too many nested parentheses | `int_pdfs = [quad(stats.pearson3(skew).pdf, neg_inf, x_eval)[0]` |
| 4039 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_kdeoth.py | 8 | 1 | invalid syntax | `from pytest import raises as assert_raises` |
| 4040 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_entropy.py | 31 | 52 | invalid decimal literal | `xp_assert_less(xp.abs(S - 4.), xp.asarray(1.e - 5))` |
| 4041 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_resampling.py | 89 | 11 | invalid syntax. Perhaps you forgot a comma? | `rng = np.random.RandomState(0)` |
| 4042 | venv_creative/lib/python3.13/site-packages/scipy/stats/tests/test_sampling.py | 28 | 1 | invalid syntax | `class StandardNormal:` |
| 4043 | venv_creative/lib/python3.13/site-packages/yarl/_parse.py | 14 | 5 | invalid syntax. Perhaps you forgot a comma? | `"\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f\x10"` |
| 4044 | venv_creative/lib/python3.13/site-packages/functorch/dim/delayed_mul_tensor.py | 43 | 20 | unexpected indent | `return self._batchtensor_data` |
| 4045 | venv_creative/lib/python3.13/site-packages/functorch/dim/reference.py | 58 | 17 | invalid syntax. Perhaps you forgot a comma? | `f"inferred dimension does not evenly fit into larger dimension: {lhs_size} vs {rhs_s}"` |
| 4046 | venv_creative/lib/python3.13/site-packages/skimage/__init__.py | 82 | 1 | invalid syntax | `def __dir__():` |
| 4047 | venv_creative/lib/python3.13/site-packages/skimage/filters/tests/test_fft_based.py | 24 | 1 | invalid syntax | `def test_butterworth_2D_zeros_dtypes(dtype, squared_butterworth):` |
| 4048 | venv_creative/lib/python3.13/site-packages/skimage/filters/tests/test_edges.py | 24 | 9 | invalid syntax. Perhaps you forgot a comma? | `np.tri(10, 10, -1).astype(bool) ¦ np.tri(10, 10, -2).astype(bool).transpose()` |
| 4049 | venv_creative/lib/python3.13/site-packages/skimage/registration/_phase_cross_correlation.py | 61 | 5 | invalid syntax | `else:` |
| 4050 | venv_creative/lib/python3.13/site-packages/skimage/restoration/_denoise.py | 198 | 13 | invalid syntax | `else:` |
| 4051 | venv_creative/lib/python3.13/site-packages/skimage/restoration/tests/test_restoration.py | 71 | 1 | invalid syntax | `def test_unsupervised_wiener(dtype):` |
| 4052 | venv_creative/lib/python3.13/site-packages/skimage/segmentation/boundaries.py | 29 | 49 | invalid syntax. Perhaps you forgot a comma? | `[(2 * s - 1) for s in label_img.shape], label_img.dtype` |
| 4053 | venv_creative/lib/python3.13/site-packages/skimage/segmentation/tests/test_slic.py | 74 | 5 | invalid syntax. Perhaps you forgot a comma? | `assert_equal(len(np.unique(seg)), 4)` |
| 4054 | venv_creative/lib/python3.13/site-packages/skimage/color/colorlabel.py | 27 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `color_dict = {k: v for k, v in rgb_colors.__dict__.items() if isinstance(v, tuple)}` |
| 4055 | venv_creative/lib/python3.13/site-packages/skimage/color/tests/test_colorlabel.py | 9 | 1 | invalid syntax | `from skimage._shared.testing import expected_warnings` |
| 4056 | venv_creative/lib/python3.13/site-packages/skimage/io/tests/test_io.py | 30 | 1 | invalid syntax | `def test_stack_basic():` |
| 4057 | venv_creative/lib/python3.13/site-packages/skimage/measure/fit.py | 137 | 9 | invalid syntax | `return np.linalg.norm(res, axis = 1)` |
| 4058 | venv_creative/lib/python3.13/site-packages/skimage/measure/_polygon.py | 65 | 12 | unexpected indent | `projected_lengths0 = dr0 * dr + dc0 * dc` |
| 4059 | venv_creative/lib/python3.13/site-packages/skimage/measure/tests/test_blur_effect.py | 11 | 79 | invalid syntax. Perhaps you forgot a comma? | `ski.filters.gaussian(image, sigma = 1, channel_axis=-1), channel_axis=-1` |
| 4060 | venv_creative/lib/python3.13/site-packages/skimage/_shared/tests/test_warnings.py | 40 | 47 | unindent does not match any outer indentation level | `with expected_warnings(['some warnings']):` |
| 4061 | venv_creative/lib/python3.13/site-packages/skimage/morphology/misc.py | 31 | 1 | invalid syntax | `def default_footprint(func):` |
| 4062 | venv_creative/lib/python3.13/site-packages/skimage/morphology/tests/test_skeletonize.py | 28 | 5 | invalid syntax | `def test_wrong_ndim(self, ndim, method):` |
| 4063 | venv_creative/lib/python3.13/site-packages/skimage/feature/sift.py | 54 | 9 | invalid syntax. Perhaps you forgot a comma? | `d[p0 + 1, p1 + 1, p2]` |
| 4064 | venv_creative/lib/python3.13/site-packages/skimage/feature/util.py | 143 | 9 | invalid syntax | `raise ValueError(mesg)` |
| 4065 | venv_creative/lib/python3.13/site-packages/skimage/feature/brief.py | 14 | 5 | invalid syntax | `np2 = Version(np.__version__) >= Version('2')` |
| 4066 | venv_creative/lib/python3.13/site-packages/skimage/feature/corner.py | 45 | 5 | invalid syntax | `return derivatives` |
| 4067 | venv_creative/lib/python3.13/site-packages/skimage/feature/blob.py | 87 | 5 | invalid syntax | `return vol / (4.0 / 3 * math.pi * min(r1, r2) ** 3)` |
| 4068 | venv_creative/lib/python3.13/site-packages/skimage/feature/tests/test_peak.py | 95 | 9 | invalid syntax | `assert len(peaks_limited) == 2` |
| 4069 | venv_creative/lib/python3.13/site-packages/skimage/transform/hough_transform.py | 77 | 5 | invalid syntax | `if a.size > 0:` |
| 4070 | venv_creative/lib/python3.13/site-packages/skimage/transform/tests/test_hough_transform.py | 330 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 325 | `),` |
| 4071 | venv_creative/lib/python3.13/site-packages/skimage/transform/tests/test_radon_transform.py | 479 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 473 | `).T` |
| 4072 | venv_creative/lib/python3.13/site-packages/skimage/transform/tests/test_warps.py | 15 | 1 | invalid syntax | `from skimage.transform._warps import (_linear_polar_mapping, _log_polar_mapping,` |
| 4073 | venv_creative/lib/python3.13/site-packages/skimage/draw/draw_nd.py | 47 | 12 | unexpected indent | `else:` |
| 4074 | venv_creative/lib/python3.13/site-packages/skimage/draw/tests/test_draw.py | 12 | 1 | invalid syntax | `from skimage.measure import regionprops` |
| 4075 | venv_creative/lib/python3.13/site-packages/docx/section.py | 351 | 9 | invalid syntax | `return Section(self._document_elm.sectPr_lst[key], self._document_part)` |
| 4076 | venv_creative/lib/python3.13/site-packages/docx/shared.py | 6 | 20 | '(' was never closed | `from typing import (TYPE_CHECKING, Any, Callable, Generic, Iterator, List, Tuple,` |
| 4077 | venv_creative/lib/python3.13/site-packages/docx/document.py | 80 | 12 | unexpected indent | `runs = [runs] if isinstance(runs, Run) else runs` |
| 4078 | venv_creative/lib/python3.13/site-packages/docx/comments.py | 28 | 16 | '(' was never closed | `return (` |
| 4079 | venv_creative/lib/python3.13/site-packages/docx/oxml/coreprops.py | 40 | 35 | invalid syntax. Perhaps you forgot a comma? | `"cp:revision", successors=()` |
| 4080 | venv_creative/lib/python3.13/site-packages/docx/oxml/simpletypes.py | 78 | 5 | invalid syntax | `def validate_string(cls, value: Any) -> str:` |
| 4081 | venv_creative/lib/python3.13/site-packages/docx/oxml/section.py | 18 | 1 | invalid syntax | `from docx.shared import Length, lazyproperty` |
| 4082 | venv_creative/lib/python3.13/site-packages/docx/oxml/document.py | 49 | 41 | '(' was never closed | `sectPr: CT_SectPr ¦ None = ZeroOrOne(  # pyright: ignore[reportAssignmentType]` |
| 4083 | venv_creative/lib/python3.13/site-packages/docx/oxml/table.py | 11 | 1 | invalid syntax | `from docx.exceptions import InvalidSpanError` |
| 4084 | venv_creative/lib/python3.13/site-packages/docx/oxml/xmlchemy.py | 113 | 9 | invalid syntax | `for key, value in namespace.items():` |
| 4085 | venv_creative/lib/python3.13/site-packages/docx/oxml/comments.py | 16 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 4086 | venv_creative/lib/python3.13/site-packages/docx/oxml/text/run.py | 62 | 12 | unexpected indent | `for e in self.xpath("./*[not(self::w:rPr)]"):` |
| 4087 | venv_creative/lib/python3.13/site-packages/docx/oxml/text/font.py | 17 | 1 | invalid syntax | `from docx.oxml.xmlchemy import (BaseOxmlElement, OptionalAttribute, RequiredAttribute,` |
| 4088 | venv_creative/lib/python3.13/site-packages/docx/drawing/__init__.py | 40 | 22 | '(' was never closed | `xpath_expr = (` |
| 4089 | venv_creative/lib/python3.13/site-packages/docx/opc/part.py | 172 | 12 | unexpected indent | `self._rels = Relationships(self._partname.baseURI)` |
| 4090 | venv_creative/lib/python3.13/site-packages/docx/dml/color.py | 15 | 8 | unexpected indent | `from docx.oxml.text.run import CT_R` |
| 4091 | venv_creative/lib/python3.13/site-packages/docx/enum/text.py | 42 | 5 | invalid syntax. Perhaps you forgot a comma? | `"""Paragraph characters are distributed to fill entire width of paragraph."""` |
| 4092 | venv_creative/lib/python3.13/site-packages/docx/image/tiff.py | 337 | 16 | unexpected indent | `else:  # pragma: no cover` |
| 4093 | venv_creative/lib/python3.13/site-packages/docx/image/jpeg.py | 91 | 19 | '(' was never closed | `% (` |
| 4094 | venv_creative/lib/python3.13/site-packages/docx/image/helpers.py | 88 | 16 | unexpected indent | `return bytes_` |
| 4095 | venv_creative/lib/python3.13/site-packages/docx/image/image.py | 46 | 16 | unexpected indent | `with open(path, "rb") as f:` |
| 4096 | venv_creative/lib/python3.13/site-packages/docx/text/run.py | 202 | 12 | unexpected indent | `self._r.insert_comment_range_start_above(comment_id)` |
| 4097 | venv_creative/lib/python3.13/site-packages/pydantic_core/__init__.py | 16 | 1 | invalid syntax | `from .core_schema import CoreConfig, CoreSchema, CoreSchemaType, ErrorType` |
| 4098 | venv_creative/lib/python3.13/site-packages/pydantic_core/core_schema.py | 83 | 8 | unexpected indent | `typed_dict_total: bool  # default: True` |
| 4099 | venv_creative/lib/python3.13/site-packages/tomlkit/container.py | 14 | 1 | invalid syntax | `from tomlkit.items import item as _item` |
| 4100 | venv_creative/lib/python3.13/site-packages/pandas/core/accessor.py | 123 | 9 | invalid syntax | `def _create_delegator_method(name: str):` |
| 4101 | venv_creative/lib/python3.13/site-packages/pandas/core/nanops.py | 15 | 1 | invalid syntax | `from pandas.compat._optional import import_optional_dependency` |
| 4102 | venv_creative/lib/python3.13/site-packages/pandas/core/algorithms.py | 25 | 1 | invalid syntax | `from pandas.core.dtypes.common import (ensure_float64, ensure_object,` |
| 4103 | venv_creative/lib/python3.13/site-packages/pandas/core/resample.py | 16 | 1 | invalid syntax | `from pandas._libs.tslibs.dtypes import freq_to_period_freqstr` |
| 4104 | venv_creative/lib/python3.13/site-packages/pandas/core/arraylike.py | 341 | 5 | invalid syntax | `for item in inputs:` |
| 4105 | venv_creative/lib/python3.13/site-packages/pandas/core/series.py | 5992 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 5983 | `) -> Series:` |
| 4106 | venv_creative/lib/python3.13/site-packages/pandas/core/sorting.py | 23 | 5 | invalid syntax | `from pandas.core.arrays import ExtensionArray` |
| 4107 | venv_creative/lib/python3.13/site-packages/pandas/core/frame.py | 2292 | 60 | leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers | `<https://developers.googleblog.com / 2022 / 02 / making - oauth - flows - safer.html?m = 1#disallowed - oob>`_.` |
| 4108 | venv_creative/lib/python3.13/site-packages/pandas/core/sample.py | 47 | 9 | invalid syntax | `else:` |
| 4109 | venv_creative/lib/python3.13/site-packages/pandas/core/apply.py | 20 | 1 | invalid syntax | `from pandas.compat._optional import import_optional_dependency` |
| 4110 | venv_creative/lib/python3.13/site-packages/pandas/core/reshape/merge.py | 26 | 1 | invalid syntax | `from pandas.core.arrays import ArrowExtensionArray, BaseMaskedArray, ExtensionArray` |
| 4111 | venv_creative/lib/python3.13/site-packages/pandas/core/reshape/encoding.py | 18 | 1 | invalid syntax | `from pandas.core.dtypes.dtypes import ArrowDtype, CategoricalDtype` |
| 4112 | venv_creative/lib/python3.13/site-packages/pandas/core/reshape/reshape.py | 18 | 1 | invalid syntax | `from pandas.core.dtypes.dtypes import ExtensionDtype` |
| 4113 | venv_creative/lib/python3.13/site-packages/pandas/core/strings/accessor.py | 1896 | 16 | leading zeros in decimal integer literals are not permitted; use an 0o prefix for octal integers | `0     -01` |
| 4114 | venv_creative/lib/python3.13/site-packages/pandas/core/tools/timedeltas.py | 16 | 1 | invalid syntax | `from pandas.core.arrays.timedeltas import sequence_to_td64ns` |
| 4115 | venv_creative/lib/python3.13/site-packages/pandas/core/dtypes/cast.py | 20 | 1 | invalid syntax | `from pandas._libs.tslibs.timedeltas import array_to_timedelta64` |
| 4116 | venv_creative/lib/python3.13/site-packages/pandas/core/dtypes/generic.py | 12 | 5 | invalid syntax | `from pandas.core.arrays import (DatetimeArray, ExtensionArray, NumpyExtensionArray,` |
| 4117 | venv_creative/lib/python3.13/site-packages/pandas/core/dtypes/dtypes.py | 22 | 1 | invalid syntax | `from pandas._libs.tslibs.dtypes import PeriodDtypeBase, abbrev_to_npy_unit` |
| 4118 | venv_creative/lib/python3.13/site-packages/pandas/core/groupby/generic.py | 19 | 1 | invalid syntax | `import numpy as np` |
| 4119 | venv_creative/lib/python3.13/site-packages/pandas/core/groupby/ops.py | 24 | 1 | invalid syntax | `from pandas.core.dtypes.missing import isna, maybe_fill` |
| 4120 | venv_creative/lib/python3.13/site-packages/pandas/core/groupby/grouper.py | 260 | 13 | invalid syntax | `else:` |
| 4121 | venv_creative/lib/python3.13/site-packages/pandas/core/groupby/groupby.py | 33 | 1 | invalid syntax | `from pandas.compat.numpy import function as nv` |
| 4122 | venv_creative/lib/python3.13/site-packages/pandas/core/internals/array_manager.py | 18 | 1 | invalid syntax | `from pandas.core.construction import (ensure_wrapped_if_datetimelike, extract_array,` |
| 4123 | venv_creative/lib/python3.13/site-packages/pandas/core/internals/blocks.py | 24 | 1 | invalid syntax | `from pandas.core import missing` |
| 4124 | venv_creative/lib/python3.13/site-packages/pandas/core/internals/managers.py | 2036 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 2030 | `}` |
| 4125 | venv_creative/lib/python3.13/site-packages/pandas/core/computation/align.py | 65 | 53 | unindent does not match any outer indentation level | `term_values = (term.value for term in terms)` |
| 4126 | venv_creative/lib/python3.13/site-packages/pandas/core/computation/pytables.py | 141 | 80 | invalid syntax. Perhaps you forgot a comma? | `self.op, left, right, queryables = self.queryables, encoding = self.encoding` |
| 4127 | venv_creative/lib/python3.13/site-packages/pandas/core/computation/ops.py | 49 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_binary_math_ops = ("arctan2",)` |
| 4128 | venv_creative/lib/python3.13/site-packages/pandas/core/window/rolling.py | 28 | 1 | invalid syntax | `from pandas.core.dtypes.dtypes import ArrowDtype` |
| 4129 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/categorical.py | 32 | 1 | invalid syntax | `from pandas.core.dtypes.dtypes import (ArrowDtype, CategoricalDtype,` |
| 4130 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/interval.py | 990 | 19 | unterminated string literal (detected at line 990) | `author's discretion whether to ignore "copy = False" or to raise.` |
| 4131 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/datetimes.py | 20 | 1 | invalid syntax | `from pandas._libs.tslibs.dtypes import abbrev_to_npy_unit` |
| 4132 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/string_.py | 28 | 1 | invalid syntax | `from pandas.core.dtypes.common import (is_array_like, is_bool_dtype, is_integer_dtype,` |
| 4133 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/_ranges.py | 16 | 1 | invalid syntax | `if TYPE_CHECKING:` |
| 4134 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/masked.py | 15 | 1 | invalid syntax | `from pandas.compat import IS64, is_platform_windows` |
| 4135 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/datetimelike.py | 21 | 1 | invalid syntax | `from pandas._libs.tslibs.fields import RoundTo, round_nsint64` |
| 4136 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/base.py | 1644 | 15 | unterminated string literal (detected at line 1644) | `it's called by :meth:`Series.reindex`, or any other method` |
| 4137 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/_mixins.py | 15 | 1 | invalid syntax | `from pandas.core import missing` |
| 4138 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/arrow/array.py | 19 | 1 | invalid syntax | `from pandas.core import algorithms as algos` |
| 4139 | venv_creative/lib/python3.13/site-packages/pandas/core/arrays/sparse/array.py | 28 | 1 | invalid syntax | `from pandas.core.dtypes.astype import astype_array` |
| 4140 | venv_creative/lib/python3.13/site-packages/pandas/core/indexes/accessors.py | 306 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 295 | `}` |
| 4141 | venv_creative/lib/python3.13/site-packages/pandas/core/indexes/base.py | 1103 | 50 | unterminated string literal (detected at line 1103) | `-1 are regarded as NA. If Index doesn't hold NA, raise ValueError.` |
| 4142 | venv_creative/lib/python3.13/site-packages/pandas/util/_validators.py | 40 | 1 | invalid syntax | `def _check_for_default_values(fname, arg_val_dict, compat_args) -> None:` |
| 4143 | venv_creative/lib/python3.13/site-packages/pandas/util/_exceptions.py | 12 | 8 | unexpected indent | `from types import FrameType` |
| 4144 | venv_creative/lib/python3.13/site-packages/pandas/io/pytables.py | 23 | 1 | invalid syntax | `from pandas._config import config, get_option, using_copy_on_write, using_string_dtype` |
| 4145 | venv_creative/lib/python3.13/site-packages/pandas/io/html.py | 1258 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 1250 | `):` |
| 4146 | venv_creative/lib/python3.13/site-packages/pandas/io/common.py | 23 | 1 | invalid syntax | `from urllib.parse import urljoin` |
| 4147 | venv_creative/lib/python3.13/site-packages/pandas/io/parsers/readers.py | 18 | 1 | invalid syntax | `import numpy as np` |
| 4148 | venv_creative/lib/python3.13/site-packages/pandas/io/parsers/c_parser_wrapper.py | 41 | 13 | invalid syntax. Perhaps you forgot a comma? | `self.index_col is not False  # type: ignore[has - type]` |
| 4149 | venv_creative/lib/python3.13/site-packages/pandas/tests/test_algos.py | 1731 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 1717 | `),` |
| 4150 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/test_logical_ops.py | 92 | 13 | invalid syntax. Perhaps you forgot a comma? | `r"Logical ops \(and, or, xor\) between Pandas objects and "` |
| 4151 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/test_constructors.py | 17 | 1 | invalid syntax | `from pandas._libs import iNaT, lib` |
| 4152 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/test_arithmetic.py | 13 | 1 | invalid syntax | `from pandas._libs import lib` |
| 4153 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/methods/test_astype.py | 14 | 1 | invalid syntax | `from pandas._libs.tslibs import iNaT` |
| 4154 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/methods/test_fillna.py | 11 | 1 | invalid syntax | `from pandas.core.arrays import period_array` |
| 4155 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/methods/test_map.py | 542 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 532 | `),` |
| 4156 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/methods/test_compare.py | 20 | 66 | invalid syntax. Perhaps you forgot a comma? | `[["a", "x"], ["c", "z"]], index = indices, columns = columns` |
| 4157 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/methods/test_replace.py | 33 | 9 | invalid syntax | `assert expected.iloc[2, 2] is None` |
| 4158 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/accessors/test_cat_accessor.py | 8 | 1 | invalid syntax | `from pandas.core.arrays.categorical import CategoricalAccessor` |
| 4159 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/indexing/test_getitem.py | 14 | 1 | invalid syntax | `from pandas._libs.tslibs import conversion, timezones` |
| 4160 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/indexing/test_setitem.py | 14 | 1 | invalid syntax | `from pandas.compat.numpy import np_version_gt2, np_version_gte1p24` |
| 4161 | venv_creative/lib/python3.13/site-packages/pandas/tests/series/indexing/test_get.py | 73 | 9 | closing parenthesis ')' does not match opening parenthesis '[' on line 49 | `),` |
| 4162 | venv_creative/lib/python3.13/site-packages/pandas/tests/reshape/concat/test_dataframe.py | 25 | 5 | positional argument follows keyword argument | `def test_concat_tuple_keys(self):` |
| 4163 | venv_creative/lib/python3.13/site-packages/pandas/tests/reshape/merge/test_merge.py | 738 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 724 | `}` |
| 4164 | venv_creative/lib/python3.13/site-packages/pandas/tests/apply/test_invalid_arg.py | 214 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 196 | `}` |
| 4165 | venv_creative/lib/python3.13/site-packages/pandas/tests/apply/test_series_apply.py | 9 | 1 | invalid syntax | `from pandas.tests.apply.common import series_transform_kernels` |
| 4166 | venv_creative/lib/python3.13/site-packages/pandas/tests/apply/test_frame_apply.py | 566 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 548 | `}` |
| 4167 | venv_creative/lib/python3.13/site-packages/pandas/tests/apply/test_frame_transform.py | 48 | 1 | invalid syntax | `def test_transform_listlike(axis, float_frame, ops, names):` |
| 4168 | venv_creative/lib/python3.13/site-packages/pandas/tests/strings/test_split_partition.py | 79 | 8 | unexpected indent | `with pytest.raises(` |
| 4169 | venv_creative/lib/python3.13/site-packages/pandas/tests/strings/test_find_replace.py | 19 | 75 | invalid syntax. Perhaps you forgot a comma? | `["foo", np.nan, "fooommm__foo", "mmm_", "foommm[_]+bar"], dtype = np.object_` |
| 4170 | venv_creative/lib/python3.13/site-packages/pandas/tests/strings/test_strings.py | 36 | 76 | invalid syntax. Perhaps you forgot a comma? | `np.float64 if is_object_or_nan_string_dtype(any_string_dtype) else "Int64"` |
| 4171 | venv_creative/lib/python3.13/site-packages/pandas/tests/strings/test_api.py | 18 | 6 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `ids, _ = zip(*_any_allowed_skipna_inferred_dtype)  # use inferred type as id` |
| 4172 | venv_creative/lib/python3.13/site-packages/pandas/tests/strings/test_extract.py | 14 | 74 | unindent does not match any outer indentation level | `with pytest.raises(ValueError, match="expand must be True or False"):` |
| 4173 | venv_creative/lib/python3.13/site-packages/pandas/tests/tools/test_to_timedelta.py | 62 | 13 | invalid syntax. Perhaps you forgot a comma? | `[np.timedelta64(0, "ns"), np.timedelta64(10, "s").astype("m8[ns]")]` |
| 4174 | venv_creative/lib/python3.13/site-packages/pandas/tests/tools/test_to_datetime.py | 903 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 896 | `),` |
| 4175 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/test_masked.py | 31 | 1 | invalid syntax | `from pandas.core.dtypes.common import (is_float_dtype, is_signed_integer_dtype,` |
| 4176 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/test_string.py | 49 | 5 | invalid syntax | `assert arrow_array.num_chunks == 2` |
| 4177 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/test_numpy.py | 153 | 1 | invalid syntax | `def data_for_twos(dtype):` |
| 4178 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/test_arrow.py | 3277 | 37 | too many nested parentheses | `ArrowExtensionArray(pa.array([expected, None], type = pa.int32()))` |
| 4179 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/decimal/test_decimal.py | 17 | 1 | invalid syntax | `@pytest.fixture` |
| 4180 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/date/array.py | 43 | 34 | invalid syntax | `if string == cls.__name__:` |
| 4181 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/json/array.py | 109 | 9 | invalid syntax | `else:` |
| 4182 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/list/array.py | 83 | 5 | invalid syntax | `def take(self, indexer, allow_fill = False, fill_value = None):` |
| 4183 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/base/methods.py | 29 | 9 | invalid syntax | `assert res.dtype == np.uint64` |
| 4184 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/base/dtype.py | 69 | 26 | '(' was never closed | `df = pd.DataFrame(` |
| 4185 | venv_creative/lib/python3.13/site-packages/pandas/tests/extension/base/ops.py | 15 | 8 | unexpected indent | `frame_scalar_exc: type[Exception] ¦ None = TypeError` |
| 4186 | venv_creative/lib/python3.13/site-packages/pandas/tests/resample/test_resampler_grouper.py | 217 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 204 | `),` |
| 4187 | venv_creative/lib/python3.13/site-packages/pandas/tests/resample/test_datetime_index.py | 584 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 572 | `),` |
| 4188 | venv_creative/lib/python3.13/site-packages/pandas/tests/resample/test_resample_api.py | 294 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 272 | `),` |
| 4189 | venv_creative/lib/python3.13/site-packages/pandas/tests/util/test_hashing.py | 444 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 432 | `}` |
| 4190 | venv_creative/lib/python3.13/site-packages/pandas/tests/config/test_config.py | 93 | 12 | unexpected indent | `msg = r"No such keys\(s\)"` |
| 4191 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/test_parquet.py | 70 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 56 | `),` |
| 4192 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/test_common.py | 30 | 1 | invalid syntax | `class CustomFSPath:` |
| 4193 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/test_gcs.py | 14 | 1 | invalid syntax | `from pandas.compat.pyarrow import pa_version_under17p0` |
| 4194 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/test_sql.py | 4550 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 4534 | `):` |
| 4195 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/test_s3.py | 11 | 48 | unindent does not match any outer indentation level | `from botocore.response import StreamingBody` |
| 4196 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/formats/test_css.py | 89 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 81 | `),` |
| 4197 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/formats/test_to_csv.py | 155 | 13 | invalid syntax. Perhaps you forgot a comma? | `df.to_csv(decimal=",", sep=";", float_format="%.2f")` |
| 4198 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/formats/style/test_to_latex.py | 85 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 79 | `)  # no midrule` |
| 4199 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/formats/style/test_bar.py | 180 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 174 | `},` |
| 4200 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/excel/test_readers.py | 36 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 31 | `),` |
| 4201 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/parser/test_unsupported.py | 28 | 1 | invalid syntax | `def python_engine(request):` |
| 4202 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/parser/test_python_parser_only.py | 77 | 1 | positional argument follows keyword argument | `def test_sniff_delimiter_comment(python_parser_only):` |
| 4203 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/parser/test_na_values.py | 14 | 5 | invalid syntax. Perhaps you forgot a comma? | `"ignore:Passing a BlockManager to DataFrame:DeprecationWarning"` |
| 4204 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/parser/usecols/test_usecols_basic.py | 14 | 5 | invalid syntax. Perhaps you forgot a comma? | `"ignore:Passing a BlockManager to DataFrame:DeprecationWarning"` |
| 4205 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/parser/common/test_read_errors.py | 39 | 5 | invalid syntax | `with pytest.raises(ValueError, match = msg):` |
| 4206 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/parser/common/test_ints.py | 104 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 90 | `}` |
| 4207 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/json/test_json_table_schema.py | 72 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 62 | `}` |
| 4208 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/json/test_ujson.py | 20 | 1 | invalid syntax | `from pandas.compat import IS64` |
| 4209 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/json/test_normalize.py | 26 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 20 | `},` |
| 4210 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/pytables/test_select.py | 35 | 5 | invalid syntax | `with ensure_clean_store(setup_path) as store:` |
| 4211 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/pytables/test_read.py | 72 | 5 | invalid syntax | `with ensure_clean_store(setup_path) as store:` |
| 4212 | venv_creative/lib/python3.13/site-packages/pandas/tests/io/pytables/test_file_handling.py | 12 | 1 | invalid syntax | `from pandas.errors import ClosedFileError, PossibleDataLossError` |
| 4213 | venv_creative/lib/python3.13/site-packages/pandas/tests/tseries/offsets/test_ticks.py | 112 | 45 | invalid syntax. Perhaps you forgot a comma? | `2 * Second(), datetime(2010, 1, 1), datetime(2010, 1, 1, 0, 0, 2)` |
| 4214 | venv_creative/lib/python3.13/site-packages/pandas/tests/tseries/offsets/test_offsets.py | 686 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 673 | `),` |
| 4215 | venv_creative/lib/python3.13/site-packages/pandas/tests/copy_view/test_chained_assignment_deprecation.py | 43 | 1 | invalid syntax | `def test_methods_iloc_getitem_item_cache(` |
| 4216 | venv_creative/lib/python3.13/site-packages/pandas/tests/interchange/test_spec_conformance.py | 32 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `ids=["str_data", "float_data", "int_data"],` |
| 4217 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/test_logical_ops.py | 48 | 5 | invalid syntax | `def test_logical_operators_nans(self, left, right, op, expected, frame_or_series):` |
| 4218 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/test_reductions.py | 457 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 450 | `},` |
| 4219 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/test_constructors.py | 3549 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 3542 | `}` |
| 4220 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/test_stack_unstack.py | 354 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 343 | `),` |
| 4221 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/test_api.py | 82 | 9 | invalid syntax | `for key in list("ABCD"):` |
| 4222 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/test_arithmetic.py | 903 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 894 | `),` |
| 4223 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/methods/test_shift.py | 43 | 9 | invalid syntax | `with tm.assert_produces_warning(FutureWarning, match = msg):` |
| 4224 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/methods/test_sample.py | 30 | 53 | invalid syntax. Perhaps you forgot a comma? | `obj.sample(n = 4, random_state = seed), obj.sample(n = 4, random_state = seed)` |
| 4225 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/methods/test_reset_index.py | 13 | 1 | invalid syntax | `from pandas.core.dtypes.common import is_float_dtype, is_integer_dtype` |
| 4226 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/methods/test_set_index.py | 520 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 509 | `}` |
| 4227 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/methods/test_rank.py | 309 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 302 | `),` |
| 4228 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/methods/test_to_csv.py | 1625 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 1615 | `}` |
| 4229 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/indexing/test_getitem.py | 506 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 498 | `),` |
| 4230 | venv_creative/lib/python3.13/site-packages/pandas/tests/frame/indexing/test_indexing.py | 935 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 925 | `}` |
| 4231 | venv_creative/lib/python3.13/site-packages/pandas/tests/dtypes/test_inference.py | 28 | 1 | invalid syntax | `from pandas._libs import lib` |
| 4232 | venv_creative/lib/python3.13/site-packages/pandas/tests/groupby/test_grouping.py | 172 | 13 | closing parenthesis '}' does not match opening parenthesis '(' on line 165 | `}` |
| 4233 | venv_creative/lib/python3.13/site-packages/pandas/tests/groupby/test_raises.py | 362 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 356 | `),` |
| 4234 | venv_creative/lib/python3.13/site-packages/pandas/tests/groupby/test_groupby.py | 650 | 17 | closing parenthesis '}' does not match opening parenthesis '[' on line 632 | `}` |
| 4235 | venv_creative/lib/python3.13/site-packages/pandas/tests/groupby/test_filters.py | 33 | 1 | invalid syntax | `def test_filter_single_column_df():` |
| 4236 | venv_creative/lib/python3.13/site-packages/pandas/tests/groupby/test_numeric_only.py | 79 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 73 | `},` |
| 4237 | venv_creative/lib/python3.13/site-packages/pandas/tests/groupby/methods/test_describe.py | 15 | 52 | invalid syntax. Perhaps you forgot a comma? | `np.arange(10, dtype = np.float64), index = date_range("2020 - 01 - 01", periods = 10)` |
| 4238 | venv_creative/lib/python3.13/site-packages/pandas/tests/groupby/methods/test_rank.py | 13 | 22 | unindent does not match any outer indentation level | `ser = Series(cat)` |
| 4239 | venv_creative/lib/python3.13/site-packages/pandas/tests/groupby/aggregate/test_aggregate.py | 77 | 17 | closing parenthesis ')' does not match opening parenthesis '[' on line 64 | `),` |
| 4240 | venv_creative/lib/python3.13/site-packages/pandas/tests/plotting/test_misc.py | 12 | 1 | invalid syntax | `from pandas.tests.plotting.common import (_check_colors, _check_legend_labels,` |
| 4241 | venv_creative/lib/python3.13/site-packages/pandas/tests/plotting/frame/test_frame.py | 18 | 1 | invalid syntax | `from pandas.core.dtypes.api import is_list_like` |
| 4242 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/string_/test_string.py | 20 | 1 | invalid syntax | `from pandas.core.dtypes.common import is_dtype_equal` |
| 4243 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/masked/test_arithmetic.py | 51 | 1 | invalid syntax | `def test_array_scalar_like_equivalence(data, all_arithmetic_operators):` |
| 4244 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/categorical/test_constructors.py | 12 | 1 | invalid syntax | `from pandas._config import using_string_dtype` |
| 4245 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/categorical/test_missing.py | 85 | 5 | invalid syntax | `def test_fillna_raises(self, fillna_kwargs, msg):` |
| 4246 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/datetimes/test_constructors.py | 39 | 16 | unindent does not match any outer indentation level | `msg = (` |
| 4247 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/boolean/test_logical.py | 31 | 40 | unindent does not match any outer indentation level | `op = lambda x, y: rop(y, x)` |
| 4248 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/boolean/test_construction.py | 51 | 40 | invalid syntax. Perhaps you forgot a comma? | `np.array([True, False, True]), np.array([False, False, False])` |
| 4249 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/floating/test_arithmetic.py | 24 | 9 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `ids=["add", "mul", "sub", "div", "floordiv", "mod"],` |
| 4250 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/sparse/test_libsparse.py | 82 | 12 | invalid syntax | `ids=[` |
| 4251 | venv_creative/lib/python3.13/site-packages/pandas/tests/arrays/sparse/test_astype.py | 22 | 79 | invalid syntax. Perhaps you forgot a comma? | `np.array([0.0, 2.0], dtype = dtype.subtype), IntIndex(4, [2, 3]), dtype` |
| 4252 | venv_creative/lib/python3.13/site-packages/pandas/tests/arithmetic/test_period.py | 20 | 18 | invalid syntax | `_common_mismatch = [` |
| 4253 | venv_creative/lib/python3.13/site-packages/pandas/tests/arithmetic/test_datetime64.py | 1721 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 1712 | `),` |
| 4254 | venv_creative/lib/python3.13/site-packages/pandas/tests/arithmetic/test_timedelta64.py | 223 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 213 | `),` |
| 4255 | venv_creative/lib/python3.13/site-packages/pandas/tests/generic/test_series.py | 25 | 9 | invalid syntax | `assert ser.index.name is None` |
| 4256 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexing/test_iloc.py | 1388 | 25 | closing parenthesis '}' does not match opening parenthesis '[' on line 1381 | `}` |
| 4257 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexing/test_loc.py | 256 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 249 | `}` |
| 4258 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexing/test_indexing.py | 44 | 70 | invalid syntax. Perhaps you forgot a comma? | `[2.33j, 1.23 + 0.1j, 2.2, 1.0], index=[3, 4, 5, 6], name="bar"` |
| 4259 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexing/test_floats.py | 10 | 1 | invalid syntax | `def gen_obj(klass, index):` |
| 4260 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexing/common.py | 28 | 31 | unindent does not match any outer indentation level | `new_axes[ax] = key` |
| 4261 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexing/test_coercion.py | 36 | 5 | invalid syntax | `opts = request.config.option` |
| 4262 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexing/multiindex/test_getitem.py | 17 | 1 | invalid syntax | `@pytest.mark.parametrize(` |
| 4263 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexing/multiindex/test_loc.py | 22 | 1 | invalid syntax | `def frame_random_data_integer_multi_index():` |
| 4264 | venv_creative/lib/python3.13/site-packages/pandas/tests/scalar/interval/test_constructors.py | 22 | 5 | invalid syntax | `def test_construct_errors(self, left, right):` |
| 4265 | venv_creative/lib/python3.13/site-packages/pandas/tests/scalar/timedelta/test_constructors.py | 45 | 5 | invalid syntax | `def test_units_H_T_S_L_N_U_deprecated(self, unit, unit_depr):` |
| 4266 | venv_creative/lib/python3.13/site-packages/pandas/tests/scalar/timedelta/test_timedelta.py | 56 | 32 | unindent does not match any outer indentation level | `assert td._value == val` |
| 4267 | venv_creative/lib/python3.13/site-packages/pandas/tests/scalar/timestamp/test_constructors.py | 39 | 62 | unindent does not match any outer indentation level | `msg = f"cannot convert input {val} with the unit 'D'"` |
| 4268 | venv_creative/lib/python3.13/site-packages/pandas/tests/scalar/timestamp/test_timestamp.py | 75 | 5 | invalid syntax | `@pytest.mark.parametrize("tz", [None, "US / Eastern"])` |
| 4269 | venv_creative/lib/python3.13/site-packages/pandas/tests/scalar/timestamp/methods/test_round.py | 12 | 1 | invalid syntax | `from pandas._libs.tslibs.dtypes import NpyDatetimeUnit` |
| 4270 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/test_any_index.py | 129 | 67 | unindent does not match any outer indentation level | `with pytest.raises(InvalidIndexError, match = r"\[0 1\]"):` |
| 4271 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/test_indexing.py | 24 | 1 | invalid syntax | `from pandas.core.dtypes.common import is_float_dtype, is_scalar` |
| 4272 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/test_old_base.py | 48 | 21 | closing parenthesis ')' does not match opening parenthesis '[' on line 37 | `),` |
| 4273 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/test_index_new.py | 15 | 1 | invalid syntax | `from pandas._libs.tslibs.timezones import maybe_get_tz` |
| 4274 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/test_base.py | 18 | 1 | invalid syntax | `from pandas.compat import IS64` |
| 4275 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/test_numpy_compat.py | 8 | 1 | invalid syntax | `from pandas.api.types import is_complex_dtype, is_numeric_dtype` |
| 4276 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/ranges/test_range.py | 49 | 5 | invalid syntax | `def test_start_stop_step_attrs(self, index, start, stop, step):` |
| 4277 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/base_class/test_reshape.py | 32 | 12 | unexpected indent | `tm.assert_index_equal(Index(["b", "c", "e", "d"]), result.insert(-1, "e"))` |
| 4278 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/interval/test_constructors.py | 12 | 1 | invalid syntax | `from pandas.core.arrays import IntervalArray` |
| 4279 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/interval/test_indexing.py | 11 | 1 | invalid syntax | `from pandas.errors import InvalidIndexError` |
| 4280 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/multi/test_analytics.py | 21 | 5 | invalid syntax | `with pytest.raises(NotImplementedError, match = msg):` |
| 4281 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/multi/test_indexing.py | 40 | 19 | invalid syntax. Perhaps you forgot a comma? | `stacked = df.stack(future_stack = True)` |
| 4282 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/multi/test_setops.py | 16 | 1 | invalid syntax | `def test_set_ops_error_cases(idx, case, sort, method):` |
| 4283 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/multi/test_monotonic.py | 27 | 5 | invalid syntax | `assert i.is_monotonic_increasing is False` |
| 4284 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/multi/test_duplicates.py | 29 | 5 | invalid syntax | `return mi` |
| 4285 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/period/test_indexing.py | 12 | 1 | invalid syntax | `from pandas._libs.tslibs import period as libperiod` |
| 4286 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/period/test_partial_slicing.py | 63 | 12 | unexpected indent | `values = [` |
| 4287 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/categorical/test_formats.py | 101 | 12 | unexpected indent | `with cf.option_context("display.unicode.east_asian_width", True):` |
| 4288 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/categorical/test_category.py | 35 | 12 | unexpected indent | `result = ci.insert(-1, "a")` |
| 4289 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/numeric/test_indexing.py | 135 | 5 | invalid syntax | `def test_get_indexer_methods(self, reverse, expected, method):` |
| 4290 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/numeric/test_numeric.py | 31 | 13 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `ids=["mixed", "float", "mixed_dec", "float_dec"],` |
| 4291 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/numeric/test_astype.py | 81 | 12 | unexpected indent | `result = idx.to_series().set_axis(range(3)).astype(dtype)` |
| 4292 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/datetimes/test_constructors.py | 183 | 21 | closing parenthesis '}' does not match opening parenthesis '[' on line 175 | `}` |
| 4293 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/datetimes/test_date_range.py | 18 | 1 | invalid syntax | `from pandas._libs.tslibs import timezones` |
| 4294 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/datetimes/test_scalar_compat.py | 52 | 5 | invalid syntax | `def test_dti_date2(self, dtype):` |
| 4295 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/datetimes/methods/test_round.py | 39 | 5 | invalid syntax | `def test_round_invalid(self, freq, error_msg):` |
| 4296 | venv_creative/lib/python3.13/site-packages/pandas/tests/indexes/datetimes/methods/test_tz_localize.py | 14 | 1 | invalid syntax | `try:` |
| 4297 | venv_creative/lib/python3.13/site-packages/pandas/_testing/__init__.py | 19 | 1 | invalid syntax | `from pandas._testing._warnings import assert_produces_warning, maybe_produces_warning` |
| 4298 | venv_creative/lib/python3.13/site-packages/pandas/_testing/contexts.py | 213 | 5 | invalid syntax | `else:` |
| 4299 | venv_creative/lib/python3.13/site-packages/pandas/plotting/_matplotlib/converter.py | 26 | 1 | invalid syntax | `from pandas.core.indexes.datetimes import date_range` |
| 4300 | venv_creative/lib/python3.13/site-packages/pandas/plotting/_matplotlib/core.py | 18 | 1 | invalid syntax | `from pandas.core.dtypes.dtypes import CategoricalDtype, ExtensionDtype` |
| 4301 | venv_creative/lib/python3.13/site-packages/dateutil/rrule.py | 36 | 18 | expression cannot contain assignment, perhaps you meant "=="? | `M366MASK = tuple([1]*31+[2]*29+[3]*31+[4]*30+[5]*31+[6]*30 +` |
| 4302 | venv_creative/lib/python3.13/site-packages/dateutil/parser/_parser.py | 67 | 29 | invalid syntax. Perhaps you forgot a comma? | `raise TypeError('Parser must be a string or character stream, not '` |
| 4303 | venv_creative/lib/python3.13/site-packages/aiohappyeyeballs/impl.py | 70 | 8 | unexpected indent | `exceptions: List[List[Union[OSError, RuntimeError]]] = []` |
| 4304 | venv_creative/lib/python3.13/site-packages/pydub/audio_segment.py | 33 | 1 | invalid syntax | `from .utils import (_fd_or_path_or_tempfile, audioop, db_to_float, get_array_type,` |
| 4305 | venv_creative/lib/python3.13/site-packages/python_http_client/client.py | 11 | 8 | unexpected indent | `from urllib.parse import urlencode` |
| 4306 | venv_creative/lib/python3.13/site-packages/whisper/decoding.py | 44 | 6 | invalid syntax | `):` |
| 4307 | venv_creative/lib/python3.13/site-packages/whisper/normalizers/english.py | 58 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 31 | `}` |
| 4308 | venv_creative/lib/python3.13/site-packages/platformdirs/api.py | 12 | 8 | unexpected indent | `from typing import Literal` |
| 4309 | venv_creative/lib/python3.13/site-packages/platformdirs/windows.py | 239 | 12 | unexpected indent | `import winreg  # noqa: PLC0415` |
| 4310 | venv_creative/lib/python3.13/site-packages/stripe/_api_requestor.py | 9 | 1 | invalid syntax | `from urllib.parse import parse_qs, urlencode, urlsplit, urlunsplit` |
| 4311 | venv_creative/lib/python3.13/site-packages/stripe/_payment_link.py | 372 | 13 | invalid syntax. Perhaps you forgot a comma? | `Literal["automatic", "automatic_async", "manual"]` |
| 4312 | venv_creative/lib/python3.13/site-packages/stripe/__init__.py | 44 | 40 | invalid syntax. Perhaps you forgot a comma? | `os.path.dirname(__file__), "data", "ca - certificates.crt"` |
| 4313 | venv_creative/lib/python3.13/site-packages/stripe/_subscription.py | 8 | 1 | invalid syntax | `from stripe._createable_api_resource import CreateableAPIResource` |
| 4314 | venv_creative/lib/python3.13/site-packages/stripe/_util.py | 13 | 1 | invalid syntax | `from urllib.parse import parse_qsl, quote_plus  # noqa: F401` |
| 4315 | venv_creative/lib/python3.13/site-packages/stripe/_any_iterator.py | 16 | 12 | unexpected indent | `self._async_iterator = async_iterator` |
| 4316 | venv_creative/lib/python3.13/site-packages/stripe/_stripe_object.py | 401 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 388 | `}` |
| 4317 | venv_stable/lib/python3.11/site-packages/pycodestyle.py | 66 | 9 | invalid syntax. Perhaps you forgot a comma? | `sys.version_info < (3, 10) and` |
| 4318 | venv_stable/lib/python3.11/site-packages/autopep8.py | 112 | 5 | invalid syntax. Perhaps you forgot a comma? | `r'^[ \t\f]*#.*?coding[:=][ \t]*([-_.a-zA-Z0-9]+)'` |
| 4319 | venv_stable/lib/python3.11/site-packages/sympy/core/add.py | 31 | 5 | invalid syntax | `positive_args = len(expr.args) - negative_args` |
| 4320 | venv_stable/lib/python3.11/site-packages/sympy/core/exprtools.py | 25 | 1 | invalid syntax | `from collections import defaultdict` |
| 4321 | venv_stable/lib/python3.11/site-packages/sympy/core/mul.py | 397 | 41 | unindent does not match any outer indentation level | `return [S.NaN], [], None` |
| 4322 | venv_stable/lib/python3.11/site-packages/sympy/core/function.py | 60 | 1 | invalid syntax | `from sympy.utilities.iterables import (has_dups, sift, iterable,` |
| 4323 | venv_stable/lib/python3.11/site-packages/sympy/core/expr.py | 184 | 16 | invalid syntax. Perhaps you forgot a comma? | `args = (len(args), tuple(args))` |
| 4324 | venv_stable/lib/python3.11/site-packages/sympy/concrete/expr_with_limits.py | 14 | 1 | invalid syntax | `from sympy.logic.boolalg import BooleanFunction` |
| 4325 | venv_stable/lib/python3.11/site-packages/sympy/printing/str.py | 102 | 5 | invalid syntax | `def _print_Basic(self, expr):` |
| 4326 | venv_stable/lib/python3.11/site-packages/sympy/printing/latex.py | 48 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `tex_greek_dictionary = {` |
| 4327 | venv_stable/lib/python3.11/site-packages/sympy/printing/pretty/pretty.py | 380 | 44 | invalid syntax | `if (count_total_deriv > 1) != False:` |
| 4328 | venv_stable/lib/python3.11/site-packages/sympy/logic/boolalg.py | 218 | 5 | invalid syntax | `def binary_symbols(self):` |
| 4329 | venv_stable/lib/python3.11/site-packages/sympy/logic/algorithms/lra_theory.py | 473 | 23 | unindent does not match any outer indentation level | `M = self.A` |
| 4330 | venv_stable/lib/python3.11/site-packages/sympy/solvers/bivariate.py | 79 | 5 | invalid syntax | `if len(fterms) == 1:` |
| 4331 | venv_stable/lib/python3.11/site-packages/sympy/solvers/solvers.py | 25 | 1 | invalid syntax | `from sympy.core.logic import fuzzy_not, fuzzy_and` |
| 4332 | venv_stable/lib/python3.11/site-packages/sympy/solvers/simplex.py | 149 | 9 | invalid syntax. Perhaps you forgot a comma? | `A = M - Mj * (Mi / Mij)` |
| 4333 | venv_stable/lib/python3.11/site-packages/sympy/solvers/solveset.py | 18 | 1 | invalid syntax | `from sympy.core.containers import Tuple` |
| 4334 | venv_stable/lib/python3.11/site-packages/sympy/solvers/ode/subscheck.py | 130 | 13 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `funcs = set().union(*funcs)` |
| 4335 | venv_stable/lib/python3.11/site-packages/sympy/solvers/ode/systems.py | 12 | 1 | invalid syntax | `from sympy.functions import (exp, im, cos, sin, re, Piecewise,` |
| 4336 | venv_stable/lib/python3.11/site-packages/sympy/solvers/ode/ode.py | 238 | 1 | invalid syntax | `from sympy.core.multidimensional import vectorize` |
| 4337 | venv_stable/lib/python3.11/site-packages/sympy/testing/tests/test_code_quality.py | 84 | 25 | unindent does not match any outer indentation level | `continue` |
| 4338 | venv_stable/lib/python3.11/site-packages/sympy/integrals/meijerint.py | 43 | 1 | invalid syntax | `from sympy.core.mul import Mul` |
| 4339 | venv_stable/lib/python3.11/site-packages/sympy/integrals/transforms.py | 10 | 1 | invalid syntax | `from sympy.core.mul import Mul` |
| 4340 | venv_stable/lib/python3.11/site-packages/sympy/integrals/integrals.py | 102 | 9 | invalid syntax | `return obj` |
| 4341 | venv_stable/lib/python3.11/site-packages/sympy/assumptions/handlers/matrices.py | 16 | 1 | invalid syntax | `from sympy.matrices.expressions.blockmatrix import reblock_2x2` |
| 4342 | venv_stable/lib/python3.11/site-packages/sympy/assumptions/handlers/order.py | 26 | 1 | invalid syntax | `def _NegativePredicate_number(expr, assumptions):` |
| 4343 | venv_stable/lib/python3.11/site-packages/sympy/plotting/series.py | 15 | 1 | invalid syntax | `from sympy.core.sympify import sympify` |
| 4344 | venv_stable/lib/python3.11/site-packages/sympy/sets/sets.py | 2331 | 33 | unterminated string literal (detected at line 2332) | `raise TypeError("Invalid input: '%s', input args \` |
| 4345 | venv_stable/lib/python3.11/site-packages/sympy/interactive/printing.py | 72 | 5 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `dvioptions = dvi.split()` |
| 4346 | venv_stable/lib/python3.11/site-packages/sympy/functions/special/hyper.py | 22 | 1 | invalid syntax | `from sympy.functions import factorial, RisingFactorial` |
| 4347 | venv_stable/lib/python3.11/site-packages/sympy/functions/combinatorial/numbers.py | 28 | 1 | invalid syntax | `from sympy.functions.elementary.exponential import log` |
| 4348 | venv_stable/lib/python3.11/site-packages/sympy/functions/elementary/integers.py | 49 | 9 | invalid syntax | `for t in Add.make_args(arg):` |
| 4349 | venv_stable/lib/python3.11/site-packages/sympy/functions/elementary/complexes.py | 10 | 1 | invalid syntax | `from sympy.core.logic import fuzzy_not, fuzzy_or` |
| 4350 | venv_stable/lib/python3.11/site-packages/sympy/functions/elementary/trigonometric.py | 24 | 1 | invalid syntax | `from sympy.logic.boolalg import And` |
| 4351 | venv_stable/lib/python3.11/site-packages/sympy/tensor/array/array_comprehension.py | 38 | 30 | invalid syntax. Perhaps you forgot a comma? | `raise ValueError('ArrayComprehension requires values lower and upper bound'` |
| 4352 | venv_stable/lib/python3.11/site-packages/sympy/physics/control/lti.py | 36 | 1 | invalid syntax | `def _roots(poly, var):` |
| 4353 | venv_stable/lib/python3.11/site-packages/sympy/physics/optics/gaussopt.py | 46 | 1 | invalid syntax | `from sympy.core.expr import Expr` |
| 4354 | venv_stable/lib/python3.11/site-packages/sympy/physics/quantum/gate.py | 39 | 1 | invalid syntax | `from sympy.physics.quantum.matrixutils import matrix_tensor_product, matrix_eye` |
| 4355 | venv_stable/lib/python3.11/site-packages/sympy/parsing/autolev/_listener_autolev_antlr.py | 19 | 17 | invalid syntax. Perhaps you forgot a comma? | `AutolevParser = getattr(autolevparser, 'AutolevParser', None)` |
| 4356 | venv_stable/lib/python3.11/site-packages/sympy/simplify/combsimp.py | 54 | 31 | unindent does not match any outer indentation level | `return gammasimp(expr)` |
| 4357 | venv_stable/lib/python3.11/site-packages/sympy/simplify/hyperexpand.py | 71 | 1 | invalid syntax | `from sympy.core.mod import Mod` |
| 4358 | venv_stable/lib/python3.11/site-packages/sympy/vector/coordsysrect.py | 27 | 1 | invalid syntax | `class CoordSys3D(Basic):` |
| 4359 | venv_stable/lib/python3.11/site-packages/sympy/diffgeom/diffgeom.py | 14 | 1 | invalid syntax | `from sympy.core.cache import cacheit` |
| 4360 | venv_stable/lib/python3.11/site-packages/sympy/stats/stochastic_process_types.py | 49 | 1 | invalid syntax | `from sympy.stats.stochastic_process import StochasticPSpace` |
| 4361 | venv_stable/lib/python3.11/site-packages/sympy/matrices/matrixbase.py | 53 | 1 | invalid syntax | `from .utilities import _iszero, _is_zero_after_expand_mul` |
| 4362 | venv_stable/lib/python3.11/site-packages/sympy/matrices/expressions/matmul.py | 12 | 1 | invalid syntax | `from sympy.matrices.exceptions import NonInvertibleMatrixError` |
| 4363 | venv_stable/lib/python3.11/site-packages/pygments/lexers/_postgres_builtins.py | 572 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `PSEUDO_TYPES = tuple(sorted(set(PSEUDO_TYPES) - set(map(str.lower, KEYWORDS))))` |
| 4364 | venv_stable/lib/python3.11/site-packages/pygments/lexers/objective.py | 197 | 9 | closing parenthesis '}' does not match opening parenthesis '[' on line 191 | `}` |
| 4365 | venv_stable/lib/python3.11/site-packages/pygments/lexers/modula2.py | 355 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 338 | `}` |
| 4366 | venv_stable/lib/python3.11/site-packages/pygments/lexers/sql.py | 225 | 5 | closing parenthesis '}' does not match opening parenthesis '[' on line 218 | `}` |
| 4367 | venv_stable/lib/python3.11/site-packages/kombu/serialization.py | 17 | 1 | invalid syntax | `from .utils.compat import entrypoints` |
| 4368 | venv_stable/lib/python3.11/site-packages/kombu/transport/redis.py | 127 | 1 | invalid syntax | `def get_redis_error_classes():` |
| 4369 | venv_stable/lib/python3.11/site-packages/kombu/transport/virtual/exchange.py | 59 | 1 | invalid syntax | `class DirectExchange(ExchangeType):` |
| 4370 | venv_stable/lib/python3.11/site-packages/flask_cors/core.py | 45 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `FLASK_CORS_EVALUATED = '_FLASK_CORS_EVALUATED'` |
| 4371 | venv_stable/lib/python3.11/site-packages/docutils/nodes.py | 157 | 9 | invalid syntax | `try:` |
| 4372 | venv_stable/lib/python3.11/site-packages/docutils/parsers/rst/tableparser.py | 83 | 17 | invalid syntax | `else:` |
| 4373 | venv_stable/lib/python3.11/site-packages/docutils/utils/__init__.py | 82 | 5 | invalid syntax | `def __init__(self, source, report_level, halt_level, stream=None,` |
| 4374 | venv_stable/lib/python3.11/site-packages/docutils/transforms/frontmatter.py | 127 | 9 | invalid syntax | `return True` |
| 4375 | venv_stable/lib/python3.11/site-packages/docutils/transforms/references.py | 88 | 13 | expression cannot contain assignment, perhaps you meant "=="? | `target['refid'] = target['ids'][0]` |
| 4376 | venv_stable/lib/python3.11/site-packages/docutils/transforms/universal.py | 68 | 1 | expected ':' | `#                or settings.source_url:` |
| 4377 | venv_stable/lib/python3.11/site-packages/mpmath/libmp/gammazeta.py | 40 | 1 | invalid syntax | `from .libelefun import (\` |
| 4378 | venv_stable/lib/python3.11/site-packages/mpmath/functions/hypergeometric.py | 47 | 1 | expected ':' | `#             and not have_singular_nongamma_weight:` |
| 4379 | venv_stable/lib/python3.11/site-packages/pyppeteer/launcher.py | 62 | 17 | invalid syntax | `AUTOMATION_ARGS = [` |
| 4380 | venv_stable/lib/python3.11/site-packages/IPython/core/prefilter.py | 25 | 1 | invalid syntax | `from .macro import Macro` |
| 4381 | venv_stable/lib/python3.11/site-packages/IPython/core/completerlib.py | 55 | 24 | expression cannot contain assignment, perhaps you meant "=="? | `import_re = re.compile(r'(?P<name>[^\W\d]\w*?)'` |
| 4382 | venv_stable/lib/python3.11/site-packages/IPython/core/inputtransformer2.py | 89 | 16 | invalid syntax. Perhaps you forgot a comma? | `initial_re=re.compile(r'^>>>( ¦$)')` |
| 4383 | venv_stable/lib/python3.11/site-packages/IPython/core/magics/namespace.py | 63 | 5 | invalid syntax | `@line_magic` |
| 4384 | venv_stable/lib/python3.11/site-packages/IPython/terminal/interactiveshell.py | 633 | 13 | closing parenthesis ')' does not match opening parenthesis '[' on line 623 | `),` |
| 4385 | venv_stable/lib/python3.11/site-packages/IPython/terminal/pt_inputhooks/qt.py | 31 | 1 | expected ':' | `#                     and not os.environ.get('WAYLAND_DISPLAY'):` |
| 4386 | venv_stable/lib/python3.11/site-packages/IPython/utils/wildcard.py | 91 | 1 | invalid syntax | `def list_namespace(namespace, type_pattern, filter, ignore_case=False, show_all=False):` |
| 4387 | venv_stable/lib/python3.11/site-packages/markdown/treeprocessors.py | 141 | 31 | invalid syntax | `if not matched:` |
| 4388 | venv_stable/lib/python3.11/site-packages/gast/gast.py | 41 | 9 | invalid syntax | `for i in range(len(args)):` |
| 4389 | venv_stable/lib/python3.11/site-packages/jedi/parser_utils.py | 23 | 1 | invalid syntax | `def get_executable_nodes(node, last_added=False):` |
| 4390 | venv_stable/lib/python3.11/site-packages/jedi/plugins/django.py | 46 | 1 | invalid syntax | `@inference_state_function_cache()` |
| 4391 | venv_stable/lib/python3.11/site-packages/jedi/plugins/pytest.py | 23 | 1 | invalid syntax | `def execute(callback):` |
| 4392 | venv_stable/lib/python3.11/site-packages/jedi/plugins/stdlib.py | 162 | 13 | invalid syntax | `except ParamIssue:` |
| 4393 | venv_stable/lib/python3.11/site-packages/jedi/api/completion.py | 42 | 1 | expected ':' | `#                     and p.name not in used_kwargs:` |
| 4394 | venv_stable/lib/python3.11/site-packages/jedi/api/__init__.py | 120 | 59 | invalid syntax. Perhaps you forgot a comma? | `project, environment=environment, script_path=self.path` |
| 4395 | venv_stable/lib/python3.11/site-packages/jedi/api/classes.py | 85 | 5 | invalid syntax | `def __init__(self, inference_state, name):` |
| 4396 | venv_stable/lib/python3.11/site-packages/jedi/api/helpers.py | 55 | 1 | invalid syntax | `def get_on_completion_name(module_node, lines, position):` |
| 4397 | venv_stable/lib/python3.11/site-packages/jedi/api/project.py | 97 | 5 | invalid syntax | `def save(self):` |
| 4398 | venv_stable/lib/python3.11/site-packages/jedi/api/file_name.py | 53 | 37 | '(' was never closed | `yield classes.Completion(` |
| 4399 | venv_stable/lib/python3.11/site-packages/jedi/api/refactoring/__init__.py | 122 | 9 | closing parenthesis '}' does not match opening parenthesis '(' on line 116 | `}` |
| 4400 | venv_stable/lib/python3.11/site-packages/jedi/api/refactoring/extract.py | 20 | 1 | invalid syntax | `def extract_variable(inference_state, path, module_node, name, pos, until_pos):` |
| 4401 | venv_stable/lib/python3.11/site-packages/jedi/inference/finder.py | 73 | 26 | '[' was never closed | `names = reversed([` |
| 4402 | venv_stable/lib/python3.11/site-packages/jedi/inference/analysis.py | 58 | 5 | invalid syntax | `def __eq__(self, other):` |
| 4403 | venv_stable/lib/python3.11/site-packages/jedi/inference/sys_path.py | 111 | 1 | expected ':' | `#                         and c[1].type == 'trailer':` |
| 4404 | venv_stable/lib/python3.11/site-packages/jedi/inference/references.py | 54 | 1 | invalid syntax | `def _find_defining_names(module_context, tree_name):` |
| 4405 | venv_stable/lib/python3.11/site-packages/jedi/inference/flow_analysis.py | 49 | 1 | expected ':' | `#             or not context.inference_state.flow_analysis_enabled:` |
| 4406 | venv_stable/lib/python3.11/site-packages/jedi/inference/docstrings.py | 45 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `REST_ROLE_PATTERN = re.compile(r':[^`]+:`([^`]+)`')` |
| 4407 | venv_stable/lib/python3.11/site-packages/jedi/inference/dynamic_params.py | 94 | 29 | Generator expression must be parenthesized | `function_value, arguments` |
| 4408 | venv_stable/lib/python3.11/site-packages/jedi/inference/syntax_tree.py | 71 | 1 | expected ':' | `#                     and context.get_value() is inference_state.builtins_module:` |
| 4409 | venv_stable/lib/python3.11/site-packages/jedi/inference/star_args.py | 40 | 1 | expected ':' | `#                     and argument.children[0] == '*' * param_name.star_count:` |
| 4410 | venv_stable/lib/python3.11/site-packages/jedi/inference/value/instance.py | 32 | 9 | expression cannot contain assignment, perhaps you meant "=="? | `self._instance = instance` |
| 4411 | venv_stable/lib/python3.11/site-packages/jedi/inference/value/dynamic_arrays.py | 99 | 1 | expected ':' | `#                             or execution_trailer.children[0] != '(' \` |
| 4412 | venv_stable/lib/python3.11/site-packages/jedi/inference/value/klass.py | 72 | 9 | invalid syntax | `for result_value in inferred:` |
| 4413 | venv_stable/lib/python3.11/site-packages/jedi/inference/value/function.py | 78 | 5 | invalid syntax | `def name(self):` |
| 4414 | venv_stable/lib/python3.11/site-packages/jedi/inference/compiled/access.py | 42 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `MethodDescriptorType = type(str.replace)` |
| 4415 | venv_stable/lib/python3.11/site-packages/jedi/inference/compiled/value.py | 61 | 9 | invalid syntax | `try:` |
| 4416 | venv_stable/lib/python3.11/site-packages/jedi/inference/compiled/getattr_static.py | 102 | 1 | expected ':' | `#                 and _safe_is_data_descriptor(klass_result):` |
| 4417 | venv_stable/lib/python3.11/site-packages/pyquery/pyquery.py | 47 | 1 | invalid syntax | `def with_camel_case_alias(func):` |
| 4418 | venv_stable/lib/python3.11/site-packages/engineio/server.py | 214 | 25 | invalid syntax. Perhaps you forgot a comma? | `r = self._bad_request('Not an accepted origin.')` |
| 4419 | venv_stable/lib/python3.11/site-packages/engineio/async_server.py | 204 | 17 | invalid syntax | `for client in self.sockets.values()` |
| 4420 | venv_stable/lib/python3.11/site-packages/numpy/ctypeslib.py | 57 | 1 | invalid syntax | `import os` |
| 4421 | venv_stable/lib/python3.11/site-packages/numpy/distutils/ccompiler.py | 17 | 1 | invalid syntax | `from distutils.errors import (` |
| 4422 | venv_stable/lib/python3.11/site-packages/numpy/distutils/misc_util.py | 50 | 1 | invalid syntax | `class InstallableLib:` |
| 4423 | venv_stable/lib/python3.11/site-packages/numpy/distutils/system_info.py | 3076 | 17 | closing parenthesis '}' does not match opening parenthesis '(' on line 3069 | `}` |
| 4424 | venv_stable/lib/python3.11/site-packages/numpy/distutils/core.py | 153 | 33 | invalid syntax. Perhaps you forgot a comma? | `raise TypeError("invalid description of extension module "` |
| 4425 | venv_stable/lib/python3.11/site-packages/numpy/distutils/fcompiler/__init__.py | 21 | 1 | invalid syntax | `import os` |
| 4426 | venv_stable/lib/python3.11/site-packages/numpy/distutils/command/build_src.py | 24 | 1 | invalid syntax | `from numpy.distutils.from_template import process_file as process_f_file` |
| 4427 | venv_stable/lib/python3.11/site-packages/numpy/f2py/cfuncs.py | 87 | 1 | cannot assign to subscript here. Maybe you meant '==' instead of '='? | `typedefs['complex_float'] = 'typedef struct {float r,i;} complex_float;'` |
| 4428 | venv_stable/lib/python3.11/site-packages/numpy/f2py/crackfortran.py | 273 | 5 | cannot assign to subscript here. Maybe you meant '==' instead of '='? | `badnames[n] = n + '_bn'` |
| 4429 | venv_stable/lib/python3.11/site-packages/numpy/testing/_private/utils.py | 26 | 1 | invalid syntax | `from numpy import isfinite, isnan, isinf` |
| 4430 | venv_stable/lib/python3.11/site-packages/numpy/lib/function_base.py | 17 | 1 | invalid syntax | `from numpy.core.umath import (` |
| 4431 | venv_stable/lib/python3.11/site-packages/numpy/lib/arraypad.py | 115 | 5 | invalid syntax | `order = 'F' if array.flags.fnc else 'C'  # Fortran and not also C-order` |
| 4432 | venv_stable/lib/python3.11/site-packages/pasta/base/codegen.py | 126 | 20 | unindent does not match any outer indentation level | `val = default` |
| 4433 | venv_stable/lib/python3.11/site-packages/safety/alerts/requirements.py | 35 | 5 | invalid syntax | `def is_valid(self):` |
| 4434 | venv_stable/lib/python3.11/site-packages/babel/messages/extract.py | 35 | 1 | invalid syntax | `from functools import lru_cache` |
| 4435 | venv_stable/lib/python3.11/site-packages/socketio/server.py | 174 | 5 | invalid syntax | `def send(self, data, to=None, room=None, skip_sid=None, namespace=None,` |
| 4436 | venv_stable/lib/python3.11/site-packages/socketio/async_server.py | 124 | 5 | invalid syntax | `def is_asyncio_based(self):` |
| 4437 | venv_stable/lib/python3.11/site-packages/sphinx/directives/__init__.py | 225 | 13 | invalid syntax. Perhaps you forgot a comma? | `'no-index' in self.options` |
| 4438 | venv_stable/lib/python3.11/site-packages/sphinx/ext/intersphinx.py | 144 | 5 | invalid syntax. Perhaps you forgot a comma? | `r.raise_for_status()` |
| 4439 | venv_stable/lib/python3.11/site-packages/tensorflow/python/autograph/impl/conversion.py | 76 | 9 | invalid syntax. Perhaps you forgot a comma? | `'{} appears to be decorated by wrapt, which is not yet supported'` |
| 4440 | venv_stable/lib/python3.11/site-packages/tensorflow/python/keras/metrics.py | 155 | 22 | expected 'else' after 'if' expression | `self._dtype = (backend.floatx() if dtype is None` |
| 4441 | venv_stable/lib/python3.11/site-packages/tensorflow/python/keras/layers/core.py | 127 | 15 | invalid syntax. Perhaps you forgot a comma? | `outputs = inputs * math_ops.cast(boolean_mask, inputs.dtype)` |
| 4442 | venv_stable/lib/python3.11/site-packages/tensorflow/python/keras/engine/base_layer_utils.py | 144 | 1 | invalid syntax | `def collect_previous_mask(input_tensors):` |
| 4443 | venv_stable/lib/python3.11/site-packages/tensorflow/python/keras/engine/training_eager_v1.py | 64 | 7 | invalid syntax | `targets = new_targets` |
| 4444 | venv_stable/lib/python3.11/site-packages/tensorflow/python/keras/engine/training.py | 101 | 5 | invalid syntax | `return method(self, *args, **kwargs)` |
| 4445 | venv_stable/lib/python3.11/site-packages/tensorflow/python/tools/api/generator/create_python_api.py | 100 | 3 | invalid syntax | `return import_list[0][0]` |
| 4446 | venv_stable/lib/python3.11/site-packages/tensorflow/python/checkpoint/functional_saver.py | 478 | 79 | closing parenthesis '}' does not match opening parenthesis '[' on line 473 | `for task, shardable_tensors in self._shardable_tensors_by_task.items()}` |
| 4447 | venv_stable/lib/python3.11/site-packages/tensorflow/python/checkpoint/restore.py | 104 | 7 | invalid syntax | `return False  # Not a new assignment` |
| 4448 | venv_stable/lib/python3.11/site-packages/tensorflow/python/saved_model/tracing_utils.py | 46 | 35 | unindent does not match any outer indentation level | `raise NotImplementedError(` |
| 4449 | venv_stable/lib/python3.11/site-packages/tensorflow/python/framework/type_spec.py | 177 | 9 | invalid syntax | `if attribute_supertype is None:` |
| 4450 | venv_stable/lib/python3.11/site-packages/tensorflow/python/kernel_tests/nn_ops/depthwise_conv_op_base.py | 63 | 13 | invalid syntax. Perhaps you forgot a comma? | `x1[:, start_height:end_height, start_width:end_width, k, np.newaxis]` |
| 4451 | venv_stable/lib/python3.11/site-packages/tensorflow/python/training/queue_runner_impl.py | 35 | 1 | invalid syntax | `@tf_export(v1=["train.queue_runner.QueueRunner", "train.QueueRunner"])` |
| 4452 | venv_stable/lib/python3.11/site-packages/tensorflow/python/training/saving/saveable_object_util.py | 580 | 5 | closing parenthesis '}' does not match opening parenthesis '(' on line 574 | `}` |
| 4453 | venv_stable/lib/python3.11/site-packages/tensorflow/python/distribute/mirrored_strategy.py | 87 | 40 | invalid syntax | `if num_workers == 1 and not all_local:` |
| 4454 | venv_stable/lib/python3.11/site-packages/tensorflow/python/distribute/ps_values.py | 52 | 1 | invalid syntax | `class AggregatingVariable(resource_variable_ops.BaseResourceVariable,` |
| 4455 | venv_stable/lib/python3.11/site-packages/tensorflow/python/distribute/single_loss_example.py | 49 | 3 | invalid syntax | `return single_loss_step, layer` |
| 4456 | venv_stable/lib/python3.11/site-packages/tensorflow/python/distribute/cross_device_ops.py | 82 | 42 | invalid syntax | `if not check_destinations(destinations):` |
| 4457 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/special_math_ops.py | 612 | 1 | invalid syntax | `def _enclosing_tpu_context():` |
| 4458 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/sparse_ops.py | 142 | 14 | invalid syntax. Perhaps you forgot a comma? | `values = array_ops.gather_nd(tensor, indices)` |
| 4459 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/parsing_ops.py | 50 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_construct_sparse_tensors_for_sparse_features = \` |
| 4460 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/cond_v2.py | 110 | 5 | positional argument follows keyword argument | `return _build_cond(` |
| 4461 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/control_flow_ops.py | 87 | 1 | invalid syntax | `def _NextIteration(tensor, name=None):` |
| 4462 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/gradients_util.py | 130 | 3 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `pending_count = collections.defaultdict(int)` |
| 4463 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/math_ops.py | 194 | 13 | invalid syntax. Perhaps you forgot a comma? | `start = array_ops.broadcast_to(start, broadcast_shape)` |
| 4464 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/embedding_ops.py | 79 | 13 | expected 'else' after 'if' expression | `axes=(list(range(ids_rank, params_rank)) if ids_static and params_static` |
| 4465 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/linalg/linear_operator_util.py | 116 | 5 | invalid syntax | `return value` |
| 4466 | venv_stable/lib/python3.11/site-packages/tensorflow/python/ops/distributions/student_t.py | 44 | 1 | invalid syntax | `@tf_export(v1=["distributions.StudentT"])` |
| 4467 | venv_stable/lib/python3.11/site-packages/tensorflow/python/tpu/device_assignment.py | 96 | 23 | invalid syntax. Perhaps you forgot a comma? | `core_assignment = numpy_compat.np_asarray(core_assignment, dtype=np.int32)` |
| 4468 | venv_stable/lib/python3.11/site-packages/tensorflow/python/data/experimental/ops/parsing_ops.py | 37 | 23 | invalid syntax. Perhaps you forgot a comma? | `raise TypeError("Input dataset should be a dataset of vectors of "` |
| 4469 | venv_stable/lib/python3.11/site-packages/tensorflow/python/data/ops/from_generator_op.py | 125 | 33 | invalid syntax | `if output_shapes is not None:` |
| 4470 | venv_stable/lib/python3.11/site-packages/tensorflow/python/eager/backprop_util.py | 50 | 26 | unindent does not match any outer indentation level | `return first_type` |
| 4471 | venv_stable/lib/python3.11/site-packages/tensorflow/python/eager/polymorphic_function/concrete_function.py | 99 | 3 | invalid syntax. Perhaps you forgot a comma? | `backward_function_attr.update(common_attributes)` |
| 4472 | venv_stable/lib/python3.11/site-packages/tensorflow/python/eager/polymorphic_function/polymorphic_function.py | 124 | 1 | invalid syntax | `class _FrequentTracingDetector(object):` |
| 4473 | venv_stable/lib/python3.11/site-packages/tensorflow/python/debug/cli/command_parser.py | 56 | 1 | invalid syntax | `def parse_command(command):` |
| 4474 | venv_stable/lib/python3.11/site-packages/tensorflow/python/debug/lib/debug_data.py | 237 | 1 | invalid syntax | `def extract_core_metadata_from_event_proto(event):` |
| 4475 | venv_stable/lib/python3.11/site-packages/tensorboard/_vendor/bleach/_vendor/html5lib/html5parser.py | 28 | 1 | invalid syntax | `def parse(doc, treebuilder="etree", namespaceHTMLElements=True, **kwargs):` |
| 4476 | venv_stable/lib/python3.11/site-packages/tensorboard/_vendor/bleach/_vendor/html5lib/_tokenizer.py | 1498 | 55 | too many nested parentheses | `self.tokenQueue.append({"type": tokenTypes["ParseError"], "data":` |
| 4477 | venv_stable/lib/python3.11/site-packages/tensorboard/_vendor/bleach/_vendor/html5lib/filters/whitespace.py | 21 | 1 | expected ':' | `#                     and (preserve or token["name"] in self.spacePreserveElements):` |
| 4478 | venv_stable/lib/python3.11/site-packages/yaml/scanner.py | 268 | 5 | invalid syntax | `def next_possible_simple_key(self):` |
| 4479 | venv_stable/lib/python3.11/site-packages/yaml/error.py | 66 | 76 | unmatched ')' | `or self.context_mark.column != self.problem_mark.column):` |
| 4480 | venv_stable/lib/python3.11/site-packages/yaml/representer.py | 7 | 1 | invalid syntax | `from .error import *` |
| 4481 | venv_stable/lib/python3.11/site-packages/yaml/reader.py | 41 | 9 | invalid syntax | `else:` |
| 4482 | venv_stable/lib/python3.11/site-packages/yaml/resolver.py | 73 | 1 | expected ':' | `#                     and not isinstance(node_check, str) \` |
| 4483 | venv_stable/lib/python3.11/site-packages/yaml/emitter.py | 172 | 5 | invalid syntax | `def expect_nothing(self):` |
| 4484 | venv_stable/lib/python3.11/site-packages/flasgger/utils.py | 59 | 11 | invalid syntax. Perhaps you forgot a comma? | `= swagger.config.get('optional_fields') or OPTIONAL_FIELDS` |
| 4485 | venv_stable/lib/python3.11/site-packages/celery/platforms.py | 51 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `EX_OK = getattr(os, 'EX_OK', 0)` |
| 4486 | venv_stable/lib/python3.11/site-packages/celery/backends/mongodb.py | 265 | 13 | closing parenthesis '}' does not match opening parenthesis '[' on line 259 | `}` |
| 4487 | venv_stable/lib/python3.11/site-packages/feedparser/api.py | 114 | 1 | expected ':' | `#        and urllib.parse.urlparse(url_file_stream_or_string)[0] in ('http', 'https', 'ftp', 'file', 'feed'):` |
| 4488 | venv_stable/lib/python3.11/site-packages/parso/python/tree.py | 60 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_RETURN_STMT_CONTAINERS = set(['suite', 'simple_stmt']) ¦ _FLOW_CONTAINERS` |
| 4489 | venv_stable/lib/python3.11/site-packages/parso/python/pep8.py | 15 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_NON_STAR_TYPES = ('term', 'import_from', 'power')` |
| 4490 | venv_stable/lib/python3.11/site-packages/parso/python/diff.py | 110 | 1 | expected ':' | `#                     and node.get_start_pos_of_prefix() == (1, 0):` |
| 4491 | venv_stable/lib/python3.11/site-packages/parso/python/errors.py | 22 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `_COMP_FOR_TYPES = ('comp_for', 'sync_comp_for')` |
| 4492 | venv_stable/lib/python3.11/site-packages/parso/python/tokenize.py | 116 | 5 | invalid syntax. Perhaps you forgot a comma? | `r'(?:\{\{¦\}\}¦\\N\{' + unicode_character_name` |
| 4493 | venv_stable/lib/python3.11/site-packages/parso/pgen2/grammar_parser.py | 45 | 26 | invalid syntax. Perhaps you forgot a comma? | `version_info=parse_version_string('3.9')` |
| 4494 | venv_stable/lib/python3.11/site-packages/reportlab/lib/testutils.py | 106 | 1 | invalid syntax | `def mockUrlRead(name):` |
| 4495 | venv_stable/lib/python3.11/site-packages/reportlab/graphics/barcode/lto.py | 46 | 1 | expected ':' | `#             or (subtype not in ascii_uppercase + string_digits) :` |
| 4496 | venv_stable/lib/python3.11/site-packages/reportlab/graphics/barcode/code128.py | 272 | 1 | expected ':' | `#                     and l[i+1] in digits:` |
| 4497 | venv_stable/lib/python3.11/site-packages/billiard/pool.py | 34 | 1 | invalid syntax | `from .compat import get_errno, mem_rss, send_offset` |
| 4498 | venv_stable/lib/python3.11/site-packages/future/backports/email/_header_value_parser.py | 210 | 5 | invalid syntax | `@property` |
| 4499 | venv_stable/lib/python3.11/site-packages/future/backports/email/feedparser.py | 193 | 1 | expected ':' | `#                and not root.is_multipart():` |
| 4500 | venv_stable/lib/python3.11/site-packages/future/standard_library/__init__.py | 244 | 1 | invalid syntax | `class RenameImport(object):` |
| 4501 | venv_stable/lib/python3.11/site-packages/scipy/odr/_odrpack.py | 51 | 1 | invalid syntax. Maybe you meant '==' or ':=' instead of '='? | `odr = __odrpack.odr` |
| 4502 | venv_stable/lib/python3.11/site-packages/scipy/optimize/_shgo.py | 489 | 30 | invalid syntax. Perhaps you forgot a comma? | `shc.fail_routine(mes="Failed to find a feasible minimizer point. "` |
| 4503 | venv_stable/lib/python3.11/site-packages/scipy/optimize/_linprog_simplex.py | 237 | 13 | invalid syntax. Perhaps you forgot a comma? | `f"The pivot operation produces a pivot value of:{pivval: .1e}, "` |
| 4504 | venv_stable/lib/python3.11/site-packages/scipy/optimize/_minimize.py | 26 | 1 | invalid syntax | `from ._trustregion_dogleg import _minimize_dogleg` |
| 4505 | venv_stable/lib/python3.11/site-packages/scipy/optimize/_trustregion_constr/qp_subproblem.py | 22 | 1 | invalid syntax | `def eqp_kktfact(H, c, A, b):` |
| 4506 | venv_stable/lib/python3.11/site-packages/scipy/interpolate/_polyint.py | 11 | 9 | invalid syntax | `__all__ = ["KroghInterpolator", "krogh_interpolate",` |
| 4507 | venv_stable/lib/python3.11/site-packages/scipy/interpolate/_interpolate.py | 173 | 1 | invalid syntax | `def _do_extrapolate(fill_value):` |
| 4508 | venv_stable/lib/python3.11/site-packages/scipy/sparse/_coo.py | 19 | 1 | invalid syntax | `from ._base import issparse, SparseEfficiencyWarning, _spbase, sparray` |
| 4509 | venv_stable/lib/python3.11/site-packages/scipy/signal/_signaltools.py | 119 | 5 | closing parenthesis ')' does not match opening parenthesis '[' on line 115 | `):` |
| 4510 | venv_stable/lib/python3.11/site-packages/email_validator/validate_email.py | 93 | 22 | expected 'else' after 'if' expression | `ret.original = ((local_part if not is_quoted_local_part` |
| 4511 | venv_stable/lib/python3.11/site-packages/dateutil/parser/_parser.py | 69 | 29 | invalid syntax. Perhaps you forgot a comma? | `raise TypeError('Parser must be a string or character stream, not '` |
| 4512 | venv_stable/lib/python3.11/site-packages/pyflakes/checker.py | 50 | 1 | invalid syntax | `def _is_tuple_constant(node):  # type: (ast.AST) -> bool` |
| 4513 | venv_stable/lib/python3.11/site-packages/passlib/tests/test_ext_django_source.py | 21 | 1 | invalid syntax | `if has_min_django:` |