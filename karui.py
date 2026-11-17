#!/usr/bin/env python3
"""Karui（軽い）- パイプでつなぐ超軽量クエリ言語。SQLiteに変換して実行する。

例: from users | where age > 20 | select name, age | sort age desc | take 3
from で始まらない行は、そのまま SQL として実行される（CREATE / INSERT など）。
"""
import re
import sqlite3
import sys

# クォート内の | では分割しない
PIPE = re.compile(r"\|(?=(?:[^']*'[^']*')*[^']*$)")


def compile_karui(src: str) -> str:
    """Karui の1文を SQL に変換する。"""
    steps = [s.strip() for s in PIPE.split(src) if s.strip()]
    q = {"from": None, "where": [], "select": "*", "group": None,
         "sort": None, "take": None}
    for step in steps:
        cmd, _, arg = step.partition(" ")
        arg = arg.strip()
        if cmd == "from":
            q["from"] = arg
        elif cmd == "where":
            q["where"].append(f"({arg})")
        elif cmd == "select":
            q["select"] = arg
        elif cmd == "group":
            q["group"] = arg
        elif cmd == "sort":
            q["sort"] = arg
        elif cmd == "take":
            q["take"] = int(arg)
        else:
            raise SyntaxError(f"不明なコマンド: {cmd}")
    if not q["from"]:
        raise SyntaxError("from がありません")

    sql = f"SELECT {q['select']} FROM {q['from']}"
    if q["where"]:
        sql += " WHERE " + " AND ".join(q["where"])
    if q["group"]:
        sql += f" GROUP BY {q['group']}"
    if q["sort"]:
        sql += f" ORDER BY {q['sort']}"
    if q["take"] is not None:
        sql += f" LIMIT {q['take']}"
    return sql


def run(db: sqlite3.Connection, line: str) -> None:
    sql = compile_karui(line) if line.startswith("from ") else line
    cur = db.execute(sql)
    db.commit()
    if cur.description:
        print(" | ".join(c[0] for c in cur.description))
        for row in cur.fetchall():
            print(" | ".join(str(v) for v in row))


def main() -> None:
    db = sqlite3.connect(sys.argv[1] if len(sys.argv) > 1 else ":memory:")
    print("Karui REPL（終了: exit / 変換だけ見る: 先頭に ? ）")
    while True:
        try:
            line = input("karui> ").strip()
        except EOFError:
            break
        if not line:
            continue
        if line == "exit":
            break
        try:
            if line.startswith("?"):
                print(compile_karui(line[1:].strip()))
            else:
                run(db, line)
        except Exception as e:
            print("エラー:", e)


if __name__ == "__main__":
    main()
