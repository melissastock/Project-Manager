-- Google OAuth integration tables for PM Portal.
-- Security posture:
-- - refresh tokens are stored encrypted
-- - scopes are explicit and auditable
-- - sync cursors support incremental reads with low data duplication

CREATE TYPE "IntegrationProvider" AS ENUM ('GOOGLE');
CREATE TYPE "IntegrationStatus" AS ENUM ('ACTIVE', 'REAUTH_REQUIRED', 'REVOKED', 'DISABLED');
CREATE TYPE "DataClass" AS ENUM ('PUBLIC', 'INTERNAL', 'CONFIDENTIAL', 'REGULATED');
CREATE TYPE "AuditAction" AS ENUM (
  'CONNECT_INITIATED',
  'CONNECT_COMPLETED',
  'SCOPES_UPDATED',
  'TOKEN_REFRESHED',
  'TOKEN_REFRESH_FAILED',
  'SYNC_STARTED',
  'SYNC_COMPLETED',
  'SYNC_FAILED',
  'RECORD_ACCESSED',
  'REVOKED',
  'PURGED'
);

CREATE TABLE "integration_connections" (
  "id" TEXT NOT NULL,
  "workspace_id" TEXT NOT NULL,
  "owner_user_id" TEXT NOT NULL,
  "provider" "IntegrationProvider" NOT NULL,
  "provider_account_id" TEXT NOT NULL,
  "email" TEXT,
  "status" "IntegrationStatus" NOT NULL DEFAULT 'ACTIVE',
  "scopes" TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
  "needs_manual_override" BOOLEAN NOT NULL DEFAULT false,
  "created_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "last_synced_at" TIMESTAMPTZ(6),
  CONSTRAINT "integration_connections_pkey" PRIMARY KEY ("id")
);

CREATE UNIQUE INDEX "integration_connections_workspace_provider_account_key"
ON "integration_connections" ("workspace_id", "provider", "provider_account_id");
CREATE INDEX "integration_connections_workspace_provider_status_idx"
ON "integration_connections" ("workspace_id", "provider", "status");

CREATE TABLE "oauth_credentials" (
  "id" TEXT NOT NULL,
  "integration_connection_id" TEXT NOT NULL,
  "encrypted_refresh_token" TEXT NOT NULL,
  "token_version" INTEGER NOT NULL DEFAULT 1,
  "access_token_expires_at" TIMESTAMPTZ(6),
  "refresh_token_issued_at" TIMESTAMPTZ(6),
  "last_refresh_at" TIMESTAMPTZ(6),
  "refresh_failure_count" INTEGER NOT NULL DEFAULT 0,
  "created_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "oauth_credentials_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "oauth_credentials_integration_connection_id_key" UNIQUE ("integration_connection_id")
);

CREATE TABLE "sync_cursors" (
  "id" TEXT NOT NULL,
  "integration_connection_id" TEXT NOT NULL,
  "resource_type" TEXT NOT NULL,
  "cursor" TEXT,
  "last_successful_sync_at" TIMESTAMPTZ(6),
  "last_attempted_sync_at" TIMESTAMPTZ(6),
  "last_error" TEXT,
  "created_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "sync_cursors_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "sync_cursors_integration_resource_type_key"
    UNIQUE ("integration_connection_id", "resource_type")
);

CREATE TABLE "integration_audit_events" (
  "id" TEXT NOT NULL,
  "integration_connection_id" TEXT NOT NULL,
  "actor_user_id" TEXT,
  "action" "AuditAction" NOT NULL,
  "scope_delta" JSONB,
  "resource_type" TEXT,
  "resource_id" TEXT,
  "metadata" JSONB,
  "data_class" "DataClass" NOT NULL DEFAULT 'INTERNAL',
  "created_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "integration_audit_events_pkey" PRIMARY KEY ("id")
);

CREATE INDEX "integration_audit_events_connection_created_idx"
ON "integration_audit_events" ("integration_connection_id", "created_at");
CREATE INDEX "integration_audit_events_action_created_idx"
ON "integration_audit_events" ("action", "created_at");

CREATE TABLE "data_classification_policies" (
  "id" TEXT NOT NULL,
  "workspace_id" TEXT NOT NULL,
  "gmail_default_class" "DataClass" NOT NULL DEFAULT 'CONFIDENTIAL',
  "calendar_default_class" "DataClass" NOT NULL DEFAULT 'INTERNAL',
  "store_message_body_by_default" BOOLEAN NOT NULL DEFAULT false,
  "store_attachments_by_default" BOOLEAN NOT NULL DEFAULT false,
  "retention_days_internal" INTEGER NOT NULL DEFAULT 365,
  "retention_days_confidential" INTEGER NOT NULL DEFAULT 180,
  "retention_days_regulated" INTEGER NOT NULL DEFAULT 90,
  "created_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMPTZ(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT "data_classification_policies_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "data_classification_policies_workspace_id_key" UNIQUE ("workspace_id")
);

ALTER TABLE "oauth_credentials"
ADD CONSTRAINT "oauth_credentials_integration_connection_id_fkey"
FOREIGN KEY ("integration_connection_id") REFERENCES "integration_connections"("id")
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "sync_cursors"
ADD CONSTRAINT "sync_cursors_integration_connection_id_fkey"
FOREIGN KEY ("integration_connection_id") REFERENCES "integration_connections"("id")
ON DELETE CASCADE ON UPDATE CASCADE;

ALTER TABLE "integration_audit_events"
ADD CONSTRAINT "integration_audit_events_integration_connection_id_fkey"
FOREIGN KEY ("integration_connection_id") REFERENCES "integration_connections"("id")
ON DELETE CASCADE ON UPDATE CASCADE;
