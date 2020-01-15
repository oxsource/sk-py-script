#!/bin/python3
from optparse import OptionParser  
import simpleaudio as sa
import os

def __filter(path, ext = ".wav"):
    collects = []
    for root, dirs, files in os.walk(path):
        for f in files:
            splits = os.path.splitext(f)
            if splits is None or len(splits) != 2:
                continue
            if splits[1] != ext:
                continue
            collects.append(os.path.join(root, f))
    return collects

def __foreach(files, index, output):
    total = len(files) - 1
    for (i, f) in enumerate(files):
        print("<%s-%s> %s." % (i, total, f))
        if i < index:
            print("skip...")
            continue
        try:
            while True:
                wave_obj = sa.WaveObject.from_wave_file(f)
                play_obj = wave_obj.play()
                play_obj.wait_done()
                cmd = input("Tell me your choice(Y[right]/N[error]/R[replay]/Q[quit]):")
                if cmd in ["Y", "y"]:
                    __save(f, output, True)
                    break
                elif cmd in ["N", "n"]:
                    __save(f, output, False)
                    break
                elif cmd in ["R", "r"]:
                    continue
                elif cmd in ["Q", "q"]:
                    print("user quit.")
                    return
                else:
                    print("error input! try again...")
                    continue
        except BaseException as exp:
            print("exit by except: %s" % exp)
            break
    print("process finish.")

def __save(file_name, output, success):
    if success:
        return
    kw = os.path.basename(file_name)
    lines = []
    with open(output, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            if kw in line:
                lines[idx] = line.replace("小维小维", "noise")
                break
    if len(lines) <= 0:
        raise Exception("no match line for <%s>." % file_name)

    with open(output, 'w', encoding = 'utf-8') as f:
        f.writelines(lines)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-r", "--read", dest="read")
    parser.add_option("-w", "--write", dest="write")
    parser.add_option("-i", "--index", dest="index")
    option , _ = parser.parse_args()
    '''param read file'''
    if option.read is None:
        raise Exception("please special read file path.")
    read_path = option.read
    '''param write file'''
    if option.write is None:
        raise Exception("please special write file path.")
    write_path = option.write
    '''param start index'''
    try:
        start_index = int(option.index)
    except BaseException:
        start_index = -1
    '''process'''
    files = __filter(read_path)
    __foreach(files, start_index, write_path)

