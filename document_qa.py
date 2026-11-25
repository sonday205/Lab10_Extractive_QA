
import argparse
from typing import Dict, Any
import torch
from transformers import AutoTokenizer, AutoModelForQuestionAnswering


class MiniDocumentQA:
    def __init__(
        self,
        model_name_or_path: str = "distilbert-base-uncased-distilled-squad",
        max_length: int = 384,
        stride: int = 128,
    ):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
        self.model = AutoModelForQuestionAnswering.from_pretrained(model_name_or_path).to(self.device)
        self.model.eval()
        self.max_length = max_length
        self.stride = stride

    @torch.no_grad()
    def answer(self, question: str, document: str, max_answer_len: int = 35, n_best: int = 20) -> Dict[str, Any]:
        inputs = self.tokenizer(
            question.strip(),
            document,
            truncation="only_second",
            max_length=self.max_length,
            stride=self.stride,
            return_overflowing_tokens=True,
            return_offsets_mapping=True,
            padding="max_length",
            return_tensors="pt",
        )

        offset_mapping = inputs.pop("offset_mapping")
        inputs.pop("overflow_to_sample_mapping")

        best_score = -1e9
        best_result = {
            "question": question,
            "answer": "",
            "score": 0.0,
            "char_span": (0, 0),
            "window_index": 0,
        }

        num_windows = inputs["input_ids"].size(0)
        model_inputs = {k: v.to(self.device) for k, v in inputs.items()}
        outputs = self.model(**model_inputs)

        for win_idx in range(num_windows):
            seq_ids = inputs.sequence_ids(win_idx)
            offsets = offset_mapping[win_idx].tolist()
            start_logits = outputs.start_logits[win_idx].cpu().numpy()
            end_logits = outputs.end_logits[win_idx].cpu().numpy()

            valid_ctx_indices = [idx for idx, sid in enumerate(seq_ids) if sid == 1]
            if not valid_ctx_indices:
                continue

            top_starts = sorted(valid_ctx_indices, key=lambda idx: start_logits[idx], reverse=True)[:n_best]
            top_ends = sorted(valid_ctx_indices, key=lambda idx: end_logits[idx], reverse=True)[:n_best]

            for i in top_starts:
                for j in top_ends:
                    if i <= j and (j - i + 1) <= max_answer_len:
                        score = float(start_logits[i] + end_logits[j])
                        if score > best_score:
                            best_score = score
                            c_start, c_end = offsets[i][0], offsets[j][1]
                            best_result = {
                                "question": question,
                                "answer": document[c_start:c_end],
                                "score": round(score, 4),
                                "char_span": (c_start, c_end),
                                "window_index": win_idx,
                            }

        return best_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mini Document Extractive QA System")
    parser.add_argument("--model", type=str, default="distilbert-base-uncased-distilled-squad")
    parser.add_argument("--question", type=str, default=None)
    parser.add_argument("--context", type=str, default=None)
    args = parser.parse_args()

    sample_document = (
        "Extractive Question Answering is a natural language processing task where a model "
        "identifies a contiguous span of text from a given context passage to answer a user question. "
        "Unlike generative QA, extractive models predict two probability distributions over the input "
        "tokens: one for the start position and one for the end position of the answer span. "
        "In LAB 10 at VNU University of Science, students fine-tune pretrained Transformers on SQuAD "
        "using offset mapping and a sliding window stride of 128 tokens."
    )

    sample_questions = [
        "What two probability distributions do extractive models predict?",
        "What dataset do students fine-tune pretrained Transformers on?",
        "What sliding window stride is used in LAB 10?",
    ]

    qa_system = MiniDocumentQA(model_name_or_path=args.model)

    if args.question and args.context:
        res = qa_system.answer(args.question, args.context)
        print(f"Q: {res['question']}\nA: {res['answer']} (score={res['score']}, span={res['char_span']})")
    else:
        for q in sample_questions:
            res = qa_system.answer(q, sample_document)
            print(f"Q: {res['question']}")
            print(f"A: {res['answer']} | score={res['score']} | char_span={res['char_span']}\n")
