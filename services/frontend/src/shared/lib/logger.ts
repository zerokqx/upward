import { Logger } from "tslog";

export const logger = new Logger({
  name: "Upward",
  type: "pretty",
  minLevel: 0,
});

export const authLogger = logger.getSubLogger({ name: "Auth" });
