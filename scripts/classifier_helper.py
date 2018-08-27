# Script to aid in classifying the large volume of images for
# training purposes.

import cv2
import os
import pathlib
import csv

training_data_dir = input("Directory for training data used in this classifier: ")

training_data_path = f"./training/{training_data_dir}"
if not os.path.exists(training_data_path):
    raise Exception("Cannot find the specified directory for training data")

text_file_names = [
    file_name
    for file_name in os.listdir(training_data_path)
    if file_name.endswith(".txt")
]

categories = [
    file_name[:-4]
    for file_name in text_file_names
]

if len(categories) == 0:
    raise Exception(
        "It is expected that you created text files for every category prior to \
        running this script."
    )

already_classified = set()

for file_name in text_file_names:
    with open(f"{training_data_path}/{file_name}", 'r') as f:
        for line in f:
            line = line.strip()
            if line != "":
                already_classified.add(line)

available_to_classify = set()

unlabeled_data_dir = "./data/unlabeled_frames"
for folder in pathlib.Path("./data/unlabeled_frames").iterdir():
    if folder.is_dir():
        for image_path in folder.iterdir():
            rel_path = str(image_path)[len(unlabeled_data_dir) - 1:]
            available_to_classify.add(rel_path.replace("\\", "/"))

available_to_classify -= already_classified

options = {
    f"{i + 1:x}": img_path
    for i, img_path in enumerate(sorted(categories))
}

for i, o in options.items():
    print(f"{i}: {o}")

for path in available_to_classify:
    image = cv2.imread(os.path.join(unlabeled_data_dir, path))
    cv2.imshow('image',image)
    key_pressed = cv2.waitKey(0)

    escape_key = 27
    if key_pressed == escape_key:
        break

    else:
        key_pressed_chr = chr(key_pressed)
        chosen_option = options[key_pressed_chr]

        with open(os.path.join(training_data_path, f"{chosen_option}.txt"), "a") as datafile:
            datafile.write(path.replace("\\", "/"))
            datafile.write("\n")


cv2.destroyAllWindows()

print("Done classifying")
