declare module "cloudflare:workers" {
  export const env: {
    REVIEW_QUEUE?: {
      get(key: string): Promise<string | null>;
      put(key: string, value: string): Promise<void>;
    };
  };
}
