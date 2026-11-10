from PIL import Image
import numpy as np
import os

output_dir = r"D:\做个游戏\美术参考\建筑\成品"
rail_files = ["义冢.png", "药园.png", "码头.png"]

for fname in rail_files:
    path = os.path.join(output_dir, fname)
    if not os.path.exists(path):
        print(f"文件不存在：{fname}")
        continue
    img = Image.open(path).convert("RGBA")
    arr = np.array(img).astype(np.int16)
    h, w = arr.shape[:2]
    corner_pixels = [arr[0,0,:3], arr[0,w-1,:3], arr[h-1,0,:3], arr[h-1,w-1,:3]]
    bg_color = np.mean(corner_pixels, axis=0)
    tol = 40
    diff = np.abs(arr[:,:,:3] - bg_color)
    bg_mask = (diff[:,:,0] < tol) & (diff[:,:,1] < tol) & (diff[:,:,2] < tol)
    # 栏杆缝隙里的背景白全部抠掉
    arr[bg_mask, 3] = 0
    out = Image.fromarray(arr.astype(np.uint8), "RGBA")
    out.save(path)
    print(f"已处理栏杆空隙：{fname}")
print("三个带栏杆素材的空隙白全部抠除完成")
