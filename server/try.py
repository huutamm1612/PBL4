import torch

print(torch.cuda.is_available())
# Kiểm tra GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Tạo một ma trận ngẫu nhiên 5x5 trên GPU
matrix = torch.rand(5, 5, device=device)

# In ra ma trận
print("Ma trận gốc:")
print(matrix)

# Đặt vị trí (x, y)
x, y = 2, 2  # Vị trí bất kỳ trong ma trận

# Lấy đường chéo chính
diagonal_main = matrix.diagonal(offset=y - x)

# Lấy đường chéo phụ
diagonal_anti = matrix.diagonal(offset=x + y - matrix.size(0) + 1)

# In ra các phần tử trên đường chéo
print(f"\nCác phần tử trên đường chéo chính đi qua ({x}, {y}):", diagonal_main)
print(f"Các phần tử trên đường chéo phụ đi qua ({x}, {y}):", diagonal_anti)
