import frame_cap
import object_selection
img_file_path='./output/caps/baseline.png'
template_file_path='./output/regions/template.png'
frame_cap.capture_calibration_image(img_file_path)
# temporary -- must specify template corners.
startx,starty=845,656
endx,endy=1183,708
object_selection.save_template_from_image(img_file_path, startx, starty, endx, endy, 'tl',template_file_path)
