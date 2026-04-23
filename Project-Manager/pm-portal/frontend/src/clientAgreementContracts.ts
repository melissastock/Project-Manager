import { z } from "zod";

export const pricingModelSchema = z.enum(["fixed", "package", "retainer", "mixed"]);
export const agreementStatusSchema = z.enum([
  "draft",
  "under_review",
  "ready_for_signature",
  "active",
  "locked",
  "amended",
]);

export const agreementDeliverableSchema = z.object({
  id: z.string().optional(),
  title: z.string().min(1),
  description: z.string().default(""),
  due_date: z.string().default(""),
  acceptance_criteria: z.string().default(""),
});

export const intakeResponseSchema = z.object({
  client_goals: z.string().default(""),
  success_criteria: z.string().default(""),
  communication_preferences: z.string().default(""),
  primary_contact: z.string().default(""),
  required_assets: z.array(z.string()).default([]),
  constraints: z.string().default(""),
  dependencies: z.string().default(""),
  budget_range_usd: z.string().default(""),
  scope_boundaries: z.string().default(""),
  compliance_requirements: z.string().default(""),
  approval_authority: z.string().default(""),
  risk_assumptions: z.string().default(""),
  completed: z.boolean().default(false),
  completed_at: z.string().nullable().default(null),
});

export const clientAgreementCreateSchema = z.object({
  project: z.string().min(1),
  client_name: z.string().min(1),
  package_name: z.string().default(""),
  product_brief: z.string().default(""),
  scope_definition: z.string().default(""),
  deliverables_summary: z.string().default(""),
  pricing_model: pricingModelSchema.default("fixed"),
  price_terms_json: z.record(z.string(), z.unknown()).default({}),
  owner_role: z.string().default("business_owner"),
  neuro_worker_type: z.string().default("unspecified"),
  intake: intakeResponseSchema,
  deliverables: z.array(agreementDeliverableSchema).default([]),
});

export const clientAgreementUpdateSchema = clientAgreementCreateSchema.partial();

export const agreementMessageCreateSchema = z.object({
  author_name: z.string().min(1),
  author_role: z.string().default("client"),
  message: z.string().min(1),
  visibility: z.enum(["client_and_team", "internal_only"]).default("client_and_team"),
});

export const changeOrderCreateSchema = z.object({
  requested_by: z.string().min(1),
  requested_scope_delta: z.string().min(1),
  requested_price_delta: z.string().default(""),
  requested_timeline_delta: z.string().default(""),
});
