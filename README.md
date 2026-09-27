# KPI Dictionary & Data Quality Contract

## 1. Project Overview & Ownership
- **Dataset Domain:** EdTech & Commercial Operations
- **Business Decision Owner:** VP of Revenue Operations & Commercial Finance
- **Technical Steward:** Lead Analytics Engineer

---
## 2. KPI Dictionary (8 Metrics)

| KPI ID | KPI Name | Business Definition | Formula | Grain | Inclusions & Exclusions | Metric Owner | Refresh Cadence |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **KPI-01** | Gross Merchandise Value (GMV) | Total gross revenue of all orders before markdowns. | `SUM(quantity * unit_price)` | Line item | Exclude duplicate row `RT-1004` | Commercial Finance | Daily (T+1) |
| **KPI-02** | Net Realized Revenue | Total revenue collected from completed orders. | `SUM(quantity * unit_price * (1 - discount_pct/100))` | Line item | Only `payment_status = 'Paid'` | VP Finance | Daily (T+1) |
| **KPI-03** | Average Order Value (AOV) | Net realized revenue per unique paid transaction. | `Net Realized Revenue / COUNT(DISTINCT order_id)` | Order | Filtered to `payment_status = 'Paid'` | Growth Lead | Weekly |
| **KPI-04** | Payment Settlement Rate | Percentage of initiated orders successfully settled. | `(COUNT(DISTINCT Paid orders) / COUNT(DISTINCT order_id)) * 100` | Order Batch | Exclude duplicates | RevOps Lead | Daily |
| **KPI-05** | Discount Intensity Rate | Percentage discount applied against total gross paid sales. | `1 - (SUM(Net Realized Revenue) / SUM(Gross Value of Paid Orders))` | Segment & Category | Filtered to `payment_status = 'Paid'` | Commercial Director | Weekly |
| **KPI-06** | Refund Ratio | Share of customer transaction value reversed via refunds. | `SUM(Refunded Value) / SUM(Paid + Refunded Value) * 100` | Product Category | Filtered to `Paid` and `Refunded` | Support Lead | Weekly |
| **KPI-07** | Segment Revenue Share | Distribution of net revenue across persona segments. | `(Segment Net Revenue / Total Net Revenue) * 100` | Segment | Filtered to `payment_status = 'Paid'` | Marketing Lead | Monthly |
| **KPI-08** | Pipeline Leakage Rate | Share of gross potential order volume trapped in pending/failed states. | `SUM(Pending + Failed Value) / Total GMV * 100` | Pipeline Batch | Exclude duplicates | RevOps Lead | Daily |

---

## 3. Data Quality Contract

| Quality Dimension | Rule & Field | Target Threshold | Severity | Automated Action |
| :--- | :--- | :--- | :--- | :--- |
| **Uniqueness** | Primary Key on `order_id` | 0 duplicates | P1 (Critical) | Pipeline halts; deduplicate prior to downstream aggregation. |
| **Completeness** | Mandatory values in `order_id`, `order_date`, `city`, `customer_segment` | Null rate = 0.0% | P1 (Critical) | Quarantine invalid records to `quarantine_retail_orders`. |
| **Validity** | `quantity` must be integer > 0; `discount_pct` in [0, 100] | 100% conforming | P2 (High) | Route failed rows to dead-letter queue (DLQ). |
| **Validity** | `order_date` ISO `YYYY-MM-DD` format between `2025-01-01` and present | 100% conforming | P2 (High) | Apply regex date-parser fallback; flag unparseable rows. |
| **Consistency** | Case normalization for `customer_segment` and `payment_status` | 100% post-transform | P3 (Medium) | Automatic normalization mapping layer in ELT pipeline. |

---

## 4. Profiling Findings (`retail-orders-raw.csv`)
1. **Uniqueness:** Row `RT-1004` is duplicated.
2. **Completeness:** `order_date` missing in `RT-1011`, `city` missing in `RT-1005`, and `discount_pct` missing in `RT-1003`.
3. **Validity:** Invalid month index in `RT-1006` (`2026-13-10`), string value `'two'` in `RT-1008`, negative quantity `-1` in `RT-1006`, and discount `105.0%` in `RT-1007`.
4. **Consistency:** Lowercase casing issues in `RT-1003` (`student`) and `RT-1002` (`paid`).
