import argparse, csv
from collections import Counter
from datetime import datetime, timedelta

CATS = {"Billing": ["invoice", "refund", "charge", "payment", "billing"],
        "Login": ["password", "login", "locked", "2fa", "sign in"],
        "Bug": ["error", "crash", "bug", "broken", "not working"],
        "Feature": ["feature", "suggestion", "would be nice", "request"]}
URGENT = ["urgent", "asap", "outage", "cannot access", "data loss", "down"]
SLA_HOURS = {"High": 4, "Normal": 24}

def classify(text):
    t = text.lower()
    cat = next((c for c, kws in CATS.items() if any(k in t for k in kws)), "General")
    pri = "High" if any(k in t for k in URGENT) else "Normal"
    return cat, pri

def make_demo(path):
    now = datetime.now()
    rows = [("T-1", 30, "Charged twice", "I was charged twice, need a refund"),
            ("T-2", 2, "Site down", "Whole dashboard is down, urgent!"),
            ("T-3", 20, "Password reset", "I am locked out, password link fails"),
            ("T-4", 50, "Idea", "Feature request: dark mode would be nice"),
            ("T-5", 6, "App crash", "Error on export, app crash every time"),
            ("T-6", 1, "Question", "How do I change my display name?")]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "created", "subject", "body"])
        for i, hrs, s, b in rows:
            w.writerow([i, (now - timedelta(hours=hrs)).isoformat(timespec="seconds"), s, b])

def main():
    p = argparse.ArgumentParser(description="Support ticket triage + SLA check")
    p.add_argument("file", nargs="?", default="tickets.csv")
    p.add_argument("--demo", action="store_true")
    args = p.parse_args()
    if args.demo:
        make_demo(args.file)

    now, tickets = datetime.now(), []
    with open(args.file, newline="") as f:
        for r in csv.DictReader(f):
            cat, pri = classify(r["subject"] + " " + r["body"])
            age = (now - datetime.fromisoformat(r["created"])).total_seconds() / 3600
            tickets.append({"id": r["id"], "subject": r["subject"], "category": cat,
                            "priority": pri, "age_h": round(age, 1),
                            "breached": age > SLA_HOURS[pri]})
    tickets.sort(key=lambda t: (t["priority"] != "High", -t["age_h"]))

    print(f"\n{'ID':<6}{'Pri':<8}{'Category':<10}{'Age(h)':>7}  {'SLA':<8}Subject")
    for t in tickets:
        sla = "BREACHED" if t["breached"] else "ok"
        print(f"{t['id']:<6}{t['priority']:<8}{t['category']:<10}{t['age_h']:>7}  {sla:<8}{t['subject']}")
    print("\nBy category:", dict(Counter(t["category"] for t in tickets)))
    print(f"SLA breaches: {sum(t['breached'] for t in tickets)} of {len(tickets)}\n")

    with open("triaged.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=tickets[0].keys())
        w.writeheader()
        w.writerows(tickets)

if __name__ == "__main__":
    main()