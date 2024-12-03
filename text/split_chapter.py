def split_chapter(filename, num_files):
    """
    将一个文件按照章节分割成多个文件
    :param filename: 文件名
    :param num_files: 分割数
    :return: 返回分割后的文件名列表
    """
    # 读取原始文件的内容到列表中
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # 计算每个文件应该包含的段落数量
    output_filenames = []
    num_lines = len(lines)
    print("章节总段落数：",(num_lines+1)//2)
    lines_per_file = num_lines // num_files
    print("每个文件段落数：")
    # 遍历要分割的文件数目
    for i in range(num_files):
        start_idx = i * lines_per_file  # 计算起始段落的索引
        end_idx = (i + 1) * lines_per_file if i < num_files - 1 else num_lines  # 计算结束段落的索引
        print((end_idx-start_idx+1)//2)

        # 构造输出文件名，以每个文件的第一段开头的四个汉字为文件名保存
        output_filename = f"D:/pythonProject/split_chapter/{lines[start_idx][:4]}.txt"
        output_filenames.append(output_filename)

        # 将切割后的段落写入新文件
        with open(output_filename, 'w', encoding='utf-8') as file:
            file.write("".join(lines[start_idx:end_idx])) # 把列表转化成str写入文件

    print("文件分割完成！")
    return output_filenames  # 返回输出文件名列表

