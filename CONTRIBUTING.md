# Contributing to Vault-Mind

Thanks for your interest in contributing to Vault-Mind! This project was built for OSDHack 2026 and welcomes contributions from the community.

## Ways to Contribute

- 🐛 Report bugs by opening an issue
- 💡 Suggest features or improvements
- 📝 Improve documentation
- 🔧 Submit code fixes or new features via pull request

## Getting Started

1. **Fork** the repository
2. **Clone** your fork:
   ```bash
   git clone https://github.com/<your-username>/Vault-Mind.git
   cd Vault-Mind
   ```
3. **Set up your environment** — follow the [Setup section in README.md](./README.md#setup)
4. **Create a branch** for your change:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Making Changes

- Keep changes focused — one feature/fix per pull request
- Follow the existing code style (see `src/` for examples: clear docstrings, type hints where practical)
- Test your changes locally with `python app.py ingest` / `python app.py chat` (and `python web_app.py` if UI-related) before submitting
- Update `README.md` if your change affects setup, usage, or behavior
- **Add an entry to [CHANGELOG.md](./CHANGELOG.md)** under an `[Unreleased]` section describing your change
- If this is your first contribution, add yourself to [CONTRIBUTORS.md](./CONTRIBUTORS.md)

## Submitting a Pull Request

1. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a pull request against `main` on the upstream repo
3. Describe **what** changed and **why** in the PR description
4. A GitHub Actions check will confirm `CHANGELOG.md` was updated — make sure this passes

## Code of Conduct

Be respectful and constructive. This project follows the general spirit of the [OSDHack 2026 Fair Play Rules](https://github.com/Maharshi-Paul/Vault-Mind/blob/main/CODE_OF_CONDUCT.md) — no harmful, abusive, or plagiarized contributions.

## Questions?

Open an issue or reach out via the contact info in the main repository.
