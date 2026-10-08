# Private/local architecture proposal (phase 5)

Status: design only. No private runtime, real import, database, deployment or
migration is implemented or authorized by this document. No actual holdings,
accounts, provider exports, private URLs, secrets or user-specific targets belong
in this repository. The public demo remains invented and separate.

## Boundary

PUBLIC SYNTHETIC: source, tests, invented fixtures, build output.
PRIVATE LOCAL (future, separately approved): owner-selected files -> local import
quarantine -> validated immutable source records -> reconciled ledger -> private
read-only interface. No outbound network or public-demo upload in this path.

Use an owner-controlled offline directory outside the repository. Do not rely on
.gitignore as the privacy boundary: no real input/output ever enters the public
worktree or its build directory. No silent cloud sync, analytics, remote error
reporting or automatic screenshot capture. Explicitly approved export is local
and destination-reviewed; do not treat a private URL as a safe public artifact.

## Proposed data layers

1. Raw input quarantine: retain original bytes locally, hash and import batch ID;
   validate type/size, never execute macros/scripts or embedded instructions.
2. Normalization: typed decimal strings, currency, provider transaction identity,
   dates and source references. Record rejected rows with local-only reasons.
3. Reconciliation: idempotent duplicate checks, reversals/corrections rather than
   rewriting history, cost-basis checks and separate cash/income/KF ledgers.
4. Manual market snapshots: price/FX currency/date/source, stale/incomplete flags.
5. Derived views: input lineage, completeness, calculation version; missing is
   unavailable, not zero. A payment date is not proof of a received dividend.

Possible local storage: SQLite for transaction integrity and indexed lineage;
raw sources in a separate local folder. Decide retention, encryption, backups and
key custody before implementation. SQLite alone is not an encryption solution.
Decimal strings should survive storage round-trips without float conversion.
Use immutable batch IDs and migration rollback on an invented test database.

## Implementation gates (future decisions, not tasks)

- Owner chooses the machine, storage folder and trusted audience.
- Agree import format, which facts may be retained, encryption/key custody,
  backup destinations, retention/deletion and recovery procedure.
- Threat model shared machine, theft, cloud-sync folders, malware, accidental git
  commit, logs/backups and exported screenshots. Offline is not a security proof.
- Prove the full path using invented data first, with no real files in tests/CI.
- Approve each real-data access and any distribution separately. Do not turn a
  design approval into permission to deploy, import or share.

## Acceptance matrix before any real-data trial

| Area | Required evidence using invented data |
| --- | --- |
| Network | Import/view/reset makes no outbound request, including error paths |
| Paths | Source/database/cache/log/export excluded from public worktree/build |
| Idempotency | Repeat import adds no duplicate; collision becomes a review item |
| Money | Decimal round-trips; fees/FX/partial sale reconcile to source |
| Income | Received evidence required; announced/estimated/KF remain separate |
| Missing data | No complete total for missing price, FX or required tax data |
| Privacy | Logs redact identifiers; export preview shows exact audience/content |
| Recovery | Local backup/restore and migrations tested; no hidden cloud copy |
| Deletion | Retention and deleting derived caches/backups clearly documented |

## Non-goals

No broker login/trade execution, credential collection, public hosting of real
data, paid market feeds, cloud account, automatic syncing or tax advice. No
promises of authentication, encryption or offline guarantees until tested in
an approved implementation. This PR changes documentation only.
