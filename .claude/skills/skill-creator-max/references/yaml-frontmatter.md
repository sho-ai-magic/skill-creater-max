# YAMLフロントマター 完全リファレンス

## 最小限の必須形式

```yaml
---
name: your-skill-name
description: 何をするか。「トリガーフレーズ」と言われたときに使用する。
---
```

---

## 全フィールド一覧

```yaml
---
name: skill-name-in-kebab-case            # 必須
description: 説明とトリガー条件           # 必須
license: MIT                              # 任意: オープンソース時のライセンス
allowed-tools: "Bash(python3:*) WebFetch" # 任意: ツールアクセス制限
compatibility: Claude.ai, Claude Code     # 任意: 1〜500文字、動作環境
metadata:                                 # 任意: カスタムフィールド
  author: Company Name
  version: 1.0.0
  mcp-server: server-name
  category: productivity
  tags: [project-management, automation]
  documentation: https://example.com/docs
  support: support@example.com
---
```

---

## name フィールドの規則

| 条件 | 正しい例 | 誤った例 |
|------|---------|---------|
| kebab-case のみ | `notion-project-setup` | `Notion Project Setup` |
| スペース禁止 | `my-skill` | `my skill` |
| アンダースコア禁止 | `my-skill` | `my_skill` |
| 大文字禁止 | `my-skill` | `MySkill` |
| 予約語禁止 | `project-helper` | `claude-helper` / `anthropic-tool` |
| フォルダ名と一致 | フォルダ名=`my-skill`, name=`my-skill` | フォルダ名=`my-skill`, name=`myskill` |

---

## description フィールドの規則

必須要素:
1. **何をするか**（機能の説明）
2. **いつ使うか**（具体的なトリガーフレーズ）

制約:
- 1024文字以内
- XMLタグ（`<` `>`）禁止
- 具体的なタスク名を含める
- 関連するファイルタイプがあれば明記する

### 良い description の例

```yaml
# 具体的でトリガーフレーズがある
description: Figmaデザインファイルを解析し、開発者向けのハンドオフドキュメントを生成する。ユーザーが「デザインスペック」「コンポーネントドキュメント」「Figmaを解析して」「design handoff」と言ったときに使用する。

# トリガーフレーズが豊富
description: Linearプロジェクトのワークフロー管理（スプリント計画、タスク作成、ステータス管理）を行う。「スプリント計画」「Linearタスク」「プロジェクト計画」「チケットを作って」「sprint planning」と言われたときに使用する。

# 価値提案が明確
description: PayFlowの顧客オンボーディングをエンドツーエンドで処理する。アカウント作成・支払い設定・サブスクリプション管理を行う。「新規顧客をオンボード」「サブスクリプション設定」「PayFlowアカウントを作成」と言われたときに使用する。
```

### 悪い description の例

```yaml
# 曖昧すぎる
description: プロジェクトを管理します。

# トリガーがない
description: 高度なマルチページドキュメントシステムを生成します。

# 技術的すぎてユーザートリガーがない
description: 階層関係を持つProjectエンティティモデルを実装します。
```

---

## セキュリティ制約

### フロントマターで禁止されているもの

| 禁止事項 | 理由 |
|---------|------|
| XMLタグ（`< >`） | フロントマターはシステムプロンプトに挿入されるため、悪意あるコンテンツがインジェクションを引き起こす可能性がある |
| 名前に `claude` / `anthropic` | 予約語 |
| コード実行（YAML内） | 安全なYAMLパーサーを使用しているため |

---

## よくあるエラーと修正方法

```yaml
# エラー: デリミタなし
name: my-skill
description: 何かをする

# 修正
---
name: my-skill
description: 何かをする
---
```

```yaml
# エラー: 引用符が閉じていない
description: "何かをする

# 修正
description: 何かをする
# または
description: "何かをする"
```

```yaml
# エラー: 不正な名前
name: My Cool Skill

# 修正
name: my-cool-skill
```
