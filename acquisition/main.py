# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: abrar <abrar.patel@ensiie.eu>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2024/06/27 15:51:57 by abrar             #+#    #+#              #
#    Updated: 2024/07/24 11:22:34 by abrar            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import os
import theta
import pprint
import argparse


def main() -> None:

    parser = argparse.ArgumentParser(description='Control Ricoh Theta S camera.')
    parser.add_argument('-ip', default='192.168.1.1', help='IP address of the camera. Default is 192.168.1.1 .')
    parser.add_argument('--dir', default='./', help='Directory to save images from the live preview or on the disk. Default is the current directory.')
    parser.add_argument('-tl', '--time-limit', type=int, default=3, help='Time limit in seconds for taking video')
    parser.add_argument('action', choices=['take_picture', 'list_all', 'get_latest_image', 'get_live_preview', 'take_video', 'get_latest_video', 'delete', 'get_latest_files'], help="Action to perform on the camera.")
    parser.add_argument('--detail', action="store_true", help='Display detailed information.')
    parser.add_argument('-n', default=3, type=int, help='Number of file to display/save')
    parser.add_argument('--uri', help="URI to delete on the disk of the camera. The 'list_all' action return informations containing files' URI.")
    parser.add_argument('--all', action="store_true", help="Option to delete all the files on the disk of the camera.")
    args = parser.parse_args()
    thetas = theta.RicohThetaS(args.ip)

    if not os.path.exists(f"{args.dir}"):
        print(f"Error: Creating directory of {args.dir}")
        os.makedirs(f"{args.dir}")

    print(60 * "=")
    print("Getting basic info...")
    pprint.pprint(thetas.info())

    print(60 * "=")
    print("Getting state...")
    pprint.pprint(thetas.state())

    print(60 * "=")
    print("Starting session...")
    thetas.startSession()
    print("Session started.")

    print(60 * "=")
    match args.action:
        case 'take_picture':
            thetas.setCaptureMode('image')
            print("Taking picture...")
            thetas.takePicture()
        case 'list_all':
            print("Listing files...")
            images = thetas.listAll(args.n, args.detail) if args.detail else thetas.listAll(args.n)
            pprint.pprint(images)
        case 'get_latest_image':
            print("Getting image...")
            thetas.getLatestImage()
        case 'get_live_preview':
            thetas.setCaptureMode('image')
            print("Getting live preview...")
            dir = args.dir + ('/' if not args.dir.endswith('/') else '')
            thetas.getLivePreview(dir = dir)
        case 'take_video':
            print("Taking video...")
            thetas.takeVideo(args.time_limit)
        case 'get_latest_video':
            print("Getting latest video...")
            thetas.getLatestVideo()
        case 'delete':
            if args.all :
                res = input("Are you sure you want to delete all files ? (yes or no)")
                if not res.lower() in ['yes','y'] : return 
                print("Deleting all files...")
                thetas.deleteAll()
            else :
                res = input(f"Are you sure you want to delete {args.uri} ? (yes or no)")
                if not res.lower() in ['yes','y']  : return 
                print(f"Deleting {args.uri}...")
                thetas.delete(args.uri)
        case 'get_latest_files':
            entries = thetas.listAll(args.n)['results']['entries']
            print("Getting latest files...")
            for entry in entries:
                thetas.getImage(entry['uri'], dir=args.dir)
        
    
    print(60 * "=")
    print("Closing session...")
    thetas.closeSession()
    print("Session closed.")


if __name__ == "__main__":
    main()
