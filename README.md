# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

My domain is the **Unofficial** UniFi Home Networking and Troubleshooting Guide. It helps with

purchasing the right Ubiquiti gear, configuring it (VLANs, PoE, and so on), and fixing it when
firmware updates break things.

Ubiquiti's **official** docs tell you what a device is, but not which model actually fits a real
home, which firmware versions are stable for most people, or how to segment IoT devices safely. We
can find this knowledge from forum threads and Reddit posts written by people who have already hit
these problems.

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #   | Source                | Type         | URL or file path                                                                                                                                                            |
| --- | --------------------- | ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | UniFi Community forum | Forum thread | https://community.ui.com/questions/Should-I-skip-the-U6-and-purchase-a-U7/c1dda185-c2a0-447b-b3e3-215344d44b2c                                                              |
| 2   | UniFi Community forum | Forum thread | https://community.ui.com/questions/Dream-Router-vs-Cloud-Gateway-Ultra-and-U6/0914f6b2-05e8-4e1f-8eef-5583683fed3b                                                          |
| 3   | UniFi Community forum | Forum thread | https://community.ui.com/questions/UDM-Pro-vs-Cloud-Gateway-Ultra/a590a25b-c3b9-498b-b399-8cf7669404af                                                                      |
| 4   | UniFi Community forum | Forum thread | https://community.ui.com/questions/Cloud-Gateway-Ultra-vs-Dream-Machine-vs-Gateway-Max/931df9fa-560d-49e0-aba0-af21c75e09ed                                                 |
| 5   | UniFi Community forum | Forum thread | https://community.ui.com/questions/Creating-a-separate-IOT-network-looking-for-best-practice/137ef556-e12b-4270-88e0-a5b01bab9b3f                                           |
| 6   | UniFi Community forum | Forum thread | https://community.ui.com/questions/Attempting-to-make-THE-UniFi-IoT-VLAN-Walk-through/d7658f5c-e1ba-4a07-8fed-1fea240bd2fd                                                  |
| 7   | LazyAdmin             | Blog guide   | https://lazyadmin.nl/home-network/unifi-vlan-configuration/                                                                                                                 |
| 8   | The Smart Home Hookup | Blog guide   | https://www.thesmarthomehookup.com/unifi-setup-from-scratch-setting-up-vlans-and-firewall-rules/                                                                            |
| 9   | UniFi Community forum | Forum thread | https://community.ui.com/questions/How-much-power-from-POE-do-my-Access-Points-really-need/71927a12-661e-41fc-b859-32f37984cd77                                             |
| 10  | UniFi Community forum | Forum thread | https://community.ui.com/questions/U7-Pro-Power-and-POE-POE-switch-port/38bb1b43-db32-4e1e-9321-539ff12bc093                                                                |
| 11  | UniFi Community forum | Forum thread | https://community.ui.com/questions/Firmware-update-to-6-2-49-bricked-my-UAP-AC-Pro-AP-in-mesh-mode-now-says-Offline-or-Adoption-Failed/6617e272-4f4d-4e02-9fc7-4a0b301679f4 |
| 12  | UniFi Community forum | Forum thread | https://community.ui.com/questions/UniFi-AP-AC-IW-bricked-during-update/6f7e930d-006e-4649-933d-86e6f0e268ea                                                                |
| 13  | UniFi Community forum | Forum thread | https://community.ui.com/questions/Unifi-Network-Controller-installation-with-docker/920311f0-c4fe-453f-bda3-e7e39160e5b0                                                   |
| 14  | Pi My Life Up         | Blog guide   | https://pimylifeup.com/unifi-docker/                                                                                                                                        |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
about 800 characters (roughly 180 to 200 tokens)

**Overlap:**
about 150 characters (roughly 35 tokens, about 18 percent)

