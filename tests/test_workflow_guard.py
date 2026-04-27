import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "_vendor"))
import yaml


ROOT = Path(__file__).resolve().parents[1]
SAMPLE_PROJECT_ID = "SER20260424-001"


def load_workflow_guard():
    spec = importlib.util.spec_from_file_location("workflow_guard", ROOT / "tools" / "workflow_guard.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class WorkflowGuardTests(unittest.TestCase):
    def test_validate_command_passes(self):
        result = subprocess.run(
            [sys.executable, "tools/workflow_guard.py", "validate"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("validation passed", result.stdout)

    def test_status_reports_creative_stage_for_epxx(self):
        result = subprocess.run(
            [sys.executable, "tools/workflow_guard.py", "status", "--project", SAMPLE_PROJECT_ID, "--episode", "epXX"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = yaml.safe_load(result.stdout)
        episode = payload["projects"][0]["episodes"][0]
        self.assertEqual(episode["orchestration_result"]["current_stage"], "创意定义")
        self.assertTrue(episode["orchestration_result"]["needs_business_review"])
        self.assertTrue(episode["orchestration_result"]["needs_compliance_review"])

    def test_status_orchestration_output_matches_schema(self):
        workflow_guard = load_workflow_guard()
        result = subprocess.run(
            [sys.executable, "tools/workflow_guard.py", "status", "--project", SAMPLE_PROJECT_ID, "--episode", "epXX"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = yaml.safe_load(result.stdout)
        episode = payload["projects"][0]["episodes"][0]
        orchestration_schema = yaml.safe_load((ROOT / "schemas" / "orchestration-result.schema.yaml").read_text())
        ledger_schema = yaml.safe_load((ROOT / "schemas" / "segment-ledger.schema.yaml").read_text())
        orchestration_issues = workflow_guard.validate_json_schema(episode["orchestration_result"], orchestration_schema)
        ledger_issues = workflow_guard.validate_json_schema(episode["segment_ledger"], ledger_schema)
        self.assertFalse(orchestration_issues, "\n".join(issue.message for issue in orchestration_issues))
        self.assertFalse(ledger_issues, "\n".join(issue.message for issue in ledger_issues))

    def test_sync_compat_generates_notice(self):
        result = subprocess.run(
            [sys.executable, "tools/workflow_guard.py", "sync-compat"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        producer_agent = (ROOT / ".claude" / "agents" / "producer-agent.md").read_text()
        self.assertTrue(producer_agent.startswith("<!-- compat mirror:"))
        self.assertIn(".claude/skills/", producer_agent)

    def test_script_schema_rejects_action_description(self):
        workflow_guard = load_workflow_guard()
        schema = yaml.safe_load((ROOT / "schemas" / "script.schema.yaml").read_text())
        payload = {
            "metadata": {
                "series_id": "SER001",
                "episode_id": "ep01",
                "version": "1.0",
                "status": "draft",
                "created_at": "2026-04-24T00:00:00+08:00",
                "updated_at": "2026-04-24T00:00:00+08:00",
                "based_on": {},
            },
            "episode": {
                "title": "测试",
                "goal": "测试目标",
                "synopsis": "测试梗概",
                "core_conflict": "测试冲突",
            },
            "scenes": [
                {
                    "scene_id": "SCENE_01",
                    "location": "酒馆",
                    "time": "夜",
                    "characters": ["阿烬"],
                    "action_description": "旧字段",
                    "dialogue": [],
                    "emotion": "紧张",
                    "value_change": "+",
                    "production_note": "note",
                    "estimated_duration": "15s",
                }
            ],
            "structure_check": {},
            "platform_check": {},
            "risks": {},
            "confirmed_items": [],
            "pending_items": [],
        }
        issues = workflow_guard.validate_json_schema(payload, schema)
        joined = "\n".join(issue.message for issue in issues)
        self.assertIn("unexpected key `action_description`", joined)

    def test_starter_templates_match_schemas(self):
        workflow_guard = load_workflow_guard()
        template_schema_pairs = {
            "templates/series/creative-bible.template.yaml": "schemas/creative-bible.schema.yaml",
            "templates/series/synopsis.template.yaml": "schemas/synopsis.schema.yaml",
            "templates/series/episode-plan.template.yaml": "schemas/episode-plan.schema.yaml",
            "templates/reviews/business-review-report.template.yaml": "schemas/business-review.schema.yaml",
            "templates/reviews/compliance-report.template.yaml": "schemas/compliance-review.schema.yaml",
            "templates/episodes/epXX/script/script.template.yaml": "schemas/script.schema.yaml",
            "templates/episodes/epXX/segments/segments.template.yaml": "schemas/segments.schema.yaml",
            "templates/episodes/epXX/segments/tasks/epXX-SEG01.template.yaml": "schemas/segment-task.schema.yaml",
            "templates/episodes/epXX/assets/asset-manifest.template.yaml": "schemas/asset-manifest.schema.yaml",
            "templates/episodes/epXX/assets/asset-prompts.template.yaml": "schemas/asset-prompts.schema.yaml",
            "templates/episodes/epXX/assets/asset-index.template.yaml": "schemas/asset-index.schema.yaml",
            "templates/episodes/epXX/assets/asset-archive.template.yaml": "schemas/asset-archive.schema.yaml",
            "templates/episodes/epXX/videos/video-prompts.template.yaml": "schemas/video-prompts.schema.yaml",
            "templates/episodes/epXX/videos/video-tasks.template.yaml": "schemas/video-tasks.schema.yaml",
            "templates/episodes/epXX/videos/video-tasks-final.template.yaml": "schemas/video-tasks.schema.yaml",
            "templates/episodes/epXX/videos/video-archive.template.yaml": "schemas/video-archive.schema.yaml",
            "templates/episodes/epXX/orchestration/orchestration-result.template.yaml": "schemas/orchestration-result.schema.yaml",
            "templates/episodes/epXX/orchestration/segment-ledger.template.yaml": "schemas/segment-ledger.schema.yaml",
        }
        for template_path, schema_path in template_schema_pairs.items():
            with self.subTest(template=template_path):
                payload = yaml.safe_load((ROOT / template_path).read_text())
                schema = yaml.safe_load((ROOT / schema_path).read_text())
                issues = workflow_guard.validate_json_schema(payload, schema)
                self.assertFalse(issues, "\n".join(issue.message for issue in issues))


if __name__ == "__main__":
    unittest.main()
