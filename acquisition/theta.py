# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    theta.py                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: abrar <abrar.patel@ensiie.eu>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/27 15:54:16 by abrar             #+#    #+#              #
#    Updated: 2024/08/06 17:43:20 by abrar            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

"""
Extensions to the Open Spherical Camera API specific to the Ricoh Theta S.
Documentation here:
https://developers.theta360.com/en/docs/v2/api_reference/

Open Spherical Camera API proposed here:
https://developers.google.com/streetview/open-spherical-camera/reference

The library is an evolution of:
https://github.com/codetricity/theta-s-api-tests/blob/master/thetapylib.py

"""

import json
import os
import time
import timeit
import requests
import cv2
import numpy as np
from image_processor import split_image
import osc





__all__ = ['g_ricohOptions', 'ricohFileFormats', 'RicohThetaS']

#
# Ricoh Theta S
#

#
# Ricoh-specific options
#

'''
Reference:
https://developers.theta360.com/en/docs/v2/api_reference/options/
'''

g_ricohOptions = [
            # Custom read-only options
            "_wlanChannel", "_remainingVideos",

            # Custom options
            "_captureInterval", "_captureIntervalSupport", "_captureNumber",
            "_captureNumberSupport", "_filter", "_filterSupport", "_HDMIreso",
            "_HDMIresoSupport", "_shutterVolume", "_shutterVolumeSupport"
            ]

ricohFileFormats = {
    "image_5k" : {'width': 5376, 'type': 'jpeg', 'height': 2688},
    "image_2k" : {'width': 2048, 'type': 'jpeg', 'height': 1024},
    "video_HD_1080" : {"type": "mp4", "width": 1920, "height": 1080},
    "video_HD_720" : {"type": "mp4", "width": 1280, "height": 720}
}