**Why these choices fit your documents:**
The binding constraint is the embedding model, not a guess. `all-MiniLM-L6-v2` has a maximum
sequence length of **256 word pieces and silently truncates anything longer**, so embedding a 600
word forum post as one chunk would throw away everything after roughly the first 200 words. Capping
chunks at about 800 characters keeps every chunk fully inside what the model actually reads, with
margin. The corpus is also mixed. It is part short forum replies (1 to 4 sentences, already a
complete thought) and part long blog guides (many paragraphs), so splitting on paragraph and
sentence boundaries keeps a short reply intact as one chunk while breaking a long guide into topic
coherent pieces. The overlap of about 18 percent protects facts that straddle a boundary, such as
_"The U7 Pro needs…"_ followed by _"…PoE+, not standard 802.3af."_ Smaller chunks of about 200
characters lose their subject, and larger ones of about 1500 characters exceed the token limit and
dilute the embedding.

**Final chunk count:**
**181 chunks** across 14 documents (sizes 187 to 912 characters, max about
228 tokens, under the 256 token limit, which confirms the design held).

### Sample chunks (5, each labeled with source)

**1. `blog_vlan_smarthomehookup.txt` (chunk 2)**

> "…you can think of each VLAN as a completely separate network with a different router, a different
> switch, and different access points. By default, one VLAN can't access another VLAN any more than
> you can access your neighbor's home network from your own. The advantage of a VLAN is… the
> separation happens via software… we can easily set up different firewall rules…"

**2. `forum_gateway_udr-vs-ucg-ultra.txt` (chunk 1)**

> "…[the Dream Router] has the built in AP. The Ultra can only run Network. If adding cameras is in
> your plans, the UDR is the better choice. The Ultra has better hardware specs and both have 4 port
> switches… It will also handle your Gbe connection a little better because of the 2.5 Gb WAN port."

**3. `forum_poe_u7pro-switch-port.txt` (chunk 11)**

> "…performance, please connect the access point to a PoE+ compliant port.' My ports can deliver the
> power it requires, but I still see this message. … I have a Ubiquiti branded PoE+ injector
> connected to a UAP-AC-IW as this device requires PoE+ for proper passthrough…"

**4. `blog_vlan_lazyadmin.txt` (chunk 0)**

> "How to Setup and Secure UniFi VLAN. When you have a UniFi Security Gateway or UniFi Dream Machine
> (UDM, UDM Pro) you can create different VLANs on your network. Virtual LANs (VLANs) allow you to
> divide your physical network into virtual networks, offering isolation, security, and scalability…"

**5. `forum_ap_u6-vs-u7.txt` (chunk 7)**

> "…U6 and U7 equipment can coexist with older APs… The big concern with U7 (and U6-Enterprise) is
> the fact that new 6 GHz APs need 2.5 GbE PoE+ connections to reach their full potential. Without
> upgrading your wired Ethernet infrastructure, they are just expensive wall decorations."

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
`all-MiniLM-L6-v2` via `sentence-transformers`. It runs locally with no API key, no
rate limits, and no cost, it is fast on CPU, and it outputs compact 384 dimensional vectors that
ChromaDB handles easily, which is ideal for a small local corpus.

**Production tradeoff reflection:**
If I were deploying this for real users and cost were not a constraint, the factor that matters most
is context length. MiniLM caps out at 256 tokens, which is the real ceiling I designed my chunking
around, so a model with a longer window such as `text-embedding-3-large`, Voyage, or Cohere could
embed a whole post or guide section as one vector and remove the truncation problem. Domain accuracy
is nearly as important, because my text is dense with jargon like the model names U6, U7, and UDM
Pro, plus terms such as 802.3at, VLAN, and mDNS, so a larger or domain tuned model would represent
"U7 Pro" and "U6" as more distinct vectors and reduce the version confusion failure I expect. I
would also weigh latency and the choice between local and hosted models, because MiniLM is instant
locally with no rate limits or cost per query, whereas an API model adds latency and a cost on every
query but scales and offloads compute. Multilingual support does not matter now since my corpus is
only English, but I would switch to a model like `multilingual-e5` or `BGE-M3` if I ever added
forums in other languages. Finally, dimensionality drives storage and speed, since 384 dimensions
are cheap to store and fast to search, while models that output 1536 or 3072 dimensions improve
quality but use more memory and slow the search as the corpus grows.

