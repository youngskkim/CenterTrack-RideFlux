# 자율주행 다중 객체 추적 인공지능 모델 개발 챌린지 솔루션 (2위, KAIST-VDCLab)
본 솔루션은 [CenterTrack](README-CenterTrack.md) 을 사용하여 다중 객체 검출 및 추적을 수행함.

## 데이터 전처리
[CenterTrack codebase](https://github.com/xingyizhou/CenterTrack) 를 이용해 네트워크를 학습시키기 위해 
`tools` 폴더의 `convert_rideflux_to_coco.py`를 이용하여 RideFlux 데이터셋을 COCO 데이터셋 포맷으로 변환함.
샘플마다 이미지의 크기가 다르고 해상도가 높기 때문에 네트워크에 입력되는 이미지를 [928, 1440]로 다운샘플링 함. 

## 학습
네트워크 학습은 `src` 폴더의 `main.py` 을 통해 진행하며, KITTI Object Tracking Dataset에서 학습된 pre-trained [모델](models/kitti_fulltrain.pth) 을 이용하여
네트워크를 initialize 함.
rideflux 데이터셋은 데이터의 frequency가 높고 데이터 샘플이 충분히 많다고 판단하여 학습 시에는 전체 데이터셋의 1/2을 샘플링하여 학습을 진행함.
학습 시 하이퍼파라미터는 learning rate 1e-4로 4 GPU에서 batch size 24로 20 epoch 학습 하였으며 15 epoch에서 learning rate를 1/10로 decay 함.
학습 시 augmentation으로 이미지에 random crop, scale, flip을 사용함.

## 추론
네트워크 추론은 `src` 폴더의 `test.py` 을 통해 진행함.
추론 시 이미지 flip을 이용해 test time augmentation을 사용했으며, tracking threshold가 0.3 이상인 track을 최종 결과로 제출함.

## 모델
최종 학습된 [모델](models/rideflux.pth)은 `models` 폴더에 제공됨.