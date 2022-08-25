from asyncio import as_completed
from concurrent.futures import process
from operator import truediv
import cv2
import mediapipe as mp
import threading
import queue
import concurrent.futures
import threading
import time

forceBreak = False

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose  



T_BASE_DELAY = 1

DEBUG_MODE = True


def DEBUG_PRINT(x):
    global DEBUG_MODE
    if DEBUG_MODE == True:
        print(x)

def scanCameras():      
        cameras = []
        for i in range(100):
            cap = cv2.VideoCapture(i)
            ret, frame = cap.read()
            if(ret == True):
                cameras.append(i)
        
        return cameras


def setCap(cams):
    capList = []
    for n in cams:
        capList.append(cv2.VideoCapture(n))
    return cams, capList

class queueData():
    def __init__(self, frameNum, camID, frame):
        self._frameNum = frameNum
        self._camID = camID
        self._frame = frame
        self._result = None
        self._overlayedFrame = None

    def getQueueData(self):
        return [ self._frameNum, self._camID, self._frame, self._result, self._overlayedFrame ]

    def setQueueData(self, frameNum, camID, frame):
        self._frameNum = frameNum
        self._camID = camID
        self._frame = frame

    def getQueueFrame(self):
        return self._frame

    def getSelf(self):
        return self

    def setQueuePose(self, pose):
        self._pose = pose

    def getQueueResult(self):
        return self._result
    
    def setOverlayedFrame(self, overlayedFrame):
        self._overlayedFrame = overlayedFrame

    def __str__(self):
        return f"FN: {self._frameNum}, CID: {self._camID}"


def t_parseFramesToQueue(cap, capNum, outQueue, debug = None):
    if(debug != None): 
        print('t_parseFramesToQueue Has Started...')
        start = time.perf_counter()

    ret = True
    frameNum = 0
    while ret == True:
        ret, frame = cap.read()
        
        if(outQueue.full() == False):
            queueObj = queueData(frameNum, capNum, frame)
            outQueue.put(queueObj)
            frameNum +=1
        else:
            DEBUG_PRINT("frameQueue full")
            time.sleep(1)
    
        if(debug != None):
            end = time.perf_counter()
            debug["Element"] = queueObj
            debug["ExecutionTime"] = end - start
            debug["Error"] = ret
            return
        
        time.sleep(T_BASE_DELAY)
            
    


def t_processQueueFrameWithMP(inQueue, outQueue, debug = None):
    if(debug != None): 
        print('t_processQueueFrameWithMP Has Started...')
        start = time.perf_counter()

    while inQueue.full != True:
        ret = False
        if(inQueue.empty() == False):
            queueObj = inQueue.get().getSelf()
            with mp_pose.Pose(
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5) as pose:

                queueObj._frame.flags.writeable = False
                queueObj._frame = cv2.cvtColor(queueObj._frame, cv2.COLOR_BGR2RGB)
                queueObj._result = pose.process(queueObj._frame)
                outQueue.put(queueObj) 

        else:
            ret = "processQueue empty"

        
        if(debug != None):
            end = time.perf_counter()
            debug["Element"] = queueObj
            debug["ExecutionTime"] = end - start
            debug["Error"] = ret
            return

        
        time.sleep(T_BASE_DELAY)
    



def t_drawLandmarks(inQueue, outQueue, debug = None):
    if(debug != None): 
        print('t_drawLandmarks Has Started...')
        start = time.perf_counter()

    while inQueue.full != True:
        ret = False
        if(inQueue.empty() == False):
            queueObj = inQueue.get().getSelf()
            queueObj._frame.flags.writeable = True
            queueObj._frame = cv2.cvtColor(queueObj._frame, cv2.COLOR_RGB2BGR)
            mp_drawing.draw_landmarks(
                queueObj._frame,
                queueObj._result.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())

            queueObj.setOverlayedFrame(queueObj._frame)
            outQueue.put(queueObj)

        else: 
            ret = 'drawQueue empty'


        if(debug != None):
            end = time.perf_counter()
            debug["Element"] = queueObj
            debug["ExecutionTime"] = end - start
            debug["Error"] = ret
            return
        
        time.sleep(T_BASE_DELAY)   

    return



