"""
LAB 10: Extractive Question Answering Model, Evaluation Metrics & Heuristic Baseline
"""

import re
import string
from collections import Counter
from typing import List, Tuple, Dict, Optional

import torch
import torch.nn as nn
from transformers import AutoModel, AutoConfig


def normalize_answer(s: str) -> str:
    """Chuẩn hóa văn bản theo chuẩn SQuAD: lowercase, bỏ dấu câu, bỏ mạo từ a/an/the, chuẩn khoảng trắng."""
    def remove_articles(text: str) -> str:
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text: str) -> str:
        return " ".join(text.split())

    def remove_punc(text: str) -> str:
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    return white_space_fix(remove_articles(remove_punc(s.lower())))


def compute_exact_match(prediction: str, ground_truth: str) -> float:
    """Tính điểm Exact Match (EM) sau chuẩn hóa."""
    return float(normalize_answer(prediction) == normalize_answer(ground_truth))


def compute_f1(prediction: str, ground_truth: str) -> float:
    """Tính điểm Token-level F1 theo chuẩn SQuAD."""
    pred_tokens = normalize_answer(prediction).split()
    gold_tokens = normalize_answer(ground_truth).split()

    if len(pred_tokens) == 0 or len(gold_tokens) == 0:
        return float(pred_tokens == gold_tokens)

    common = Counter(pred_tokens) & Counter(gold_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0

    precision = num_same / len(pred_tokens)
    recall = num_same / len(gold_tokens)
    return (2 * precision * recall) / (precision + recall)


def keyword_overlap_baseline(question: str, context: str) -> str:
    """
    Heuristic Baseline (Mục 21):
    1. Tìm câu trong context có số từ khóa trùng với câu hỏi nhiều nhất.
    2. Loại bỏ stopwords và các từ đã xuất hiện trong câu hỏi để trích xuất candidate span.
    """
    stopwords = {
        "what", "which", "who", "whom", "whose", "where", "when", "why", "how",
        "is", "are", "was", "were", "the", "a", "an", "in", "on", "of", "to",
        "for", "with", "by", "at", "from", "as", "and", "or", "that", "this"
    }
    q_words = set(normalize_answer(question).split()) - stopwords
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", context) if s.strip()]
    if not sentences:
        return ""

    best_sent = max(
        sentences,
        key=lambda s: len(q_words & set(normalize_answer(s).split()))
    )
    cand_tokens = [
        w for w in best_sent.rstrip(".!?").split()
        if normalize_answer(w) not in q_words and normalize_answer(w) not in stopwords
    ]
    return " ".join(cand_tokens[:5]) if cand_tokens else best_sent


class ExtractiveQAModel(nn.Module):
    """
    Pretrained Transformer Backbone + Span Prediction Head (Start & End Classifiers).
    """

    def __init__(self, model_name: str = "distilbert-base-uncased"):
        super().__init__()
        self.config = AutoConfig.from_pretrained(model_name)
        self.encoder = AutoModel.from_pretrained(model_name, config=self.config)
        self.qa_outputs = nn.Linear(self.config.hidden_size, 2)

    def forward(
        self,
        input_ids: torch.Tensor,
        attention_mask: torch.Tensor,
        token_type_ids: Optional[torch.Tensor] = None,
        start_positions: Optional[torch.Tensor] = None,
        end_positions: Optional[torch.Tensor] = None,
    ) -> Dict[str, Optional[torch.Tensor]]:
        encoder_kwargs = {
            "input_ids": input_ids,
            "attention_mask": attention_mask,
        }
        # Chỉ truyền token_type_ids cho các kiến trúc hỗ trợ (BERT, ALBERT, ELECTRA...)
        if token_type_ids is not None and self.config.model_type in {"bert", "albert", "electra", "xlnet"}:
            encoder_kwargs["token_type_ids"] = token_type_ids

        outputs = self.encoder(**encoder_kwargs)
        sequence_output = outputs.last_hidden_state          # [batch_size, seq_len, hidden_size]
        logits = self.qa_outputs(sequence_output)            # [batch_size, seq_len, 2]
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1)              # [batch_size, seq_len]
        end_logits = end_logits.squeeze(-1)                  # [batch_size, seq_len]

        loss = None
        if start_positions is not None and end_positions is not None:
            # Bỏ qua các vị trí ngoài phạm vi sequence length nếu có
            ignored_index = start_logits.size(1)
            start_positions = start_positions.clamp(0, ignored_index)
            end_positions = end_positions.clamp(0, ignored_index)

            loss_fct = nn.CrossEntropyLoss(ignore_index=ignored_index)
            start_loss = loss_fct(start_logits, start_positions)
            end_loss = loss_fct(end_logits, end_positions)
            loss = (start_loss + end_loss) / 2.0

        return {
            "loss": loss,
            "start_logits": start_logits,
            "end_logits": end_logits,
        }


def decode_best_span(
    start_logits: torch.Tensor,
    end_logits: torch.Tensor,
    offset_mapping: List[Tuple[int, int]],
    sequence_ids: List[Optional[int]],
    context_text: str,
    max_answer_len: int = 30,
    n_best_size: int = 20,
) -> Tuple[str, float]:
    """
    Tìm cặp chỉ số (i, j) thuộc phần context (sequence_ids == 1) thỏa mãn i <= j
    và j - i + 1 <= max_answer_len sao cho start_logits[i] + end_logits[j] lớn nhất.
    """
    start_scores = start_logits.detach().cpu().numpy()
    end_scores = end_logits.detach().cpu().numpy()

    valid_indices = [idx for idx, seq_id in enumerate(sequence_ids) if seq_id == 1]
    if not valid_indices:
        return "", -1e9

    top_starts = sorted(valid_indices, key=lambda idx: start_scores[idx], reverse=True)[:n_best_size]
    top_ends = sorted(valid_indices, key=lambda idx: end_scores[idx], reverse=True)[:n_best_size]

    best_score = -1e9
    best_span = (valid_indices[0], valid_indices[0])

    for i in top_starts:
        for j in top_ends:
            if i <= j and (j - i + 1) <= max_answer_len:
                score = float(start_scores[i] + end_scores[j])
                if score > best_score:
                    best_score = score
                    best_span = (i, j)

    char_start = offset_mapping[best_span[0]][0]
    char_end = offset_mapping[best_span[1]][1]
    return context_text[char_start:char_end], best_score
