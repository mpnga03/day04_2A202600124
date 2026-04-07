# ✈️ TravelBuddy - AI Travel Agent

TravelBuddy là một AI Agent thông minh được xây dựng bằng **LangGraph** và **LangChain**, đóng vai trò như một trợ lý du lịch thân thiện. Hệ thống có khả năng tự động lập luận và gọi các công cụ (tools) để tra cứu chuyến bay, tìm khách sạn và tính toán ngân sách cho các chuyến đi tại Việt Nam.

## ✨ Tính năng nổi bật

- **Multi-Step Tool Chaining:** Tự động kết nối các công cụ (Tìm chuyến bay ➡️ Tính toán ngân sách ➡️ Tìm khách sạn phù hợp).
- **Tra cứu thông minh:** Hỗ trợ tra cứu ngược chiều chuyến bay nếu tuyến đường chính không có sẵn.
- **Quản lý ngân sách:** Tự động tính toán tổng chi phí và cảnh báo nếu lịch trình vượt quá ngân sách của khách hàng.
- **Guardrails (Ràng buộc an toàn):** Từ chối trả lời các câu hỏi ngoài lề (code, chính trị, toán học) và tuân thủ định dạng phản hồi chuẩn.

## 📂 Cấu trúc thư mục

```text
travelbuddy/
│
├── agent.py            # Chứa logic chính của LangGraph, khởi tạo Agent và Chat loop
├── tools.py            # Chứa mock database và định nghĩa các tools (@tool)
├── system_prompt.txt   # File cấu hình Persona, Rules và Workflow cho LLM
└── README.md
