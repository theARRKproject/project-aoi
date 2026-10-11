# Development notes

## Phase 1: Personal identity and behavior

The aim was to create Aoi as a consistent character rather than a general question-answering bot. Earlier experiments gathered dialogue references and designed a personality and response style. This public repository uses a generic placeholder persona to avoid publishing private reference conversations.

## Phase 2: Model experiments

The prototype experimented with Python, PyTorch and Qwen2.5-3B. Work included tokenisers, chat templates, local model loading, and decoding generated messages. Debugging focused on missing responses, model inputs and output token handling.

## Phase 3: Persistent conversations

A SQLite design was introduced to store role-tagged messages with timestamps and conversation IDs. Recent messages could then be reused in later prompts. This repository shows that approach with a small, testable schema.

## Phase 4: Long-term note retrieval

The next experiment involved saving memories, using sentence embeddings, scoring relevance to a new question, and injecting matching notes into the prompt. The earlier design explored a relevance threshold around `0.30`. The reconstructed implementation includes an optional embedding retriever and a dependency-free keyword mode.

## Problems worked through

- Inconsistent or empty AI generations.
- Token or tensor shape mismatches.
- Errors in SQLite setup and column/table use.
- Correctly ordering conversation history and ranked memory results.
- Separating prompt instructions from facts in retrieved notes.

## Next development milestone

Connect the real model to the memory store and run repeatable conversational tests. Test recall, corrections, made-up memories, and whether the assistant retains its intended personality. Then optimise for target hardware and consider Ubuntu server deployment.
