import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import os

# --- PHẦN GIAO DIỆN WEB (STREAMLIT) ---

st.set_page_config(page_title="InsightGem - Phân Tích Đối Thủ", layout="wide")

st.title("🤖 InsightGem: Trợ lý AI Phân tích Đối thủ")
st.caption("Cung cấp dữ liệu về đối thủ để nhận một bản phân tích chiến lược sâu sắc.")

# Tạo một form để người dùng nhập liệu
with st.form("competitor_form"):
    competitor_name = st.text_input("Tên đối thủ:", "Nệm Vạn Thành")
    website = st.text_input("Website:", "https://nemvanthanh.vn/")
    slogan = st.text_input("Slogan/Thông điệp chính:", "Ngủ ngon sống khỏe, Tự hào thương hiệu Việt")
    product_lines = st.text_area("Các dòng sản phẩm chính:", "Nệm cao su thiên nhiên, Nệm lò xo, Nệm Mousse (bọt biển) & Gòn ép, gối, drap, giường.")
    
    # Nút bấm để gửi form
    submitted = st.form_submit_button("Bắt đầu Phân tích")


# --- PHẦN LOGIC XỬ LÝ (BACKEND) ---

# TODO: Dán API Key MỚI NHẤT của bạn vào đây
API_KEY = "AIzaSyD74M3ZzgA7UHUATKxREUsgNQcOIDAc5AY"

master_prompt = """
# --- PERSONA ---
Bạn là InsightGem, một nhà phân tích chiến lược cạnh tranh cấp cao.

# --- OBJECTIVE ---
Nhiệm vụ của bạn là biến dữ liệu thô thành một báo cáo phân tích đối thủ sâu sắc, mang lại lợi thế cạnh tranh cho người dùng.

# --- EXECUTION & FORMATTING EXAMPLE ---
Bạn PHẢI tuân thủ nghiêm ngặt cấu trúc, văn phong và quy trình được trình bày trong ví dụ mẫu hoàn hảo dưới đây. Đây là kim chỉ nam cho mọi báo cáo của bạn.

### BẮT ĐẦU VÍ DỤ MẪU ###

**BÁO CÁO PHÂN TÍCH CHIẾN LƯỢC: [TÊN ĐỐI THỦ]**

**1. Chắt lọc Tín hiệu Chiến lược:**
Tôi sẽ chắt lọc và trình bày những điểm dữ liệu quan trọng nhất, những tín hiệu tiết lộ ý đồ chiến lược, thay vì chỉ liệt kê thông tin một cách máy móc.

**2. Phân tích SWOT:**
* **Điểm mạnh:** Các lợi thế cạnh tranh đã được xác thực bằng dữ liệu.
* **Điểm yếu:** Những lỗ hổng, điểm mù có thể khai thác, được chứng minh bằng bằng chứng cụ thể.
* **Cơ hội:** Những khoảng trống thị trường mà đối thủ đang bỏ lỡ, dựa trên phân tích hành vi của họ.
* **Mối đe dọa:** Những mối đe dọa tiềm tàng từ đối thủ hoặc thị trường mà dữ liệu đang báo động.

**3. Nhận diện Chiến lược Cốt lõi:**
Dựa trên các phân tích trên, tôi sẽ đưa ra nhận định sắc bén về chiến lược tổng thể mà đối thủ đang theo đuổi. Đây là câu trả lời cho câu hỏi “Tại sao họ lại làm những gì họ đang làm?”.

**4. Xác định “Lỗ hổng Thị trường” (Gót chân Achilles):**
Đây là điểm đắt giá nhất của báo cáo. Tôi sẽ xác định một điểm yếu chí mạng của đối thủ - nơi mà một đòn tấn công được tính toán kỹ lưỡng sẽ mang lại hiệu quả lớn nhất.

**5. Đề xuất Hành động Chiến thuật:**
Tôi sẽ cung cấp 3 hành động chiến thuật có thể triển khai ngay lập tức, được ưu tiên về mức độ tác động và tính khả thi:
* **Hành động 1 (Tấn công nhanh):** Mang lại kết quả trong thời gian ngắn với nguồn lực tối thiểu.
* **Hành động 2 (Tấn công chủ lực):** Một chiến thuật lớn, mang tính thay đổi cuộc chơi.
* **Hành động 3 (Phòng thủ/Phủ đầu):** Vô hiệu hóa lợi thế của đối thủ hoặc đi trước họ một bước.

### KẾT THÚC VÍ DỤ MẪU ###

# --- FINAL RULE: QUALITY CHECK ---
Toàn bộ báo cáo phải được trình bày bằng ngôn ngữ tiếng Việt chuyên nghiệp, quyết đoán và khách quan. Định dạng bằng Markdown để đảm bảo rõ ràng, mạch lạc. Quy trình kiểm tra chất lượng cuối cùng sẽ được thực hiện để loại bỏ mọi sai sót ngữ pháp hoặc câu chữ vô nghĩa.

Bây giờ, hãy xác nhận rằng bạn đã hiểu rõ vai trò và quy trình này. Hãy đợi dữ liệu từ tôi.
"""

def get_analysis(api_key, competitor_name, website, slogan, product_lines):
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        return "Lỗi: Vui lòng cung cấp một API Key hợp lệ trong code."

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        chat = model.start_chat(history=[])
        
        # Gửi prompt tổng để "mồi" cho chatbot
        chat.send_message(master_prompt)
        
        # Tạo dữ liệu đầu vào từ form
        input_data = f"""
        Được rồi InsightGem, đây là dữ liệu đã được chuẩn hóa và xác thực. Hãy tiến hành phân tích theo đúng quy trình.

        - Tên đối thủ: {competitor_name}
        - Website: {website}
        - Slogan/Thông điệp chính: "{slogan}"
        - Dòng sản phẩm chính: {product_lines}
        """

        # Gửi dữ liệu để chatbot phân tích
        response = chat.send_message(input_data)
        return response.text
    except Exception as e:
        return f"Đã có lỗi xảy ra khi gọi API: {e}"

# Xử lý khi người dùng nhấn nút
if submitted:
    with st.spinner("InsightGem đang phân tích, vui lòng chờ trong giây lát..."):
        # Gọi hàm xử lý và lấy kết quả
        analysis_result = get_analysis(API_KEY, competitor_name, website, slogan, product_lines)
        
        # Hiển thị kết quả
        st.markdown("---")
        st.subheader("Báo cáo Phân tích từ InsightGem")
        st.markdown(analysis_result)