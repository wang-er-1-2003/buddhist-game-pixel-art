from PIL import Image, ImageDraw
import numpy as np
import os
from collections import deque

input_dir = r"D:\做个游戏\美术参考\建筑\需要加工"
output_dir = r"D:\做个游戏\美术参考\建筑\成品"
os.makedirs(output_dir, exist_ok=True)

def edge_cutout(img):
    img = img.convert("RGBA")
    arr = np.array(img)
    h, w = arr.shape[:2]
    # 标记所有近白像素（RGB>235，三通道都满足）
    white_mask = (arr[:,:,0] > 235) & (arr[:,:,1] > 235) & (arr[:,:,2] > 235)
    # BFS从四个角开始，找连通到边界的白色区域
    visited = np.zeros((h, w), dtype=bool)
    q = deque()
    # 把所有边界上的白色像素作为种子点
    for x in range(w):
        for y in [0, h-1]:
            if white_mask[y, x] and not visited[y, x]:
                q.append((y, x))
                visited[y, x] = True
    for y in range(h):
        for x in [0, w-1]:
            if white_mask[y, x] and not visited[y, x]:
                q.append((y, x))
                visited[y, x] = True
    # 洪水填充扩散
    while q:
        y, x = q.popleft()
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and white_mask[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))
    # 连通到边界的白色区域设为透明
    arr[visited, 3] = 0
    return Image.fromarray(arr)

for fname in os.listdir(input_dir):
    if not fname.lower().endswith(".png"):
        continue
    in_path = os.path.join(input_dir, fname)
    out_path = os.path.join(output_dir, fname)
    try:
        img = Image.open(in_path)
        cut = edge_cutout(img)
        cut.save(out_path)
        print(f"已抠图：{fname}")
    except Exception as e:
        print(f"抠图失败：{fname}，错误：{e}")
print("全部批量抠图完成")
