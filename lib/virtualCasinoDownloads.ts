export const casinoDownloadGroups = [
  {
    title: "Frozen inputs",
    files: [
      { label: "Protocol v1.0", file: "protocol-v1.0.json", type: "JSON" },
      { label: "Player policy manifest", file: "player-manifest.json", type: "JSON" },
      { label: "Game mathematics", file: "game-mathematics.json", type: "JSON" },
      { label: "Run metadata & seed reveal", file: "run-metadata.json", type: "JSON" },
    ],
  },
  {
    title: "Visible world",
    files: [
      { label: "Summary", file: "visible-summary.json", type: "JSON" },
      { label: "Player outcomes", file: "players.csv", type: "CSV" },
      { label: "Cohort outcomes", file: "cohorts.csv", type: "CSV" },
      { label: "Game outcomes", file: "games.csv", type: "CSV" },
      { label: "Daily time series", file: "daily-timeseries.csv", type: "CSV" },
      { label: "Hashed checkpoints", file: "checkpoints.json", type: "JSON" },
      { label: "Immutable wager ledger", file: "visible-ledger.ndjson.gz", type: "NDJSON.GZ" },
    ],
  },
  {
    title: "Replication laboratory",
    files: [
      { label: "World summaries", file: "replication-worlds.csv", type: "CSV" },
      { label: "Policy summaries", file: "replication-players.csv", type: "CSV" },
      { label: "Cohort summaries", file: "replication-cohorts.csv", type: "CSV" },
    ],
  },
  {
    title: "Source & schema",
    files: [
      { label: "Source manifest", file: "source-manifest.json", type: "JSON" },
      { label: "Simulation engine", file: "source/engine/simulate.mjs", type: "ESM" },
      { label: "Game mathematics source", file: "source/engine/games.mjs", type: "ESM" },
      { label: "Replay procedure", file: "source/scripts/replay.mjs", type: "ESM" },
      { label: "Ledger event schema", file: "source/schemas/ledger-event.schema.json", type: "JSON Schema" },
      { label: "Reference PostgreSQL schema", file: "source/schemas/postgres.sql", type: "SQL" },
      { label: "Environment lock file", file: "environment-package-lock.json", type: "JSON" },
    ],
  },
  {
    title: "Documentation",
    files: [
      { label: "Architecture", file: "ARCHITECTURE.md", type: "Markdown" },
      { label: "Preregistration", file: "PREREGISTRATION.md", type: "Markdown" },
      { label: "Methods", file: "METHODS.md", type: "Markdown" },
      { label: "Safety review", file: "SAFETY.md", type: "Markdown" },
      { label: "Data dictionary", file: "DATA_DICTIONARY.md", type: "Markdown" },
      { label: "Production-scale boundary", file: "PRODUCTION-SCALE.md", type: "Markdown" },
      { label: "Changelog", file: "CHANGELOG.md", type: "Markdown" },
      { label: "SHA-256 checksums", file: "checksums.sha256", type: "Text" },
    ],
  },
] as const;

export const casinoDownloadFiles = casinoDownloadGroups.flatMap((group) =>
  group.files.map(({ file }) => file),
);
