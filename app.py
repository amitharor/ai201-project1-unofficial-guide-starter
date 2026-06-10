"""
Milestone 5 — Gradio query interface for the Unofficial UniFi Guide.

Run:  python app.py   then open http://localhost:7860
"""

import gradio as gr

from query import ask

EXAMPLES = [
    "Does the UniFi Cloud Gateway Ultra have a built-in Wi-Fi access point?",
    "Why should I put IoT devices on a separate VLAN?",
    "Can I run the UniFi Network controller in Docker?",
    "How much PoE power do UniFi access points need?",
]


def handle_query(question):
    if not question or not question.strip():
        return "Please enter a question.", ""
    result = ask(question)
    if result["sources"]:
        sources = "\n".join(f"• {s}" for s in result["sources"])
    else:
        sources = "(no relevant sources — answer not grounded in the documents)"
    return result["answer"], sources


with gr.Blocks(title="The Unofficial UniFi Guide") as demo:
    gr.Markdown(
        "# The Unofficial UniFi Guide\n"
        "Ask about UniFi home networking. Answers come **only** from collected community "
        "forum threads and blog guides, with the source documents shown."
    )
    inp = gr.Textbox(label="Your question", placeholder="e.g. What PoE standard does a U7 Pro need?")
    btn = gr.Button("Ask", variant="primary")
    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved from", lines=4)

    gr.Examples(examples=EXAMPLES, inputs=inp)

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])


if __name__ == "__main__":
    demo.launch()
