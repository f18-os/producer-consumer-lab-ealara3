
import os
import time
import threading
import cv2
import numpy as np
import base64
import queue

#mutex = threading.Lock() #used to transfer data
waitFill = threading.BoundedSemaphore(10)
fillFirst = threading.BoundedSemaphore(10)
sem = threading.BoundedSemaphore(10)
sem2 = threading.BoundedSemaphore(10)
#mutex = threading.Lock()
#mutex2 = threading.Lock()
q = queue.Queue()
q2 = queue.Queue()

class ExtractFrames(threading.Thread):                            #ExtractFrames

    outputDir    = 'frames'
    clipFileName = 'clip.mp4'
    # initialize frame count

    def __init__(self):
        threading.Thread.__init__(self)
        for i in range(10):
            fillFirst.acquire()             #This lock will make to start with extracting
            waitFill.acquire()              #this lock will wait for the extracting extract 10
        #self.q = q

    def run(self):
        #count = 0
        mutex = threading.Lock()                            #This is used in case there are more extract methods
        count = 0
        vidcap = cv2.VideoCapture(self.clipFileName)
        # read one frame
        success,image = vidcap.read()
        l=0

        print("Reading frame {} {} ".format(count, success))
        while success:
          sem.acquire()
          mutex.acquire()
          #mutex.acquire()
          # get a jpg encoded frame
          #success, jpgImage = cv2.imencode('.jpg', image)

          #encode the frame as base 64 to make debugging easier
          #jpgAsText = base64.b64encode(jpgImage)

          # add the frame to the buffer
          q.put(image)

          # write the current frame out as a jpeg image
          #cv2.imwrite("{}/frame_{:04d}.jpg".format(self.outputDir, count), image)
          success,image = vidcap.read()

          print('Reading frame {}'.format(count))
          #self.q.task_done
          count += 1
          for i in range(10):
            l+=1
          #time.sleep(1)
          #mutex.release()
          if(q.empty()):
              if(q2.empty()):
                  sem.release()
                  fillFirst.release()
                  #fillFirst.release()
                  print("exit")
                  break
          mutex.release()
          fillFirst.release()

        #for i in range(8):
        #    fillFirst.release()
          #sem.release()



class ConvertToGrayscale(threading.Thread):


    def __init__(self):
        threading.Thread.__init__(self)
        #self.q = q
        #self.q2 = q2

    def run(self):
        # initialize frame count
        #mutex1 = threading.Lock()
        count = 0
        n = 0
        l = 0
        while True:
            fillFirst.acquire()                         #so it dont release to many times
            #sem.acquire()
            sem2.acquire()
            #mutex.acquire()
            #mutex2.acquire()
            # get the next frame file name
            #inFileName = "{}/frame_{:04d}.jpg".format(q.get(), count)
            # load the next file
            #inputFrame = cv2.imread(inFileName, cv2.IMREAD_COLOR)
            #print(inputFrame)
            #while inputFrame is not None:
            print("Converting frame {}".format(count))

            # convert the image to grayscale
            grayscaleFrame = cv2.cvtColor(q.get(), cv2.COLOR_BGR2GRAY)

            count += 1
            q2.put(grayscaleFrame)
            #self.q2.task_done
            for i in range(10):
                i+=1
            #time.sleep(1)
            #mutex2.release()
            #mutex.release()
            if(q.empty()):
                #print(q2.empty())
                if(q2.empty()):
                    #sem2.release()
                    print("exit2")
                    sem2.release()
                    waitFill.release()
                    sem.release()
                    break
            waitFill.release()
            #time.sleep(1)
            sem.release()
        for i in range(9):
            waitFill.release()


        #sem2.release()
        fillFirst.release()


class DisplayFrames(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        #self.q2 = q2

    def run(self):
        #mutex3 = threading.Lock()
        count = 0
        l = 0
        while True:
            waitFill.acquire()
            #mutex2.acquire()
            img = q2.get()

            # decode the frame
            #jpgRawImage = base64.b64decode(frameAsText)

            # convert the raw frame to a numpy array
            #jpgImage = np.asarray(bytearray(jpgRawImage), dtype=np.uint8)

            # get a jpg encoded frame
            #img = cv2.imdecode( jpgImage ,cv2.IMREAD_UNCHANGED)

            print("Displaying frame {}".format(count))
            time.sleep(.042)                                                    #this will send wait to send 24 fps by dividing ()(1/24) /1000) it has to sleep .042
            cv2.imshow("Video", img)
            if cv2.waitKey(42) and 0xFF == ord("q"):
                break

            #time.sleep(1)
            count += 1
            #mutex2.release()
            #self.q2.task_done
            for i in range(10):
                l+=1
            sem2.release()
            if (q.empty()):
                if q2.empty():
                    print("Thank you for watching the video")
                    break
        #for i in range(10):
            #for i in range(10):

            #fillFirst.release()
            #waitFill.release()
            #print("here",count)
        waitFill.release()
        #sem2.release()

        print("Finished displaying all frames")
        # cleanup the windows
        cv2.destroyAllWindows()


#sem = threading.BoundedSemaphore(11)  #I will push 11 in the stack but I will pop 10
#sem2 = threading.BoundedSemaphore(10)


ext = ExtractFrames()
#ext.run(q)
ext.start()

con = ConvertToGrayscale()
#con.run(q,q2)
con.start()

dis = DisplayFrames()
#dis.run(q2)
dis.start()
