import { z } from "zod";

export const ownerRoleSchema = z.enum([
  "business_owner",
  "portfolio_owner",
  "technical_owner",
  "gtm_owner",
  "customer_service_owner",
]);

export const neuroWorkerTypeSchema = z.enum([
  "adhd",
  "audhd",
  "autistic",
  "neurotypical",
  "unspecified",
]);

export const googleScopeSchema = z.enum([
  "openid",
  "email",
  "profile",
  "https://www.googleapis.com/auth/calendar.readonly",
  "https://www.googleapis.com/auth/gmail.readonly",
  "https://www.googleapis.com/auth/admin.directory.user.readonly",
]);

export const integrationStatusSchema = z.enum([
  "ACTIVE",
  "REAUTH_REQUIRED",
  "REVOKED",
  "DISABLED",
]);

export const syncResourceSchema = z.enum([
  "calendar.event",
  "gmail.message.metadata",
  "gmail.message.full",
]);

export const connectGoogleRequestSchema = z.object({
  workspaceId: z.string().min(1),
  ownerRole: ownerRoleSchema,
  neuroWorkerType: neuroWorkerTypeSchema.optional(),
  requestedScopes: z.array(googleScopeSchema).min(1),
  redirectUri: z.string().url(),
});

export const connectGoogleResponseSchema = z.object({
  authorizationUrl: z.string().url(),
  state: z.string().min(10),
});

export const oauthCallbackRequestSchema = z.object({
  code: z.string().min(8),
  state: z.string().min(10),
  workspaceId: z.string().min(1),
  redirectUri: z.string().url(),
});

export const oauthCallbackResponseSchema = z.object({
  integrationConnectionId: z.string().min(1),
  status: integrationStatusSchema,
  grantedScopes: z.array(z.string()).default([]),
  account: z.object({
    providerAccountId: z.string().min(1),
    email: z.string().email(),
  }),
});

export const addScopesRequestSchema = z.object({
  addScopes: z.array(googleScopeSchema).min(1),
  redirectUri: z.string().url(),
});

export const addScopesResponseSchema = connectGoogleResponseSchema;

export const revokeIntegrationRequestSchema = z.object({
  reason: z
    .enum([
      "owner_requested_disconnect",
      "security_policy_change",
      "scope_reduction",
      "credential_rotation",
    ])
    .default("owner_requested_disconnect"),
});

export const revokeIntegrationResponseSchema = z.object({
  integrationConnectionId: z.string().min(1),
  status: z.literal("REVOKED"),
  revokedAt: z.string().datetime(),
});

export const triggerSyncRequestSchema = z.object({
  resources: z.array(syncResourceSchema).min(1),
  mode: z.enum(["incremental", "full"]).default("incremental"),
});

export const triggerSyncResponseSchema = z.object({
  jobId: z.string().min(1),
  status: z.enum(["queued", "running"]),
});

export const auditItemSchema = z.object({
  id: z.string().min(1),
  action: z.string().min(1),
  actorUserId: z.string().nullable().optional(),
  createdAt: z.string().datetime(),
  metadata: z.record(z.string(), z.unknown()).optional(),
});

export const auditResponseSchema = z.object({
  items: z.array(auditItemSchema),
  nextCursor: z.string().nullable().optional(),
});

export type OwnerRole = z.infer<typeof ownerRoleSchema>;
export type NeuroWorkerType = z.infer<typeof neuroWorkerTypeSchema>;
export type ConnectGoogleRequest = z.infer<typeof connectGoogleRequestSchema>;
export type ConnectGoogleResponse = z.infer<typeof connectGoogleResponseSchema>;
export type OauthCallbackRequest = z.infer<typeof oauthCallbackRequestSchema>;
export type OauthCallbackResponse = z.infer<typeof oauthCallbackResponseSchema>;
export type AddScopesRequest = z.infer<typeof addScopesRequestSchema>;
export type AddScopesResponse = z.infer<typeof addScopesResponseSchema>;
export type RevokeIntegrationRequest = z.infer<typeof revokeIntegrationRequestSchema>;
export type RevokeIntegrationResponse = z.infer<typeof revokeIntegrationResponseSchema>;
export type TriggerSyncRequest = z.infer<typeof triggerSyncRequestSchema>;
export type TriggerSyncResponse = z.infer<typeof triggerSyncResponseSchema>;
export type AuditResponse = z.infer<typeof auditResponseSchema>;
