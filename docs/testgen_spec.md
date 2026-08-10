# Spec: TestGen Sync CLI Tool (tg)
#
# Requirements:
# 1. Provide a global CLI command `tg`.
# 2. Command `tg file <path>` generates unittest or pytest test file for the given source file.
# 3. Command `tg scan` scans undocumented or untested files in src/ and creates corresponding tests.
#
# Invariants:
# - Must support local Ollama and custom models.
# - Output files go to tests/ folder (e.g., tests/test_<filename>.py).
# - Preserve existing tests if any, or prompt before overwriting.
