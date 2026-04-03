```mermaid
graph TD

    claude -->|depends on| facts
    facts
    gh-extensions -->|depends on| misc-packages
    git -->|depends on| facts
    git -->|depends on| omz-zshrc
    misc-dotfiles -->|depends on| facts
    misc-dotfiles -->|depends on| misc-packages
    misc-packages
    omz-zshrc -->|depends on| facts
    omz-zshrc -->|depends on| misc-packages

    classDef facts fill:#4a9eff,stroke:#2b7de9,color:#fff
    classDef role fill:#2d2d2d,stroke:#555,color:#fff
    classDef default fill:#2d2d2d,stroke:#555,color:#fff
    class facts facts
```
