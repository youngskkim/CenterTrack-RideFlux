@misc{luiten2020trackeval,
  author =       {Jonathon Luiten, Arne Hoffhues},
  title =        {TrackEval},
  howpublished = {\url{https://github.com/JonathonLuiten/TrackEval}},
  year =         {2020}
}


1. minimum_requirements
ujson
numpy
scipy






2. 제출 데이터의 경로 및 데이터(.json) 포맷
제출 데이터의 경로, 데이터 포맷은 배포한 학습용 데이터의 경로, 포맷과 동일합니다.

예시)
tracker_path
|——eval_type
	|—— <SeqName01>
	    |—— json0
		|—— SeqName01_000.json
		|—— SeqName01_001.json
		...
		|—— SeqName01_199.json
	|—— <SeqName02>
	    |—— json0
		|—— SeqName02_000.json
		|—— SeqName02_001.json
		...
		|—— SeqName02_199.json
	|—— <SeqName03>
	...
	|—— <SeqName_n>



예시)
tracker_path
|——train
    |—— 10002
        |—— json0
            |—— 10002_000.json
            |—— 10002_001.json
            ...
            |—— 10002_199.json
    |—— 10003
        |—— json0
            |—— 10003_000.json
            |—— 10003_001.json
            ...
            |—— 10003_199.json
    |—— 10004
    ...
|——val
    |——
    ...
|——test
    |——
    ...


예시) 
{
    "annotations": [
        {
            "bbox": [
                x1,
                y1,
                x2,
                y2
            ],
            "attribute": {
                "track_id": x
            },
            "class": "y"
        },

        ...

        {
            "bbox": [
                x1,
                y1,
                x2,
                y2
            ],
            "attribute": {
                "track_id": x
            },
            "class": "y"
        },
    ],
    "information": {
        "filename": "SeqName0_000.jpg",
        "resolution": [
            width,
            height
        ]
    }
}






3. TRACKEVAL
MOTA 계산을 위한 코드입니다.
해당 코드는 mot_challenge 데이터 포맷을 사용하기 때문에 배포, 제출 데이터의 json 포맷을 mot_challenge 데이터 포맷으로 변환 후 코드를 실행합니다.
변환 방법은 4 참고



명령어
python3 scripts/run_mot_challenge.py --SPLIT_TO_EVAL {0} --TRACKERS_TO_EVAL {1}

{0} 평가할 데이터셋의 타입(train, val, test 중 택1)
{1} 제출할 tracker의 이름. 



예시)
python3 scripts/run_mot_challenge.py --SPLIT_TO_EVAL val --TRACKERS_TO_EVAL NEWTRACKER


MOTA결과는 터미널 또는 trackeval/data/trackers/mot_challenge/AI_CHALLENGE-eval_type/TRACKER_NAME/ 위치에 있는 .txt, .csv파일로 확인 가능합니다.



4. _convert.py
학습, 제출 데이터 포맷인 .json 형식을 mot_challenge 포맷으로 변환하는 코드입니다.
_convert.py 파일은 배포 했을 때의 위치, TrackEval/_convert.py에 있음을 가정합니다.


명령어
python3 ./_convert.py --GT_PATH {0} --TRACKER_PATH {1} --TYPE_TO_EVAL {2} --TRACKER {3}

{0} 학습용 데이터(gt)의 최상위 디렉토리 경로
예시)

{0}
|——train
    |—— 10002
        |—— json0
            |—— 10002_000.json
            |—— 10002_001.json
            ...
            |—— 10002_199.json
    |—— 10003
        |—— json0
            |—— 10003_000.json
            |—— 10003_001.json
            ...
            |—— 10003_199.json
    |—— 10004
    ...
|——val
    |——
    ...
|——test
    |——
    ...

{1} tracker에 의해 생성된 데이터의 최상위 디렉토리 경로. 2번 설명 예시의 tracker_path와 동일합니다.
{2} 변환하는 데이터셋의 타입(train, val, test, 다중선택 가능)
{3} tracker의 이름. tracker 데이터 변환({1}을 입력했을 경우)시에만 입력합니다. 3. TRACKEVAL의 {1}과 일치해야합니다..



예시)
python3 _convert.py --GT_PATH ~/AI_CHALLENGE/GT_DATA --TRACKER_PATH ~/AI_CHALLENGE/TRACKER_DATA --TYPE_TO_EVAL val test --TRACKER NEWTRACKER


gt와 tracker의 최상위 경로는 2번 설명 예시의 tracker_path에 해당합니다.
_convert.py를 실행할 경우
TrackEval/data/gt/mot_challenge/ 또는 TrackEval/data/trackers/mot_challenge/위치에 변환된 데이터가 저장됩니다.



예시)
python3 _convert.py --GT_PATH ~/AI_CHALLENGE/GT_DATA --TRACKER_PATH ~/AI_CHALLENGE/TRACKER_DATA --TYPE_TO_EVAL val test --TRACKER NEWTRACKER 를 실행한 경우

TrackEval
|——data
    |——gt
        |——mot_challenge
            |——AI_CHALLENGE-val   
                |—— <SeqName01>
                    |—— gt
                        |—— gt.txt
                    |—— seqinfo.ini
                |—— <SeqName02>
                    |—— ...
                |—— <SeqName03>
                    |—— ...
            |——AI_CHALLENGE-test   
                |—— <SeqName01>
                    |—— gt
                        |—— gt.txt
                    |—— seqinfo.ini
                |—— <SeqName02>
                    |—— ...
                |—— <SeqName03>
                    |—— ...
            |——seqmaps
                |——AI_CHALLENGE-val.txt
                |——AI_CHALLENGE-test.txt
    |——trackers
        |——mot_challenge
            |——AI_CHALLENGE-val
                |——NEWTRACKER
                    |——data
                        |—— SeqName01.txt
                        |—— SeqName02.txt
                        |—— SeqName03.txt
                        ...
            |——AI_CHALLENGE-test
                |——NEWTRACKER
                    |——data
                        |—— SeqName01.txt
                        |—— SeqName02.txt
                        |—— SeqName03.txt
                        ...

