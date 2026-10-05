import { defineConfig } from "orval";

const DOCS_URL = process.env.DOCS_SERVICE_URL || "http://localhost:5000";

const MUTATOR_CONFIG = {
  path: "./src/shared/api/axios-client.ts",
  name: "customInstance",
};

export default defineConfig({
  bff: {
    input: {
      target: `${DOCS_URL}/specs/bff.json`,
    },
    output: {
      target: "./src/shared/api/bff/bff.ts",
      schemas: "./src/shared/api/bff/model",
      client: "react-query",
      httpClient: "axios",
      mode: "tags-split",
      namingConvention: "kebab-case",
      override: {
        mutator: MUTATOR_CONFIG,
      },
    },
  },
});
