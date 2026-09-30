import { defineConfig } from 'orval';

const BASE_TARGET_PATH = './src/shared/api/orval';

const targetPath = <T extends string>(
  name: T,
): `${typeof BASE_TARGET_PATH}/${T}/${T}.ts` => {
  return `${BASE_TARGET_PATH}/${name}/${name}.ts`;
};

const MUTATOR_CONFIG = {
  path: './src/shared/api/axios-client.ts',
  name: 'customInstance',
};

const IDENTIFY_URL = process.env.IDENTIFY_SERVICE_URL || 'http://127.0.0.1:3001';
const UPTIME_URL = process.env.UPTIME_SERVICE_URL || 'http://127.0.0.1:3000';

export default defineConfig({
  'identify-service': {
    input: {
      target: `${IDENTIFY_URL}/docs/docs.json`,
    },
    output: {
      target: targetPath('identify-service'),
      baseUrl: IDENTIFY_URL,
      client: 'axios',
      httpClient: 'axios',
      mode: 'tags-split',
      namingConvention: 'kebab-case',
      override: {
        mutator: MUTATOR_CONFIG,
      },
    },
  },

  'uptime-service': {
    input: {
      target: `${UPTIME_URL}/docs/docs.json`,
    },
    output: {
      target: targetPath('uptime-service'),
      baseUrl: UPTIME_URL,
      client: 'axios',
      httpClient: 'axios',
      mode: 'tags-split',
      namingConvention: 'kebab-case',
      override: {
        mutator: MUTATOR_CONFIG,
      },
    },
  },
});
