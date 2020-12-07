# site_compare
Proof of concept code for using the Structural Similarity Index Measurement (SSIM) for comparing 2 websites.


code takes 2 arguments, '-f' and '-s', which are the domains to be compared.  This PoC will then use the selenuium webdriver for Chrome (chromedriver),
to take screenshots of the 2 domains.  The PoC will then use the SSIM equation provided in skimage.metrics to generate a score of the similarity
between the 2 sites.

If the user specifies the '-S' or '--show' the PoC will display the original images, as well as the greyscale version, and also display images of the 
"threshold" difference image, as well as the "contours" image, which is an image that is highlighted to by finding countours to find regions of diferences
between the 2 sites, with the diferences outlined in a rectangular bounding box.  
