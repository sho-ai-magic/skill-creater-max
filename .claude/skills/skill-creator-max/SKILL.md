---
name: skill-creator-max
description: Anthropic公式ガイドに準拠したClaudeスキルを対話的に設計・生成・検証するメタスキル。ユースケース定義からSKILL.md作成、検証スクリプト実行まで一貫してガイドする。「スキルを作って」「スキルを作りたい」「SKILL.mdを書いて」「新しいスキルを作成」「skill作成」「make a skill」「create a skill」「build a skill」「SKILL.md作成」と言われたときに使用する。MCPサーバー向けのスキル強化にも対応。
metadata:
  author: sho-ai-magic
  version: 1.0.0
  category: meta-skill
allowed-tools: "Bash(python3:*)"
---

# skill-creator-max

Anthropic公式ガイドに準拠したClaudeスキルを、対話的に設計・生成・検証するためのメタスキルです。

## 重要

- スキルフォルダ内には **絶対に README.md を置かない**（SKILL.md に統合する）
- フォルダ名・`name` フィールドは **kebab-case のみ**（スペース・大文字・アンダースコア禁止）
- `description` には **「何をするか」と「いつ使うか」の両方** が必須
- XMLタグ（`< >`）は frontmatter に使用禁止
- 名前に `claude` または `anthropic` は使用禁止（予約語）

---

## ワークフロー

詳細は `references/anthropic-guide.md` を参照。以下の7ステップで進める。

### Step 1: ユースケースの特定

ユーザーに以下を質問する:
1. このスキルで何を達成したいか？（具体的なゴール）
2. ユーザーはどんな言葉でこのスキルを呼び出すか？（トリガーフレーズ2〜5個）
3. MCPサーバーと連携するか？するなら対象サービス名は？

回答を踏まえ、3つのユースケースカテゴリのいずれかに分類する（`references/anthropic-guide.md` の「ユースケース3分類」を参照）:
- **カテゴリ1**: ドキュメント・アセット作成
- **カテゴリ2**: ワークフロー自動化
- **カテゴリ3**: MCPエンハンスメント

### Step 2: 設計パターンの選択

`references/patterns.md` を参照し、ユースケースに最適なパターンを提案する:
- Sequential Workflow（順次ワークフロー）
- Multi-MCP Coordination（複数MCP連携）
- Iterative Refinement（反復改善）
- Context-Aware Tool Selection（状況対応ツール選択）
- Domain-Specific Intelligence（ドメイン特化知識）

### Step 3: スキル雛形の生成

```bash
python3 scripts/init_skill.py <スキル名> <出力先ディレクトリ>
```

例:
```bash
python3 scripts/init_skill.py my-new-skill /path/to/output
Expected output: スキルフォルダが生成され、SKILL.md テンプレートが配置される
```

### Step 4: frontmatter の作成

`references/yaml-frontmatter.md` を参照して description を設計する。

CRITICAL: description に必ず含めること:
- **何をするか**（機能の説明）
- **いつ使うか**（具体的なトリガーフレーズ、日本語＋英語）
- 1024文字以内
- XMLタグ（`< >`）禁止

良い例:
```yaml
description: Figmaデザインファイルを解析し、開発者向けのハンドオフドキュメントを生成する。ユーザーが「デザインスペック」「コンポーネントドキュメント」「Figmaを解析して」「design handoff」と言ったときに使用する。
```

悪い例:
```yaml
description: プロジェクトを管理します。
```

### Step 5: 指示文の作成

- 重要な指示は冒頭の `## 重要` セクションに配置
- 箇条書き・番号リストを活用（曖昧な表現を避ける）
- エラーハンドリングを含む
- 具体的な例（入力・出力）を提供
- 詳細ドキュメントは `references/` に分離し、SKILL.md からリンクする

### Step 6: 検証スクリプトの実行

```bash
python3 scripts/validate_skill.py <スキルフォルダのパス>
Expected output: ✅ 全項目パス（または ❌ と具体的なエラー内容）
```

エラーが出た場合は内容に従い修正し、再度実行する。

### Step 7: テストの実施

`references/checklist.md` のチェックリストを使い、3種類のテストを行う:
1. **トリガーテスト**: 関連クエリでスキルが90%以上自動起動するか
2. **機能テスト**: 正しい出力が生成され、APIエラーが0件か
3. **パフォーマンス比較**: スキルあり/なしでトークン数・手戻り回数を比較

---

## 例

### 例1: 議事録作成スキルを作りたい場合

ユーザー: 「会議の議事録を自動生成するスキルを作りたい」

アクション:
1. カテゴリ1（ドキュメント作成）に分類
2. Iterative Refinement パターンを提案
3. `python3 scripts/init_skill.py meeting-minutes-creator .` で雛形生成
4. description 例: 「会議メモや録音テキストから整形された議事録を生成する。『議事録を作って』『会議まとめ』『meeting minutes』と言われたときに使用する。」
5. validate で検証

### 例2: MCPサーバー連携スキルを作りたい場合

カテゴリ3を選択し、`references/patterns.md` の「Multi-MCP Coordination」パターンを参照する。

---

## トラブルシューティング

**エラー: スキルが起動しない**
- description のトリガーフレーズを具体化する
- 「〜したい」「〜して」など実際に言いそうな表現を追加する

**エラー: validate_skill.py が失敗する**
- エラーメッセージに従い SKILL.md を修正する
- `references/yaml-frontmatter.md` で正しい形式を確認する

**エラー: 指示が守られない**
- 重要指示を `## 重要` セクションに移動して先頭に置く
- 箇条書きを `CRITICAL:` プレフィックスで強調する