### Retrieval tests (3 queries + explanation for 2)

| Query                                              | Top result (source, distance)                        | Relevant?                    |
| -------------------------------------------------- | ---------------------------------------------------- | ---------------------------- |
| "Why put IoT devices on a separate VLAN?"          | `blog_vlan_smarthomehookup.txt` chunk 2, **0.252**   | Yes                          |
| "What PoE standard does a U7 Pro need?"            | `forum_poe_ap-power-needs.txt` chunk 0, **0.347**    | On topic, but not the answer |
| "Does the Cloud Gateway Ultra have a built in AP?" | `forum_gateway_udmpro-vs-ucg.txt` chunk 0, **0.501** | Borderline                   |

**Why the IoT VLAN results are relevant:** the top chunk explains VLANs as fully separate networks,
and the next one (`lazyadmin`) explicitly ties separate VLANs to IoT security. That is a direct, low
distance (0.25) semantic match even though the query shares few exact words with the documents.

**Why the Cloud Gateway results are borderline:** distances cluster at 0.50 to 0.54 because the
gateway threads are dense with similar model names (UCG, UDM, UDR, UXG). The answer is in the top 5,
but it is stated comparatively ("the Ultra can only run Network… the UDR has the built in AP"), so
the match is weaker. This is an empirical example of the version confusion risk named in planning.md.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
he model is told to (1) answer using **only** the provided
context and never use outside knowledge, (2) reply with the exact phrase _"I don't have enough
information on that."_ when the context is insufficient, (3) never invent model names, specs,
numbers, or steps, and (4) be concise. A **relevance filter** also drops any retrieved chunk with
cosine distance at or above 0.75 before generation, so an off topic query reaches the model with no
context and is refused, often without an API call at all.

**How source attribution is surfaced in the response:**
Sources are collected **programmatically**
from the retrieved chunks' metadata (the source filename stored at indexing time), not generated by
the LLM, so citations cannot be hallucinated. A refusal correctly returns no sources.

### Example responses (2 grounded and cited, 1 out of scope)

**Grounded 1.** _Q: "Why should I put IoT devices on a separate VLAN?"_

> A: "…because the security of these devices is not always as it should be… If an IoT device is
> compromised, it could allow a hacker to access the rest of the network. By isolating IoT devices on
> a separate VLAN, you can limit the potential damage…"
> **Sources:** blog_vlan_smarthomehookup.txt, blog_vlan_lazyadmin.txt, forum_vlan_iot-best-practice.txt

**Grounded 2.** _Q: "Does the UniFi Cloud Gateway Ultra have a built in Wi-Fi access point?"_

> A: "No, the UniFi Cloud Gateway Ultra does not have a built in Wi-Fi access point… which contrasts
> it with the Dream Router that has a built in AP."
> **Sources:** forum_gateway_udmpro-vs-ucg.txt, forum_gateway_ucg-vs-udm-vs-max.txt, forum_gateway_udr-vs-ucg-ultra.txt

**Out of scope.** _Q: "How do I bake sourdough bread?"_

> A: "I don't have enough information on that." **Sources:** (none)

---

## Query Interface

**Tool:** Gradio (`app.py`). Run `python app.py`, then open http://localhost:7860.

**Input field:** a single "Your question" textbox, plus clickable example questions.

**Output fields:** "Answer" (the grounded response) and "Retrieved from" (the list of source
documents the answer drew from).

**Sample interaction transcript:**

