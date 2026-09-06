"""Japanese display labels for the public UI; stored values stay unchanged."""

VOCAB_TYPES = {"vocab": "一般語彙", "katakana": "カタカナ語"}
VOCAB_LEVELS = {"0": "未設定", **{str(n): f"N{n}" for n in range(1, 6)}}
FEEDBACK_TYPES = {
    "vocab_suggestion": "単語に関する提案",
    "bulk_vocab_request": "単語の一括追加申請",
    "bug_report": "不具合の報告",
    "feature_request": "機能の追加・改善要望",
    "others": "その他",
}
EVENT_TYPES = {
    "vocab_request_result": "単語申請の審査結果",
    # Only staff receive these notifications, even on the shared notifications page.
    "new_vocab_request": "New vocabulary request",
    "vocab": "単語",
    "weight_update_by_system": "出題優先度の自動更新",
    "feedback_reply": "フィードバックへの返信",
}
REQUEST_TYPES_JA = {"create": "追加", "update": "変更", "delete": "削除", "restore": "復元"}
REQUEST_TYPES_EN = {"create": "Creation", "update": "Update", "delete": "Deletion", "restore": "Restoration"}
