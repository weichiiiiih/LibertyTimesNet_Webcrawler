#兩個檔案找相同的，不相同的存
# 到新檔案裡
def read_titles_from_file(file_path):
    titles = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    current_title = None
    current_index = None
    
    for line in lines:
        line = line.strip()
        if line.startswith('項目：'):
            current_index = line.split('：', 1)[1]
        elif line.startswith('標題：'):
            current_title = line.split('：', 1)[1]
            if current_index and current_title:
                titles[current_title] = current_index
    
    return titles

def get_matching_indices(file1_titles, file2_titles):
    matching_indices = set()
    
    for title, index in file1_titles.items():
        if title in file2_titles:
            matching_indices.add(file2_titles[title])
    
    return matching_indices

def filter_file(input_file_path, output_file_path, matching_indices):
    with open(input_file_path, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        current_index = None
        write_line = True
        for line in lines:
            line = line.strip()
            if line.startswith('項目：'):
                current_index = line.split('：', 1)[1]
                write_line = current_index not in matching_indices
            if write_line:
                outfile.write(line + '\n')
                if line.startswith('發表時間：'):
                    write_line = True  # Reset flag after writing complete item

# 文件路径
file1_path = '/Users/weichiiiiih/Desktop/Cword_mainland_all拷貝.txt'
file2_path = '/Users/weichiiiiih/Desktop/Cword_mainlander_all拷貝.txt'
output_file_path = '/Users/weichiiiiih/Desktop/mainlander_de.txt'

# 读取文件标题
file1_titles = read_titles_from_file(file1_path)
file2_titles = read_titles_from_file(file2_path)

# 获取匹配的项目编号
matching_indices = get_matching_indices(file1_titles, file2_titles)

# 过滤文件并写入新文件
filter_file(file2_path, output_file_path, matching_indices)

print(f"Filtered content has been written to {output_file_path}")
