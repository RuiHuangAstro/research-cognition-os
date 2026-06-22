# Research DAG Design Principles

Source: User's research cognition OS design session (2026-05-11)

## Three DAG Views

Every research project needs three separate DAG views, not one giant graph.

### 1. Cognitive DAG — "How did my understanding evolve?"

Purpose: Give AI and future-self a quick entry into the project's intellectual history.

Example chain:
```
empirical model → analytical formula → catalog comparison → emldetect replication → psfgen bug → rollback audit
```

### 2. Trust DAG — "Which conclusions depend on which code/data/PSF/catalog?"

Purpose: Bug-impact tracing. When a node fails, trace downstream to find all contaminated conclusions.

Example chain:
```
my_psfgen_v0.6 → replica PSF image → replica emldetect ML histogram → conclusion: PSF wing explains tail
```

When `my_psfgen_v0.6` has a bug, the entire downstream chain turns red.

### 3. Frontier DAG — "What should I work on right now?"

Purpose: Daily attention allocator. Only 5–10 nodes. This is the graph you look at every morning.

Example:
```
Current frontier:
1. Audit psfgen bug impact
2. Build anchor PSF test
3. Rerun replica-vs-official comparison
4. Reassess ML tail explanation
```

## Node Types

| Code | Type | Meaning |
|------|------|---------|
| Q | Question | Research question |
| H | Hypothesis | Testable hypothesis |
| D | Derivation | Analytical/theoretical derivation |
| E | Experiment | Simulation / catalog test / computation |
| I | Insight | Settled conclusion (knowledge) |
| B | Bug/Blocker | Bug or blocking issue |

## Edge Types

| Edge | Meaning |
|------|---------|
| supports | A provides evidence for B |
| depends_on | A requires B's output |
| invalidates | A disproves / overturns B |
| supersedes | A replaces B (B is obsolete) |
| motivates | A naturally leads to asking B |
| contaminates | A (bug) pollutes downstream B's validity |

## Trust States & Colors

| State | Mermaid classDef | Color | Action |
|-------|-----------------|-------|--------|
| Trusted | `fill:#d8f5d0,stroke:#2b7a2b` | Green | Don't re-invest attention |
| Provisional | `fill:#fff3bf,stroke:#b8860b` | Yellow | Use with caution |
| Questioned | `fill:#ffd6d6,stroke:#b22222` | Red | Prioritize audit |
| Deprecated | `fill:#e5e5e5,stroke:#777` | Gray | Archive, no attention |
| Current | `fill:#d6e8ff,stroke:#1f5fbf,stroke-width:3px` | Blue | Invest attention now |

## Acyclicity Rule

DAG must not have back-edges. When a rollback happens, create a new node:

```
S04: old emldetect replication  →  B01: psfgen bug  →  S04b: corrected emldetect replication
```

This preserves history and keeps the graph traversable.

## Attention Investment Formula

```
Priority = Downstream Impact × Uncertainty × Leverage / Cost
```

| Factor | Meaning |
|--------|---------|
| Downstream Impact | How many downstream conclusions does this node affect? |
| Uncertainty | How uncertain is this node right now? |
| Leverage | If resolved, how much downstream work does it unblock? |
| Cost | Time/effort to resolve |

**Rule**: Always invest attention in the node with the highest Priority score.

## Five Diagnostic Questions

When reading a DAG, ask:

1. Which green nodes should I stop wasting attention on?
2. Which red nodes contaminate the most downstream conclusions?
3. Which yellow nodes, if resolved, would unlock the most downstream work?
4. Are there too many blue (current) nodes? (Scattered attention = problem)
5. Are there gray (deprecated) nodes still occupying mental space?

## Tool Progression

1. **Phase 1**: Mermaid (text, Git-friendly, AI-readable)
2. **Phase 2**: Obsidian Canvas (manual drag, visual, connects to notes)
3. **Phase 3**: Graphviz (auto-generate from YAML/manifest data)

Don't start with automation. Draw 20 nodes by hand first to understand your project's structure.