import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools" / "_vendor"))
import yaml


ROOT = Path(__file__).resolve().parents[1]


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

    def test_status_reports_v2_shape_for_new_project(self):
        result = subprocess.run(
            [sys.executable, "tools/workflow_guard.py", "status", "--project", "NEW", "--episode", "ep01"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = yaml.safe_load(result.stdout)
        episode = payload["projects"][0]["episodes"][0]
        self.assertIn("studio_status", episode)
        self.assertIn("shot_ledger", episode)
        self.assertEqual(episode["studio_status"]["current_stage"], "作品与剧本")
        self.assertEqual(episode["studio_status"]["next_agent"], "story-agent")

    def test_starter_templates_match_schemas(self):
        workflow_guard = load_workflow_guard()
        template_schema_pairs = {
            "templates/series/creative-thesis.template.yaml": "schemas/creative-thesis.schema.yaml",
            "templates/episodes/epXX/script/script.template.yaml": "schemas/script.schema.yaml",
            "templates/episodes/epXX/script/script-doctor-report.template.yaml": "schemas/script-doctor-report.schema.yaml",
            "templates/episodes/epXX/director/shot-design-table.template.yaml": "schemas/shot-design-table.schema.yaml",
            "templates/episodes/epXX/assets/visual-style-bible.template.yaml": "schemas/visual-style-bible.schema.yaml",
            "templates/episodes/epXX/assets/asset-index.template.yaml": "schemas/asset-index.schema.yaml",
            "templates/episodes/epXX/seedance/seedance-calibration-report.template.yaml": "schemas/seedance-calibration-report.schema.yaml",
            "templates/episodes/epXX/seedance/generation-failure-library.template.yaml": "schemas/generation-failure-library.schema.yaml",
            "templates/episodes/epXX/seedance/manual-generation-package.template.yaml": "schemas/manual-generation-package.schema.yaml",
            "templates/episodes/epXX/music/suno-music-task-card.template.yaml": "schemas/suno-music-task-card.schema.yaml",
        }
        for template_path, schema_path in template_schema_pairs.items():
            with self.subTest(template=template_path):
                payload = yaml.safe_load((ROOT / template_path).read_text())
                schema = yaml.safe_load((ROOT / schema_path).read_text())
                issues = workflow_guard.validate_json_schema(payload, schema)
                self.assertFalse(issues, "\n".join(issue.message for issue in issues))

    def test_manual_generation_template_respects_seedance_rules(self):
        payload = yaml.safe_load((ROOT / "templates/episodes/epXX/seedance/manual-generation-package.template.yaml").read_text())
        task = payload["tasks"][0]
        self.assertLessEqual(len(task["platform_upload_manifest"]), 9)
        self.assertTrue(task["audio"]["dialogue_present"])
        self.assertIn("Audio:", task["audio"]["prompt_text"])
        self.assertEqual(task["target_model"], "Seedance 2.0")

    def test_sync_compat_generates_v2_mirror(self):
        result = subprocess.run(
            [sys.executable, "tools/workflow_guard.py", "sync-compat"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        producer_agent = (ROOT / ".claude" / "agents" / "studio-producer.md").read_text()
        self.assertTrue(producer_agent.startswith("<!-- compat mirror:"))
        self.assertTrue((ROOT / ".claude" / "skills" / "seedance-upload-package" / "SKILL.md").exists())


if __name__ == "__main__":
    unittest.main()
