# 生成专家的节点csv文件
# 主键是 'author_id',内容为'author-' + 知网的 'code'，例如 'author-12345678'

import csv
import os
import file_util

class AuthorGenerator:
    input_path = "" # 原始论文文件目录
    output_filename = "../data_output/node_authors.csv"
    author_header = ['author_id:ID', 'name', ':LABEL']

    def __init__(self, input_path):
        self.input_path = input_path
        file_util.FileUtil.write_header(self.output_filename, self.author_header)

    def generate_one_file(self, input_filename):
        num = 0 #生成的节点或关系数
        actual_filename = self.input_path + '/' + input_filename
        with open(actual_filename, 'r', encoding='utf-8') as fin:
            reader = csv.DictReader(fin)
            with open(self.output_filename, 'a+', encoding='utf-8', newline='') as fout:
                writer = csv.DictWriter(fout, self.author_header)
                for row in reader:
                    authors_str = row['authors']
                    if len(authors_str) < 1:
                        continue
                    # 得到 作者-code形式的元组
                    authors_with_link = authors_str.split('&')
                    author_row = {}  # 待存入的一行作者的信息
                    for awl in authors_with_link:
                        author_row[':LABEL'] = 'Author'  # 打上author的node标签
                        # 提取出作者的名字、code，把code作为唯一id，利用知网帮忙去重
                        # todo 这里有个问题，有的人code是null，所以如果链接是null
                        if len(awl) > 0:
                            # 提取名字
                            name = awl.split('-')[0]
                            author_row['name'] = name
                            # 提取作者的code,因为code是纯数字，所以加个英文开头好些，直观，又不容易重复
                            id =  awl.split('-')[1]
                            # 如果人的code是null，就暂时将名字作为唯一id
                            if id != 'null':
                                author_row['author_id:ID'] = 'author-' +id
                            else:
                                author_row['author_id:ID'] = name
                            writer.writerow(author_row)
                            num += 1
        return num

    def generate(self):
        '''
        提取某个指定目录下的所有文件或节点
        :return:
        '''
        for one_file in os.listdir(self.input_path):
            print('开始抽取', one_file, '的节点及关系信息')
            num = self.generate_one_file(one_file)
            print('从', one_file, '中抽取了', num, '个节点或关系信息, 保存至', self.output_filename)




if __name__ == '__main__':
    g = AuthorGenerator('../data_input/qikan')
    # g.generate_one_file('2021_journal.csv')
    g.generate()