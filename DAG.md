```mermaid
graph TD

    misc-dotfiles -->|depends on| facts
    misc-dotfiles -->|depends on| misc-packages
    omz-zshrc -->|depends on| facts
    omz-zshrc -->|depends on| misc-packages
    git -->|depends on| omz-zshrc
    git -->|depends on| facts
```

