# from fuzzer import odds_file
import db

stats = db.init_stats("odds_master.json")

def calculate_final_stats(s):
    p = 1.0
    for i in range(len(s)-1):
        p_index = stats[s[i]][0].index(s[i+1])
        p *= stats[s[i]][1][p_index]

    return p

if __name__ == '__main__':
    pass
