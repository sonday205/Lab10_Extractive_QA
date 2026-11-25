# Prediction Before Experiment

Prediction 1: Trùng lặp từ khóa giữa câu hỏi và ngữ cảnh

Mô hình dễ bị nhầm ở giai đoạn đầu huấn luyện nếu đoạn văn chứa nhiều câu lặp lại từ khóa giống câu hỏi nhưng không chứa đáp án thật. Tuy nhiên, sau khi fine-tune đầy đủ, cơ chế Self-Attention của Transformer sẽ hiểu ngữ cảnh tốt hơn để phân biệt đúng chủ thể cần tìm và giảm lỗi nhầm lẫn này.

Prediction 2: Ảnh hưởng của độ dài đáp án đến dự đoán ranh giới

Đáp án càng dài thì việc dự đoán chính xác hai đầu ranh giới càng khó. Với đáp án ngắn 1 token, điểm đầu và điểm cuối trùng nhau nên mô hình dễ đoán đúng tuyệt đối. Với đáp án dài nhiều từ, mô hình dễ lấy thừa hoặc thiếu các từ phụ ở hai đầu như mạo từ hay giới từ, làm điểm Exact Match giảm mạnh dù F1 vẫn khá cao.

Prediction 3: Ngữ cảnh chứa nhiều thông tin không liên quan

Hiệu năng của mô hình sẽ giảm khi ngữ cảnh có quá nhiều thông tin thừa. Các đoạn văn nhiễu làm phân tán sự chú ý của mô hình, tạo thêm nhiều từ khóa gây nhiễu và dễ đẩy câu chứa đáp án thật ra ngoài giới hạn độ dài của một cửa sổ xử lý.

Prediction 4: Thay đổi thứ tự các câu trong ngữ cảnh

Việc đảo thứ tự câu có thể làm giảm nhẹ độ chính xác của mô hình. Khi thứ tự câu bị xáo trộn, mạch liên kết giữa các đại từ thay thế và danh từ gốc bị đứt gãy, đồng thời câu chứa đáp án có thể bị đẩy xuống cuối đoạn và rơi vào vùng bị cắt bớt.
