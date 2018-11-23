# -*- coding:utf-8 -*-

import os
import re

class TextGenerator:

    def __init__(self, folder='../data/major_contracts_3000'):
        self.folder_path = folder

    def set_folder(self, folder):
        if os.path.isdir(folder):
            self.folder_path = folder
        else:
            print('TextGenerator: '+folder+' isn\'t a folder')

    def get_data_files(self):
        all_files = list()
        cur_files = os.listdir(self.folder_path)
        for file_name in cur_files:
            full_file = os.path.join(self.folder_path, file_name)
            
            if os.path.isfile(full_file):
                all_files.append(full_file)
        
        return all_files

    def article_generator(self):
        all_files = self.get_data_files()
        for file_path in all_files:
            with open(file_path) as file:
                article = str()
                for line in file:
                    article = article + line.decode('utf-8')
                
                yield article

    def sentence_generator(self):     
        generator = self.article_generator()
        for article in generator:
            
            start = current = 0
            flag = False
            length = len(article)
            while current < length:
                status = self.__is_valid(article[current])
                if not status and not flag:
                    start += 1
                elif status and not flag:
                    start += 1
                    flag = True
                elif not status and flag:
                    yield article[start:current]
                    start = current
                    flag = False
                
                current += 1

    def __is_valid(self, uchar):
        return self.__is_chinese(uchar) or uchar.isalpha()

    def __is_chinese(self, uchar):
        if uchar >= u'\u4e00' and uchar <= u'\u9fff':
            return True
        else:
            return False

    

    
