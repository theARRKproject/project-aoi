# Project status and evidence

This page separates **the past Aoi development work** from **the reconstructed showcase code** in this repository.

## Earlier development (based on project notes)

| Area | State in original experiments | Detail |
| --- | --- | --- |
| Personality planning | Prototyped | Designed Aoi's character behavior and conversation examples |
| Local language model | Prototyped | Experimented with Qwen2.5-3B, PyTorch and Transformers |
| Prompting | Prototyped | Tried chat templates and persona injection |
| SQLite chat history | Prototyped | Conversation IDs, timestamps and recent-message loading |
| Semantic memory retrieval | Early prototype | Tested SentenceTransformer embeddings and relevance scores |
| Reliable generation | Unresolved | Hit empty replies and generation issues |
| End-to-end memory behavior | Unresolved | Still needed testing and quality improvements |
| Ubuntu deployment | Planned | Not a completed deployment |
| Voice, vision and avatar | Ideas | Not part of the prototype |

## What this repository contains

**Reconstructed showcase code:** The exact historical `.py` files were not available when this repository was assembled. The included modules are a new, readable reference implementation of the same concepts, not a byte-for-byte copy of the user's earlier source code.

**Locally testable parts:** Database persistence, turn ordering, manual memory addition, keyword-based search, and a deterministic demonstration have unit tests.

**Optional, environment-dependent parts:** Qwen inference and SentenceTransformer ranking are implemented as integrations, but they need downloaded models and compatible hardware. Their runtime quality and resource use have not been verified by the small offline unit test suite.

**Not finished:** Automatic long-term learning, memory conflict handling, strong privacy/security controls, stable multi-platform deployment, rich UI, audio, vision and character animation.

## Honest demo language

> "Aoi is an in-progress local AI assistant project. I prototyped a local language model, personalisation through system prompts, conversation logging in SQLite, and relevant-memory retrieval. This repository reconstructs and documents the architecture and includes a tested storage demo. A reliable full assistant remains in development."
