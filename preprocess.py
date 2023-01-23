import json
import codecs
import pandas as pd

f = codecs.open('corpus/processed_songs_bulk_api.json', 'w', encoding='utf-8')
df = pd.read_csv('corpus/170032N_SPB_Hari_Mano_Karthik.csv')


def checkString(val):
    return isinstance(val, str)


list_ = [[["உருவகம்_1", 'metaphor_1'], ["மூலம்_1", 'metaphor1_source_domain'], ["இலக்கு_1", 'metaphor1_target_domain'],
          ["விளக்கம்_1", 'metaphor_1_interpretation']],
         [["உருவகம்_2", 'metaphor_2'], ["மூலம்_2", 'metaphor2_source_domain'], ["இலக்கு_2", 'metaphor2_target_domain'],
          ["விளக்கம்_2", 'metaphor_2_interpretation']],
         [["உருவகம்_3", 'metaphor_3'], ["மூலம்_3", 'metaphor3_source_domain'], ["இலக்கு_3", 'metaphor3_target_domain'],
          ["விளக்கம்_3", 'metaphor_3_meaning']]]

for i in range(df.shape[0]):
    dict_ = {}
    dict_["பாடல் வரிகள்"] = df['lyrics'][i]
    dict_["இசையமைப்பாளர் "] = df['composer'][i]
    dict_["பாடல்"] = df["song_name"][i]
    dict_["பாடலாசிரியர்"] = df['lyricist'][i]
    dict_["பாடகர்கள்"] = df['singers'][i]
    dict_["வருடம்"] = json.dumps(int(df['year'][i]))

    for j in range(3):
        for k in range(4):
            val = df[list_[j][k][1]][i]

            if checkString(val):
                dict_[list_[j][k][0]] = val


    f.write('{ "index" : { "_index" : "lyrics_metaphors_db_4", "_id" :' + str(i) + ' } }\n')
    json.dump(dict_, f, ensure_ascii=False)
    f.write('\n')
    i += 1
