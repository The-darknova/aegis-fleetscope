import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  client: 'fetch',
  input: '../shared/openapi/openapi.yaml',
  output: 'src/api',
});
