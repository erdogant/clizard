Algorithm – Technical Workflow of the CLI Tool
================================================

The algorithm page outlines the logical flow that a typical command‑line interface (CLI) tool follows when it processes user input, prepares data, stores embeddings, retrieves relevant information, and finally generates an answer.  The design is intentionally modular: each stage can be swapped out for a different implementation without affecting the others.  Below we describe every step in depth, illustrate how the key functions are used, and provide a concise ASCII diagram that visualises the overall data path.

Data Ingestion
--------------

Collecting raw input from the user or external sources is the first operation performed by any CLI tool.  The *auto_cli* decorator centralises this responsibility by wrapping the main function of the application.  When the program starts, it automatically invokes *parse_args*, ensuring that all command‑line arguments are parsed into a single :class:`argparse.Namespace` object.  This design eliminates boilerplate code in every script and guarantees that downstream components receive a consistent data structure.

The decorator also accepts a pre‑configured parser instance, allowing developers to declare options once and reuse them across multiple commands.  Because the parsing occurs before any business logic runs, it is possible to validate arguments early, provide helpful error messages, or even load configuration files from a *config_path* parameter that persists user sessions.

The following table documents the parameters accepted by both *auto_cli* and *parse_args*.  It shows their types, default values, and why each exists in the workflow.

.. list-table:: Parameters for auto_cli and parse_args
   :widths: 20 30 50
   :header-rows: 1

   * - Name
     - Type
     - Description
   * - parser
     - argparse.ArgumentParser
     - Pre‑configured parser instance used to parse command line arguments.
   * - args
     - argparse.Namespace
     - Optional pre‑parsed arguments; if omitted, parser.parse_args() is executed.

The following code snippet demonstrates how the decorator is applied and how the wrapped function receives parsed arguments:

.. code-block:: python

    from my_cli import auto_cli, parse_args

    def my_main_function(args):
        # args is an argparse.Namespace with all CLI options
        print(f"User supplied: {args}")

    cli = auto_cli(parser=my_parser)(my_main_function)
    cli.run()

Chunking
--------

Large documents or data streams can overwhelm memory and reduce the quality of downstream embeddings.  Chunking addresses this by dividing input into smaller, manageable pieces.  The algorithm typically uses token limits (e.g., 512 tokens) or semantic boundaries such as paragraph breaks to decide split points.  By normalising the size of each chunk, the embedding model can process them consistently and efficiently.

The following example shows how a long text might be split:

.. code-block:: python

    # Example: split a long text into 512‑token chunks
    chunks = chunk_text(long_document, max_tokens=512)

Embedding
---------

Once data is partitioned, each chunk is transformed into a high‑dimensional vector.  This step uses an embedding model—either a local transformer or a cloud service—to capture semantic meaning in numerical form.  The resulting vectors are stored alongside the original text so that similarity search can later retrieve the most relevant chunks for a given query.

The code below demonstrates generating embeddings for a list of chunks:

.. code-block:: python

    # Example: embed a list of text chunks
    embeds = [model.embed(chunk) for chunk in chunks]

Storage
-------

Embeddings, together with metadata such as identifiers or source locations, are persisted to a vector store.  The storage backend is abstracted away from the rest of the pipeline; common choices include FAISS for local search, Pinecone for managed services, or simple in‑memory dictionaries during prototyping.  Persisting embeddings enables fast retrieval without re‑computing them on every run.

A typical persistence call looks like this:

.. code-block:: python

    # Example: add embeddings to an in‑memory store
    store.add(embeds, metadata=[{'id': i} for i in range(len(chunks))])

Retrieval
---------

When a user submits a query, the system generates an embedding for that query and searches the vector store for the most similar chunks.  Cosine similarity is the default metric, but other distance functions can be plugged in if needed.  The algorithm returns the top‑k results, which are then fed into the inference stage.

The retrieval step is illustrated below:

.. code-block:: python

    # Example: retrieve top 5 similar chunks
    results = store.query(query_embedding, k=5)

Inference
---------

The final phase combines the retrieved context with the original user prompt and passes it to a language model.  The LLM generates a response that incorporates both the query and relevant background information.  This step may involve concatenating multiple retrieved chunks into a single prompt or using more sophisticated prompting strategies.

Here is how inference typically looks:

.. code-block:: python

    # Example: generate answer
    prompt = f"{user_query}\nContext:\n{'\n'.join([r['text'] for r in results])}"
    answer = model.generate(prompt)

ASCII Workflow Diagram
---------------------

The following ASCII diagram visualises the data flow through each component.  It is a high‑level abstraction; actual implementations may use different data structures or additional intermediate steps.

.. code-block:: text

    ┌─────────────────────┐
    │ User Input (CLI)    │
    ├─────────────────────┤
    │ Data Ingestion      │
    ├─────────────────────┤
    │ Chunking            │
    ├─────────────────────┤
    │ Embedding           │
    ├─────────────────────┤
    │ Storage             │
    ├─────────────────────┤
    │ Retrieval           │
    ├─────────────────────┤
    │ Inference           │
    └─────────────────────┘

.. include:: add_bottom.add