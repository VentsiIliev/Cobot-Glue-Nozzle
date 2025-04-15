import ezdxf
from ezdxf import bbox
import matplotlib.pyplot as plt
import math
import numpy as np


class DXFPathExtractor:
    def __init__(self, filename, wp_layer="0", spray_layer="2", target_size=(750, 500)):
        self.filename = filename
        self.wp_layer = wp_layer
        self.spray_layer = spray_layer
        self.target_layers = [wp_layer, spray_layer]
        self.target_size = target_size
        self.wpCnt = []
        self.sprayPatternCnt = []

        self._load_dxf()
        self._add_border()
        self._extract_paths()

    def _load_dxf(self):
        self.doc = ezdxf.readfile(self.filename)
        self.msp = self.doc.modelspace()

    def _add_border(self):
        cache = bbox.Cache()
        first_bbox = bbox.extents(self.msp, cache=cache)
        if first_bbox:
            cx = (first_bbox.extmin.x + first_bbox.extmax.x) / 2
            cy = (first_bbox.extmin.y + first_bbox.extmax.y) / 2
            self._draw_rectangle(cx, cy, self.target_size[0], self.target_size[1])

    def _draw_rectangle(self, cx, cy, width, height):
        hw = width / 2
        hh = height / 2
        bl = (cx - hw, cy - hh)
        br = (cx + hw, cy - hh)
        tr = (cx + hw, cy + hh)
        tl = (cx - hw, cy + hh)

        self.msp.add_lwpolyline(
            points=[bl, br, tr, tl, bl],
            close=True,
            dxfattribs={'layer': 'border'}
        )

    def _circle_to_points(self, center, radius, segments=36):
        return [
            (
                center[0] + radius * math.cos(2 * math.pi * i / segments),
                center[1] + radius * math.sin(2 * math.pi * i / segments),
            )
            for i in range(segments)
        ]

    def _extract_paths(self):
        for entity in self.msp:
            if entity.dxf.layer not in self.target_layers:
                continue
            print("Type: ",entity.dxftype())
            current_list = self.wpCnt if entity.dxf.layer == self.wp_layer else self.sprayPatternCnt

            if entity.dxftype() == 'LINE':
                start = entity.dxf.start
                end = entity.dxf.end
                current_list.append((start.x, start.y))
                current_list.append((end.x, end.y))

            elif entity.dxftype() == 'LWPOLYLINE':
                for pt in entity.get_points():
                    current_list.append((pt[0], pt[1]))

            elif entity.dxftype() == 'CIRCLE':
                center = (entity.dxf.center.x, entity.dxf.center.y)
                radius = entity.dxf.radius
                current_list.extend(self._circle_to_points(center, radius))

            elif entity.dxftype() == "POLYLINE":
                print("POLYLINE not implementet")
            elif entity.dxftype() == "ARC"
                print("ARC not implementet")
            elif entity.dxftype() == "ELLIPSE":
                print("ELLIPSE not implementet")
            elif entity.dxftype() == "SPLINE":
                print("SPLINE not implementet")

    def get_paths(self):
        return self.wpCnt, self.sprayPatternCnt

    def get_opencv_contours(self):
        if self.wpCnt:
            self.wpCnt.append(self.wpCnt[0])  # Close workpiece contour
        if self.sprayPatternCnt:
            self.sprayPatternCnt.append(self.sprayPatternCnt[0])  # Close spray pattern contour

        wp_contour = np.array(self.wpCnt, dtype=np.float32).reshape(-1, 1, 2)
        sp_contour = np.array(self.sprayPatternCnt, dtype=np.float32).reshape(-1, 1, 2)
        return wp_contour, sp_contour


    def save_dxf(self, output_file="modified.dxf"):
        self.doc.saveas(output_file)

    def plot(self):
        def extract_xy(coords):
            x_vals = [p[0] for p in coords]
            y_vals = [p[1] for p in coords]
            return x_vals, y_vals

        plt.figure(figsize=(10, 8))
        if self.wpCnt:
            x_wp, y_wp = extract_xy(self.wpCnt)
            plt.plot(x_wp, y_wp, label="Workpiece", color='blue')

        if self.sprayPatternCnt:
            x_sp, y_sp = extract_xy(self.sprayPatternCnt)
            plt.plot(x_sp, y_sp, label="Spray Pattern", color='red')

        plt.axis("equal")
        plt.title("DXF Paths")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.legend()
        plt.grid(True)
        plt.show()


# ---------------------------
# Entry point for CLI usage
# ---------------------------
if __name__ == "__main__":
    # dxf_file = "rectTest.dxf"  # Change as needed
    dxf_file = "Untitled3.dxf"  # Change as needed
    extractor = DXFPathExtractor(dxf_file)

    wp, spray = extractor.get_paths()
    print("✅ Workpiece Points:", wp)
    print("✅ Spray Pattern Points:", spray)

    extractor.plot()
    extractor.save_dxf("plate_with_border.dxf")
