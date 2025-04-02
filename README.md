# lelem (ლელემ)

A Python library that allows for LLM conversations in which the LLM takes an active part by issuing commands and accepting replies from the user. In a way, it resembles MCP behavior without the MCP overhead.

The "agent" terminology is deliberately avoided to emphasize the focus on simple request/response interactions without the more complex behaviors a traditional agent (not in the model context) should exhibit.

One specific behavior `lelem` should help to achieve is the possibility to conduct an interaction regarding a source code project that is managed in `git`, and has testing functionality (either an existing one or one that's created as part of the interaction with the model). The wish is to let the model modify code directly, commit changes to git (possibly on context branches), and autonomously run tests in order to validate its operations (and possibly roll back when needed).

Future behaviors may include planning (making a plan, interact over it with the human operator, and executing it), RAG functionality, model memory management (to avoid overloading the context), and collaboration among several models (local and cloud-based).

The name `lelem` is best pronounced using Georgian accent.

## Components

`lelem` implements basic functionality of a model conversation via a Conversation class and a set of conversation scripts with common models: OpenAI, Anthropic (Claude), Google (Gemini), DeepSeek, and through LangChain (previously mentioned models as well as Ollama and llama.cpp). Open source models that can run locally are naturally preferable when costs come to mind, and it proves effective to test them in hosted environments to verify the local setup.

On top of the conversation functionality there's an Actor behavior: models are instructed to issue commands (in replies) to be responded to (in questions) by the conversation operator (which is a Python script, conducting an automatic or semi-automatic conversation).

When comparing the range of available models it is apparent that smaller models tend to have less success in comprehending the actor instructions. This may be mitigated by improving instructions or fine-tuning, but there's a good chance that the limitations are fundamental.

## Execution

Technically, the conversation takes place inside a container. This gives good control of the environment and sandboxes the operation. In order to be more effective, actual working spaces (e.g., the git repo) can be kept on a bind mount.

`lelem` is best installed inside the container in an in-place editing mode (via `make install`).

When running with local LLMs on Linux, a useful configuration can include Proxmox running a Linux VM with a passed-through GPU and nVidia drivers installed, with it in turn running a container like above. This may look over-complicated, but as GPU configuration have many moving parts and will change over time, some control over changes is in order. It is also not a bad idea to pin-point versions of components.

On macOS, lacking native container support, `tart` can be used to configure native VMs. Inside the VM, installing Ollama should be enough for running local models.

Automation is taken care of by the `Classico` library.

## Model instructions (aka "prologs")

There is a mechanism that allow for tinkering with prologs. It is based on a root file (e.g. `prolog/apprentice-system.1`) that may contain include directives (lines that start with `@`) and comments (lines that start with `#`). Files that are included are taken verbatim (in order not to over complicate things). The `.number` postfix of prolog files is a convention that supports switching between alternative prompt.

Use `prolog` to display the prolog text.

## Supported commands

* `fread`

* `fwrite`

* `exec`

* `git-add`

* `git-commit`

