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
chezmoi edit ~/.zshrc        # edit the source (decrypts if encrypted)
chezmoi diff                 # preview what apply would change
chezmoi apply                # render source → live $HOME
```

Publish to GitHub:

```sh
chezmoi git add -A
chezmoi git commit -m "…"
chezmoi git push
```

Pull and apply in one command:

```sh
chezmoi update               # = git pull + apply
```

Add an existing live file to chezmoi management:

```sh
chezmoi add ~/.vimrc                # plain
chezmoi add --encrypt ~/.vimrc      # encrypted
```

Stop managing a file:

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