```
Your question:  Can I run the UniFi Network controller in Docker?
Answer:         Yes, you can run the UniFi Network Controller in a Docker container. This
                method simplifies setup and allows for easy updates.
Retrieved from: • blog_controller_pimylifeup.txt
```

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question                                                                      | Expected answer                                  | System response (summarized)                                                        | Retrieval quality                                 | Response accuracy      |
| --- | ----------------------------------------------------------------------------- | ------------------------------------------------ | ----------------------------------------------------------------------------------- | ------------------------------------------------- | ---------------------- |
| 1   | Does the Cloud Gateway Ultra have a built in Wi-Fi AP?                        | No, gateway only, no built in AP                 | "No… contrasts with the Dream Router, which has one." (plus sources)                | Partially relevant (borderline, 0.50)             | **Accurate**           |
| 2   | Why put IoT devices on a separate VLAN?                                       | Security isolation, contain a compromised device | Correct and thorough, a compromised IoT device can't reach the main LAN             | Relevant (0.25)                                   | **Accurate**           |
| 3   | What PoE standard does a U7 Pro need?                                         | PoE+ (802.3at)                                   | "I don't have enough information on that."                                          | Off target (answer chunk ranked 8th, outside k=5) | **Inaccurate**         |
| 4   | What is suggested when an AP shows "Adoption Failed" after a firmware update? | Factory reset and re-adopt                       | Muddled, mentions rogue apps, firmware regression, and "resetting may be necessary" | Partially relevant                                | **Partially accurate** |
| 5   | Is the UDM Pro good for multi gig (over 1 Gbps) internet?                     | RJ45 WAN is 1 GbE, needs SFP+ for multi gig      | "I don't have enough information on that."                                          | Off target (fact not in corpus)                   | **Inaccurate**         |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Q3, "What PoE standard does a U7 Pro access point need to be powered?"

**What the system returned:**
"I don't have enough information on that." (a refusal, no sources)

**Root cause (tied to a specific pipeline stage):**
A **retrieval top k miss**. The answer is in the
corpus. `forum_poe_u7pro-switch-port.txt` chunk 11 says _"please connect the access point to a PoE+
compliant port… this device requires PoE+."_ But at k=5 that chunk ranks **8th**, just outside the
retrieval window. The top 5 results are all about PoE wattage (5 to 8W draw), which match the query
vocabulary ("PoE… power… U7") more densely than the chunk stating the actual standard. So the
grounded model never received the answer and correctly refused rather than guessing.

**What you would change to fix it:**
Raise k, or better, add a keyword and BM25 **hybrid search**.
"PoE+" is an exact keyword that lexical search would catch even when semantic ranking buries it.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
Anchoring chunk size on the verified 256 token
MiniLM limit in planning.md gave me a concrete, defensible number instead of a guess. When I built
and ran the pipeline, the largest chunk came out at about 228 tokens, under the limit and exactly as
the spec intended, so the design held without rework.

**One way your implementation diverged from the spec, and why:**
The spec named LangChain's
`RecursiveCharacterTextSplitter`, but I implemented an equivalent custom recursive splitter (same
separator hierarchy plus overlap merge) to avoid adding LangChain as a dependency and to keep the
splitting logic transparent and easy to debug.

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- _What I gave the AI:_
  my planning.md Documents and Chunking Strategy sections, and asked it to build
  the ingestion pipeline (`load_documents`, `clean_text`, `chunk_text`).

- _What it produced:_
  a working pipeline, but the first run leaked a blog byline and an affiliate ad
  into a chunk.

- _What I changed or overrode:_
  I caught the leaked ad on inspection and directed a second cleaning
  pass to strip it, then deliberately left the residual "Copy" and category tag noise after deciding
  that an aggressive filter would also eat real content.

**Instance 2**

- _What I gave the AI:_
  the failing U7 PoE query, and asked it to diagnose why the system refused.

- _What it produced:_
  a diagnosis showing the answer chunk ranked 8th (outside k=5), and the option to
  raise k to 8 to fix it.
- _What I changed or overrode:_
  I overrode the k=8 fix and chose to keep k=5, documenting the
  retrieval miss as my failure case, since raising k to mask one gap would add noise to every query
  and defeat the evaluation's purpose.
