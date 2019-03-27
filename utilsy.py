import firearm
from PIL import Image
import os
#import numpy as np
from colorama import Fore


class Utilsy:

    def detect_firearm(self, image_path, output_path):
        image = Image.open(image_path)
        PATH_TO_LABELS = os.path.join('data', 'label_map.pbtxt')

        firearms = firearm.Firearm()
        try:
                image_np = firearms.load_image_into_numpy_array(image=image)
                #image_np_expanded = np.expand_dims(image_np, axis=0)
                graph = firearms.load_graph('frozen_graph.pb')

                output_dict = firearms.run_inference_for_single_image(image_np, graph)

                indexes = [k for k, v in enumerate(output_dict['detection_scores']) if (v > 0.5)]
                if indexes:
                    print(Fore.RED +  "    Firearm detected" + Fore.RESET)
                    firearms.process_image(image_np, output_dict, PATH_TO_LABELS,output_path)
                    os.remove(image_path)
                    return True
                else:
                    print(Fore.GREEN +  "No firearms detected" + Fore.RESET)
                    return False
        except Exception as e:
            print("Unknown error during loading image")
            print(e.args)
