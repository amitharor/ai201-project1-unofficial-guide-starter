"""
Milestone 6 — Evaluation harness.

Runs all 5 evaluation questions (from planning.md) through ask() and prints, for each:
the question, expected answer, the system's actual response, which chunks were retrieved
(source + distance), and the cited sources. Accuracy is judged by hand from this output.

Run:  python evaluate.py
"""

from query import ask

EVAL = [
    {
        "q": "Does the UniFi Cloud Gateway Ultra have a built-in Wi-Fi access point?",
        "expected": "No. It is a gateway only (no built-in AP, no PoE, no storage); you add a separate AP.",
    },
    {
        "q": "Why do people recommend putting IoT / smart-home devices on a separate VLAN?",
        "expected": "Security isolation — IoT gear is poorly secured; a separate VLAN + firewall "
                    "rules stop a compromised device from reaching the main LAN.",
    },
    {
        "q": "What PoE standard does a U7 Pro access point need to be powered?",
        "expected": "PoE+ (802.3at). Standard PoE (802.3af) is not enough.",
    },
    {
        "q": "What is suggested when a UniFi AP shows 'Adoption Failed / Offline' after a firmware update?",
        "expected": "Factory-reset the AP and re-adopt it; mesh-mode APs are especially prone to this.",
    },
    {
        "q": "Is the UDM Pro a good choice for a multi-gig (over 1 Gbps) internet connection?",
        "expected": "Its RJ45 WAN port is 1 GbE; multi-gig WAN needs the SFP+ port.",
    },
]


def main():
    for i, item in enumerate(EVAL, 1):
        result = ask(item["q"])
        print("\n" + "=" * 80)
        print(f"Q{i}: {item['q']}")
        print("-" * 80)
        print(f"EXPECTED : {item['expected']}")
        print(f"\nSYSTEM   : {result['answer']}")
        print(f"\nSOURCES  : {', '.join(result['sources']) if result['sources'] else '(none)'}")
        print("\nRETRIEVED CHUNKS (after relevance filter):")
        if not result["chunks"]:
            print("  (none passed the relevance filter)")
        for c in result["chunks"]:
            snippet = " ".join(c["text"].split())[:90]
            print(f"  - {c['distance']:.3f}  {c['source']} (chunk {c['chunk_index']}): {snippet}...")


if __name__ == "__main__":
    main()
