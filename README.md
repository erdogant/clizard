# clizard

[![Python](https://img.shields.io/pypi/pyversions/clizard.svg)](https://pypi.org/project/clizard/)
[![PyPI](https://img.shields.io/pypi/v/clizard.svg)](https://pypi.org/project/clizard/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docs](https://img.shields.io/badge/Sphinx-Docs-blue.svg)](https://erdogant.github.io/clizard/)
[![Stars](https://img.shields.io/github/stars/erdogant/clizard)](https://github.com/erdogant/clizard)
[![Downloads](https://static.pepy.tech/personalized-badge/clizard?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=PyPI%20downloads/month)](https://pepy.tech/project/clizard)

> Clizard is a lightweight Python toolkit that streamlines the creation and management of command‑line interfaces (CLIs). It automatically generates common argparse options—such as verbosity, configuration file paths, help flags—and wraps them in a rich‑based chat CLI for interactive use. By providing utilities like `build_parser`, `auto_cli`, and decorators such as `command`, developers can focus on business logic while still delivering polished, user‑friendly CLIs with minimal boilerplate. The library also offers JSON‑backed configuration handling (`Config`), automatic loading of `.clizard` files, and helper functions to discover main entry points or Snakemake configs. Clizard’s goal is to reduce repetitive CLI code, improve consistency across projects, and enable rapid prototyping of command‑line tools with a clean, declarative API.

---

## 📖 Table of Contents
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Dependencies](#-dependencies)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [Citation](#-citation)
- [License](#-license)

---

## ✨ Features

- Build argparse parsers with common options
- Auto-generate rich CLI from existing ArgumentParser
- Persist settings in a JSON-backed Config store
- Register slash‑commands via @command decorator

---

## 🚀 Installation

**Stable release (PyPI):**
```bash
pip install clizard
```

**Latest development version:**
```bash
pip install git+https://github.com/erdogant/clizard.git@main
```

**Clone and install locally:**
```bash
git clone https://github.com/erdogant/clizard.git
cd clizard
pip install -e .
```

---

## ⚡ Quick Start

```bash
# Go to the repo dir.
clizard

```

```python
# Or create a clizard_cli make file
from clizard import Config
cfg = Config('mytool.clizard')
print(cfg.settings)
```


---

## 📚 Documentation

Full documentation, including API reference and examples, is available at:
**[https://erdogant.github.io/clizard/](https://erdogant.github.io/clizard/)**

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request on [GitHub](https://github.com/erdogant/clizard).

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request


---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](https://github.com/erdogant/clizard/blob/master/LICENSE) file for details.
