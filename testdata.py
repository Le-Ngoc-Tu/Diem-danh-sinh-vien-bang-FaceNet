import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# Dữ liệu cho các mô hình
data = {
    "Phương pháp": ["FaceNet", "DeepFace", "OpenFace", "VGGFace"],
    "Độ chính xác (%)": [98.5, 97.0, 96.5, 98.0],
    "Recall (%)": [97.0, 95.5, 94.0, 96.5],
    "Tỷ lệ sai (%)": [1.5, 2.0, 2.5, 2.0]
}

# Chuyển dữ liệu thành DataFrame
df = pd.DataFrame(data)

# Đặt kiểu hiển thị của Seaborn
sns.set(style="whitegrid")

# Thiết lập biểu đồ
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

# Vẽ biểu đồ cột cho Độ chính xác
sns.barplot(x="Phương pháp", y="Độ chính xác (%)", data=df, ax=ax[0])
ax[0].set_title("So sánh Độ chính xác giữa các mô hình")
# Vẽ đường màu đỏ qua các điểm cao nhất
max_accuracy = df["Độ chính xác (%)"]
ax[0].plot(df["Phương pháp"], max_accuracy, 'ro-', linestyle='--', linewidth=2)

# Vẽ biểu đồ cột cho Recall
sns.barplot(x="Phương pháp", y="Recall (%)", data=df, ax=ax[1])
ax[1].set_title("So sánh Recall giữa các mô hình")
# Vẽ đường màu đỏ qua các điểm cao nhất
max_recall = df["Recall (%)"]
ax[1].plot(df["Phương pháp"], max_recall, 'ro-', linestyle='--', linewidth=2)

# Vẽ biểu đồ cột cho Tỷ lệ sai
sns.barplot(x="Phương pháp", y="Tỷ lệ sai (%)", data=df, ax=ax[2])
ax[2].set_title("So sánh Tỷ lệ sai giữa các mô hình")
# Vẽ đường màu đỏ qua các điểm cao nhất
max_error_rate = df["Tỷ lệ sai (%)"]
ax[2].plot(df["Phương pháp"], max_error_rate, 'ro-', linestyle='--', linewidth=2)

# Kiểm tra và tạo thư mục 'train_img' nếu chưa tồn tại
output_dir = "train_img"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Lưu biểu đồ vào thư mục train_img
output_path = os.path.join(output_dir, "comparison_charts_with_lines.png")
plt.tight_layout()
plt.savefig(output_path)

# Hiển thị biểu đồ
plt.show()
