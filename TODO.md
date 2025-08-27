## 1. Project Setup
- [x] Thêm pre-commit hooks (`check-added-large-files`)
- [ ] Thiết lập cấu trúc thư mục project (src/, tests/, app/, etc.)

---

## 2. Data Handling
- [x] Thu thập data
- [x] Làm sạch và chuẩn hóa dữ liệu (cleaning, formatting, handle missing)

---

## 3. Model Training
- [x] Train ML model
- [ ] Evaluate model (accuracy, precision, recall, F1-score)
- [ ] Lưu model (`.pkl`, `.joblib`, `.h5`)

---

## 4. API Development
- [ ] Viết pipeline: tiền xử lý dữ liệu trước khi predict (inference-time preprocessing)
- [ ] Viết API (FastAPI) để nhận input và trả kết quả dự đoán (Tích hợp pipeline xử lý dữ liệu trong endpoint `/predict`)
- [ ] Viết `Pydantic` model cho dữ liệu đầu vào (request)
- [ ] Viết `Pydantic` model cho dữ liệu đầu ra (response)

---

## 5. Deployment
- [ ] Viết `Dockerfile` để đóng gói app
- [ ] Tạo file `requirements.txt`
- [ ] Kiểm thử chạy Docker container local

---

## 6. Documentation
- [ ] Viết tài liệu `README.md` đầy đủ
  - Hướng dẫn cài đặt & chạy local
  - Ví dụ usage (curl / HTTP client)
  - Cách build docker

---------
Fix: 
- [ ] Sửa lại học lực: 1: tốt, 2: khá, 3: đạt, 4: chưa đạt.
- [ ] Sửa lại hạnh kiểm: 1: tốt, 2: khá, 3: đạt, 4: chưa đạt.
- [ ] Rmit -> hb_12 -> 1