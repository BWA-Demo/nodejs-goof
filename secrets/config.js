// Demo secrets for Snyk Secrets scanning (nodejs-goof).
// Every credential below is FAKE and non-functional — it exists only so
// `snyk secrets test` has hard-coded secrets to detect. Do NOT use in real code;
// real apps should load secrets from a vault or environment variables.

module.exports = {
  // Cloud credentials committed straight into source (classic leak).
  aws: {
    accessKeyId: 'AKIAQYLPMN5HGOOFDEMO',
    secretAccessKey: 'x8Kd9fQ2pLmN7vB3zRt6Y1wS4uH0jG5cAeD8fI2',
    region: 'us-east-1',
  },

  // Third-party API tokens.
  stripeSecretKey: 'sk_live_51GoofDemo00AbCdEfGhIjKlMnOpQrStUvWxYz1234567890',
  slackToken: 'xoxb-1234567890-0987654321-GoofDemoFakeSlackTokenXyz',
  githubToken: 'ghp_GoofDemoFakePersonalAccessToken0123456789abcd',

  // Database connection string with inline password.
  databaseUrl: 'postgres://admin:SuperSecretPassword@db.internal:5432/goof',

  // Symmetric app secret used to sign sessions/JWTs.
  jwtSigningSecret: 'goof-demo-please-rotate-me-9f8e7d6c5b4a3210',
};

// Private key pasted into the repo (fake, truncated — not a usable key).
const PRIVATE_KEY = `-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEAx3Kd9fQ2pLmN7vB3zRt6Y1wS4uH0jG5cAeD8fI2GoofDemoKey
Fake0000000000000000000000000000000000000000000000000000000000Key
-----END RSA PRIVATE KEY-----`;

module.exports.privateKey = PRIVATE_KEY;
