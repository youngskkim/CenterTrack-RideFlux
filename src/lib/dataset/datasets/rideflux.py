from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import pycocotools.coco as coco
import numpy as np
import torch
import json
import cv2
import os
import math
from collections import defaultdict

from ..generic_dataset import GenericDataset
from utils.ddd_utils import compute_box_3d, project_to_image

class RideFlux(GenericDataset):
  num_categories = 3
  default_resolution = [928, 1440]
  class_name = ['pedestrian', 'vehicle', 'bike']
  # negative id is for "not as negative sample for abs(id)".
  # 0 for ignore losses for all categories in the bounding box region
  # ['Pedestrian', 'Car', 'Cyclist', 'Van', 'Truck',  'Person_sitting',
  #       'Tram', 'Misc', 'DontCare']
  cat_ids = {1:1, 2:2, 3:3, 4:-2, 5:-2, 6:-1, 7:-9999, 8:-9999, 9:0}
  max_objs = 50
  def __init__(self, opt, split):
    data_dir = os.path.join(opt.data_dir, 'rideflux')
    img_dir = os.path.join(
      data_dir, '{}'.format(split))
    ann_file_ = split if opt.dataset_version == '' else opt.dataset_version
    ann_path = os.path.join(
      data_dir, 'annotations', '{}.json'.format(ann_file_))
    self.images = None
    super(RideFlux, self).__init__(opt, split, ann_path, img_dir)
    self.alpha_in_degree = False
    self.num_samples = len(self.images)

    print('Loaded {} {} samples'.format(split, self.num_samples))


  def __len__(self):
    return self.num_samples

  def _to_float(self, x):
    return float("{:.2f}".format(x))


  def save_results_mot(self, results, save_dir):
    results_dir = os.path.join(save_dir, 'results_mot')
    if not os.path.exists(results_dir):
      os.mkdir(results_dir)
    for video in self.coco.dataset['videos']:
      video_id = video['id']
      file_name = video['file_name']
      out_path = os.path.join(results_dir, '{}.txt'.format(file_name))
      f = open(out_path, 'w')
      images = self.video_to_images[video_id]
      tracks = defaultdict(list)
      for image_info in images:
        if not (image_info['id'] in results):
          continue
        result = results[image_info['id']]
        frame_id = image_info['frame_id']
        for item in result:
          if not ('tracking_id' in item):
            item['tracking_id'] = np.random.randint(100000)
          if item['active'] == 0:
            continue
          tracking_id = item['tracking_id']
          bbox = item['bbox']
          bbox = [bbox[0], bbox[1], bbox[2], bbox[3]]
          tracks[tracking_id].append([frame_id] + bbox)
      rename_track_id = 0
      for track_id in sorted(tracks):
        rename_track_id += 1
        for t in tracks[track_id]:
          f.write('{},{},{:.2f},{:.2f},{:.2f},{:.2f},-1,-1,-1,-1\n'.format(
            t[0], rename_track_id, t[1], t[2], t[3]-t[1], t[4]-t[2]))
      f.close()


  def save_results_json(self, results, save_dir):
    results_dir = os.path.join(save_dir, 'results_json')
    if not os.path.exists(results_dir):
      os.mkdir(results_dir)
    for video in self.coco.dataset['videos']:
      video_id = video['id']
      seq_name = video['file_name']
      seq_dir = os.path.join(results_dir, seq_name, 'json0')
      if not os.path.exists(seq_dir):
        os.makedirs(seq_dir)
      images = self.video_to_images[video_id]
      for image_info in images:
        out_path = os.path.join(seq_dir, '{}_{:03d}.json'.format(seq_name, image_info['frame_id']-1))
        out = {'annotations': []}
        result = results[image_info['id']]
        for item in result:
          cat = item['class'] - 1
          bbox = item['bbox']
          track_id = item['tracking_id']
          det = {'bbox': [int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])],
                 'attribute': {'track_id': track_id},
                 'class': self.class_name[cat]}
          out['annotations'].append(det)

        json.dump(out, open(out_path, 'w'))


  def run_eval(self, results, save_dir):
    self.save_results(results, save_dir)
