<!-- BEGIN CODEX CLOUD CONTEXT -->
## Cloud session context

For a Linux cloud task, run `bash tools/cloud-layer/codex-setup.sh` if setup has
not run, then read `_brain/00-READ-FIRST.md` and every context file it names that
exists. Read `_brain/memory/MEMORY.md` and relevant named memory files. Read this
repository's `CLAUDE.md` too when present. These explicit reads are required;
setup checking file existence does not mean the model has read the context.

Reusable cloud guidance is in `tools/cloud-layer/skills/*/SKILL.md`. Read the
matching file explicitly if the app does not discover it as a named skill.
App plugins, MCP connections, live agents and chats remain environment-specific.
Use available CLI/tools; never claim an unavailable connector works from a config.

Keep work and memory scoped to this repository. Never clone the owner's full
business vault into a client/minimal task. Put new facts in a new named file in
`_brain/memory/`. Existing-memory corrections go in a new dated file under
`_brain/inbox/`, naming the intended target and evidence, for review in the owning
session; direct edits to generated existing memory can be overwritten by sync.
Shared/business-brain corrections use their named inbox files when documented.
Commit a concise project handoff before switching apps. Never commit credentials.
<!-- END CODEX CLOUD CONTEXT -->

