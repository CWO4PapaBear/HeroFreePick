# Server implementation audit

`audit_server_implementation.py` produces a read-only inventory from the effective addon catalogue, the recorded server purchase catalogue, local stock and Area 52 Spell DBCs, and historical test logs. It does not run gameplay tests or change the server.

Run with Python and `lupa.lua51` available:

```text
python tools/audit/audit_server_implementation.py --workspace PATH_TO_CAN_WORKSPACE --output PATH_TO_REPORT_FOLDER
```

The workspace must contain the existing `work/area52-review`, `work/regalia/dbc_sources`, and `outputs/Hero_ClassPlus_All_Classes_Test` reference artifacts. The script uses only the initialization section of the Lua test harness, not test scenarios that mutate catalogue state.

Outputs:

- `AUDIT.html`: searchable per-entry catalogue with class/status filters and detailed evidence.
- `REPORT.md`: counts, incomplete groups, discrepancies and class breakdown.
- `implementation-catalogue.json`: all entries, canonical aliases, mode support, stock availability, source numeric differences, blockers and evidence hashes.
- `missing-spells.json`: missing stock IDs and their referencing entries. These are candidates for investigation, not an instruction to allocate new IDs.
- `spell-ids.json`: explicit IDs for the optional live collector.

## Classification boundaries

- Stock purchase support means the current Class+ metadata and grant code contain a route; it is not proof of matching Area 52 effects or exhaustive gameplay correctness.
- Reference review means text or nonvisual numeric DBC fields differ. Field changes are evidence for investigation, not proof that every difference needs a patch.
- Existing talent-tree ability aliases retain their canonical purchase and are excluded from TP-commit counts.
- Group-only reference spells need not exist as castable server spells when an entitlement controls their grants. Missing member spells still need work.
- Staged talent records are separated from active catalogue nodes.
- Classic native progression and the unimplemented Hybrid/Hero commit paths are reported independently.

## Optional live evidence

The current environment cannot access WSL (E_ACCESSDENIED), so the saved-data report does not inspect live SQL overrides or loaded SpellMgr state. To collect relevant database rows without changing anything, run `collect_live_evidence.py` in WSL with Docker access, supplying `--ids spell-ids.json --output live-evidence.json`. Defaults target `classless-test-database` and `classless-test-worldserver`; override those arguments for another explicitly selected server.

The collector issues SELECT queries only. It records spell_dbc overrides, proc/script bindings, ranks, learned-spell links and linked-spell rows for requested IDs. It does not restart containers, alter a database, teach spells or dump credentials. SQL presence still requires core/gameplay verification; the server's loaded DBC and transitive ranks may require further inspection.
