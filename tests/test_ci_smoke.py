"""Day 16 scaffold smoke tests — run in CI to verify structure."""
import os
import re


def test_env_example_exists():
    assert os.path.exists(".env.example")

def test_gitignore_excludes_env():
    with open(".gitignore") as f:
        assert ".env" in f.read()

def test_requirements_exists():
    assert os.path.exists("requirements.txt")

def test_src_modules_exist():
    for m in ["src/agent.py", "src/policy_engine.py", "src/audit_logger.py", "src/retriever.py"]:
        assert os.path.exists(m), f"Missing: {m}"

def test_governance_policies_exist():
    assert os.path.exists("governance/policies/pii-protection.yaml")

def test_dockerfile_exists():
    assert os.path.exists("Dockerfile")

def test_no_hardcoded_secrets():
    pattern = re.compile(r"sk-[a-zA-Z0-9]{20,}")
    for root, _, files in os.walk("src"):
        for fname in files:
            if fname.endswith(".py"):
                content = open(os.path.join(root, fname)).read()
                assert not pattern.search(content), f"Hardcoded key in {fname}"
