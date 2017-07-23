from youtube3.youtube import *
import json
from oauth2client.tools import argparser

if __name__ == "__main__":
    argparser.add_argument('--workDir')
    argparser.add_argument('--maxCount')
    argparser.add_argument('--inputFile')
    argparser.add_argument('--start')

    argparser.add_argument('--end')
    argparser.add_argument('--recommendedFile')
    argparser.add_argument('--excludedFile')
    argparser.add_argument('--postponedFile')

    args = argparser.parse_args()
    count = 0
    recommended = {}
    excluded = {}
    postponed = {}
    inputFile = args.inputFile or 'liked.json'
    recommendedFile = args.recommendedFile or 'recommended.json'
    excludedFile = args.excludedFile or 'excluded.json'
    postponedFile = args.postponedFile or 'postponed.json'

    maxCount = args.maxCount or 5

    with open(args.workDir+'/'+inputFile,'r',encoding="utf-8") as f:
        liked = json.load(f)

    if os.path.isfile(args.workDir + '/'+recommendedFile ):
        with open(args.workDir + '/'+recommendedFile , 'r', encoding="utf-8") as f:
            recommended = dict(json.load(f))

    if os.path.isfile(args.workDir + '/'+excludedFile ):
        with open(args.workDir + '/'+excludedFile , 'r', encoding="utf-8") as f:
            excluded = dict(json.load(f))

    if os.path.isfile(args.workDir + '/'+postponedFile ):
        with open(args.workDir + '/'+postponedFile  , 'r', encoding="utf-8") as f:
            postponed = dict(json.load(f))


    start = int(args.start) if args.start else 0
    end = min(int(args.end),len(liked)) if args.end else len(liked)

    youtube = Youtube(get_authenticated_service(args))

    likedList = list(liked.items())[start:end]
    for videoId,title in likedList:
        print("Now processing %s, %s" % (videoId, title))
        for relatedvideos in youtube.iterate_related_videos(videoId,maxCount):
            for item in relatedvideos['items']:
                rvideoId, rtitle = item['id']['videoId'],item['snippet']['title']
                if rvideoId not in liked and rvideoId not in excluded and rvideoId not in postponed:
                    if rvideoId not in recommended:
                        recommended[rvideoId] = {"title" : rtitle,"count" : 1}
                    else:
                        recommended[rvideoId]["count"] +=1
    recommendedSorted = sorted(recommended.items(), key=lambda x: x[1]["count"], reverse=True)
    with open(args.workDir + '/'+recommendedFile, 'w', encoding="utf-8") as f:
        json.dump(recommendedSorted , f, ensure_ascii=False)
