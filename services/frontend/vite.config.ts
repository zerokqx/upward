import { tanstackRouter } from "@tanstack/router-plugin/vite";
import react, { reactCompilerPreset } from "@vitejs/plugin-react";
import babel from "@rolldown/plugin-babel";
import { defineConfig } from "vite";

const APP = "./src/app";
// https://vite.dev/config/
export default defineConfig({
  server: { host: "0.0.0.0" },
  resolve: {
    tsconfigPaths: true,
  },
  plugins: [
    tanstackRouter({
      target: "react",
      autoCodeSplitting: true,
      routesDirectory: APP.concat("/routes"),
      generatedRouteTree: APP.concat("/routeTree.gen.ts"),
    }),
    react(),
    babel({ presets: [reactCompilerPreset()] }),
  ],
});
