/**
 * Validate the secret name so that it doesn't end with 6 characters and a hyphen.
 */
export const validateSecretName = (secretName: string) => {
  // Note, this should not end with a hyphen and 6 characters, otherwise secrets manager won't be
  // able to find the secret using a partial ARN.
  if (/-(.){6}$/.test(secretName)) {
    throw new Error(
      "the secret name should not end with a hyphen and 6 characters",
    );
  }
};

export const JWT_SECRET_NAME = "orcabus/token-service-jwt"; // pragma: allowlist secret
validateSecretName(JWT_SECRET_NAME);


export const SERVICE_USER_SECRET_NAME = "orcabus/token-service-user"; // pragma: allowlist secret
validateSecretName(JWT_SECRET_NAME);
