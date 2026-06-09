# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My domain is the Unofficial UniFi Home Networking and Troubleshooting Guide. It will help in purchasing the right Ubiquiti gear, configuring it (VLANs, PoE, etc.), and fixing it when the firmware updates break things.

Ubiquiti's unofficial docs tell what a device is, but not which model actually fits a real home, which firmware versions are stable for most people, or how to segment IoT devices safely. We can find this knowledge from forum threads and reddit from people who have encountered these problems.

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source                | Description                                                     | URL or location                                                                                                                                                             |
| --- | --------------------- | --------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Unifi forum           | Should I skip the U6 and purchase a U7                          | https://community.ui.com/questions/Should-I-skip-the-U6-and-purchase-a-U7/c1dda185-c2a0-447b-b3e3-215344d44b2c                                                              |
| 2   | Unifi forum           | Dream Router vs Cloud Gateway Ultra and U6+                     | https://community.ui.com/questions/Dream-Router-vs-Cloud-Gateway-Ultra-and-U6/0914f6b2-05e8-4e1f-8eef-5583683fed3b                                                          |
| 3   | Unifi forum           | UDM Pro vs. Cloud Gateway Ultra                                 | https://community.ui.com/questions/UDM-Pro-vs-Cloud-Gateway-Ultra/a590a25b-c3b9-498b-b399-8cf7669404af                                                                      |
| 4   | Unifi forum           | Cloud Gateway Ultra vs Dream Machine vs Gateway Max             | https://community.ui.com/questions/Cloud-Gateway-Ultra-vs-Dream-Machine-vs-Gateway-Max/931df9fa-560d-49e0-aba0-af21c75e09ed                                                 |
| 5   | Unifi forum           | Creating a separate IOT network - looking for best practice     | https://community.ui.com/questions/Creating-a-separate-IOT-network-looking-for-best-practice/137ef556-e12b-4270-88e0-a5b01bab9b3f                                           |
| 6   | Unifi forum           | Attempting to make THE UniFi IoT VLAN Walk-through              | https://community.ui.com/questions/Attempting-to-make-THE-UniFi-IoT-VLAN-Walk-through/d7658f5c-e1ba-4a07-8fed-1fea240bd2fd                                                  |
| 7   | Lazy Admin            | How to Setup and Secure UniFi VLAN                              | https://lazyadmin.nl/home-network/unifi-vlan-configuration/                                                                                                                 |
| 8   | The Smart Home Hookup | Setting Up VLANs and Firewall Rules                             | https://www.thesmarthomehookup.com/unifi-setup-from-scratch-setting-up-vlans-and-firewall-rules/                                                                            |
| 9   | Unifi forum           | How much power from POE do my Access Points really need?        | https://community.ui.com/questions/How-much-power-from-POE-do-my-Access-Points-really-need/71927a12-661e-41fc-b859-32f37984cd77                                             |
| 10  | Unifi forum           | U7 Pro Power and POE/POE+ switch port                           | https://community.ui.com/questions/U7-Pro-Power-and-POE-POE-switch-port/38bb1b43-db32-4e1e-9321-539ff12bc093                                                                |
| 11  | Unifi forum           | Firmware update to 6.2.49 bricked my UAP-AC-Pro AP in mesh mode | https://community.ui.com/questions/Firmware-update-to-6-2-49-bricked-my-UAP-AC-Pro-AP-in-mesh-mode-now-says-Offline-or-Adoption-Failed/6617e272-4f4d-4e02-9fc7-4a0b301679f4 |
| 12  | Unifi forum           | UniFi AP-AC-IW bricked during update                            | https://community.ui.com/questions/UniFi-AP-AC-IW-bricked-during-update/6f7e930d-006e-4649-933d-86e6f0e268ea                                                                |
| 13  | Unifi forum           | Unifi Network Controller installation with docker               | https://community.ui.com/questions/Unifi-Network-Controller-installation-with-docker/920311f0-c4fe-453f-bda3-e7e39160e5b0                                                   |
| 14  | Pi My Life Up         | Setting up the UniFi Network Controller using Docker            | https://pimylifeup.com/unifi-docker/                                                                                                                                        |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question | Expected answer |
| --- | -------- | --------------- |
| 1   |          |                 |
| 2   |          |                 |
| 3   |          |                 |
| 4   |          |                 |
| 5   |          |                 |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
