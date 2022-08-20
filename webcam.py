#I want to create a script that would help me manipulate the webcam of a system

#Useful libraries that I would be working with -->
import os
import sys
import cv2 as cv
import socket
import pickle
import struct
import imutils
import ip_info

#exit()
#Declaring the class
class Webcam:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.user, self.host, self.publicIP, self.privateIP = ip_info.main()
        self.port = 6699

    #This function tells me how many webcams are active on a device
    def camScanner(self):
        active = []
        for p in [0,1,2,3,4,5]:
            cam = cv.VideoCapture(p)
            res, img = cam.read()
        
            if res:
                cv.waitKey(0)
                active.append(p)
                print(True)
            else:
                print(False)
            cam.release()
            cv.destroyAllWindows()
        return active

    #This function would handle the webcam snapshots
    def snapShot(self, camPort = 0):
        try:
            self.cam = cv.VideoCapture(camPort)
            result, image = self.cam.read()
            file = f"snapShot.jpg"
            if result:
                #cv.imshow("image", image)
                cv.imwrite(file, image)
                cv.waitKey(0)
                stat = f"{file} has been captured"
            else:
                stat = "Image not detected"
        except Exception as e:
            stat = f"An error when snapshotting due to [{e}]"
        finally:
            self.cam.release()
            cv.destroyAllWindows()
            return stat

    #This function would handle the sender's webcam stream
    def receiver(self, host):
        self.s.connect((host, self.port))
        data = b""
        payloadSize = struct.calcsize("Q")
        while True:
            while len(data) < payloadSize:
                packet = self.s.recv(4 * 1024)
                if not packet:
                    break
                data += packet
            packedMsgSize = data[:payloadSize]
            data = data[payloadSize:]
            msgSize = struct.unpack("Q", packedMsgSize)[0]

            while len(data) < msgSize:
                data += self.s.recv(4 * 1024)
            frameData = data[:msgSize]
            data = data[msgSize:]
            frame = pickle.loads(frameData)
            cv.imshow("Receiver Webcam", frame)
            key = cv.waitKey(1) & 0xFF
            if key == ord("q"):
                break
        self.s.close()
        pass

    #This function would handle the receiving of the sender's webcam stream\
    def sender(self):
        self.s.bind((self.privateIP, self.port))
        self.s.listen(10)
        print(f"Listening on {self.privateIP}: {self.port}")

        while True:
            client_soc, addr = self.s.accept()
            print(f"{addr} has connected successfully")
            if client_soc:
                vid = cv.VideoCapture(0)
                while vid.isOpened():
                    img, frame = vid.read()
                    frame = imutils.resize(frame, width = 320)
                    a = pickle.dumps(frame)
                    message = struct.pack("Q", len(a)) + a
                    client_soc.sendall(message)
                    #cv.imshow("Sender video", frame)
                    key = cv.waitKey(1) & 0xFF
                    if key == ord("q"):
                        client_soc.close()


if __name__ == "__main__":
    print("WEBCAM MANIPULATOR\n")

    cam = Webcam().sender()

    print("\nExecuted successfully!!")