def t_playProcesssedVideo(inQueue, debug = None):
    if(debug != None): 
        print('t_playProcesssedVideo Has Started...')
        start = time.perf_counter()

    while True:
        ret = False
        if(inQueue.empty() == False):
            queueObj = inQueue.get().getSelf()
            cv2.imshow('frame', queueObj._overlayedFrame)

        else:
            ret = 'playVideoQueue empty'

        if(debug != None):
            end = time.perf_counter()
            debug["Element"] = queueObj
            debug["ExecutionTime"] = end - start
            debug["Error"] = ret
            return

        time.sleep(T_BASE_DELAY)
    


def localCamPoseToGlobalCamPose(x, y, z):

    return

def t_triangulateFrames():
    


    return

""" 
def averageFilter(inQueue, filterSize):
    averagedQueue = queue.Queue()
    if(filterSize == None):
        filterSize= 5

    filterBuffer = [None] * filterSize
    print("Averaging filter")
    #pre-populate filter 
    for i in range(filterSize - 1 ):
        filterBuffer[i] = inQueue.get()
    while(inQueue.empty != True):
        #add new buffer element
        filterBuffer[4] = inQueue.get()
        avg = [0.0, 0.0, 0.0, 0.0]
        for x in filterBuffer:
            avg[0] += x. $rest here
            avg[1] fgdfg
            avg[2] fgdfsd
            avg[3] sfdsf
        for i in avg:
            i /= filterSize
        averagedQueue.put(avg)
        #shift buffer
        for i in range(len(filterBuffer) -1):
            filterBuffer[i] = filterBuffer[i+1]

    return averagedQueue   

 """
def getQueueDelta(inQueue):
    deltaQueue = queue.Queue()
    
    buffer = [None] * 2
    #pre-fill
    buffer[0] = inQueue.get()
    maxDiff = 0.0
    while(inQueue.empty() != True):
        buffer[1] = inQueue.get()
        diff = buffer[1] - buffer[0]

        if(abs(diff) > maxDiff):
            maxDiff = abs(diff)

        deltaQueue.put(diff)
        buffer[0] = buffer[1]
    
    return deltaQueue, maxDiff

    

class cameraConfig():

    def __init__(self, capNum):
        self._capNum = capNum
        self._adjust = [0.0, 0.0, 0.0]
        return

    def calibrate(self):
        cap = cv2.VideoCapture(self._capNum)
        frameQueue = queue.Queue()
        falseCounter = 0
        print(f"Recording... [{self._capNum}]")
        for _ in range(100):
            ret, frame = cap.read()
            if(ret == True):
                frameQueue.put(frame)
            if(ret == False):
                falseCounter+=1
                if(falseCounter > 5):
                    return False
        
        resultQueue = queue.Queue()
        print("Processing...")
        while(frameQueue.empty != True):
            f = frameQueue.get()
            with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:

                f.flags.writeable = False
                f = cv2.cvtColor(f, cv2.COLOR_BGR2RGB)
                result = pose.process(f)
                resultQueue.put(result)

        avgQueue = averageFilter(resultQueue, None)

        diffQueue, maxDiff = getQueueDelta(avgQueue)

        self.cameraAdjust = [abs(maxDiff[0]) * 0.2, abs(maxDiff[1]) * 0.2, abs(maxDiff[2]) * 0.2]
        
            
        return True

    

        



# cap = cv2.VideoCapture(0)

# rawQueue = queue.Queue(60*15)
# resultQueue = queue.Queue()
# overlayQueue = queue.Queue()

# parsingThread = threading.Thread(target=t_parseFramesToQueue, args=(cap, 0, rawQueue ))
# processingThread = threading.Thread(target=t_processQueueFrameWithMP, args = (rawQueue, resultQueue))
# overlayThread = threading.Thread(target=t_drawLandmarks, args = (resultQueue, overlayQueue ))
# displayThread = threading.Thread(target=t_playProcesssedVideo, args=(overlayQueue, ))

# parsingThread.start()
# processingThread.start()
# overlayThread.start()
# displayThread.start()

# DEBUG_PRINT('threads started')

# def main():



#     print(scanCameras)

    
#     while(1):
#         time.sleep(.2)
        
        



#main()


"""    
    with concurrent.futures.ProcessPoolExecutor() as executor:
        res = [executor.submit(t_parseFramesToQueue, cap, 0)]

        for f in concurrent.futures.as_completed(res):
            print(f.result())
"""

