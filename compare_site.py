#!/usr/bin/env python3
import argparse
import imutils
import cv2
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
from skimage.metrics import structural_similarity
import os
import platform

def screenshot_domain(domain, out_dir):
    """
    function to take screenshot of supplied domain
    """

    try:
        print(f"collecting screenshot of {domain}!")
        options = webdriver.ChromeOptions()
        options.headless = True
        try:
            # installs chrome webdriver
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        except exception as E:
            print(f"Unable to install/update Chrome webdriver because {E}")
        url = "http://" + str(domain).strip('[]')
        driver.get(url)

        ss_path = str(out_dir + domain + '.png')

        driver.set_window_size(1024, 768)  # May need manual adjustment
        driver.get_screenshot_as_file(ss_path)
        driver.quit()
        print(f"Screenshot for {domain} saved to {ss_path}")
    except WebDriverException as exception:
        print(f"Unable to screenshot {domain}!")

def ssim_compare(imgA, imgB):

    # load the two input images
    imageA = cv2.imread(imgA)
    imageB = cv2.imread(imgB)

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = structural_similarity(grayA, grayB, full=True)
    print("SSIM: {}".format(round(score, 2)))
    rounded_score = round(score, 2)

    if rounded_score == 1.00:
        print(f"{imgA} Is identical to {imgB} with a score of {str(rounded_score)}!")
    elif rounded_score > .90:
        print(f"{imgA} Is similar to {imgB} with a score of {str(rounded_score)}!")
    elif rounded_score < .90:
        print(f"{imgA} Is different from {imgB} with a score of {str(rounded_score)}!")

def ssim_compare_show(imgA, imgB):

    # load the two input images
    imageA = cv2.imread(imgA)
    imageB = cv2.imread(imgB)

    # convert the images to grayscale
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = structural_similarity(grayA, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(round(score, 2)))
    rounded_score = round(score, 2)

    if rounded_score == 1.00:
        print(f"{imgA} Is identical to {imgB} with a score of {str(rounded_score)}!")
    elif rounded_score > .90:
        print(f"{imgA} Is similar to {imgB} with a score of {str(rounded_score)}!")
    elif rounded_score < .90:
        print(f"{imgA} Is different from {imgB} with a score of {str(rounded_score)}!")

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # loop over the contours
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)

    # show the output images
    cv2.imshow("Site 1", imageA)
    cv2.imshow("site 2", imageB)
    cv2.imshow("Diff", diff)
    cv2.imshow("Thresh", thresh)
    cv2.waitKey(0)


def main():
    #setting variables
    os.environ['WDM_LOG_LEVEL'] = '0'
    if platform.system() == "Windows":
        out_dir = 'C:\\temp\\'
    else:
        out_dir = '/tmp/'
        
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--first", required=True,
                    help="first input site")
    ap.add_argument("-s", "--second", required=True,
                    help="second input site")
    ap.add_argument('-S', '--show', dest='show', action='store_true', default=False,
                    help='Show comparison output images')
    arguments = ap.parse_args()

    first = arguments.first
    second = arguments.second

    screenshot_domain(first, out_dir)
    screenshot_domain(second, out_dir)

    imgA = out_dir + first + '.png'
    imgB = out_dir + second + '.png'

    if arguments.show:
        ssim_compare_show(imgA, imgB)
    else:
        ssim_compare(imgA, imgB)

if __name__ == "__main__":
    main()

