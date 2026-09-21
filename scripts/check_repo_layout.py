"""PHASE 0003: enforce the normative top-level repository layout.

Validates `docs/REPO_LAYOUT_SPEC.md` section 1 and 3 without modifying
runtime behavior. Exits 0 when compliant, 1 with violation list otherwise.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_ENTRIES = (
    "src",
    "tests",
    "docs",
    "scripts",
    "pyproject.toml",
    "requirements.txt",
    "pytest.ini",
    "run_vertical_slice.py",
    ".gitignore",
    "README.md",
)

REQUIRED_DOCS = (
    "REPO_LAYOUT_SPEC.md",
    "PRD.md",
    "ARCHITECTURE.md",
    "MASTER_ROADMAP_1000_PHASES.json",
    "ROADMAP_DEPENDENCIES.md",
    "PHASE_COMPLETION_POLICY.md",
    "IMPLEMENTATION_STATUS.md",
)

GITIGNORE_TOKENS = (
    "__pycache__/",
    "*.db",
    "*.log",
    "audit_logs/",
    ".winai/",
)


def check_layout(root: Path = ROOT) -> list:
    violations = []
    for name in REQUIRED_ENTRIES:
        if not (root / name).exists():
            violations.append(f"missing required top-level entry: {name}")
    for name in REQUIRED_DOCS:
        if not (root / "docs" / name).exists():
            violations.append(f"missing required doc: {name}")
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    for token in GITIGNORE_TOKENS:
        if token not in gitignore:
            violations.append(f".gitignore must exclude {token}")
    return violations


def main() -> int:
    violations = check_layout()
    if violations:
        for v in violations:
            print(f"VIOLATION: {v}")
        return 1
    print("Repository layout compliant with docs/REPO_LAYOUT_SPEC.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
