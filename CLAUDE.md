## graphify

Graphify is optional local code-navigation tooling. Generated output under `graphify-out/` is intentionally untracked and must not be assumed to exist.

Rules:
- Do not generate or regenerate Graphify output unless the user explicitly approves it.
- When a local `graphify-out/graph.json` exists, use `graphify query "<question>"` for codebase questions, `graphify path "<A>" "<B>"` for relationships, and `graphify explain "<concept>"` for focused concepts.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- Do not automatically update Graphify after unrelated code changes.
- Do not commit generated Graphify output unless a future explicit repository policy approves it.
