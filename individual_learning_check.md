# Individual Learning Check

## 1. Extractive QA khác classification như thế nào?
Classification gán một nhãn cố định cho toàn bộ đoạn văn bản dựa trên vector đại diện chung. Ngược lại, Extractive QA tìm vị trí bắt đầu và kết thúc để trích xuất một đoạn văn bản con liên tục bên trong ngữ cảnh làm câu trả lời.

## 2. Tại sao QA cần start và end position?
Câu trả lời là một đoạn văn bản liên tục có độ dài thay đổi tùy theo từng câu hỏi. Việc dự đoán đồng thời hai vị trí bắt đầu và kết thúc giúp mô hình khoanh vùng trọn vẹn cả đoạn đáp án mà không bị đứt quãng.

## 3. Character offset khác token index như thế nào?
Character offset là vị trí đếm theo từng ký tự trong chuỗi văn bản gốc, bao gồm cả khoảng trắng và dấu câu. Token index là vị trí thứ tự của từng từ hoặc mảnh từ sau khi văn bản đã được tách từ và chèn thêm các token đặc biệt.

## 4. Tại sao cần offset mapping?
Dữ liệu huấn luyện cung cấp vị trí đáp án theo ký tự, trong khi mô hình Transformer lại tính toán và dự đoán dựa trên chỉ số token. Offset mapping đóng vai trò cầu nối ánh xạ qua lại giữa hai hệ tọa độ này để gán nhãn khi học và cắt đúng chuỗi văn bản khi dự đoán.

## 5. Stride dùng để làm gì?
Stride quy định số lượng token gối đầu lên nhau giữa hai cửa sổ trượt liên tiếp khi chia nhỏ một ngữ cảnh dài. Nhờ phần chồng lấn này, nếu câu trả lời nằm đúng ranh giới bị cắt ở cửa sổ trước thì nó vẫn xuất hiện nguyên vẹn ở cửa sổ tiếp theo.

## 6. Vì sao context dài có thể phải chia thành nhiều window?
Các mô hình Transformer tiêu chuẩn có giới hạn cứng về độ dài chuỗi đầu vào tối đa, thường là 384 hoặc 512 token. Ngoài ra, chi phí bộ nhớ của cơ chế tự chú ý tăng rất nhanh theo bình phương độ dài chuỗi nên cần chia nhỏ ngữ cảnh thành nhiều cửa sổ để xử lý.

## 7. Exact Match đo điều gì?
Exact Match đo tỷ lệ phần trăm các câu hỏi mà câu trả lời do mô hình dự đoán khớp chính xác từng ký tự với đáp án chuẩn sau khi đã đưa về chữ thường, bỏ dấu câu và mạo từ.

## 8. F1 của QA khác gì với accuracy?
Accuracy chỉ đánh giá đúng hoặc sai hoàn toàn trên toàn bộ mẫu dự đoán. Trong khi đó, F1 của QA tính mức độ trùng lặp ở cấp độ từng từ giữa câu dự đoán và đáp án chuẩn, giúp ghi nhận điểm thành phần ngay cả khi mô hình chỉ đoán đúng một phần.

## 9. Vì sao prediction có thể có $F1 > 0$ nhưng $EM = 0$?
Trường hợp này xảy ra khi câu dự đoán có chứa một vài từ trùng với đáp án chuẩn nên điểm $F1 > 0$, nhưng lại bị thừa hoặc thiếu một số từ ở hai đầu khiến hai chuỗi không giống nhau hoàn toàn nên $EM = 0$.

## 10. Wrong-start và wrong-end khác nhau như thế nào?
Wrong-start là lỗi mô hình chọn đúng điểm kết thúc nhưng lệch điểm bắt đầu, thường do lấy thừa mạo từ, giới từ hoặc bỏ sót tính từ đứng trước. Ngược lại, wrong-end là lỗi chọn đúng điểm mở đầu nhưng ngắt quá sớm hoặc kéo dài quá mức ở phần cuối cụm từ.

## 11. Extractive QA khác RAG ở đâu?
Extractive QA giả định đã có sẵn một đoạn ngữ cảnh chứa thông tin và chỉ trích xuất nguyên văn câu trả lời từ đoạn đó. Ngược lại, RAG phải tự tìm kiếm các tài liệu liên quan từ một kho dữ liệu lớn rồi mới dùng mô hình sinh văn bản để tổng hợp câu trả lời hoàn chỉnh.

## 12. Khi nào extractive QA không thể trả lời câu hỏi?
Mô hình không thể trả lời khi thông tin cần tìm hoàn toàn không xuất hiện trong đoạn ngữ cảnh được cung cấp, hoặc khi câu hỏi đòi hỏi phải suy luận, tính toán và tổng hợp từ nhiều câu rời rạc không nằm liền nhau.