class RicohThetaS(osc.OpenSphericalCamera):
    # Class variables / methods
    ricohOptions = g_ricohOptions

    def __init__(self, ip_base: str = "192.168.1.1", httpPort: int = 80) -> None:
        osc.OpenSphericalCamera.__init__(self, ip_base, httpPort)

    def getOptionNames(self) -> list[str]:
        return self.oscOptions + self.ricohOptions

    # 'image', '_video'
    def setCaptureMode(self, mode) -> dict | None:
        return self.setOption("captureMode", mode)

    def getCaptureMode(self) -> str | None:
        return self.getOption("captureMode")

    def listAll(self, entryCount: int = 3, detail: bool = False, sortType: str = "newest") -> dict | None:
        """
        entryCount:
                Integer No. of still images and video files to be acquired
        detail:
                Boolean (Optional)  Whether or not file details are acquired
                true is acquired by default. Only values that can be acquired
                when false is specified are "name", "uri", "size" and "dateTime"
        sort:
                String  (Optional) Specify the sort order
                newest (dateTime descending order)/ oldest (dateTime ascending order)
                Default is newest

        Reference:
        https://developers.theta360.com/en/docs/v2/api_reference/commands/camera._list_all.html
        """
        url = self._request("commands/execute")
        body = json.dumps({"name": "camera._listAll",
             "parameters": {
                "entryCount": entryCount,
                "detail": detail,
                "sort": sortType
             }
             })
        header = {"Content-Type": "application/json; charset=UTF-8", 
                  "X-Content-Type-Options": "nosniff",
                  "X-XSRF-Protected": '1'}
        try:
            req = requests.post(url, data=body, headers=header)
        except Exception as e:
            self._httpError(e)
            return None

        if req.status_code == 200:
            return req.json()
        else:
            self._oscError(req)
            return None

    def deleteAll(self) -> None:
        """
        Delete all images and videos from the camera.
        """
        entryCount = self.listAll()['results']['totalEntries']
        entries = self.listAll(entryCount)['results']['entries']
        for entry in entries:
            self.delete(entry['uri'])
            time.sleep(0.5)  # Allow time for deletion to complete

    def finishWlan(self) -> dict | None:
        """
        Turns the wireless LAN off.

        Reference:
        https://developers.theta360.com/en/docs/v2/api_reference/commands/camera._finish_wlan.html
        """
        url = self._request("commands/execute")
        body = json.dumps({"name": "camera._finishWlan",
             "parameters": {
                "sessionId": self.sid
             }
             })
        header = {"Content-Type": "application/json; charset=UTF-8", 
                  "X-Content-Type-Options": "nosniff",
                  "X-XSRF-Protected": '1'}
        try:
            req = requests.post(url, data=body, headers=header)
        except Exception as e:
            self._httpError(e)
            return None

        if req.status_code == 200:
            return req.json()
        else:
            self._oscError(req)
            return None

    def startCapture(self) -> dict | None:
        """
        Begin video capture if the captureMode is _video.  If the
        captureMode is set to image, the camera will take multiple
        still images.  The captureMode can be set in the options.
        Note that this will not work with streaming video using the
        HDMI or USB cable.

        Reference:
        https://developers.theta360.com/en/docs/v2/api_reference/commands/camera._start_capture.html
        """
        url = self._request("commands/execute")
        body = json.dumps({"name": "camera._startCapture",
             "parameters": {
                "sessionId": self.sid
             }
             })
        header = {"Content-Type": "application/json; charset=UTF-8", 
                  "X-Content-Type-Options": "nosniff",
                  "X-XSRF-Protected": '1'}
        try:
            req = requests.post(url, data=body, headers=header)
        except Exception as e:
            self._httpError(e)
            return None

        if req.status_code == 200:
            return req.json()
        else:
            self._oscError(req)
            return None

    def stopCapture(self) -> dict | None:
        """
        Stop video capture.  If in image mode, will stop
        automatic image taking.

        Reference:
        https://developers.theta360.com/en/docs/v2/api_reference/commands/camera._stop_capture.html
        """
        url = self._request("commands/execute")
        body = json.dumps({"name": "camera._stopCapture",
             "parameters": {
                "sessionId": self.sid
             }
             })
        header = {"Content-Type": "application/json; charset=UTF-8", 
                  "X-Content-Type-Options": "nosniff",
                  "X-XSRF-Protected": '1'}
        try:
            req = requests.post(url, data=body, headers=header)
        except Exception as e:
            self._httpError(e)
            return None

        if req.status_code == 200:
            return req.json()
        else:
            self._oscError(req)
            return None

    def takeVideo(self, timeLimitSeconds: int = 3) -> None:
        """
        Start video capture, wait for a specified time, and stop
        video capture.  This is useful for capturing a video
        without having to manually start and stop the capture.
        """
        self.setCaptureMode( '_video' )
        self.startCapture()
        time.sleep(timeLimitSeconds)
        self.stopCapture()

    def getVideo(self, fileUri: str, imageType: str = "full") -> bool:
        """
        Transfer the video file from the camera to computer and save the
        binary data to local storage.  This works, but is clunky.
        There are easier ways to do this. The __type parameter
        can be set to "thumb" for a thumbnail or "full" for the
        full-size video.  The default is "full".

        Reference:
        https://developers.theta360.com/en/docs/v2/api_reference/commands/camera._get_video.html
        """
        acquired = False
        if fileUri:
            url = self._request("commands/execute")
            body = json.dumps({"name": "camera._getVideo",
                 "parameters": {
                    "fileUri": fileUri,
                    "type": imageType
                 }
                 })
            header = {"Content-Type": "application/json; charset=UTF-8", 
                      "X-Content-Type-Options": "nosniff",
                      "X-XSRF-Protected": '1'}
  
            fileName = fileUri.split("/")[1]

            try:
                response = requests.post(url, data=body, headers=header, stream=True)
            except Exception as e:
                self._httpError(e)
                return acquired

            if response.status_code == 200:
                with open(fileName, 'wb') as handle:
                    for block in response.iter_content(1024):
                        handle.write(block)
                acquired = True
            else:
                self._oscError(response)

        return acquired

    def getLatestVideo(self, imageType: str = "full") -> None:
        """
        Transfer the latest file from the camera to computer and save the
        binary data to local storage.  The __type parameter
        can be set to "thumb" for a thumbnail or "full" for the
        full-size video.  The default is "full".
        """
        fileUri = self.latestFileUri()
        if fileUri:
            self.getVideo(fileUri, imageType)

    def getLivePreview(self, dir: str = './') -> None:
        """
        Save the live preview video stream to disk as a series of jpegs. 
        The capture mode must be 'image'.

        Credit for jpeg decoding:
        https://stackoverflow.com/questions/21702477/how-to-parse-mjpeg-http-stream-from-ip-camera

        Reference:
        https://developers.theta360.com/en/docs/v2/api_reference/commands/camera._get_live_preview.html
        """

        if not dir.endswith('/') :
            print("The directory path need to end with '/'.")
            return
        
        url = self._request("commands/execute")
        body = json.dumps({"name": "camera._getLivePreview",
                "parameters": {
                    "sessionId": self.sid
                 }})

        header = {"Content-Type": "application/json; charset=UTF-8", 
                  "X-Content-Type-Options": "nosniff",
                  "X-XSRF-Protected": '1'}
        try:
            response = requests.post(url, data=body, headers=header, stream=True)
        except Exception as e:
            self._httpError(e)

        if response.status_code == 200:
            bytes_ = bytes()
            # t0 = timeit.default_timer()
            i = 0
            for block in response.iter_content(1024):
                bytes_ += block

                # Search the current block of bytes for the jpg start and end
                a = bytes_.find(b'\xff\xd8')
                b = bytes_.find(b'\xff\xd9')

                # If you have a jpg, write it to disk
                if a !=- 1 and b != -1:
                    fileNamePrefix = "livePreview"
                    # print( "Writing frame %04d - Byte range : %d to %d" % (i, a, b) )
                    # Found a jpg, write to disk
                    if not os.path.exists(f"{dir}{fileNamePrefix}"):
                        os.makedirs(f"{dir}{fileNamePrefix}")
                    if not os.path.exists(f"{dir}back"):
                        os.makedirs(f"{dir}back")
                    if not os.path.exists(f"{dir}front"):
                        os.makedirs(f"{dir}front")
                    with open(f"{dir}{fileNamePrefix}/{fileNamePrefix}{i}.jpg", 'wb') as handler, \
                        open(f"{dir}back/back{i}.jpg", 'wb') as handlerback, \
                        open(f"{dir}front/front{i}.jpg", 'wb') as handlerfront:
                        jpg = bytes_[a:b+2]

                        img = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                        
                        # Split the image 
                        back_img, front_img = split_image(img) 
                        back_back_img, front_back_img = split_image(back_img)
                        back_front_img, front_front_img = split_image(front_img)

                        back_concat = cv2.hconcat([front_back_img, back_front_img])
                        front_concat = cv2.hconcat([front_front_img, back_back_img])

                        cv2.imshow(fileNamePrefix+'Back', back_concat)
                        cv2.imshow(fileNamePrefix+'Front',front_concat)
                        cv2.imshow(fileNamePrefix, img)

                        # press 'q' on the keyboard to close the windows
                        if (cv2.waitKey(1) & 0xFF == ord('q')):
                            break
                        
                        handlerback.write(cv2.imencode('.jpg', back_concat)[1])
                        handlerfront.write(cv2.imencode('.jpg', front_concat)[1])
                        handler.write(jpg)


                        # Reset the buffer to point to the next set of bytes
                        bytes_ = bytes_[b+2:]
                        # print( "Wrote frame %04d - %2.3f seconds" % (i, elapsed) )

                    i += 1
                # t1 = timeit.default_timer()
                # elapsed = t1 - t0
                # t0 = t1
                # print(f"{elapsed = } seconds")
        else:
            self._oscError(response)

# RicohThetaS

if __name__ == "__main__":
    theta = RicohThetaS()
    #theta.setCaptureMode("image")
    #theta.startCapture()
    for i in range(10099, 10113):
        theta.getImage(f"100RICOH/R00{i}.JPG")
    ()