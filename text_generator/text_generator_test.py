# -*- coding:utf-8 -*-

from text_generator import TextGenerator

all_text = TextGenerator()

article_count = 5
generator = all_text.article_generator()
for i in range(article_count):
    cur_article = generator.next()
    print('article {0}'.format(i))
    print(cur_article+'\n')

sentence_count = 20
generator = all_text.sentence_generator()
for i in range(sentence_count):
    print(generator.next())

