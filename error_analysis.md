# Error Analysis

## Phạm vi và cách phân loại

Phân tích được tạo từ 2.000 dự đoán trong `artifacts/best_predictions.csv` của lần chạy lại (SQuAD v1.1 validation, seed 42, max_length=384). Mẫu lỗi được chọn trực tiếp từ các dòng có EM = 0; không dùng ví dụ tự tạo. Phân loại ranh giới dựa trên vị trí chuỗi prediction và gold xuất hiện trong context. Nếu context có nhiều lần xuất hiện, chọn occurrence gần vị trí gold nhất. Đây là heuristic phân tích, nên một số mẫu có thể được xếp vào nhóm wrong-span dù bản chất là distractor hoặc câu trả lời dài.

## Kết quả tổng hợp

- Số mẫu: 2000
- EM = 0: 659 (32.95%)
- EM = 0 và F1 > 0: 391 mẫu
- EM = 0 và F1 = 0: 268 mẫu

| Nhóm lỗi (heuristic) | Số mẫu EM=0 |
|---|---:|
| Wrong start | 133 |
| Wrong end | 96 |
| Sai cả start/end | 74 |
| Wrong span / distractor | 356 |

Tổng nhóm trên bằng số mẫu EM=0. Nhãn wrong-span/distractor được gộp khi prediction và gold không giao nhau; để tách nguyên nhân ngữ nghĩa cần đọc context từng mẫu.

## 5 ví dụ EM=0, F1>0 lấy từ dự đoán thực tế

### Ví dụ 1
- Question: In 1890, who did the university decide to team up with?
- Gold: several regional colleges and universities
- Prediction: University of Chicago
- Nhóm: wrong_span_or_distractor
- F1: 0.1538

### Ví dụ 2
- Question: What does LGM stands for?
- Gold: Last Glacial Maximum
- Prediction: Amazon rainforest vegetation over the last 21,000 years through the Last Glacial Maximum
- Nhóm: wrong_start
- F1: 0.4286

### Ví dụ 3
- Question: What is the paper written by Richard Karp in 1972 that ushered in a new era of understanding between intractability and NP-complete problems?
- Gold: "Reducibility Among Combinatorial Problems"
- Prediction: Reducibility
- Nhóm: wrong_start_and_end
- F1: 0.4000

### Ví dụ 4
- Question: What Lake in a German island Mainau receives a fraction of the Rhine's flow?
- Gold: Lake Überlingen
- Prediction: Überlingen
- Nhóm: wrong_start
- F1: 0.6667

### Ví dụ 5
- Question: How was the civil disobedience shown in Antigone?
- Gold: obey her conscience rather than human law
- Prediction: she is afraid of how her conscience will smite her if she does not do this.
- Nhóm: wrong_span_or_distractor
- F1: 0.2286

## 15 mẫu lỗi tiêu biểu từ lần chạy

### Wrong start

- **Question:** What does LGM stands for?
  - Gold: Last Glacial Maximum
  - Prediction: Amazon rainforest vegetation over the last 21,000 years through the Last Glacial Maximum
  - F1: 0.4286
- **Question:** What Lake in a German island Mainau receives a fraction of the Rhine's flow?
  - Gold: Lake Überlingen
  - Prediction: Überlingen
  - F1: 0.6667
- **Question:** Where do juvenile platyctenids live?
  - Gold: among the plankton
  - Prediction: bottom-dwelling platyctenids, the juveniles behave more like true larvae, as they live among the plankton
  - F1: 0.2667
- **Question:** When were Joseph Schumpeter and Norman Angell at their most prolific writing period?
  - Gold: before World War I
  - Prediction: 1872–1967). While these non-Marxist writers were at their most prolific before World War I
  - F1: 0.4444

### Wrong end

- **Question:** Name one country that banned boating, driving and flying on Sundays.
  - Gold: Germany
  - Prediction: Germany, Italy, Switzerland and Norway
  - F1: 0.3333
- **Question:** What topic do private bills typically have?
  - Gold: large-scale development projects
  - Prediction: large-scale development projects such as infrastructure projects that require the use of land or property
  - F1: 0.3529
- **Question:** What does the First Company Law Directive article 11 require?
  - Gold: incorporations would only be nullified for a fixed list of reasons
  - Prediction: incorporations
  - F1: 0.1818
- **Question:** What did Stiglitz present in 2009 regarding global inequality?
  - Gold: evidence
  - Prediction: evidence in 2009 that both global inequality and inequality within countries prevent growth by limiting aggregate demand
  - F1: 0.2105

### Sai cả start/end

- **Question:** What is the paper written by Richard Karp in 1972 that ushered in a new era of understanding between intractability and NP-complete problems?
  - Gold: "Reducibility Among Combinatorial Problems"
  - Prediction: Reducibility
  - F1: 0.4000
- **Question:** What did Warsz own?
  - Gold: a village
  - Prediction: Warsz was a 12th/13th-century nobleman who owned a village located at the modern-day site of Mariensztat neighbourhood.
  - F1: 0.1333
- **Question:** What kind of light is important for chloroplasts to divide?
  - Gold: bright white light
  - Prediction: white
  - F1: 0.6667
- **Question:** Why do carotenoids make leaves change color in the fall?
  - Gold: their bright colors sometimes override the chlorophyll green
  - Prediction: sometimes override the chlorophyll green, like during the fall, when the leaves of some land plants
  - F1: 0.4000

### Wrong span / distractor

- **Question:** In 1890, who did the university decide to team up with?
  - Gold: several regional colleges and universities
  - Prediction: University of Chicago
  - F1: 0.1538
- **Question:** At what address did Goldenson secure a new headquarters for ABC?
  - Gold: 1330 Avenue of the Americas in Manhattan
  - Prediction: 7 West 66th Street
  - F1: 0.0000
- **Question:** How was the civil disobedience shown in Antigone?
  - Gold: obey her conscience rather than human law
  - Prediction: she is afraid of how her conscience will smite her if she does not do this.
  - F1: 0.2286

## Nhận xét

Các lỗi ranh giới vẫn xuất hiện khi prediction trích được một phần đáp án. Nhóm wrong-span/distractor chiếm nhiều nhất theo phép phân loại chuỗi ở trên; cần xem context để xác định chính xác lý do ngữ nghĩa của từng mẫu. EM đánh giá khớp hoàn toàn sau chuẩn hóa, còn F1 ghi nhận phần token giao nhau, vì vậy có 391 mẫu EM=0 nhưng F1>0 trong lần chạy này.
