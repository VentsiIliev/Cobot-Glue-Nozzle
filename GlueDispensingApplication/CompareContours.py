import os

import cv2
import numpy as np
import copy
import traceback
from API.shared.Contour import Contour

SIMILARITY_THRESHOLD = 70
DEFECT_THRESHOLD = 5


# def _isValid(contour):
#     """Check if the contour is valid."""
#     return contour is not None and len(contour) > 0

def _isValid(sprayPatternList):
    """Check if the contour is valid."""
    return sprayPatternList is not None and len(sprayPatternList) > 0


def findMatchingWorkpieces(workpieces, newContours):
    print(f"in findMatchingWorkpieces")
    """FIND MATCHES BETWEEN NEW CONTOURS AND WORKPIECES."""
    matched, noMatches, newContoursWithMatches = _findMatches(newContours, workpieces)

    """ALIGN MATCHED CONTOURS."""
    finalMatches = _alignContours(matched, defectsThresh=DEFECT_THRESHOLD)
    # print(f"Final Matched {len(finalMatches)} workpieces")
    return finalMatches, noMatches, newContoursWithMatches
    # return matched, noMatches, newContoursWithMatches


def _remove_contour(newContours, contour_to_remove):
    """ Safely remove the exact matching contour from newContours """
    for i, stored_contour in enumerate(newContours):
        if np.array_equal(stored_contour, contour_to_remove):
            del newContours[i]  # Remove the matching contour
            return
    print(f"Error: Could not find an exact match to remove.")


def _findMatches(newContours, workpieces):
    print(f"Finding matches ")
    matched = []  # List of matched workpieces
    noMatches = []  # List of contours that did not match
    newContourWithMatches = []
    centroidDiffList, rotationDiffList = [], []  # Store differences

    for contour in newContours.copy():
        contour = Contour(contour)  # Convert to Contour object to use the methods

        best_match = None
        best_similarity = -1  # Start with the lowest similarity
        best_centroid_diff = None
        best_rotation_diff = None

        for workpiece in workpieces:
            workpieceContour = Contour(workpiece.contour)  # Convert to Contour object to use the methods
            if workpieceContour is None:
                print(f"    Workpiece contour is None")
                continue

            similarity = _getSimilarity(workpieceContour.get_contour_points(), contour.get_contour_points())
            print(f"    Similarity: {similarity}")

            if similarity > SIMILARITY_THRESHOLD and similarity > best_similarity:
                best_match = workpiece
                #best_match.contour = contour.get_contour_points()
                best_similarity = similarity
                best_centroid_diff, best_rotation_diff = _calculateDifferences(workpieceContour, contour)
                print(f"    Diff: {best_centroid_diff}, {best_rotation_diff}")

        if best_match is not None:
            # Store the best match for this contour
            print(f"    Best Match Found - Similarity: {best_similarity}")

            # Append results
            newContourWithMatches.append(contour.get_contour_points())
            matchDict = {"workpiece": best_match,
                         "newContour": contour.get_contour_points(),
                         "centroidDiff": best_centroid_diff,
                         "rotationDiff": best_rotation_diff}

            # print the formated matchDicts
            print(f"    Matched: {matchDict}")


            # matched.append(best_match)
            matched.append(matchDict)

            _remove_contour(newContours, contour.get_contour_points())
        else:
            print(f"    No match found for this contour")
    noMatches = newContours  # Remaining unmatched contours

    return matched, noMatches, newContourWithMatches


def _alignContours(matched, defectsThresh=5):
    print("Aligning contours")
    transformedMatches = []

    for i, match in enumerate(matched):
        print(f"ITERATION {i}")
        workpiece = copy.deepcopy(match["workpiece"])
        newContour = match["newContour"]
        rotationDiff = match["rotationDiff"]
        centroidDiff = match["centroidDiff"]

        if not _isValid(workpiece.contour):
            continue

        # Prepare contour objects
        contourObj = Contour(workpiece.contour)
        sprayContours = workpiece.sprayPattern.get("Contour", [])
        sprayFills = workpiece.sprayPattern.get("Fill", [])

        sprayContourObjs = [Contour(cnt) for cnt in sprayContours if _isValid(cnt)]
        sprayFillObjs = [Contour(cnt) for cnt in sprayFills if _isValid(cnt)]

        # Rotation
        print("    Rotating")
        centroid = contourObj.getCentroid()
        contourObj.rotate(rotationDiff, centroid)

        for obj in sprayContourObjs:
            obj.rotate(rotationDiff, centroid)
        for obj in sprayFillObjs:
            obj.rotate(rotationDiff, centroid)

        # Translation
        print("    Translating")
        contourObj.translate(*centroidDiff)
        for obj in sprayContourObjs:
            obj.translate(*centroidDiff)
        for obj in sprayFillObjs:
            obj.translate(*centroidDiff)

        # Update the workpiece
        print("    Updating transformed contours")
        workpiece.contour = contourObj.get_contour_points()
        if sprayContourObjs:
            workpiece.sprayPattern["Contour"] = [obj.get_contour_points() for obj in sprayContourObjs]
        if sprayFillObjs:
            workpiece.sprayPattern["Fill"] = [obj.get_contour_points() for obj in sprayFillObjs]

        # Compare contours
        _compareContoursHullAndDefects(defectsThresh, newContour, workpiece)

        # Add to result
        transformedMatches.append(workpiece)

    return transformedMatches



