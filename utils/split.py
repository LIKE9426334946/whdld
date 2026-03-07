# utils/split.py
# 将数据集随机划分为train、val、test三个集合，并保存为txt文件

import os, random
from typing import List

def make_splits(root: str, images_dir: str, ratio=(0.8,0.1,0.1), seed: int = 42, out_dir: str = None): # 不改就为默认值
    img_dir = os.path.join(root, images_dir) # /kaggle/input/datasets/thenoart/whdld-data/image/Images
    names = [os.path.splitext(fn)[0] for fn in sorted(os.listdir(img_dir))
             if fn.lower().endswith((".jpg",".jpeg",".png"))] # 得到原始图片的所有文件名，不包括扩展名，并把它们保存为一个列表

    random.seed(seed)
    random.shuffle(names)  # 将顺序打乱

    n = len(names)
    n_train = int(n * ratio[0])
    n_val = int(n * ratio[1])

    # 划分数据
    train_ids = names[:n_train] # 共3952张图片
    val_ids = names[n_train:n_train+n_val]
    test_ids = names[n_train+n_val:]

    split_dir = out_dir if out_dir is not None else os.path.join(root, "splits")
    os.makedirs(split_dir, exist_ok=True)

    def dump(path: str, items: List[str]):
        with open(path, "w") as f:
            for x in items:
                f.write(x + "\n")

    dump(os.path.join(split_dir, "train.txt"), train_ids)
    dump(os.path.join(split_dir, "val.txt"), val_ids)
    dump(os.path.join(split_dir, "test.txt"), test_ids)

    return train_ids, val_ids, test_ids, split_dir

def read_split(path: str):
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]
