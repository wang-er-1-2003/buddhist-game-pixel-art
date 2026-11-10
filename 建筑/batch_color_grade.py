from PIL import Image
import numpy as np
import os

input_dir = r"D:\做个游戏\美术参考\建筑\需要先换色"
output_dir = r"D:\做个游戏\美术参考\建筑\需要加工"
os.makedirs(output_dir, exist_ok=True)

def grade_one(img):
    img = img.convert("RGBA")
    arr = np.array(img).astype(np.float32)
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]

    # 基础全局降饱和
    gray = 0.299*r + 0.587*g + 0.114*b
    sat_factor = 0.45
    r = gray + (r - gray)*sat_factor
    g = gray + (g - gray)*sat_factor
    b = gray + (b - gray)*sat_factor

    # 分通道色阶
    r[r>180] = r[r>180] * 0.75
    b[b<80] = b[b<80] * 0.8 + 25

    # 色相偏移
    red_mask = (r > g + 20) & (r > b + 30)
    g[red_mask] += 15
    b[red_mask] -= 5
    stone_mask = (abs(r-g) < 12) & (b < r) & (r > 90) & (r < 180)
    r[stone_mask] += 12
    g[stone_mask] += 8

    # 分层光影
    lum = 0.299*r + 0.587*g + 0.114*b
    high_mask = lum > 200
    r[high_mask] += 12
    g[high_mask] += 8
    b[high_mask] -= 5
    low_mask = lum < 70
    r[low_mask] += 8
    g[low_mask] += 4
    gold_mask = (r > 140) & (g > 110) & (b < 90)
    r[gold_mask] *= 0.65
    g[gold_mask] *= 0.58
    b[gold_mask] *= 0.45

    # sepia旧化
    sepia = 0.15
    r = r*(1-sepia) + 190*sepia
    g = g*(1-sepia) + 170*sepia
    b = b*(1-sepia) + 130*sepia

    # 色阶分离
    step = 24
    r = (r // step) * step
    g = (g // step) * step
    b = (b // step) * step

    arr[:,:,0] = np.clip(r, 0, 255)
    arr[:,:,1] = np.clip(g, 0, 255)
    arr[:,:,2] = np.clip(b, 0, 255)
    out = Image.fromarray(arr.astype(np.uint8), "RGBA")

    # 最近邻重采样对齐像素粒度
    w, h = out.size
    out = out.resize((int(w*0.58), int(h*0.58)), Image.Resampling.NEAREST)
    out = out.resize((w, h), Image.Resampling.NEAREST)
    return out

for fname in os.listdir(input_dir):
    if not fname.lower().endswith((".png", ".jpg", ".jpeg")):
        continue
    in_path = os.path.join(input_dir, fname)
    out_path = os.path.join(output_dir, fname)
    try:
        img = Image.open(in_path)
        graded = grade_one(img)
        graded.save(out_path)
        print(f"已处理：{fname}")
    except Exception as e:
        print(f"处理失败：{fname}，错误：{e}")
print("全部批量校色完成")
