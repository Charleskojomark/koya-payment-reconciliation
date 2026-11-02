#!/usr/bin/env python3
"""Payment reconciliation.

Reads payments.jsonl and works out how much money we actually collected.
Run:  python3 reconcile.py
"""
import json

latest_transactions = {}
total = 0.0
count = 0

with open("payments.jsonl") as f:
    for line in f:
        try:
            event = json.loads(line)
        except Exception:
            continue
        txn_id = event.get("txn_id")
        if not txn_id:
            continue
        ts = event.get("ts")
        if txn_id not in latest_transactions or ts > latest_transactions[txn_id].get("ts", ""):
            latest_transactions[txn_id] = event

for event in latest_transactions.values():
    if event.get("status") == "success":
        count += 1
        amount = event.get("amount", 0)
        if isinstance(amount, str):
            amount = float(amount.replace(",", ""))
        else:
            amount = float(amount)
        total += amount

with open("expected.txt") as f:
    expected = int(f.read().strip())

if count != expected:
    print(f"Check failed: counted {count} successful payments, expected {expected}.")
    print("Something in the data isn't being handled the way the README describes.")
else:
    print(f"Check passed: {count} successful payments.")
    print(f"Your code: KOYA-{round(total)}")
