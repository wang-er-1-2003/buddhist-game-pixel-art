from PIL import Image
import numpy as np
import os
from collections import deque

input_dir = r"D:\做个游戏\美术参考\建筑\需要加工"
output_dir = r"D:\做个游戏\美术参考\建筑\成品"
os.makedirs(output_dir, exist_ok=True)

def smart_cutout(img):
    img = img.convert("RGBA")
    arr = np.array(img).astype(np.int16)
    h, w = arr.shape[:2]
    # 采样四个角的实际背景颜色，取平均作为基准背景色
    corner_pixels = [
        arr[0,0,:3], arr[0,w-1,:3], arr[h-1,0,:3], arr[h-1,w-1,:3]
    ]
    bg_color = np.mean(corner_pixels, axis=0)
    # 容差设为35，覆盖校色后背景的浅米黄/暖灰偏移
    tol = 35
    # 标记和背景色差值在容差内的候选背景像素
    diff = np.abs(arr[:,:,:3] - bg_color)
    bg_mask = (diff[:,:,0] < tol) & (diff[:,:,1] < tol) & (diff[:,:,2] < tol)
    # BFS从所有边界点开始，只抠连通到边界的背景
    visited = np.zeros((h, w), dtype=bool)
    q = deque()
    for x in range(w):
        for y in [0, h-1]:
            if bg_mask[y, x] and not visited[y, x]:
                q.append((y, x))
                visited[y, x] = True
    for y in range(h):
        for x in [0, w-1]:
            if bg_mask[y, x] and not visited[y, x]:
                q.append((y, x))
                visited[y, x] = True
    while q:
        y, x = q.popleft()
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx] and bg_mask[ny, nx]:
                visited[ny, nx] = True
                q.append((ny, nx))
    # 连通到边界的背景设为透明
    arr[visited, 3] = 0
    return Image.fromarray(arr.astype(np.uint8), "RGBA")

for fname in os.listdir(input_dir):
    if not fname.lower().endswith(".png"):
        continue
    in_path = os.path.join(input_dir, fname)
    out_path = os.path.join(output_dir, fname)
    try:
        img = Image.open(in_path)
        cut = smart_cutout(img)
        cut.save(out_path)
        print(f"已回炉抠图：{fname}")
    except Exception as e:
        print(f"抠图失败：{fname}，错误：{e}")
print("全部回炉抠图完成")
