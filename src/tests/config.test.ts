import { test } from "node:test";
import assert from "node:assert/strict";
import { loadSettings } from "../config";

test("loadSettings uses defaults and config values", () => {
  const settings = loadSettings();
  assert.ok(settings.jwtSecret);
  assert.ok(settings.databaseUrl);
  assert.ok(settings.embeddingDimensions > 0);
});
