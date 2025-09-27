# Finishing Touches (Zero-Overhead)

## 1) Install the extension (no build)
```bash
bash scripts/install_extension_local.sh
```
Reload VS Code: Cmd+Shift+P → *Developer: Reload Window*.

## 2) Optional: Build VSIX and install
```bash
bash scripts/build_vsix_and_install.sh
```
(Requires internet to fetch `@vscode/vsce` once.)

## 3) Add keybindings (macOS)
```bash
node scripts/merge_keybindings.mjs overlays/keybindings.macos.json
```

## 4) Snippets
- Already included: `.vscode/ollama-snippets.code-snippets`

## 5) Quick open all AI web apps
```bash
bash scripts/open_sites.sh
```

## 6) Health check
```bash
bash scripts/diagnose.sh
```

That’s it. You now have: precompiled extension, quick install, keybindings, snippets, one-liners, and diagnostics.
