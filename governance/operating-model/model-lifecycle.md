# Model Lifecycle Management
## EuroHealth AI Helpdesk

**Owner:** AI-SE
**KAF Layer:** Layer 4 — Policy-as-Code + Layer 5 — Human-in-the-Loop

---

## 1. Version Control

| Artifact | Versioning Method | Storage |
|---------|------------------|---------|
| LLM model weights | Semantic versioning (v1.0.0) | On-prem model registry |
| System prompts | Git-tracked, tagged releases | Repository |
| Policy YAML files | Git-tracked, tagged releases | Repository |
| Knowledge base | Timestamped snapshots | Vector DB |
| Golden dataset | Versioned JSON files | Repository |

## 2. Retraining Triggers

<!-- AI-SE + AI-DS: When does the model need updating? -->

| Trigger | Detection Method | Owner |
|---------|-----------------|-------|
| Accuracy drops below threshold | Golden dataset evaluation | AI-DS |
| New Confluence content > 10% of KB | Content monitoring | AI-DS |
| Policy rules change significantly | Git diff analysis | AI-SEC |
| Drift detected in response patterns | Statistical monitoring | AI-DA |

## 3. Deployment Pipeline

<!-- AI-SE: How does a new model version get to production? -->

1. New model/prompt version → staging environment
2. Golden dataset evaluation → pass/fail gate
3. Security scan → AI-SEC approval
4. A/B test (if applicable) → metric comparison
5. Blue/green deployment → production
6. Rollback ready for 72 hours

## 4. Rollback Protocol

- Previous model version retained for minimum 30 days
- One-command rollback to previous version
- Automated rollback if error rate > <!-- threshold --> within 1 hour of deployment
