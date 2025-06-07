import streamlit as st
import hashlib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

# Hàm sinh MD5
def generate_md5(seed):
    return hashlib.md5(seed.encode()).hexdigest()

# Trích xuất đặc trưng từ MD5
def extract_features(md5_hash):
    return [int(md5_hash[i:i+2], 16) for i in range(0, 32, 2)]

# Tạo dữ liệu huấn luyện giả lập
@st.cache_data
def fake_data(seed_base="2025-06-07", rounds=1000):
    data = []
    for i in range(rounds):
        seed = f"{seed_base}:{i}"
        md5 = generate_md5(seed)
        last5 = int(md5[-5:], 16)
        d1 = (last5 >> 0) & 0x1F % 6 + 1
        d2 = (last5 >> 5) & 0x1F % 6 + 1
        d3 = (last5 >> 10) & 0x1F % 6 + 1
        total = d1 + d2 + d3
        result = "Tài" if total >= 11 else "Xỉu"
        features = extract_features(md5)
        data.append({"features": features, "result": 1 if result == "Tài" else 0})
    return pd.DataFrame(data)

# Giao diện Streamlit
st.title("🔮 Dự Đoán Tài Xỉu Từ Mã MD5")

# Huấn luyện mô hình
data = fake_data()
X = list(data['features'])
y = list(data['result'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Nhập seed
seed_input = st.text_input("🔑 Nhập Seed (VD: 2025-06-08:00)", "2025-06-08:00")

if seed_input:
    md5_input = generate_md5(seed_input)
    feature_input = extract_features(md5_input)
    prediction = model.predict([feature_input])[0]
    result = "🎯 TÀI" if prediction == 1 else "❄️ XỈU"

    st.markdown(f"**MD5:** `{md5_input}`")
    st.subheader(f"Kết quả dự đoán: {result}")
