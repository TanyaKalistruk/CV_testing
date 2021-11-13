import math
import sys
import os
import numpy as np
import cv2


class SearchObjectOnImage:

    def __init__(self, path_to_query_image: str, path_to_train_image: str, threshold: float = 0.7):
        if not os.path.isfile(path_to_query_image):
            sys.exit("Can not find a file on path '{0}'.".format(path_to_query_image))
        if not os.path.isfile(path_to_train_image):
            sys.exit("Can not find a file on path '{0}'.".format(path_to_train_image))
        self.query_image = cv2.imread(path_to_query_image)
        self.train_image = cv2.imread(path_to_train_image)
        self.threshold = threshold
        self.sift_det = cv2.xfeatures2d.SIFT_create()
        self.bf = cv2.BFMatcher()
        self.accepted_points = []
        self.rejected_points = []

    def get_size_query_image(self) -> tuple:
        """
        Returns size of query image.
        Note: columns and rows switched in opencv.
        """
        return self.query_image.shape[:2]

    def get_size_train_image(self) -> tuple:
        """
        Returns size of train image.
        Note: columns and rows switched in opencv.
        """
        return self.train_image.shape[:2]

    def get_query_img_radius(self) -> float:
        """
        Returns radius of query image.
        Used to decide that template matches are equal.
        Note: radius 50% of min side of query.
        """
        h, w = self.get_size_query_image()
        return min([h, w]) * 0.5

    def get_query_img_offset(self) -> float:
        """
        Returns offset value for query image.
        Used to decide if matched points has the same coordinates in query as cropped image.
        Note: it is 50% of radius of point sparsing.
        """
        return self.get_query_img_radius() * 0.5

    def find_matches(self):
        """
        Match template on image.
        Note: 'normed' method to easy choose a threshold from 0 to 1.
        """
        return cv2.matchTemplate(self.train_image, self.query_image, method=cv2.TM_CCOEFF_NORMED)

    def get_matched_points(self, result):
        """
        Filters by threshold found templates and returns matched points.
        Note: switching columns and rows to get x(w),y(h).
        """
        loc = np.where(result >= self.threshold)
        return zip(*loc[::-1])

    def get_values_for_matched_points(self, result):
        """Returns values of filtered matched points."""
        return [result[pt[1]][pt[0]] for pt in self.get_matched_points(result)]

    def sort_points(self, result) -> list:
        """
        Sort points based on descending values,
        it allows get better results from sparsing points method.
        """
        return [p for p, _ in reversed(sorted(zip(self.get_matched_points(result),
                                                  self.get_values_for_matched_points(result)),
                                              key=lambda pair: pair[1]))]

    def sparse_subset(self, points) -> list:
        """
        Returns a list of points that have distance between
        them more than radius of query image.
        """
        radius = self.get_query_img_radius()
        result = []
        for p in points:
            if all(get_euclid_distance(p, q) >= radius for q in result):
                result.append(p)
        return result

    def convert_imgs_to_gray(self):
        """Convert train and query images to gray color."""
        self.query_image = cv2.cvtColor(self.query_image, cv2.COLOR_BGR2GRAY)
        self.train_image = cv2.cvtColor(self.train_image, cv2.COLOR_BGR2GRAY)

    def get_common_good_matches(self, good_matches, kp1, kp2):
        """Get match points with the same coordinates on img1 and img2."""
        offset = self.get_query_img_offset()
        common_good_matches = []
        for good_match in good_matches:
            is_x_matching_within_offset = abs(kp1[good_match.queryIdx].pt[1] - kp2[good_match.trainIdx].pt[1]) <= offset
            is_y_matching_within_offset = abs(kp1[good_match.queryIdx].pt[0] - kp2[good_match.trainIdx].pt[0]) <= offset
            if is_x_matching_within_offset and is_y_matching_within_offset:
                common_good_matches.append(good_match)
        return common_good_matches

    def sift_detect_query_img(self):
        """Apply SIFT detection to the query image."""
        return self.sift_det.detectAndCompute(self.query_image, None)

    def sift_detect_train_img(self, point):
        """
        Apply SIFT detection to the part of train image.
        Note: sparsed points is (x,y) but crop function gets args (y:len,x:len)
        """
        h, w = self.get_size_query_image()
        crop_img = self.train_image[point[1]:point[1] + h, point[0]:point[0] + w]
        return self.sift_det.detectAndCompute(crop_img, None)

    def match_descriptors(self, point: tuple):
        """Match descriptors if more that 3 matching points were found."""
        kp1, des1 = self.sift_detect_query_img()
        kp2, des2 = self.sift_detect_train_img(point)
        return self.bf.knnMatch(des1, des2, k=2) if (len(kp1) >= 3 and len(kp2) >= 3) else []

    @staticmethod
    def lowe_ratio_test(matches) -> list:
        """Test found descriptors with David Lowe ratio test."""
        good_matches = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                good_matches.append(m)
        return good_matches

    def is_point_accepted(self, point, matches, good_matches, common_good_matches):
        """
        Make decision if the point is accepted.
        Note: should be at least 3 common points and more or equal than 20% of all matches.
        """
        res_dict = {
            'point': point,
            'matches': matches,
            'good_matches': good_matches,
            'common_good_matches': common_good_matches
        }
        if len(common_good_matches) >= 3 and len(common_good_matches) >= 0.2 * len(matches):
            self.accepted_points.append(res_dict)
        else:
            self.rejected_points.append(res_dict)

    def search_obj_on_template(self):
        """Looking for matches on image."""
        result = self.find_matches()
        points = self.sort_points(result)
        sparsed_points = self.sparse_subset(points)
        self.convert_imgs_to_gray()
        for pt in sparsed_points:
            matches = self.match_descriptors(pt)
            good_matches = self.lowe_ratio_test(matches)
            good_matches = sorted(good_matches, key=lambda x: x.distance)
            kp1, _ = self.sift_detect_query_img()
            kp2, _ = self.sift_detect_train_img(pt)
            common_good_matches = self.get_common_good_matches(good_matches, kp1, kp2)
            self.is_point_accepted(pt, matches, good_matches, common_good_matches)


def get_euclid_distance(point1: tuple, point2: tuple) -> float:
    """Calculates euclid distance between two points."""
    return math.sqrt(math.pow((point1[0] - point2[0]), 2) + math.pow((point1[1] - point2[1]), 2))
