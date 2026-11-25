# LAB 10: Extractive Question Answering (From Token Classification to Span Prediction)


## 1. Cấu trúc thư mục Deliverables (`lab10/`)
- `README.md`: Thông tin tái lập thực nghiệm (Reproducibility) và khai báo sử dụng AI.
- `calculation.pdf`: Bài làm phần tính toán viết tay.
- `prediction.md`: Các giả thuyết dự đoán trước khi chạy thực nghiệm.
- `tokenizer_alignment.ipynb`: Triển khai Sliding Window (`stride=128`), ánh xạ Character-to-Token Span và kiểm thử 4 trường hợp biên.
- `qa_model.py`: Định nghĩa kiến trúc `ExtractiveQAModel`, hàm chuẩn hóa EM/F1, `decode_best_span` và `keyword_overlap_baseline`.
- `qa_finetuning.ipynb`: Pipeline huấn luyện, đánh giá trên SQuAD v1.1 (Experiments 1–5) và xuất biểu đồ.
- `results.csv`: Bảng tổng hợp kết quả định lượng qua các thực nghiệm.
- `learning_curves.png`: Training loss và validation EM/F1 theo từng epoch; validation loss chưa được ghi trong lần chạy này.
- `em_f1_analysis.png`: So sánh Baseline vs. Fine-tuned Transformer và phân bố `EM=0, F1>0`.
- `answer_length_analysis.png`: Phân tích hiệu năng EM và F1 theo độ dài đáp án.
- `error_analysis.md`: Phân tích định tính và định lượng 15 mẫu lỗi (`wrong start`, `wrong end`, `wrong span`).
- `document_qa.py`: Ứng dụng Mini Document QA trả lời câu hỏi trên tài liệu tùy chỉnh.
- `reflection.md`: Bài viết tổng kết so sánh kiến trúc LAB 08 — LAB 09 — LAB 10.
- `individual_learning_check.md`: Câu trả lời phần Individual Learning Check.

## 2. Hướng dẫn chạy nhanh
```bash
pip install torch transformers datasets pandas matplotlib
python document_qa.py
```

## 3. Reproducibility (Mục 30)
- **Model:** `distilbert-base-uncased` (và `distilbert-base-uncased-distilled-squad` cho demo Document QA)
- **Tokenizer:** `AutoTokenizer` (WordPiece, `lowercase=True`)
- **Dataset:** SQuAD v1.1 (`rajpurkar/squad`)
- **Train split:** 15,000 samples (lấy mẫu ngẫu nhiên với `seed=42`)
- **Validation split:** 2,000 samples
- **Test split:** Đánh giá trên tập validation chuẩn của SQuAD v1.1
- **Max sequence length:** `384` (so sánh với `128` và `256` trong Experiment 1)
- **Stride:** `128`
- **Batch size:** `16`
- **Learning rate:** `3e-5` (Linear warmup 10% + linear decay)
- **Epochs:** `3`
- **Optimizer:** `AdamW` (`weight_decay=0.01`)
- **Random seed:** `42`
- **Hardware:** Intel Core i5-13500H, 16GB RAM, NVIDIA GeForce RTX 4050 (6GB VRAM)

## 4. AI Usage Declaration (Mục 29)
- **AI-assisted code:** Hỗ trợ cấu trúc boilerplate cho vòng lặp huấn luyện PyTorch, trực quan hóa Matplotlib và kiểm tra cú pháp API Hugging Face Tokenizer.
- **What was generated:** Khung cấu trúc các file báo cáo Markdown, hàm vẽ biểu đồ learning curves và giao diện CLI của `document_qa.py`.
- **What was modified:** Tinh chỉnh logic xử lý `overflow_to_sample_mapping`, điều chỉnh hyperparameters (`batch_size=16`, `fp16`) tối ưu cho GPU 6GB VRAM và bổ sung các ví dụ phân tích lỗi thực tế.
- **What was verified:** Kiểm chứng độc lập toàn bộ phép tính tay trong `calculations.md`, đối chiếu kết quả ánh xạ `offset_mapping` trên từng token cụ thể và kiểm tra các chỉ số EM/F1.
