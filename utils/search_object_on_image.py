import argparse
import sys
import os
import numpy as np
import cv2

from utils.helper import get_euclid_distance


class SearchObjectOnImage:

    def __init__(self, path_to_query_image: str, path_to_train_image: str, threshold: float = 0.7):
        if not os.path.isfile(path_to_query_image):
            sys.exit("Can not find a file on path '{0}'.".format(path_to_query_image))
        if not os.path.isfile(path_to_train_image):
            sys.exit("Can not find a file on path '{0}'.".format(path_to_train_image))
        self.query_image = cv2.imread(path_to_query_image)
        self.train_image = cv2.imread(path_to_train_image)
        self.threshold = threshold

    def get_size_query_image(self) -> tuple:
        """Size of query (note! that collumns and rows switched in opencv)."""
        return self.query_image.shape[:2]

    def get_size_train_image(self) -> tuple:
        """Size of train (note! that collumns and rows switched in opencv)."""
        return self.train_image.shape[:2]

    def get_template_radius(self, width, height) -> float:
        """#  Radius is a distanse between points to decide that template matches are equal. Use as radius 50% of min side of query"""
        return min([height, width]) * 0.5

    def get_offset(self, width, height) -> float:
        """#  Offset is value that used to deside if matched points has the same coords in query and croped image.
#    It is  50% of radius of point sparsing"""
        return self.get_template_radius(width, height) * 0.5

    def find_matches(self):
        return cv2.matchTemplate(self.train_image, self.query_image,
                                 cv2.TM_CCOEFF_NORMED)  # Use 'normed' method to easy choose a threshold from 0 to 1

    def get_matched_points(self):
        """# filter by threshold
            # Get matched points (note! - Remember to switch collumns and rows to get x(w),y(h))"""
        loc = np.where(result >= self.threshold)  # filter by threshold
        return zip(*loc[::-1])


def sparse_subset(points, r):
    """Return a maximal list of elements of points such that no pairs of
    points in the result have distance less than r.

    """
    result = []
    for p in points:
        if all(get_euclid_distance(p, q) >= r for q in result):
            result.append(p)
    return result


def concatenate_cv2_images(img1, img2, axis=0):
    "Concatenate two cv2 imgs to one. axis=0 for vertically (default), 1 for horizontally"
    if axis not in [0, 1]:
        sys.exit("Axis should be 0 or 1 but '{0}'".format(axis))

    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    # vis = None
    if axis == 1:
        vis = np.zeros((max(h1, h2), w1 + w2, 3), np.uint8)
        vis[:h1, :w1, :3] = img1
        vis[:h2, w1:w1 + w2, :3] = img2
    else:
        vis = np.zeros((h1 + h2, max(w1, w2), 3), np.uint8)
        vis[:h1, :w1, :3] = img1
        vis[h1:h1 + h2, :w2, :3] = img2
    return vis


ob = SearchObjectOnImage("../inp.png", "../whole.png")

h, w = ob.get_size_query_image()  # Size of query (note! that collumns and rows switched in opencv)

# Common consts
#  Radius is a distanse between points to decide that template matches are equal. Use as radius 50% of min side of query
radius = ob.get_template_radius(h, w)
#  Offset is value that used to deside if matched points has the same coords in query and croped image.
#    It is  50% of radius of point sparsing
offset = ob.get_offset(h, w)

#  Find matches and select results above threshold
result = cv2.matchTemplate(ob.train_image, ob.query_image,
                           cv2.TM_CCOEFF_NORMED)  # Use 'normed' method to easy choose a threshold from 0 to 1
loc = np.where(result >= ob.threshold)  # filter by threshold
points = zip(*loc[::-1])  # Get matched points (note! - Remember to switch collumns and rows to get x(w),y(h))

#  Save vals of matched points
vals = [result[pt[1]][pt[0]] for pt in points]

#  Sort points based on descending values from vals array
#   it allows get better results from sparsing points method
points = [p for p, _ in reversed(sorted(zip(points, vals), key=lambda pair: pair[1]))]

#  Sparce points to reduce matches
sparsed_points = sparse_subset(points, radius)

#  Match features on every cropped image build from sparced point to deside if it is real object from query
#    Initiate SIFT detector
det = cv2.xfeatures2d.SIFT_create()
#    Create BFMatcher object
bf = cv2.BFMatcher()
#    Convert query and image to gray
query_gray = cv2.cvtColor(ob.query_image, cv2.COLOR_BGR2GRAY)
image_gray = cv2.cvtColor(ob.train_image, cv2.COLOR_BGR2GRAY)

