#!/usr/bin/env python

########################################
### C-Learning 小テスト設定項目 
### (必要に応じて編集してください)
common_setting='''
"合格点数","0"
"制限時間","0"
"公開予定日時(年/月/日 時:分)",""
"締切予定日時(年/月/日 時:分)",""
"選択肢の表示方法","3"
"選択肢の並び順","0"
"点数の公開","1"
"解説の公開","1"
"正解の公開","1"
"小テストの全体的な解説","お疲れ様でした．不正解があっても前向きに捉えましょう．効果的な復習のチャンスです！"
'''[1:-1]
### 編集はここまで 
########################################

### 以下，CSV生成用コード ###
import os
import sys

quiz_file = sys.argv[1]
csv_file = sys.argv[2]

def load_file( filename ):
    with open( filename, 'r' ) as quiz:
        lines = [line.rstrip(os.linesep) for line in quiz.readlines()]
        numbers = []
        anslabs = []
        ansidxs = []
        options = []
        points = []
        for line in lines:
#            print(line)
            idx, pt, anslab, ansidx = line.split(',')
            if( idx == 'title' ):
                title = anslab
            elif( idx == 'sentence' ):
                sentence = anslab
#                print('>>>' + sentence)
            else:
                options.append(anslab)
                if( idx != 'dummy' ):
                    numbers.append(idx)
                    anslabs.append(anslab)
                    ansidxs.append(ansidx)
                    points.append(pt)

        options.sort()

        return {
            'title':title,
            'sentence':sentence,
            'numbers':numbers,
            'anslabs':anslabs,
            'ansidxs':ansidxs,
            'options':options,
            'points':points,
        }


def print_subquiz( quiz, file=sys.stdout ):
    for i, number in enumerate(quiz['numbers']):
        print( '""', file=file)
        print( '"回答形式","radio"', file=file)
        point  = quiz['points'][i]
        ansidx = quiz['ansidxs'][i]
        print( '"配点",' + '"%s"' %(point), file=file)
        sentence = quiz['sentence'].replace('NUM',str(i+1))
        print( '"問題文",' + '"'+sentence+'"', file=file)
        print( '"正解1",' + '"%s"' %(ansidx), file=file)
        for j, option in enumerate(quiz['options']):
            print( '"選択肢%d",'%(j+1) + '"%s"' %(option), file=file)

def print_all( quiz, file=sys.stdout ):
    title = quiz['title'].replace('..SHARP..','#')
    print( '"小テストタイトル",' + '"%s"' %(title), file=file)
    print( common_setting, file=file)
    print_subquiz( quiz, file=file)

quiz = load_file(quiz_file)
with open( csv_file, 'w' ) as fp:
    print_all(quiz, file=fp)
    print('converting '+quiz_file+' to '+csv_file+' ...')
