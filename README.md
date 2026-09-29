# dotfiles

My dotfiles, managed with [chezmoi](https://chezmoi.io) and encrypted with
[age](https://age-encryption.org).

## Usage

Bootstrap on a new machine (macOS or Linux):

```sh
# Step 1: copy the age private key to ~/.config/chezmoi/key.txt
# Step 2: one command — installs chezmoi, then (via a run-before script)
#         Homebrew + age/jq/tmux, fetches the pinned tmux plugins, and applies:
sh -c "$(curl -fsLS get.chezmoi.io)" -- init --apply harrisonstropkay/dotfiles
```

The age key in step 1 is the only manual step (it's a secret, so it can't live
in the repo). Everything else — Homebrew, `age`/`jq`/`tmux`
(`.chezmoidata/packages.yaml`), and the tmux plugins under `~/.tmux/plugins`
(`.chezmoiexternal.toml`) — is installed automatically by step 2.

Edit config files:

```sh
chezmoi edit --apply ~/.vimrc
```

Publish to GitHub:

```sh
chezmoi git [add/commit/push]
```

Pull and apply in one command:

```sh
chezmoi update
```

Add an existing live file to chezmoi management:

```sh
chezmoi add [--encrypt] ~/.vimrc
```

Remove an existing file from chezmoi management:

```sh
chezmoi forget ~/.vimrc
```

## Architecture

```
GitHub (remote)
   ↑↓  git push/pull
~/.local/share/chezmoi   (source dir = a normal git repo)
   ↑↓  chezmoi apply
$HOME  (~/.zshrc, ~/.gitconfig, … live files you actually use)
```
