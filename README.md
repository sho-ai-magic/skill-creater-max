# skill-creater-max

Anthropic公式スキルガイドに準拠したClaudeスキルを生成するためのメタスキル集。

## 収録スキル

### `skill-creator-max`

Anthropic公式ガイドに準拠したスキルを対話的に設計・生成・検証するメタスキル。

**使い方のトリガー例**:
- 「スキルを作って」
- 「SKILL.mdを書いて」
- 「make a skill」
- 「build a skill for [用途]」

**機能**:
- ユースケース定義の対話的ガイド
- frontmatter の自動生成
- Anthropic公式ガイドに沿った指示文の作成
- 準拠チェッカーによる機械的検証

---

## インストール

### Claude.ai

1. [`skill-creator-max/`](./skill-creator-max/) フォルダをダウンロード・ZIP圧縮する
2. Claude.ai を開く → Settings > Capabilities > Skills
3. 「Upload skill」をクリックして ZIP を選択する
4. スキルを有効化する

### Claude Code

```bash
# スキルをClaudeCodeのディレクトリにコピー
cp -r skill-creator-max ~/.claude/skills/
```

---

## 使い方

スキルをインストール後、Claudeに話しかける:

```
スキルを作りたい。[用途の説明]
```

Claudeがステップに沿ってガイドし、準拠したSKILL.mdを生成します。

### 生成されたスキルの検証

```bash
python3 skill-creator-max/scripts/validate_skill.py <スキルフォルダのパス>
```

### スキル雛形の生成

```bash
python3 skill-creator-max/scripts/init_skill.py <スキル名> <出力先>
# 例:
python3 skill-creator-max/scripts/init_skill.py my-new-skill .
```

---

## ドキュメント

- [`references/anthropic-guide.md`](./skill-creator-max/references/anthropic-guide.md) — 公式ガイド要点
- [`references/yaml-frontmatter.md`](./skill-creator-max/references/yaml-frontmatter.md) — frontmatterリファレンス
- [`references/patterns.md`](./skill-creator-max/references/patterns.md) — 5つの設計パターン
- [`references/checklist.md`](./skill-creator-max/references/checklist.md) — 品質チェックリスト

---

## ライセンス

MIT
