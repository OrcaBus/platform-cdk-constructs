import {StageName} from "./accounts";

export const icav2ProjectId: Record<StageName, string> = {
  BETA: "ea19a3f5-ec7c-4940-a474-c31cd91dbad4", // development
  GAMMA: "157b9e78-b2e1-45a7-bfcd-691159995f7c", // staging
  PROD: "eba5c946-1677-441d-bbce-6a11baadecbb", // production
};

export const icav2AccessTokenSecretId: Record<StageName, string> = {
  BETA: 'ICAv2JWTKey-umccr-prod-service-dev', // pragma: allowlist secret
  GAMMA: 'ICAv2JWTKey-umccr-prod-service-staging', // pragma: allowlist secret
  PROD: 'ICAv2JWTKey-umccr-prod-service-production', // pragma: allowlist secret
};

export const icav2BaseUrl: string = "https://ica.illumina.com/ica/rest"