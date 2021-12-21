import os
import ujson
from configparser import ConfigParser
from argparse import ArgumentParser


class ConvertExcepation(Exception):
    """Custom exception for catching expected errors."""
    ...


class Convert():

    def __init__(self, GT_PATH, TRACKER_PATH, TYPE_TO_EVAL, TRACKER):
        
        self._gt_path = GT_PATH
        self._tracker_path = TRACKER_PATH
        self._type_to_eval = TYPE_TO_EVAL
        self._trackeval_path = os.getcwd()
        self._tracker = TRACKER
        
        self.BENCHMARK = "AI_CHALLENGE"

        self.checkPathValidation()
        if not self._gt_path == None:
            self.convertGt()
            self.makeSeqmaps()
        if not self._tracker_path == None:
            self.convertTracker()

    def checkPathValidation(self):
        """check whether the paths are valid"""
        
        if not self._gt_path == None:

            if not os.path.isdir(self._gt_path):
                raise ConvertExcepation("Gt path is invalid. Please check your gt path.")
        
        if not self._tracker_path == None:
            if not os.path.isdir(self._tracker_path):
                raise ConvertExcepation("Tracker path is invalid. Please check your tracker path.")
            elif self._tracker == None:
                raise ConvertExcepation("Tracker path is valid. But, there is no tracker name. Please check your tracker name.")
        
        if self._tracker_path == None and self._gt_path == None:
            raise ConvertExcepation("At least one of Gt path and Tracker path is necessary. Please check your tracker path.")

        if self._type_to_eval == None:
            raise ConvertExcepation("At least one of train, val, test is necessary.")
        for data in self._type_to_eval:
            if not data in ["train", "val", "test"]:
                raise ConvertExcepation("{} is invalid. Valid: train, val, test".format(data))

        if not os.path.isdir(self._trackeval_path):
            raise ConvertExcepation("TrackEval path is invalid. Please check your TrackEval path.")   

    def convertGt(self):
        
        for eval in self._type_to_eval:
            challenge_name = self.BENCHMARK + "-" + eval
            print("converting GT {}...".format(challenge_name))
            eval_path = os.path.join(self._gt_path, eval)
            seq_list = sorted(os.listdir(eval_path))

            challenge_path = os.path.join(self._trackeval_path, "data", "gt", "mot_challenge", challenge_name)
            for seq in seq_list:
                seq_path = os.path.join(challenge_path, seq)
                gt_path = os.path.join(seq_path, "gt")
                self.makeDirs(gt_path)

                gt_file = os.path.join(gt_path, "gt.txt")
                seqinfo_file = os.path.join(seq_path, "seqinfo.ini")
                
                json_path = os.path.join(eval_path, seq, "json0")
                jsons = os.listdir(json_path)
                jsons = sorted(jsons, key=lambda x: x.split("_")[-1].split(".")[0])
        
                with open(gt_file, "w+") as f:
                    for json in jsons:
                        json_file = os.path.join(json_path, json)
                        frame_num = int(json.split("_")[-1].split(".")[0])
                        
                        with open(json_file,"r") as f1:
                            data=ujson.load(f1)
                        
                        if frame_num == 0:
                            config = ConfigParser()
                            config['Sequence'] = {
                                "name":challenge_name,
                                "imDir":"image0",
                                "frameRate":"10",
                                "seqLength":"200",
                                "imWidth":str(data["information"]["resolution"][0]),
                                "imHeight":str(data["information"]["resolution"][1]),
                                "imExt":".jpg",
                            }
                            with open(seqinfo_file, 'w+') as f1:
                                config.write(f1)

                        for annot in data["annotations"]:
                            string = []
                            string.append(str(frame_num + 1))
                            string.append(str(annot["attribute"]["track_id"]))
                            
                            x1, y1, x2, y2 = annot["bbox"]
                            
                            bb_left = x1                                        
                            bb_top = y1
                            bb_width = x2 - x1
                            bb_height = y2 - y1

                            string.append(str(bb_left))
                            string.append(str(bb_top))
                            string.append(str(bb_width))
                            string.append(str(bb_height))

                            string.append(str(-1))
                            string.append(str(-1))
                            string.append(str(-1))
                            string.append(str(-1))

                            string = ", ".join(string)

                            f.writelines(string + "\n")

            print("{} done.".format(challenge_name))

    def convertTracker(self):

        for eval in self._type_to_eval:
            challenge_name = self.BENCHMARK + "-" + eval
            print("converting Tracker {}...".format(challenge_name))
            eval_path = os.path.join(self._tracker_path, eval)
            seq_list = sorted(os.listdir(eval_path))

            challenge_path = os.path.join(self._trackeval_path, "data", "trackers", "mot_challenge", challenge_name, self._tracker, "data")
            self.makeDirs(challenge_path)
            for seq in seq_list:
                seq_path = os.path.join(eval_path, seq)
                tracker_file = os.path.join(challenge_path, seq+".txt")
                
                json_path = os.path.join(seq_path, "json0")
                jsons = os.listdir(json_path)
                jsons = sorted(jsons, key=lambda x: x.split("_")[-1].split(".")[0])
        
                with open(tracker_file, "w+") as f:
                    for json in jsons:
                        json_file = os.path.join(json_path, json)
                        frame_num = int(json.split("_")[-1].split(".")[0])
                        
                        with open(json_file,"r") as f1:
                            data=ujson.load(f1)
                        

                        for annot in data["annotations"]:
                            string = []
                            string.append(str(frame_num + 1))
                            string.append(str(annot["attribute"]["track_id"]))
                            
                            x1, y1, x2, y2 = annot["bbox"]
                            
                            bb_left = x1                                        
                            bb_top = y1
                            bb_width = x2 - x1
                            bb_height = y2 - y1

                            string.append(str(bb_left))
                            string.append(str(bb_top))
                            string.append(str(bb_width))
                            string.append(str(bb_height))

                            string.append(str(-1))
                            string.append(str(-1))
                            string.append(str(-1))
                            string.append(str(-1))

                            string = ", ".join(string)

                            f.writelines(string + "\n")

            print("{} done.".format(challenge_name))

    def makeDirs(self, dir):

        if not os.path.isdir(dir):
            os.makedirs(dir)

    def makeSeqmaps(self):
        
        print("making seqmaps...")

        gt_path = os.path.join(self._trackeval_path, "data", "gt", "mot_challenge")
        seqmaps_path = os.path.join(gt_path, "seqmaps")
        self.makeDirs(seqmaps_path)
        
        for eval in self._type_to_eval:
            if not os.path.isdir(os.path.join(gt_path, self.BENCHMARK+"-"+eval)):
                raise ConvertExcepation("{} was generated before. However, there is no data".format(self.BENCHMARK+"-"+eval))
       
        for eval in self._type_to_eval:
            seq_path = os.path.join(gt_path, self.BENCHMARK+"-"+eval)
            seq_list = sorted(os.listdir(seq_path))

            with open(os.path.join(seqmaps_path, self.BENCHMARK+"-"+eval+".txt"), "w+") as f:
                f.writelines("name\n")
                for seq in seq_list:
                    f.writelines(seq+"\n")

            
def main():
    
    parser = ArgumentParser(description="Converting from AI Challenge json format to MOTChallenge format")

    config = {"GT_PATH":None, "TRACKER_PATH":None, "TYPE_TO_EVAL":["train", "val", "test"], "TRACKER":None}
    
    for setting in config.keys():
        if type(config[setting]) == list:
            parser.add_argument("--" + setting, nargs='+')
        else:
            parser.add_argument("--" + setting)
    
    args = parser.parse_args().__dict__

    GT_PATH = args["GT_PATH"]
    TRACKER_PATH = args["TRACKER_PATH"]
    TYPE_TO_EVAL = args["TYPE_TO_EVAL"]
    TRACKER = args["TRACKER"]


    convert = Convert(GT_PATH, TRACKER_PATH, TYPE_TO_EVAL, TRACKER)


if __name__ == "__main__":

    main()