def _compareContoursHullAndDefects(defectsThresh, newContours, workpieceCopy):
    print(f"    Comparing hulls and defects contours")
    # Transform contours into correct shape if necessary
    """The new contour and the workpiece contour are beeing used as Contour objects to be able to use the methods of the Contour class."""
    workpieceCopyContourObject = Contour(workpieceCopy.contour)
    newContourObject = Contour(newContours)

    """CONVEXITY DEFECTS"""
    print(f"    Getting convexity defects")

    hull = workpieceCopyContourObject.getConvexHull()
    hull2 = newContourObject.getConvexHull()
    ret, workpieceDefects = workpieceCopyContourObject.getConvexityDefects()
    ret, newDefects = newContourObject.getConvexityDefects()

    """LARGEST DEFECTS"""
    print(f"    Getting largest defects")
    if workpieceDefects is None or newDefects is None:
        print(f"        Returning No defects found in workpiece contour")
        return

    workpieceLargestDefect = _getLargestDefect(workpieceDefects, workpieceCopyContourObject.get_contour_points())
    newContourLargestDefect = _getLargestDefect(newDefects, newContourObject.get_contour_points())

    if workpieceLargestDefect is None or newContourLargestDefect is None:
        print(f"        Returning No defects found in new contour")
        return

    """Calculate the Euclidean distance between the farthest points of the two contours"""

    distance = np.linalg.norm(np.array(workpieceLargestDefect) - np.array(newContourLargestDefect))
    print(f"    Distance between largest defects: {distance}")

    """ROTATE 180 DEGREES IF DISTANCE IS GREATER THAN THE THRESHOLD"""
    if distance > defectsThresh:
        print(" Rotating 180 degrees")
        newCentroid = workpieceCopyContourObject.getCentroid()
        workpieceCopyContourObject.rotate(180, newCentroid)

        """UPDATE SPRAY PATTERN IF IT EXISTS"""
        if _isValid(workpieceCopy.sprayPattern):
            sprayPattern = workpieceCopy.sprayPattern
            sprayPatternContourObject = Contour(sprayPattern)
            sprayPatternContourObject.rotate(180, newCentroid)
            workpieceCopy.sprayPattern = sprayPatternContourObject.get_contour_points()
            sprayPattern = np.squeeze(sprayPattern).tolist()
            workpieceCopy.sprayPattern = sprayPattern

        print("     wp defects", workpieceLargestDefect)
        print("     new defects", newContourLargestDefect)


def _getLargestDefect(defects, contour):
    largest_defect = max(defects, key=lambda x: x[0][3])
    s, e, f, d = largest_defect[0]  # s = start, e = end, f = far, d = distance
    start = tuple(contour[s][0])
    end = tuple(contour[e][0])
    far = tuple(contour[f][0])
    return far


def _calculateDifferences(workpieceContour, contour):
    """Calculates differences in centroid and rotation between two contours."""
    print(f"    Calculating differences")
    workpieceCentroid = workpieceContour.getCentroid()
    contourCentroid = contour.getCentroid()
    centroidDiff = np.array(contourCentroid) - np.array(workpieceCentroid)

    wpAngle = workpieceContour.getOrientation()
    contourAngle = contour.getOrientation()
    rotationDiff = contourAngle - wpAngle

    return centroidDiff, rotationDiff


def _getSimilarity(contour1, contour2):
    """Calculate similarity between two contours using shape matching."""
    # Ensure contours are valid NumPy arrays with the correct shape
    contour1 = np.array(contour1, dtype=np.float32)
    contour2 = np.array(contour2, dtype=np.float32)

    print("Contour1: ",contour1)
    print("Contour2: ",contour2)

    similarity = cv2.matchShapes(contour1, contour2, cv2.CONTOURS_MATCH_I1, 0.0)
    similarityPercent = (1 - similarity) * 100
    return similarityPercent





