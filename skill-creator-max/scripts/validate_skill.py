#!/usr/bin/env python3
"""
Anthropic公式ガイド準拠チェッカー
使い方: python3 validate_skill.py <スキルフォルダのパス>
"""
import sys
import os
import re


def check(condition: bool, message: str) -> bool:
    if condition:
        print(f"  ✅ {message}")
    else:
        print(f"  ❌ {message}")
    return condition


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """YAMLフロントマターをシンプルなパーサで抽出する。"""
    if not content.startswith("---"):
        return {}, content

    end = content.find("---", 3)
    if end == -1:
        return {}, content

    fm_text = content[3:end].strip()
    body = content[end + 3:].strip()

    fields: dict = {}
    current_key = None
    for line in fm_text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        if re.match(r"^\w[\w-]*\s*:", line):
            key, _, val = line.partition(":")
            current_key = key.strip()
            fields[current_key] = val.strip().strip('"').strip("'")
        elif current_key and line.startswith(" "):
            # マルチライン値は連結する
            fields[current_key] = (fields.get(current_key, "") + " " + line.strip()).strip()
    return fields, body


def validate(skill_path: str) -> bool:
    print(f"\n🔍 スキル検証: {skill_path}\n")
    results: list[bool] = []

    # 1. パスが存在するか
    r = check(os.path.isdir(skill_path), f"スキルフォルダが存在する: {skill_path}")
    results.append(r)
    if not r:
        return False

    folder_name = os.path.basename(os.path.abspath(skill_path))

    # 2. フォルダ名が kebab-case か
    r = check(
        bool(re.fullmatch(r"[a-z][a-z0-9-]*", folder_name)),
        f"フォルダ名が kebab-case である: {folder_name}"
    )
    results.append(r)

    # 3. 予約語チェック
    r = check(
        "claude" not in folder_name and "anthropic" not in folder_name,
        f"フォルダ名に予約語（claude/anthropic）が含まれていない"
    )
    results.append(r)

    # 4. SKILL.md が存在するか（大文字小文字厳守）
    skill_md_path = os.path.join(skill_path, "SKILL.md")
    actual_files = os.listdir(skill_path)
    r = check("SKILL.md" in actual_files, "SKILL.md が存在する（大文字小文字厳守）")
    results.append(r)
    if not r:
        return all(results)

    # 5. README.md がスキルフォルダ内にないか
    r = check("README.md" not in actual_files, "スキルフォルダ内に README.md が存在しない")
    results.append(r)

    with open(skill_md_path, encoding="utf-8") as f:
        content = f.read()

    # 6. フロントマターのデリミタが正しいか
    r = check(content.startswith("---"), "フロントマターが --- で始まる")
    results.append(r)

    has_closing = content.count("---") >= 2
    r = check(has_closing, "フロントマターの閉じデリミタ --- が存在する")
    results.append(r)

    fields, _ = parse_frontmatter(content)

    # 7. name フィールドが存在するか
    r = check("name" in fields and bool(fields.get("name")), "name フィールドが存在する")
    results.append(r)

    if "name" in fields:
        name_val = fields["name"]
        # 8. name が kebab-case か
        r = check(
            bool(re.fullmatch(r"[a-z][a-z0-9-]*", name_val)),
            f"name が kebab-case である: {name_val}"
        )
        results.append(r)

        # 9. name とフォルダ名が一致するか
        r = check(name_val == folder_name, f"name '{name_val}' とフォルダ名 '{folder_name}' が一致する")
        results.append(r)

        # 10. name に予約語がないか
        r = check(
            "claude" not in name_val and "anthropic" not in name_val,
            "name に予約語（claude/anthropic）が含まれていない"
        )
        results.append(r)

    # 11. description フィールドが存在するか
    r = check("description" in fields and bool(fields.get("description")), "description フィールドが存在する")
    results.append(r)

    if "description" in fields:
        desc = fields["description"]

        # 12. description が 1024 文字以内か
        r = check(len(desc) <= 1024, f"description が 1024 文字以内である（現在: {len(desc)} 文字）")
        results.append(r)

        # 13. description に XML タグが含まれていないか
        r = check("<" not in desc and ">" not in desc, "description に XML タグ（< >）が含まれていない")
        results.append(r)

        # 14. description に「いつ使うか」のトリガーフレーズが含まれているか（簡易チェック）
        trigger_keywords = ["use when", "use for", "ときに使用", "と言われたとき", "場合に使用", "when user"]
        has_trigger = any(kw.lower() in desc.lower() for kw in trigger_keywords)
        r = check(has_trigger, "description に「いつ使うか」を示すトリガーフレーズが含まれている")
        results.append(r)

    # 結果サマリー
    passed = sum(1 for r in results if r)
    total = len(results)
    print(f"\n{'=' * 40}")
    if all(results):
        print(f"🎉 検証完了: {passed}/{total} 項目すべてパス！")
    else:
        print(f"⚠️  検証完了: {passed}/{total} 項目パス（{total - passed} 件の問題あり）")
    print()

    return all(results)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("使い方: python3 validate_skill.py <スキルフォルダのパス>")
        sys.exit(1)

    success = validate(sys.argv[1])
    sys.exit(0 if success else 1)