#    Loop memory
res_img = np.zeros((0, 0, 3), np.uint8)  # cross loop image to save result

# {
#     'point': pt,
#     'matches': matches,
#     'good_matches': good_matches,
#     'common_good_matches': common_good_matches
# }
accepted_points = []  # points to keep. list with dict
rejected_points = []  # points to reject. list with dict
#    Loop to match
for pt in sparsed_points:
    # Crop image (note! remember - sparsed points is (x,y) but crop function gets args (y:len,x:len))
    crop_img = image_gray[pt[1]:pt[1] + h, pt[0]:pt[0] + w]

    # find the keypoints and descriptors with SURF
    img1, img2 = query_gray, crop_img
    kp1, des1 = det.detectAndCompute(img1, None)
    kp2, des2 = det.detectAndCompute(img2, None)

    # Match descriptors if enough points found
    matches = bf.knnMatch(des1, des2, k=2) if (len(kp1) >= 3 and len(kp2) >= 3) else []

    # Store all the good matches as per Lowe's ratio test.
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)

    # Sort them in the order of their distance.
    good_matches = sorted(good_matches, key=lambda x: x.distance)

    # Get match points with the same coords on img1 and img2 (within small offset)
    common_good_matches = []  # list to keep matches
    for good_match in good_matches:
        is_x_matching_within_offset = abs(kp1[good_match.queryIdx].pt[1] - kp2[good_match.trainIdx].pt[1]) <= offset
        is_y_matching_within_offset = abs(kp1[good_match.queryIdx].pt[0] - kp2[good_match.trainIdx].pt[0]) <= offset
        if is_x_matching_within_offset and is_y_matching_within_offset:
            common_good_matches.append(good_match)

    # Make decision. and save result to list
    # To keep sparsed point - We should have at least 3 common points and more or equal than 20% of all matches
    res_dict = {
        'point': pt,
        'matches': matches,
        'good_matches': good_matches,
        'common_good_matches': common_good_matches
    }
    if len(common_good_matches) >= 3 and len(common_good_matches) >= 0.2 * len(matches):
        accepted_points.append(res_dict)
    else:
        rejected_points.append(res_dict)

    # Draw black frame on images for visual separation
    cv2.rectangle(img1, (0, 0), img1.shape[:2][::-1], (0, 0, 0), 2)
    cv2.rectangle(img2, (0, 0), img2.shape[:2][::-1], (0, 0, 0), 2)
    # Draw good matches to img
    img3 = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None, flags=2)
    # Draw common good matches to img
    img4 = cv2.drawMatches(img1, kp1, img2, kp2, common_good_matches, None, flags=2)

    # Add images to result
    img34 = concatenate_cv2_images(img3, img4, axis=1)
    res_img = concatenate_cv2_images(res_img, img34, axis=0)

#  Draw red rectangle on matched querys
for pt in points:
    cv2.rectangle(ob.train_image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

#  Draw blue rectangle on matched querys, find centers of the rectangles. Draw small sircles on the centers
accepted_rectangle_centers = []
for pt in [point_dict['point'] for point_dict in accepted_points]:
    # blue rectangle
    cv2.rectangle(ob.train_image, pt, (pt[0] + w, pt[1] + h), (255, 0, 0), 2)
    rectangle_center = (pt[0] + w / 2, pt[1] + h / 2)
    # blue circle r=10
    cv2.circle(ob.train_image, rectangle_center, 10, (255, 0, 0), thickness=2, lineType=8, shift=0)
    accepted_rectangle_centers.append(rectangle_center)

print("Done with processing query image '{0}' on train image '{1}'.".format(os.path.basename("../inp.png"),
                                                                            os.path.basename("../whole.png")))
print("Threshold: '{0}'. Radius: '{1}'. Offset: '{2}'.".format(ob.threshold, radius, offset))
print("Draft points found: '{0}'. first 10 points: '{1}'".format(len(points), points[:10]))
print("Clouds found: '{0}'. points: '{1}'".format(len(sparsed_points), sparsed_points))
print("Accepted points: '{0}'. Details:'{1}'.".format(
    len(accepted_points),
    [{'mtc': len(point_dict['matches']),
      'gd': len(point_dict['good_matches']),
      'cmn': len(point_dict['common_good_matches'])} for point_dict in accepted_points]))
print("Rejected points: '{0}'. Details:'{1}'.".format(
    len(rejected_points),
    [{'mtc': len(point_dict['matches']),
      'gd': len(point_dict['good_matches']),
      'cmn': len(point_dict['common_good_matches'])} for point_dict in rejected_points]))
print("Accepted rectangle centers: '{0}'.".format(accepted_rectangle_centers))
