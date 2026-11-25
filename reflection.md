# Reflection: Từ Classification đến Span Prediction

## Sơ đồ chuyển đổi kiến trúc từ LAB 08 đến LAB 10

Pretrained Transformer nhận chuỗi đầu vào và tạo ra các vector biểu diễn ngữ cảnh, sau đó phân nhánh theo từng bài toán:

1,Từ vector đại diện [CLS] đi qua lớp tuyến tính để phân loại văn bản ở LAB 08.

2,Từ chuỗi vector của từng token đi qua bộ phân loại dùng chung để gán nhãn thực thể ở LAB 09.

3,Từ chuỗi vector của từng token đi qua hai bộ phân loại độc lập để tìm vị trí bắt đầu và kết thúc đáp án ở LAB 10.

## Giải thích sự khác biệt về Prediction Head và Target

Qua chuỗi thực hành từ LAB 08 đến LAB 10, điểm cốt lõi nhất là sự tách biệt giữa mô hình nền tảng Pretrained Transformer và đầu dự đoán chuyên biệt cho từng nhiệm vụ. Cả ba bài toán đều dùng chung một bộ mã hóa Transformer đã huấn luyện trước để biến văn bản thành các vector biểu diễn giàu ngữ cảnh. Nhờ cơ chế Self-Attention, mỗi từ trong chuỗi đều mang thông tin liên kết với toàn bộ câu. Tuy nhiên, cách khai thác các vector này và mục tiêu học lại hoàn toàn khác nhau.

Ở LAB 08 với bài toán Sequence Classification, mục tiêu là gán một nhãn duy nhất cho toàn bộ đoạn văn bản. Vì chỉ cần thông tin tổng hợp của cả chuỗi, mô hình lấy vector tại vị trí token đặc biệt [CLS] và đưa qua một lớp tuyến tính để dự đoán nhãn. Sang đến LAB 09 với bài toán Token Classification, nhiệm vụ đòi hỏi nhận diện thực thể ở mức độ từng từ. Do đó, mô hình giữ lại toàn bộ chuỗi vector đầu ra và áp dụng một bộ phân loại dùng chung lên từng token để gán nhãn tương ứng.

Đến LAB 10 với bài toán Extractive Question Answering, đầu vào gồm câu hỏi ghép với đoạn ngữ cảnh, và nhiệm vụ chuyển sang Span Prediction. Thay vì phân loại cả câu hay gán nhãn từng từ rời rạc, mục tiêu là trích xuất một đoạn văn bản liên tục chứa câu trả lời. Vì vậy, đầu dự đoán sử dụng hai bộ phân loại độc lập chiếu lên chuỗi token để tìm xác suất vị trí bắt đầu và vị trí kết thúc của đáp án. Như vậy, Pretrained Transformer đóng vai trò là bộ trích xuất đặc trưng ngữ cảnh chung, còn việc thiết kế đầu vào, hàm mất mát và prediction head mới là yếu tố quyết định loại bài toán NLP được giải quyết.