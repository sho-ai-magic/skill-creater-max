#!/usr/bin/env python3
"""
スキル雛形ジェネレータ
使い方: python3 init_skill.py <スキル名> <出力先ディレクトリ>
例:    python3 init_skill.py my-new-skill .
"""
import sys
import os
import re
import shutil


def to_kebab_case(name: str) -> str:
    """文字列を kebab-case に変換する。"""
    name = name.strip().lower()
    name = re.sub(r"[\s_]+", "-", name)
    name = re.sub(r"[^a-z0-9-]", "", name)
    name = re.sub(r"-+", "-", name).strip("-")
    return name


def init_skill(skill_name: str, output_dir: str) -> None:
    kebab_name = to_kebab_case(skill_name)

    if not kebab_name:
        print("❌ 有効なスキル名を指定してください。")
        sys.exit(1)

    if "claude" in kebab_name or "anthropic" in kebab_name:
        print(f"❌ 予約語（claude/anthropic）はスキル名に使用できません: {kebab_name}")
        sys.exit(1)

    skill_dir = os.path.join(output_dir, kebab_name)

    if os.path.exists(skill_dir):
        print(f"❌ フォルダが既に存在します: {skill_dir}")
        sys.exit(1)

    # ディレクトリ構造を作成
    for subdir in ["scripts", "references", "assets"]:
        os.makedirs(os.path.join(skill_dir, subdir))

    # テンプレートのパスを特定（このスクリプトの2階層上の assets/）
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_src = os.path.join(script_dir, "..", "assets", "SKILL.md.template")

    if os.path.isfile(template_src):
        with open(template_src, encoding="utf-8") as f:
            template_content = f.read()
        skill_md_content = template_content.replace("{{SKILL_NAME}}", kebab_name)
    else:
        # テンプレートが見つからない場合の最低限の内容
        skill_md_content = f"""---
name: {kebab_name}
description: （何をするかを書く）。「（トリガーフレーズ1）」「（トリガーフレーズ2）」と言われたときに使用する。Use when user says "（英語トリガー）".
---

# {kebab_name}

（スキルの概要を書く）

## 重要

- （重要な制約や前提条件を先頭に書く）

## 手順

### Step 1: （最初のステップ）

（具体的な指示を書く。曖昧な表現を避け、実行可能な内容にする）

### Step 2: （次のステップ）

（続きの指示）

## 例

### 例1: （代表的なシナリオ）

ユーザー: 「（ユーザーの入力例）」

アクション:
1. （Claude が行う操作）
2. （続きの操作）

結果: （期待される出力）

## トラブルシューティング

**エラー: （よくあるエラー）**
原因: （なぜ起きるか）
対処: （どう解決するか）
"""

    skill_md_path = os.path.join(skill_dir, "SKILL.md")
    with open(skill_md_path, "w", encoding="utf-8") as f:
        f.write(skill_md_content)

    # .gitkeep で空ディレクトリを保持
    for subdir in ["scripts", "references", "assets"]:
        gitkeep_path = os.path.join(skill_dir, subdir, ".gitkeep")
        with open(gitkeep_path, "w") as f:
            pass

    print(f"✅ スキル雛形を生成しました: {skill_dir}")
    print(f"\n次のステップ:")
    print(f"  1. {skill_md_path} を編集して description と指示文を記述する")
    print(f"  2. 検証を実行する:")
    print(f"     python3 {os.path.join(script_dir, 'validate_skill.py')} {skill_dir}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("使い方: python3 init_skill.py <スキル名> <出力先ディレクトリ>")
        print("例:    python3 init_skill.py my-new-skill .")
        sys.exit(1)

    init_skill(sys.argv[1], sys.argv[2])
