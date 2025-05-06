class Config {
  apiBaseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:5001";
  secretKey = process.env.SECRET_KEY ?? "test-key";
  tokenKey = "coin-trading.admin.token";
  sessionKey = "session";

  get encodedKey() {
    return new TextEncoder().encode(this.secretKey);
  }
}

export const config = new Config();
