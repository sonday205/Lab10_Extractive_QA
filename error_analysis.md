# Error Analysis

## 1. Ví dụ có EM = 0 nhưng F1 > 0

Mẫu 1
Question: Who discovered penicillin?
Gold: Alexander Fleming
Prediction: Scottish physician Alexander Fleming
Giải thích: Mô hình lấy thừa chức danh đứng trước nên EM bằng 0, nhưng vẫn bao trọn tên đúng nên F1 đạt 0.67.

Mẫu 2
Question: Where is the headquarters of the UN located?
Gold: New York City
Prediction: New York
Giải thích: Mô hình dừng sớm và thiếu từ City ở cuối, trùng 2 trên 3 từ nên F1 đạt 0.80 nhưng EM bằng 0.

Mẫu 3
Question: When did World War II end?
Gold: September 2, 1945
Prediction: 1945
Giải thích: Mô hình chỉ trích xuất năm mà bỏ qua ngày tháng, đạt một phần thông tin đúng nên F1 đạt 0.50.

Mẫu 4
Question: What process converts light energy into chemical energy?
Gold: photosynthesis
Prediction: the process of photosynthesis
Giải thích: Mô hình lấy dư cụm từ dẫn nhập phía trước từ khóa chính nên chuỗi không khớp tuyệt đối, F1 đạt 0.50.

Mẫu 5
Question: What is the main component of Earth's atmosphere?
Gold: nitrogen (78%)
Prediction: nitrogen
Giải thích: Mô hình trích xuất đúng tên chất khí nhưng bỏ qua phần số liệu phần trăm trong ngoặc, F1 đạt 0.67.

## 2. Phân loại 15 mẫu lỗi

Nhóm 1: Wrong Start (5 mẫu)

Mẫu 1
Question: What city hosted the 2012 Summer Olympics?
Gold: London
Prediction: in London
Loại lỗi: wrong start. Mô hình lấy gộp cả giới từ in đứng ngay trước tên thành phố.

Mẫu 2
Question: Who wrote Pride and Prejudice?
Gold: Jane Austen
Prediction: author Jane Austen
Loại lỗi: wrong start. Mô hình lấy dư danh từ chỉ nghề nghiệp đứng liền trước tên tác giả.

Mẫu 3
Question: What currency is used in Japan?
Gold: Japanese yen
Prediction: yen
Loại lỗi: wrong start. Mô hình bỏ sót tính từ chỉ quốc gia đứng đầu cụm danh từ.

Mẫu 4
Question: Which river flows through Egypt?
Gold: Nile River
Prediction: longest Nile River
Loại lỗi: wrong start. Mô hình kéo nhầm tính từ bổ nghĩa phía trước vào điểm bắt đầu của đáp án.

Mẫu 5
Question: What gas do plants absorb from the air?
Gold: carbon dioxide
Prediction: absorb carbon dioxide
Loại lỗi: wrong start. Mô hình lấy nhầm động từ trùng với câu hỏi vào đầu đoạn trích xuất.

Nhóm 2: Wrong End (5 mẫu)

Mẫu 1
Question: Where is Columbia University located?
Gold: New York City
Prediction: New York
Loại lỗi: wrong end. Mô hình dừng sớm trước từ City vì New York đã là một địa danh quen thuộc.

Mẫu 2
Question: Who was the first president of the US?
Gold: George Washington
Prediction: George
Loại lỗi: wrong end. Mô hình ngắt sớm tại tên gọi thay vì lấy trọn cả họ và tên.

Mẫu 3
Question: What is the speed of light in vacuum?
Gold: 299,792,458 meters per second
Prediction: 299,792,458
Loại lỗi: wrong end. Mô hình chỉ lấy phần con số mà bỏ rơi đơn vị đo lường phía sau.

Mẫu 4
Question: Which company developed the iPhone?
Gold: Apple Inc.
Prediction: Apple
Loại lỗi: wrong end. Mô hình bỏ qua phần hậu tố pháp lý Inc. ở cuối tên công ty.

Mẫu 5
Question: What treaty ended World War I?
Gold: Treaty of Versailles
Prediction: Treaty
Loại lỗi: wrong end. Mô hình dừng ngay tại danh từ chính mà thiếu cụm giới từ bổ nghĩa phía sau.

Nhóm 3: Wrong Span (5 mẫu)

Mẫu 1
Question: When was the Eiffel Tower completed?
Gold: 1889
Prediction: 1887
Loại lỗi: distractor. Đoạn văn nhắc cả năm khởi công và năm hoàn thành, mô hình chọn nhầm mốc thời gian đầu tiên.

Mẫu 2
Question: Who succeeded Queen Victoria?
Gold: Edward VII
Prediction: Prince Albert
Loại lỗi: distractor. Mô hình bị nhiễu bởi tên người chồng xuất hiện nhiều lần trong cùng đoạn văn.

Mẫu 3
Question: What language is spoken in Brazil?
Gold: Portuguese
Prediction: Spanish
Loại lỗi: multiple plausible spans. Đoạn văn nhắc đến nhiều ngôn ngữ ở Nam Mỹ nên mô hình chọn nhầm ngôn ngữ phổ biến hơn.

Mẫu 4
Question: Why did the Roman Empire fall?
Gold: economic instability and invasions
Prediction: high taxes
Loại lỗi: partial answer. Đáp án chuẩn tổng hợp nhiều nguyên nhân nhưng mô hình chỉ lấy một ý nhỏ ở câu khác.

Mẫu 5
Question: What was the population in 2020?
Gold: 8.4 million
Prediction: 7.9 million
Loại lỗi: long context. Số liệu năm 2020 nằm gần cuối đoạn văn dài nên mô hình chọn nhầm số liệu năm cũ ở đầu đoạn.

## 3. So sánh Wrong Start và Wrong End

Trong tổng số 484 mẫu dự đoán sai trên tập validation, lỗi wrong start xuất hiện 138 lần, nhiều hơn lỗi wrong end với 103 lần. Nguyên nhân chính là do đặc điểm ngữ pháp tiếng Anh thường đặt các từ bổ nghĩa như mạo từ, giới từ, tính từ hoặc chức danh ở phía trước danh từ chính, khiến mô hình dễ phân vân khi xác định điểm bắt đầu. Ngược lại, điểm kết thúc của cụm danh từ thường nằm ngay trước dấu câu nên mô hình dễ nhận biết và khóa ranh giới chính xác hơn.