# dotfiles

My dotfiles, managed with [chezmoi](https://chezmoi.io) and encrypted with
[age](https://age-encryption.org).

## What's tracked

- `~/.zshrc`
- `~/.gitconfig`
- `~/.pi/agent/models.json`
- `~/.pi/agent/settings.json`
- `~/.tmux.conf`

## Usage

Bootstrap on a new machine:

```sh
brew install chezmoi age
# Copy the age private key to ~/.config/chezmoi/key.txt
chezmoi init --apply harrisonstropkay/dotfiles
```

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
