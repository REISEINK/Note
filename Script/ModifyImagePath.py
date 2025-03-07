import os
import re
from urllib.parse import quote

def convert_image_links(text):
    """
    将 Markdown 文件中的 ![[图片文件名]] 链接替换为 GitHub Raw 链接格式。
    例如：![[Pasted image 20240123154901.png]]
    转换为：![](https://raw.githubusercontent.com/REISEINK/Note/master/Figure/Pasted%20image%2020240123154901.png)
    """
    def repl(match):
        img_name = match.group(1)  # 获取图片文件名
        encoded_img_name = quote(img_name)  # 对文件名进行 URL 编码（处理空格等特殊字符）
        # 构造新的图片链接，仓库地址和 Figure 文件夹请根据实际情况调整
        new_link = f"![](https://raw.githubusercontent.com/REISEINK/Note/master/Figure/{encoded_img_name})"
        return new_link

    # 匹配形如 ![[...]] 的图片链接格式
    pattern = re.compile(r'!\[\[(.*?)\]\]')
    return pattern.sub(repl, text)

def process_markdown_files(directory):
    """
    遍历指定文件夹（包括子文件夹）中所有 Markdown 文件，
    对每个文件应用转换函数，并将转换后的内容写回原文件。
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".md"):
                file_path = os.path.join(root, file)
                print(f"正在处理文件：{file_path}")
                # 读取文件内容
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                # 替换图片链接
                new_content = convert_image_links(content)
                # 写回文件（可备份原文件以防万一）
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"处理完成：{file_path}")

if __name__ == "__main__":
    target_directory = "../"
    process_markdown_files(target_directory)
