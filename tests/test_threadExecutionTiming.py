import sys, os
sys.path.append(os.path.join(sys.path[0],'../'))
#print(sys.path)
import main as m
import cv2
import queue
import threading
from time import perf_counter
import datetime

def test():

    cap = cv2.VideoCapture(0)

    rawQueue = queue.Queue(60*15)
    resultQueue = queue.Queue()
    overlayQueue = queue.Queue()

    threadList = dict()
    debug = dict()

    threadList["parsingThread"] = threading.Thread(target=m.t_parseFramesToQueue, args=(cap, 0, rawQueue, debug ))
    threadList["processingThread"] = threading.Thread(target=m.t_processQueueFrameWithMP, args = (rawQueue, resultQueue, debug))
    threadList["overlayThread"] = threading.Thread(target=m.t_drawLandmarks, args = (resultQueue, overlayQueue, debug ))
    threadList["displayThread"] = threading.Thread(target=m.t_playProcesssedVideo, args=(overlayQueue, debug))

    f = open("tests/test_threadExecutionTiming.txt", "w")
    printQueue = list()
    printQueue.append(f"---\nThread Execution Test, date = {datetime.datetime.now()}\n")
    for n, t in threadList.items():
        print(n + "...")
        t.start()
        t.join()
        print(str(debug["Element"]))
        et = debug["ExecutionTime"]
        printQueue.append(f"Thread Name: {n}, Execution Time: {et}\n")
    
    printQueue.append("\nEND\n")

    print(''.join(printQueue), file=f)


    return

if __name__ == "__main__":
    test()