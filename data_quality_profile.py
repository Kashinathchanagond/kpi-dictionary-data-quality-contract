import pandas as pd
import numpy as np

raw_df = pd.read_csv('retail-orders-raw (2).csv')
print(f"Total records loaded: {len(raw_df)}\n" + "="*50)

# Uniqueness Check
dup_count = raw_df.duplicated(subset=['order_id']).sum()
print(f"[UNIQUENESS] Duplicate 'order_id' count: {dup_count}")

# Completeness Check
null_summary = raw_df.isnull().sum()
print("\n[COMPLETENESS] Null Values per Column:")
print(null_summary[null_summary > 0])

# Validity & Consistency Check
valid_segments = ['Student', 'Fresher', 'Professional']
valid_statuses = ['Paid', 'Pending', 'Failed', 'Refunded']

casing_segment = raw_df[~raw_df['customer_segment'].isin(valid_segments) & raw_df['customer_segment'].notnull()]
casing_status = raw_df[~raw_df['payment_status'].isin(valid_statuses) & raw_df['payment_status'].notnull()]

print(f"\n[CONSISTENCY] Segment Issues: {len(casing_segment)}")
print(f"[CONSISTENCY] Status Issues: {len(casing_status)}")
