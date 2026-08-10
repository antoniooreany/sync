# Spec: DocGen Sync CLI Tool (dg)
#
# Requirements:
# 1. Provide a global CLI command `dg`.
# 2. Command `dg init` configurations setup.
# 3. Command `dg generate <path>` creates markdown doc using LLM.
# 4. Command `dg scan` checks changed/undocumented files.
#
# Invariants:
# - Must support local Ollama and custom models.
# - Output files go to docs/ folder.
# - Create/update docs/README.md with a table of contents.
