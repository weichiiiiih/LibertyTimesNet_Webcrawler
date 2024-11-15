# 依據爬蟲結果，在兩個檔案中找到相同的篇名，並將不相同的部分存到新檔案裡
# 範例：檔案1的關鍵字為「日本」、檔案2的關鍵字為京都
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

# 更改檔案路径
# 範例：檔案1的關鍵字為「日本」、檔案2的關鍵字為京都
file1_path = '/Users/Desktop/keyword_Japan.txt'
file2_path = '/Users/Desktop/keyword_Kyoto.txt'
output_file_path = '/Users/Desktop/Japan_Kyoto_de.txt'

# 獲取檔案標題
file1_titles = read_titles_from_file(file1_path)
file2_titles = read_titles_from_file(file2_path)

# 獲取匹配的項目編號
matching_indices = get_matching_indices(file1_titles, file2_titles)

# 過濾檔案並寫入新檔案
filter_file(file2_path, output_file_path, matching_indices)

print(f"Filtered content has been written to {output_file_path}")
