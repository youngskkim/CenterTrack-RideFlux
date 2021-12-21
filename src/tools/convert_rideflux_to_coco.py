import os
import numpy as np
import json
import cv2

# Use the same script for MOT16
DATA_PATH = '../../data/rideflux/'
OUT_PATH = DATA_PATH + 'annotations/'
# SPLITS = ['train', 'val']
SPLITS = ['test']
cats = ['pedestrian', 'vehicle', 'bike']
cat_info = []
for i, cat in enumerate(cats):
  cat_info.append({'name': cat, 'id': i + 1})
cat_ids = {cat: i + 1 for i, cat in enumerate(cats)}

def _bbox_to_coco_bbox(bbox):
  return [(bbox[0]), (bbox[1]),
          (bbox[2] - bbox[0]), (bbox[3] - bbox[1])]

if __name__ == '__main__':
  for split in SPLITS:
    data_path = DATA_PATH + split
    out_path = OUT_PATH + '{}.json'.format(split)
    out = {'images': [], 'annotations': [], 'categories': cat_info, 'videos': []}
    seqs = os.listdir(data_path)

    image_cnt = 0
    ann_cnt = 0
    video_cnt = 0
    for seq in sorted(seqs):
      video_cnt += 1
      out['videos'].append({
        'id': video_cnt,
        'file_name': seq})
      seq_path = '{}/{}/'.format(data_path, seq)
      img_path = seq_path + 'image0/'
      ann_path = seq_path + 'json0/'
      images = os.listdir(img_path)
      num_images = len([image for image in images if 'jpg' in image])
      image_range = [0, num_images - 1]
      for i in range(num_images):
        if (i < image_range[0] or i > image_range[1]):
          continue
        image_info = {'file_name': '{}/image0/{}_{:03d}.jpg'.format(seq, seq, i),
                      'id': image_cnt + i + 1,
                      'frame_id': i + 1 - image_range[0],
                      'prev_image_id': image_cnt + i if i > 0 else -1,
                      'next_image_id': \
                        image_cnt + i + 2 if i < num_images - 1 else -1,
                      'video_id': video_cnt}
        out['images'].append(image_info)
        if split != 'test':
          with open('{}/{}_{:03d}.json'.format(ann_path, seq, i)) as anns_file:
            anns_list = json.load(anns_file)
          anns = anns_list['annotations']
          for ann in anns:
            track_id = int(ann['attribute']['track_id'])
            cat = ann['class']
            category_id = cat_ids[cat]
            bbox = ann['bbox']
            ann_cnt += 1
            annotation = {'id': ann_cnt,
                          'category_id': category_id,
                          'image_id': image_cnt + i + 1,
                          'track_id': track_id,
                          'bbox': _bbox_to_coco_bbox(bbox)}
            out['annotations'].append(annotation)
      image_cnt += num_images

      print('{}: {} images'.format(seq, num_images))
    print('loaded {} for {} images and {} samples'.format(
      split, len(out['images']), len(out['annotations'])))
    json.dump(out, open(out_path, 'w'))
