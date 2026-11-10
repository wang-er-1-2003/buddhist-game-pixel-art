from PIL import Image
import numpy as np
import os

output_dir = r"D:\做个游戏\美术参考\建筑\成品"
special_files = ["庙市.png", "施粥棚.png", "素斋摊.png"]

for fname in special_files:
    path = os.path.join(output_dir, fname)
    if not os.path.exists(path):
        print(f"文件不存在：{fname}")
        continue
    img = Image.open(path).convert("RGBA")
    arr = np.array(img).astype(np.int16)
    h, w = arr.shape[:2]
    # 采样四角色值作为背景基准
    corner_pixels = [arr[0,0,:3], arr[0,w-1,:3], arr[h-1,0,:3], arr[h-1,w-1,:3]]
    bg_color = np.mean(corner_pixels, axis=0)
    tol = 40
    diff = np.abs(arr[:,:,:3] - bg_color)
    bg_mask = (diff[:,:,0] < tol) & (diff[:,:,1] < tol) & (diff[:,:,2] < tol)
    # 特殊处理：这三个棚子内部透空的背景白全部抠掉，不限制只从边缘开始
    arr[bg_mask, 3] = 0
    out = Image.fromarray(arr.astype(np.uint8), "RGBA")
    out.save(path)
    print(f"已处理特殊棚子：{fname}")
print("三个特殊摊位素材内部空白抠除完成")
